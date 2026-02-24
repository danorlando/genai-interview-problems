# LLM Request Pipeline

**Difficulty**: Hard
**Time Limit**: 45 minutes

---

## Problem Statement

You are building a production LLM request processing pipeline for a high-traffic service. Requests arrive faster than the LLM API can handle them individually, so you need a multi-stage pipeline:

1. **Ingestion**: Accept individual requests into a buffer
2. **Batching**: Group requests into batches for efficient processing. Flush a batch when either it reaches 8 items OR 0.1 seconds pass with no new request — whichever comes first.
3. **Processing**: Send batches to the LLM API, but limit how many batches are in-flight simultaneously (the API rate-limits at 5 concurrent calls)
4. **Collection**: Gather all completed responses

The pipeline should handle backpressure: when the LLM processor falls behind, the batching stage should slow down, which in turn slows request ingestion. When all requests are processed, the pipeline should shut down cleanly.

---

## Data Classes (provided)

```python
from dataclasses import dataclass

@dataclass
class LLMRequest:
    prompt: str
    request_id: str

@dataclass
class LLMResponse:
    request_id: str
    text: str
```

---

## Requirements

Build four async coroutines connected by queues:

```
simulate_requests()  →  [Queue A]  →  request_ingester()  →  [Queue B]  →  llm_processor()  →  [Queue C]  →  collect_results()
```

- **Queue A** (incoming): holds individual `LLMRequest` objects. Should be large enough to absorb bursts (maxsize=100).
- **Queue B** (processing): holds batches (`list[LLMRequest]`). Should be small to create backpressure (maxsize=10).
- **Queue C** (results): holds `LLMResponse` objects. Can be unbounded (results are consumed quickly).

**request_ingester**: Reads from Queue A, accumulates into batches, writes batches to Queue B. Flushes on size (8 items) or time (0.1s with no new item).

**llm_processor**: Reads batches from Queue B. For each batch, limits concurrent API calls to 5. Simulates an API call with `asyncio.sleep(0.5)`. Creates an `LLMResponse` for each request in the batch.

**Shutdown**: Use `None` as a sentinel. Each stage receives it, flushes any remaining work, forwards it downstream, and exits.

All four coroutines run concurrently.

---

## Verification Code

```python
import asyncio

async def simulate_requests(incoming):
    for i in range(20):
        await incoming.put(LLMRequest(prompt=f"What is {i}?", request_id=f"req-{i}"))
        await asyncio.sleep(0.05)
    await incoming.put(None)

async def collect_results(results):
    count = 0
    while True:
        response = await results.get()
        if response is None:
            break
        count += 1
        print(f"Got response: {response.request_id}")
    print(f"\nTotal processed: {count} requests")

async def main():
    incoming = asyncio.Queue(maxsize=100)
    processing = asyncio.Queue(maxsize=10)
    results = asyncio.Queue()
    semaphore = asyncio.Semaphore(5)

    await asyncio.gather(
        simulate_requests(incoming),
        request_ingester(incoming, processing),
        llm_processor(processing, results, semaphore),
        collect_results(results),
    )

asyncio.run(main())
```

**Expected**: All 20 requests processed. Batching visible in logs (fewer than 20 LLM calls). Pipeline shuts down cleanly.

---

## What To Think About

**Before coding**, consider:

1. How do you implement "flush after 0.1 seconds of no new item"? What asyncio utility lets you put a timeout on an `await`?
2. What is "backpressure" in this pipeline? Trace the chain of events when the LLM processor falls behind.
3. The sentinel `None` must propagate through every stage. What happens if one stage exits without forwarding it?

**During implementation**, consider:

- The ingester needs to handle a timeout exception — what happens to the current batch when the timeout fires?
- Should the concurrency limiter be acquired before or after reading from the processing queue?
- When the ingester receives `None`, it may have a partial batch. Don't drop it.

---

## Follow-Up Questions (for interview discussion)

1. Explain "backpressure" using this pipeline. Trace what happens when the LLM processor falls behind.
2. Why do you need both a size trigger and a time trigger for batching? What user-facing problem does each solve?
3. If you removed the concurrency limit on API calls, what failure mode would you see in production?
4. How would you add error handling if the LLM API call raises an exception for one batch?
5. What is the difference between `asyncio.Queue` and `queue.Queue`? What breaks if you use the wrong one here?
