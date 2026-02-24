# Token Budget Tracker

**Difficulty**: Medium
**Time Limit**: 25 minutes

---

## Problem Statement

You are building a shared token budget system for a multi-tenant LLM service. Multiple concurrent async tasks call the same LLM API simultaneously, and each call consumes tokens from a shared budget.

The budget starts with a fixed allowance. Before each LLM call, a task must check whether enough tokens remain and reserve them. After the call completes, unused tokens (the difference between estimated and actual usage) should be returned to the budget.

The system must behave correctly when many tasks attempt to reserve tokens at the same time — two tasks should never both see "enough budget" and both deduct, causing overspend.

---

## Requirements

Implement a `TokenBudget` class that supports:

- **Initialization** with a maximum token allowance
- **Consuming tokens**: check if enough budget remains for an estimated amount, and if so, deduct it atomically. Return `True` on success, `False` if insufficient. Two concurrent consumers must never both succeed when only enough budget exists for one.
- **Refunding tokens**: after a call completes, return the difference between estimated and actual usage to the budget. Concurrent refunds must not corrupt the balance.
- **Querying remaining balance**: a property that returns the current remaining tokens

---

## Verification Code

Use this to verify your implementation works correctly:

```python
import asyncio

async def make_llm_call(budget, call_id: int, estimated: int):
    reserved = await budget.consume(estimated)
    if not reserved:
        print(f"Call {call_id}: insufficient budget, skipping")
        return

    # Simulate an LLM API call that uses fewer tokens than estimated
    await asyncio.sleep(0.05)
    actual_used = estimated // 2

    await budget.refund(actual_used, estimated)
    print(f"Call {call_id}: used {actual_used} tokens, refunded {estimated - actual_used}")

async def main():
    budget = TokenBudget(max_tokens=1000)

    # Fire 5 concurrent calls, each estimating 300 tokens
    # Only the first 3 should succeed (300 * 3 = 900 <= 1000; 300 * 4 = 1200 > 1000)
    await asyncio.gather(*[make_llm_call(budget, i, 300) for i in range(5)])
    print(f"Final remaining: {budget.remaining}")

asyncio.run(main())
```

**Expected**: Exactly 3 calls succeed, 2 are rejected. The final remaining balance accounts for refunds.

---

## What To Think About

**Before coding**, consider:

1. This is single-threaded async code. Why is correctness even a concern? What mechanism allows another coroutine to interleave with yours?
2. Trace through two coroutines both trying to consume 600 tokens from a 1000 budget. At what point does the interleaving happen, and what goes wrong?
3. How do you make the check-and-deduct operation atomic in an async context?

**During implementation**, consider:

- Which operations need protection, and which don't?
- Should the consume and refund operations share the same protection mechanism, or use separate ones?
- Is there any I/O happening inside the critical section? What does that tell you about the cost of the protection?

---

## Follow-Up Questions (for interview discussion)

1. Why can't you use `threading.Lock` in async code? What specifically breaks?
2. If you removed all protection, describe a specific execution trace where the budget goes negative.
3. A race condition in asyncio vs. threading — what's the key difference in granularity? Why is asyncio's version "easier to reason about"?
4. If you added a `peek()` method that only reads the balance, would it need the same protection? Why or why not?
