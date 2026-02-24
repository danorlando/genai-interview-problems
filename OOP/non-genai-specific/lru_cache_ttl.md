Exercise: LRU Cache with Time-To-Live (TTL)

Description

Build an LRUCache class that implements a Least Recently Used cache with time-based expiration. This combines classic LRU eviction with TTL-based invalidation, a common pattern in production caching systems (Redis, Memcached, etc.).

Requirements

Constructor takes `capacity: int` and `default_ttl: int` (seconds).

Methods:
- `get(key: str) -> Optional[Any]`: Returns value if key exists and hasn't expired, None otherwise. Updates access order.
- `put(key: str, value: Any, ttl: Optional[int] = None)`: Stores key-value pair with TTL (uses default if not specified).
- `delete(key: str) -> bool`: Removes key if exists, returns True if deleted, False if not found.
- `clear_expired() -> int`: Removes all expired entries, returns count of removed items.
- `size() -> int`: Returns current number of valid (non-expired) entries.

Behavior:
- When cache is at capacity and a new key is added, evict the least recently used non-expired key.
- Expired entries should not count toward capacity but should be lazily removed (on access or explicit clear).
- Each get() operation should update the access order for LRU tracking.
- TTL is measured from the time of put() operation.

Implementation Notes:
- Consider using OrderedDict for LRU tracking or implement custom doubly-linked list + hash map.
- Store timestamp with each entry for TTL validation.
- Think about time complexity: get() and put() should be O(1) average case.

Deliverable (lru_cache_ttl.py)

The LRUCache implementation with:
- Proper data structure selection for O(1) operations
- Clean separation between LRU logic and TTL logic
- Type hints for all methods
- A demo in `if __name__ == "__main__":` that:
  - Creates a cache with capacity=3 and default_ttl=5
  - Demonstrates LRU eviction
  - Demonstrates TTL expiration (use time.sleep() or manual time manipulation)
  - Shows clear_expired() removing only expired entries
  - Prints cache state after each operation

Challenge Extensions (Optional):
- Add `peek(key: str)` that checks existence without updating LRU order
- Implement cache statistics: hit rate, miss rate, eviction count
- Add callback support for eviction events
- Make it thread-safe using appropriate locking mechanisms
