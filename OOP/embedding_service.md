# Embedding Service with Rate Limiting

**Difficulty**: Medium-Hard
**Time Limit**: 35 minutes

---

## Problem Statement

You are building an embedding service that wraps an external embedding API. The API enforces two independent limits:

- **Concurrent request cap**: No more than N requests in-flight at the same time
- **Per-second rate limit**: No more than M requests fired within any rolling 1-second window

A naive approach that only limits concurrency will fail — you could have 50 requests all fire in the same millisecond and still trip the per-second quota. You need both layers working together.

Implement an `EmbeddingService` class where callers can fire many embedding requests at once (via a batch method using `asyncio.gather`), but the service internally self-throttles to respect both limits.

---

## Requirements

- **Initialization**: accepts `max_concurrent` (default 50) and `requests_per_second` (default 100)
- **Single embed**: embeds one text. Must enforce both the concurrent cap AND the per-second rate limit before making the API call. Simulate the API call with `asyncio.sleep(0.1)`. Return a placeholder `[0.1, 0.2, 0.3]`.
- **Batch embed**: accepts a list of texts, launches all embeddings concurrently (using `asyncio.gather`), and returns all results. The internal limiting self-throttles — the caller doesn't need to think about pacing.
- **Rate limiter**: must implement a sliding window counter:
  - Maintain timestamps of recent requests
  - Before each request, evict timestamps older than 1 second
  - If the window is already full, sleep until the oldest timestamp ages out
  - Record the current timestamp
  - The check-and-record operation must be atomic — explain why in your implementation

Use `asyncio.get_event_loop().time()` for timestamps (not `time.time()`).

---

## Verification Code

```python
import asyncio
import time

async def main():
    service = EmbeddingService(max_concurrent=10, requests_per_second=5)
    texts = [f"Document chunk {i}" for i in range(15)]

    start = time.time()
    embeddings = await service.embed_batch(texts)
    elapsed = time.time() - start

    print(f"Embedded {len(embeddings)} texts in {elapsed:.1f}s")
    # With 15 texts and max 5/sec: expect ~3 seconds minimum

asyncio.run(main())
```

---

## What To Think About

**Before coding**, consider:

1. Why is limiting concurrency not enough? Give a concrete example where 10 requests pass the concurrent cap but still violate a 5-per-second rate limit.
2. The rate limiter reads a list of timestamps, potentially sleeps, then appends a timestamp. Why does this need protection in async code?
3. In which order should the two layers be applied? Does it matter?

**During implementation**, consider:

- The rate limiter holds its protection across an `await asyncio.sleep(...)`. Is that a problem? What does it mean for other coroutines trying to check the rate limit simultaneously?
- `asyncio.gather` fires all coroutines at once. How do the two layers work together to prevent all 15 from hitting the API simultaneously?
- What's the difference between a "sliding window" and a "fixed window" rate limiter? Which did you implement?

---

## Follow-Up Questions (for interview discussion)

1. What's the difference between a semaphore and a rate limiter? When do you need both?
2. Describe the sliding window algorithm. What are its advantages over a fixed window counter?
3. What would happen to `embed_batch` performance if `requests_per_second=1` and you embed 10 texts? Walk through the timing.
4. If you had to add a third limit — maximum 1000 tokens per second across all requests — how would you extend this class?
5. What's the difference between a binary semaphore and a lock? When would you prefer one over the other?
