import time
from typing import Optional


class RateLimiter:
    def __init__(self, rate: int, capacity: int, initial_tokens: Optional[int] = None):
        pass

    def allow(self, tokens: int = 1) -> bool:
        pass

    def try_consume(self, tokens: int = 1) -> tuple[bool, float]:
        pass

    def get_available_tokens(self) -> float:
        pass

    def reset(self) -> None:
        pass

    def wait_and_consume(self, tokens: int = 1) -> float:
        pass


if __name__ == "__main__":
    print("=== Token Bucket Rate Limiter Demo ===\n")

    limiter = RateLimiter(rate=2, capacity=10)

    # --- Burst behavior: drain the bucket quickly ---
    print("-- Burst: rapid requests against full bucket --")
    for i in range(12):
        allowed = limiter.allow()
        tokens = limiter.get_available_tokens()
        print(f"  Request {i+1:2d}: {'ALLOW' if allowed else 'DENY '} | tokens remaining: {tokens:.2f}")

    # --- try_consume: get wait time when denied ---
    print("\n-- try_consume: wait time feedback --")
    success, wait = limiter.try_consume(3)
    print(f"  try_consume(3): success={success}, wait={wait:.2f}s")

    # --- Refill: wait and watch tokens accumulate ---
    print("\n-- Refill: sleep 2s, expect ~4 new tokens --")
    before = limiter.get_available_tokens()
    time.sleep(2)
    after = limiter.get_available_tokens()
    print(f"  Tokens before: {before:.2f} | after 2s sleep: {after:.2f}")

    # --- Variable cost: expensive operation consumes more tokens ---
    print("\n-- Variable token cost --")
    limiter.reset()
    print(f"  After reset, tokens: {limiter.get_available_tokens():.2f}")
    allowed = limiter.allow(5)
    print(f"  allow(5): {'ALLOW' if allowed else 'DENY '} | tokens remaining: {limiter.get_available_tokens():.2f}")
    allowed = limiter.allow(5)
    print(f"  allow(5): {'ALLOW' if allowed else 'DENY '} | tokens remaining: {limiter.get_available_tokens():.2f}")
    allowed = limiter.allow(5)
    print(f"  allow(5): {'ALLOW' if allowed else 'DENY '} | tokens remaining: {limiter.get_available_tokens():.2f}")

    # --- wait_and_consume: blocks until tokens available ---
    print("\n-- wait_and_consume: blocks until tokens available --")
    limiter2 = RateLimiter(rate=5, capacity=5)
    limiter2.allow(5)  # drain completely
    print(f"  Bucket drained. Waiting for 3 tokens...")
    wait_time = limiter2.wait_and_consume(3)
    print(f"  Consumed after waiting {wait_time:.2f}s | tokens remaining: {limiter2.get_available_tokens():.2f}")
