# Mock Interview Problem: Async Multi-Model Inference Pipeline

## Difficulty: Medium | Time Limit: 30 minutes

## Problem Statement

You're building an inference pipeline that takes user queries and runs them through multiple AI models in stages: **intent classification**, **entity extraction**, and **response generation**. Each stage has different latency profiles and failure modes. Design a pipeline that processes queries concurrently while respecting per-stage concurrency limits and handling partial failures.

## Scenario

Your team is deploying a customer support system. Each incoming query must:

1. **Stage 1 - Classify** (fast, ~50ms): Determine intent (billing, technical, general)
2. **Stage 2 - Extract** (medium, ~150ms): Pull entities (account IDs, product names, dates)
3. **Stage 3 - Generate** (slow, ~500ms): Produce a response using the classified intent + extracted entities

Queries arrive in bursts. You need to maximize throughput while:
- Limiting each stage's concurrency independently (classify=20, extract=10, generate=5)
- Routing failed queries to a dead-letter queue with context about where they failed

## Pre-Built Utilities (provided - do not modify)

```python
import asyncio
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Intent(Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    GENERAL = "general"


@dataclass
class Query:
    id: str
    text: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class StageResult:
    query_id: str
    stage: str
    data: Any
    latency_ms: float
    success: bool
    error: str | None = None


@dataclass
class PipelineResult:
    query: Query
    intent: Intent | None = None
    entities: dict | None = None
    response: str | None = None
    stage_results: list[StageResult] = field(default_factory=list)
    completed: bool = False


class DeadLetterQueue:
    """Async-safe collection for failed queries and their failure context."""

    def __init__(self):
        self._items: list[tuple[Query, StageResult]] = []
        self._lock = asyncio.Lock()

    async def put(self, query: Query, stage_result: StageResult) -> None:
        async with self._lock:
            self._items.append((query, stage_result))

    def drain(self) -> list[tuple[Query, StageResult]]:
        items, self._items = self._items, []
        return items

    def __len__(self) -> int:
        return len(self._items)


# --- Simulated model endpoints (treat these as external services) ---

async def classify_intent(text: str) -> Intent:
    """Simulates intent classification model. Fast but occasionally fails."""
    await asyncio.sleep(random.uniform(0.03, 0.08))
    if random.random() < 0.05:
        raise TimeoutError("Classification model timed out")
    scores = {Intent.BILLING: 0, Intent.TECHNICAL: 0, Intent.GENERAL: 0}
    if any(w in text.lower() for w in ["bill", "charge", "payment", "invoice", "refund"]):
        scores[Intent.BILLING] = 0.9
    elif any(w in text.lower() for w in ["error", "bug", "crash", "slow", "broken"]):
        scores[Intent.TECHNICAL] = 0.9
    else:
        scores[Intent.GENERAL] = 0.9
    return max(scores, key=scores.get)


async def extract_entities(text: str) -> dict:
    """Simulates entity extraction model. Medium speed, moderate failure rate."""
    await asyncio.sleep(random.uniform(0.1, 0.2))
    if random.random() < 0.08:
        raise ConnectionError("Entity extraction service unavailable")
    entities = {}
    import re
    acc = re.search(r"ACC-\d+", text)
    if acc:
        entities["account_id"] = acc.group()
    entities["word_count"] = len(text.split())
    return entities


async def generate_response(intent: Intent, entities: dict, text: str) -> str:
    """Simulates response generation model. Slow, occasionally produces errors."""
    await asyncio.sleep(random.uniform(0.3, 0.7))
    if random.random() < 0.03:
        raise RuntimeError("Generation model OOM error")
    return f"[{intent.value}] Processed query with {len(entities)} entities extracted."


# --- Test data generator ---

def generate_test_queries(n: int = 50) -> list[Query]:
    templates = [
        "I was charged twice on my bill for ACC-{id}",
        "The app keeps crashing when I open ACC-{id}",
        "How do I update my profile settings?",
        "I need a refund for invoice #{id}",
        "Error 500 when accessing the dashboard for ACC-{id}",
        "What are your business hours?",
        "My payment for ACC-{id} was declined",
        "The search feature is broken and very slow",
    ]
    return [
        Query(id=f"q-{i:04d}", text=random.choice(templates).format(id=random.randint(1000, 9999)))
        for i in range(n)
    ]
```

## Your Task

Implement the following:

### 1. `StageSemaphore`
A thin wrapper around `asyncio.Semaphore` that tracks how many tasks are currently active within a stage. Must support use as an async context manager.

### 2. `InferencePipeline`
The core class. Constructor takes the three model functions and per-stage concurrency limits, and a shared `DeadLetterQueue`.

Required methods:
- `async _run_stage(stage_name, semaphore, coro) -> StageResult`: Execute a coroutine within a semaphore slot, measure latency, and catch any exception into a failed `StageResult`.
- `async process_one(query: Query) -> PipelineResult`: Run a single query through all three stages sequentially. If any stage fails, route to the dead letter queue and return a partial result — do not run subsequent stages.
- `async process_batch(queries: list[Query]) -> list[PipelineResult]`: Process all queries concurrently. Return results in the same order as input.

### Key Design Constraints
- Each stage must use its own semaphore
- A query holds a semaphore slot only while that stage is actively running
- A failed query must not block or affect other queries in the batch

## Expected Solution Structure

```python
class StageSemaphore:
    # ~15 lines

class InferencePipeline:
    def __init__(self, classify_fn, extract_fn, generate_fn,
                 classify_limit, extract_limit, generate_limit,
                 dead_letter_queue: DeadLetterQueue):
        ...

    async def _run_stage(self, stage_name, semaphore, coro) -> StageResult:
        ...

    async def process_one(self, query: Query) -> PipelineResult:
        ...

    async def process_batch(self, queries: list[Query]) -> list[PipelineResult]:
        ...
```

## Evaluation Criteria

| Criteria | Weight | What They're Looking For |
|----------|--------|--------------------------|
| Correct async patterns | 35% | Proper semaphore usage, no race conditions, gather/TaskGroup |
| Error handling | 30% | Graceful partial failures, DLQ routing, no silent swallowing |
| Clean OOP design | 25% | Single responsibility, composable stages, clear interfaces |
| Production thinking | 10% | Edge cases, typing, docstrings on public methods |

## Verification

After implementing, run this in `if __name__ == "__main__"`:

```python
async def main():
    dlq = DeadLetterQueue()
    pipeline = InferencePipeline(
        classify_fn=classify_intent,
        extract_fn=extract_entities,
        generate_fn=generate_response,
        classify_limit=20,
        extract_limit=10,
        generate_limit=5,
        dead_letter_queue=dlq,
    )
    queries = generate_test_queries(50)
    results = await pipeline.process_batch(queries)

    completed = sum(1 for r in results if r.completed)
    failed = len(dlq)
    print(f"Completed: {completed}/{len(queries)}")
    print(f"Dead letter queue: {failed} failed queries")

asyncio.run(main())
```

Expected output: ~85-95% completion rate with a small number of queries in the dead letter queue.

## Bonus (if time permits)
- Add a `max_retries` parameter to `_run_stage` with exponential backoff
- Implement a `process_stream` async generator that yields results as they complete
