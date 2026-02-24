# RAG Pipeline Phase Synchronization

**Difficulty**: Medium
**Time Limit**: 30 minutes

---

## Problem Statement

You are building a multi-stage RAG (Retrieval-Augmented Generation) pipeline that processes document chunks in parallel. The pipeline has three phases:

- **Phase 1 — Embedding**: Generate an embedding for each document chunk (all chunks run concurrently; simulate with `asyncio.sleep(random.uniform(0.1, 0.3))`)
- **Phase 2 — Scoring**: Score each chunk against a query embedding (requires ALL embeddings to exist first; simulate with `asyncio.sleep(0.05)`)
- **Phase 3 — Answer generation**: Select the top-3 highest-scoring chunks and generate an answer (requires ALL scores)

Each chunk is processed by a separate concurrent coroutine that handles Phase 1 and Phase 2 for that chunk. The critical constraint: **no chunk may start Phase 2 until every chunk has completed Phase 1**. Similarly, Phase 3 cannot start until every chunk has finished Phase 2.

If chunk-0 finishes Phase 1 quickly and jumps to Phase 2 (scoring against other chunks' embeddings), it would read incomplete data — chunks that haven't finished embedding yet.

Design a solution that synchronizes all chunk coroutines at the phase boundaries while allowing maximum parallelism within each phase.

---

## Requirements

- A coroutine `process_chunk` that takes a chunk ID, shared state dicts for embeddings and scores, and any synchronization objects you need. It runs Phase 1 and Phase 2 sequentially for its chunk, with a synchronization barrier between the two phases.
- A coroutine `rag_pipeline` that:
  - Creates shared state (embeddings dict, scores dict)
  - Launches `process_chunk` for each chunk concurrently (use structured concurrency)
  - After all chunks complete Phase 2, runs Phase 3: select top-3 by score, print them
  - Returns a mock answer string

The synchronization object you choose must be reusable (the same instance handles the Phase 1→2 barrier and the Phase 2→3 boundary). Requires Python 3.11+.

---

## Verification Code

```python
import asyncio
import random

async def main():
    chunks = [f"chunk-{i}" for i in range(6)]
    answer = await rag_pipeline(chunks, query="What is retrieval augmented generation?")
    print(f"\nFinal answer: {answer}")

asyncio.run(main())
```

**Expected output pattern** (order within phases will vary):
```
Phase 1 complete: chunk-0
Phase 1 complete: chunk-3
Phase 1 complete: chunk-1
...                           ← all 6 Phase 1s before any Phase 2
Phase 2 complete: chunk-2 score=0.73
Phase 2 complete: chunk-0 score=0.41
...                           ← all 6 Phase 2s before Phase 3
Top 3 chunks: ['chunk-4', 'chunk-0', 'chunk-2']
Generating answer from top 3 chunks...
Final answer: ...
```

---

## What To Think About

**Before coding**, consider:

1. You need all N coroutines to reach a point before any of them can proceed. What asyncio primitive enforces this "wait for everyone" behavior?
2. What argument does this primitive take on construction? How do you determine the right value?
3. You need two synchronization points (Phase 1→2 and Phase 2→3). Do you need two separate instances, or can one be reused?

**During implementation**, consider:

- Phase 3 runs in `rag_pipeline` after all chunk coroutines complete — not inside `process_chunk`. Why is this cleaner?
- What structured concurrency construct (Python 3.11+) should you use to run the chunk coroutines? How does it differ from `asyncio.gather` in error handling?

---

## Alternative Approach Discussion

There is a simpler way to implement this without the synchronization primitive:

```python
embeddings = await asyncio.gather(*[embed_chunk(c) for c in chunks])
scores = await asyncio.gather(*[score_chunk(c, embeddings) for c in chunks])
answer = generate_answer(scores)
```

Be prepared to discuss: when would you prefer the barrier-based approach over sequential `gather` calls? What does the barrier approach enable that sequential `gather` doesn't?

---

## Follow-Up Questions (for interview discussion)

1. What happens when the last coroutine arrives at the synchronization point? What happens to all the others?
2. Is it possible for chunk-0 to start Phase 2 before chunk-5 finishes Phase 1? Explain why or why not.
3. The synchronization primitive resets automatically. How does this make two-phase synchronization work with a single instance?
4. What does your structured concurrency construct do if one chunk raises an exception? How does this differ from `asyncio.gather(return_exceptions=True)`?
5. When would you choose a barrier over sequential `gather` calls?
