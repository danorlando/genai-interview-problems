import time
from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    def __init__(self, capacity: int, default_ttl: int):
        pass

    def get(self, key: str) -> Optional[Any]:
        pass

    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        pass

    def delete(self, key: str) -> bool:
        pass

    def clear_expired(self) -> int:
        pass

    def size(self) -> int:
        pass


if __name__ == "__main__":
    print("=== LRU Cache with TTL Demo ===\n")

    cache = LRUCache(capacity=3, default_ttl=5)

    # --- Demonstrate basic put/get ---
    print("-- Basic operations --")
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    print(f"get('a'): {cache.get('a')}")   # expected: 1
    print(f"get('b'): {cache.get('b')}")   # expected: 2
    print(f"size: {cache.size()}")          # expected: 3

    # --- Demonstrate LRU eviction ---
    # 'a' was accessed most recently, then 'b', then 'c' (least recent)
    # Adding 'd' should evict 'c'
    print("\n-- LRU eviction --")
    cache.put("d", 4)
    print(f"get('c') after eviction: {cache.get('c')}")  # expected: None (evicted)
    print(f"get('d'): {cache.get('d')}")                  # expected: 4
    print(f"size: {cache.size()}")                         # expected: 3

    # --- Demonstrate TTL expiration ---
    print("\n-- TTL expiration --")
    cache.put("short", "expires soon", ttl=1)
    print(f"get('short') before expiry: {cache.get('short')}")  # expected: 'expires soon'
    time.sleep(1.1)
    print(f"get('short') after expiry: {cache.get('short')}")   # expected: None

    # --- Demonstrate clear_expired ---
    print("\n-- clear_expired --")
    cache2 = LRUCache(capacity=5, default_ttl=1)
    cache2.put("x", 10)
    cache2.put("y", 20)
    cache2.put("z", 30, ttl=60)  # long-lived
    time.sleep(1.1)
    removed = cache2.clear_expired()
    print(f"Removed expired entries: {removed}")   # expected: 2
    print(f"size after clear: {cache2.size()}")    # expected: 1
    print(f"get('z'): {cache2.get('z')}")          # expected: 30

    # --- Demonstrate delete ---
    print("\n-- delete --")
    print(f"delete('z'): {cache2.delete('z')}")          # expected: True
    print(f"delete('z') again: {cache2.delete('z')}")    # expected: False
    print(f"size after delete: {cache2.size()}")          # expected: 0
