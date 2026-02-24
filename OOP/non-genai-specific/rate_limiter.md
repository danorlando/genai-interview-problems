Exercise: Token Bucket Rate Limiter

Description

Build a RateLimiter class using the Token Bucket algorithm. This is a fundamental component in API design, especially for LLM APIs where you need to control request rates and prevent abuse. Understanding rate limiting is crucial for building production-ready GenAI systems.

Requirements

Constructor takes:
- `rate: int` - tokens added per second (requests per second)
- `capacity: int` - maximum burst size (bucket capacity)
- `initial_tokens: Optional[int]` - starting tokens (defaults to capacity)

Methods:
- `allow(tokens: int = 1) -> bool`: Attempts to consume tokens. Returns True if allowed, False if insufficient tokens.
- `try_consume(tokens: int = 1) -> tuple[bool, float]`: Returns (success, wait_time). If False, wait_time indicates seconds until enough tokens available.
- `get_available_tokens() -> float`: Returns current token count (can be fractional).
- `reset()`: Refills bucket to capacity.
- `wait_and_consume(tokens: int = 1) -> float`: Blocks until tokens available, then consumes. Returns wait time in seconds.

Behavior:
- Tokens refill continuously at the specified rate (not in discrete intervals).
- When tokens are consumed, they're removed immediately.
- Bucket cannot exceed capacity even if no consumption occurs.
- Token refill calculation should account for time elapsed since last operation.
- Support fractional tokens for precise rate control.

Implementation Notes:
- Track last_refill_time to calculate elapsed time and tokens to add.
- Use time.time() for current timestamp.
- Refill formula: `min(capacity, current_tokens + (elapsed_time * rate))`
- Consider edge cases: negative tokens requested, zero rate, etc.

Deliverable (rate_limiter.py)

The RateLimiter implementation with:
- Accurate token refill calculation based on elapsed time
- Proper handling of fractional tokens
- Clean mathematical logic for token bucket algorithm
- Type hints for all methods
- A demo in `if __name__ == "__main__":` that:
  - Creates a limiter with rate=2 (2 tokens/sec), capacity=10
  - Makes rapid requests showing burst behavior (uses up tokens quickly)
  - Demonstrates rate limiting (requests get denied)
  - Shows try_consume() returning wait times
  - Uses time.sleep() to show token refill
  - Demonstrates different token costs (e.g., allow(5) for expensive operations)

Challenge Extensions (Optional):
- Create a `MultiKeyRateLimiter` that manages separate limits per API key
- Add `get_estimated_wait_time(tokens)` for better client feedback
- Implement sliding window rate limiter as alternative algorithm
- Add statistics tracking: total requests, denied requests, avg wait time
- Make it thread-safe for concurrent access
