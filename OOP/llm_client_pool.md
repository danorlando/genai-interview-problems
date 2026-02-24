# LLM Client Pool

**Difficulty**: Hard
**Time Limit**: 40 minutes

---

## Problem Statement

You are building a multi-model LLM routing service. You have multiple API clients for different models (e.g., GPT-4, Claude, Gemini), where each model may have multiple client instances representing different API keys or connections. Clients are expensive to create and must be reused, not created per request.

Implement a client pool that:

- Manages separate pools of clients per model
- Lends out one client at a time via a context manager — callers use `async with pool.get_client(model) as client:` and the client is automatically returned when the block exits (even if an exception is raised)
- Limits concurrent usage per model to the number of registered clients (if all clients are in use, additional callers wait)
- Provides a convenience `generate(model, prompt)` method that handles acquisition and release internally

---

## Data Class (provided)

```python
import asyncio
from dataclasses import dataclass

@dataclass
class LLMClient:
    model: str
    client_id: str

    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.3)  # Simulate API latency
        return f"[{self.model}:{self.client_id}] Response to: {prompt[:40]}"
```

---

## Requirements

Implement `LLMClientPool`:

- **register_model(model, clients)**: register a list of `LLMClient` instances for a model name. Sets up whatever internal state you need for that model's pool.
- **get_client(model)**: an async context manager that lends out one client:
  - On entry: wait if all clients are in use, then take one from the pool
  - On exit: return the client to the pool (even on exception)
  - Raise `ValueError` for unregistered models
- **generate(model, prompt)**: convenience wrapper — acquire a client, call its `generate`, return the result

Key design consideration: you need two kinds of protection in `get_client`:
1. **Admission control**: limit how many callers can hold a client simultaneously (matches the pool size)
2. **Mutual exclusion on the pool data structure**: briefly protect the take/return operations on the collection of available clients

These are different concerns — the admission control is held for the entire duration of client use, while the collection access is held only for the instant of take/return. Think carefully about what primitives serve each purpose and why they must be separate.

---

## Verification Code

```python
import asyncio
import time

async def main():
    pool = LLMClientPool()

    pool.register_model("gpt-4", [
        LLMClient("gpt-4", "key-1"),
        LLMClient("gpt-4", "key-2"),
    ])

    pool.register_model("claude", [
        LLMClient("claude", "key-a"),
        LLMClient("claude", "key-b"),
        LLMClient("claude", "key-c"),
    ])

    # 8 concurrent GPT-4 calls — only 2 can run at a time
    prompts = [f"Question {i}" for i in range(8)]

    start = time.time()
    results = await asyncio.gather(*[pool.generate("gpt-4", p) for p in prompts])
    elapsed = time.time() - start

    for r in results:
        print(r)
    print(f"\nElapsed: {elapsed:.1f}s")
    # 8 calls, 2 at a time, 0.3s each → expect ~1.2s (4 batches of 2)

asyncio.run(main())
```

---

## What To Think About

**Before coding**, consider:

1. For admission control (limiting concurrent clients), what primitive lets N callers through but makes the N+1th wait?
2. For protecting the client collection during take/return, what primitive provides brief mutual exclusion?
3. Why can't you use a single primitive for both? Think about how long each is held.
4. How does `@asynccontextmanager` from `contextlib` work? What maps to `__aenter__` and `__aexit__`?

**During implementation**, consider:

- The admission control must be acquired BEFORE taking from the collection. Why?
- In the `finally` block, you return the client AND release the admission control. What happens if you forget to release it? How does this manifest as a bug?
- The collection access is held only briefly (one popleft or one append). Should it ever be held during `yield`?

---

## Follow-Up Questions (for interview discussion)

1. What happens if the caller raises an exception inside `async with pool.get_client(...):`? Will the client be returned? Trace through the code.
2. If you registered 3 clients for a model and 10 callers arrive simultaneously, how many execute and how many wait? Trace the admission state.
3. What is the difference between `@asynccontextmanager` and implementing `__aenter__`/`__aexit__` directly? When would you choose each?
4. How would you add connection health checking — verify a client works before lending it out, and replace it with a fresh one if it fails?
5. What would happen if you held the collection lock for the entire duration of `yield` (not just during take/return)?
