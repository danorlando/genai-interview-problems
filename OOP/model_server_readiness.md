# Model Server Readiness Signal

**Difficulty**: Easy-Medium
**Time Limit**: 20 minutes

---

## Problem Statement

You are building an LLM inference server. On startup, the server loads a model, which takes several seconds. Meanwhile, incoming inference requests should wait — not fail — until the model is ready. Once the model finishes loading, all waiting requests should unblock simultaneously and begin processing.

Key behaviors:
- Requests that arrive while the model is loading must wait efficiently (no polling loops)
- When the model becomes ready, ALL waiting requests wake up at once (broadcast, not one-at-a-time)
- Requests that arrive after the model is already loaded should proceed immediately with no waiting
- The solution is a one-shot signal: once the model is ready, it stays ready

Implement a `ModelServer` class that coordinates model loading with concurrent request handling.

---

## Requirements

- **Initialization**: the model starts as `None` (not loaded)
- **load_model()**: simulate model loading with a 2-second delay, then store the model and broadcast readiness. Print "Model loading..." at start and "Model ready!" when done.
- **handle_request(request_id)**: wait for the model to be ready (without polling), then simulate inference with a 0.1-second delay. Return `f"Response {request_id} from {self._model}"`. Print `f"Processing request {request_id}"` before the inference.

---

## Verification Code

```python
import asyncio
import time

async def main():
    server = ModelServer()

    start = time.time()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(server.load_model())
        for i in range(5):
            tg.create_task(server.handle_request(i))

    elapsed = time.time() - start
    print(f"Total time: {elapsed:.1f}s")

asyncio.run(main())
```

**Expected**:
- "Model loading..." prints first
- After ~2 seconds, "Model ready!" prints
- All 5 requests unblock simultaneously and process concurrently
- Total time: ~2.1 seconds (not 2 + 5*0.1 = 2.5), proving the requests run in parallel after the signal

---

## What To Think About

**Before coding**, consider:

1. You need many coroutines to wait for a one-time event, then all proceed. What asyncio primitive provides a broadcast "it happened" signal?
2. How does this differ from a lock? A lock allows one-at-a-time access; you need all-at-once notification.
3. Once the signal is sent, future callers should see it immediately. Does the primitive you're considering have this property?

**During implementation**, consider:

- The primitive has `set()`, `wait()`, and `is_set()`. Which do you need for `load_model` and which for `handle_request`?
- Is there any scenario where `handle_request` needs to reset the signal? (This should inform whether "one-shot" is sufficient.)

---

## Extension: Graceful Shutdown

Once the basic version works, add a `shutdown()` method:

- After shutdown, new requests should raise `RuntimeError("Server is shutting down")`
- In-flight requests (already past the readiness check) should complete normally

Hint: you'll need a second one-shot signal for shutdown. In `handle_request`, how do you check both "am I ready?" and "am I shutting down?"

---

## Follow-Up Questions (for interview discussion)

1. Your broadcast primitive wakes all waiters simultaneously. How many waiters can it support? Is it O(1) or O(n) to wake them?
2. What's the difference between this broadcast primitive and a condition variable? When would you use each?
3. Can you always replace `await event.wait()` with a polling loop using `is_set()`? What do you lose?
4. How would you implement a "server status" endpoint that returns `{"status": "loading"}` vs. `{"status": "ready"}` using only this primitive?
5. If the model load fails, how should the server communicate this to all waiting requests?
