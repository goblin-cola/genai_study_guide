"""PRACTICE: LRU Cache

Implement class LRUCache with:

    __init__(self, capacity)
    get(self, key)       -> value or None, marks key as recently used
    put(self, key, value) -> add/update, evict oldest if over capacity

Hint: use OrderedDict from collections.
  - move_to_end(key) marks as recently used
  - popitem(last=False) removes the oldest item

Run this file to check: python 07_lru_cache_work.py

INTERVIEW QUESTIONS (this topic):
1. "Implement an LRU cache with O(1) get and put. What happens when the cache is full
   and a new item is added?"
2. "We're making expensive API calls and want to cache results. Design a cache that
   evicts the least recently used item when it hits capacity."
3. "Walk me through how you'd implement an LRU cache. What data structures would you
   combine and why?"
"""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        # YOUR CODE HERE
        pass

    def get(self, key):
        # YOUR CODE HERE
        pass

    def put(self, key, value):
        # YOUR CODE HERE
        pass


# ============================================================
# TESTS
# ============================================================

def test_basic_get_put():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1, f"Expected 1, got {cache.get('a')}"
    assert cache.get("b") == 2, f"Expected 2, got {cache.get('b')}"
    assert cache.get("c") is None, f"Missing key should return None"
    print("  basic_get_put: PASSED")


def test_eviction():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # should evict "a" (oldest)
    assert cache.get("a") is None, "a should have been evicted"
    assert cache.get("b") == 2, "b should still be there"
    assert cache.get("c") == 3, "c should still be there"
    print("  eviction: PASSED")


def test_access_updates_recency():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")     # a is now most recent, b is oldest
    cache.put("c", 3)  # should evict "b" (oldest), NOT "a"
    assert cache.get("a") == 1, "a was accessed, should NOT be evicted"
    assert cache.get("b") is None, "b should have been evicted (oldest)"
    assert cache.get("c") == 3, "c should still be there"
    print("  access_updates_recency: PASSED")


def test_update_existing():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 99)  # update a's value, should also make it most recent
    assert cache.get("a") == 99, f"a should be updated to 99, got {cache.get('a')}"
    cache.put("c", 3)   # should evict b (oldest)
    assert cache.get("b") is None, "b should be evicted"
    print("  update_existing: PASSED")


if __name__ == "__main__":
    print("Testing 07: LRU Cache\n")
    for test in [test_basic_get_put, test_eviction, test_access_updates_recency, test_update_existing]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
