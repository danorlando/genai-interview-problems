# Streaming Response Buffer

**Difficulty**: Hard
**Time Limit**: 40 minutes

---

## Problem Statement

You are building a streaming LLM response handler. The LLM streams tokens back faster than your downstream processor (e.g., text-to-speech, safety filter) can consume them. You need a bounded buffer that sits between the two:

- A **writer** adds response chunks to the buffer. If the buffer is full, the writer waits until space opens up (backpressure on the LLM stream reader).
- A **reader** takes chunks from the buffer. If the buffer is empty, the reader waits until a chunk arrives.
- When the LLM stream ends, a **close** signal must unblock all waiting writers and readers so they can exit cleanly.

The buffer must support multiple concurrent readers and writers without corrupting state. It should also expose a convenient async iterator interface so callers can do `async for text in buffer.stream()`.

---

## Data Class (provided)

```python
from dataclasses import dataclass

@dataclass
class StreamChunk:
    text: str
    is_final: bool = False
```

---

## Requirements

Implement a `StreamBuffer` class that supports:

- **Initialization** with a capacity (max chunks in the buffer)
- **write(chunk)**: add a `StreamChunk` to the buffer. Block if full; raise `RuntimeError` if the buffer has been closed.
- **read()**: remove and return the next chunk. Block if empty. If the buffer is empty AND closed, return `StreamChunk("", is_final=True)` as an end-of-stream sentinel.
- **close()**: signal end-of-stream. Must unblock ALL waiting writers and readers — not just one — so they can check the closed flag and exit.
- **stream()**: async generator that yields `chunk.text` until `is_final=True`

Key constraint: both `write` and `read` protect the same shared state. A writer and a reader must never access the buffer simultaneously. However, they need to *signal* each other: a writer signals "data available" to a reader, and a reader signals "space available" to a writer. You need a synchronization primitive that combines mutual exclusion with selective signaling.

After being woken, a waiter must re-check its condition before proceeding — another coroutine may have consumed the resource between the signal and the wakeup.

---

## Verification Code

```python
import asyncio

async def llm_stream_reader(buffer):
    tokens = ["Hello", " world", "!", " How", " are", " you?"]
    for text in tokens:
        await buffer.write(StreamChunk(text=text))
        await asyncio.sleep(0.05)  # tokens arrive at ~20/sec
    await buffer.close()

async def tts_processor(buffer):
    async for text in buffer.stream():
        print(f"Speaking: '{text}'")
        await asyncio.sleep(0.15)  # TTS is slower than token arrival

async def main():
    buffer = StreamBuffer(capacity=3)  # small to demonstrate backpressure
    await asyncio.gather(
        llm_stream_reader(buffer),
        tts_processor(buffer),
    )

asyncio.run(main())
```

**Expected**: Writer produces faster than reader consumes. With capacity=3, the writer will block after filling the buffer until the reader catches up. All tokens are eventually delivered in order.

---

## What To Think About

**Before coding**, consider:

1. You need mutual exclusion (only one coroutine in the buffer at a time) but also the ability to wait-and-signal. What asyncio primitive combines both? Why isn't a plain lock sufficient?
2. A writer needs to signal "data available" to a reader, and a reader needs to signal "space available" to a writer. Should these be the same signal or different signals? What happens if you only have one?
3. When `close()` is called, why must it wake ALL waiters rather than just one?

**During implementation**, consider:

- After being woken by a signal, why do you need a `while` loop rather than `if`? (Hint: what if two writers are both waiting for space, and only one slot opens?)
- In `read`, after the wait loop exits, the buffer might be empty AND closed — or it might have a chunk. How do you distinguish the two cases?
- `close()` needs to acquire the underlying lock and notify on BOTH signal channels. Why?

---

## Follow-Up Questions (for interview discussion)

1. The wait primitive you used releases the lock, suspends, then re-acquires. Why must it release the lock? What would happen if it didn't?
2. What is a "stolen wakeup"? Give a concrete scenario with two producers.
3. What is the difference between waking one waiter vs. waking all waiters? When is each appropriate?
4. How does the async generator `stream()` hide the `is_final` sentinel from the caller? What Python mechanism makes `yield` in an async function possible?
5. Could you implement this buffer using only a lock (no conditions)? What would you lose?
