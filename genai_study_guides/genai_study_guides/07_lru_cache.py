"""Study Guide #7: LRU Cache (Least Recently Used)

PROBLEM
-------
Build a cache with a fixed size. When it's full and you add something new,
kick out the item that hasn't been used in the longest time.

    get(key)        -> return value (or None if not found), marks as recently used
    put(key, value) -> add/update, kick out oldest if over capacity

WHY THIS SHOWS UP IN GENAI
--------------------------
LLM API calls are expensive ($) and slow (seconds). If someone asks the
same question twice, serve it from cache instead of calling the API again.
Same for embedding caches, retrieval caches, etc.

HOW IT WORKS
------------
Use an OrderedDict — it's a dict that remembers insertion order.
  - "Move to end" = this item was just used (most recent)
  - "Pop from front" = evict the oldest (least recently used)

In JS, Map preserves insertion order the same way.

EXAMPLE
-------
cache = LRUCache(2)        capacity = 2 items max
cache.put("q1", "ans1")    cache: {q1}
cache.put("q2", "ans2")    cache: {q1, q2}    (full)
cache.get("q1")            returns "ans1", moves q1 to end -> {q2, q1}
cache.put("q3", "ans3")    full! evicts q2 (oldest) -> {q1, q3}
cache.get("q2")            returns None (was evicted)

"""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        # OrderedDict remembers the order items were added
        # first item = oldest, last item = most recently used
        # in JS: new Map() does the same thing
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None

        # move to end = "I just used this, don't evict it"
        # in JS you'd do: const val = map.get(key); map.delete(key); map.set(key, val)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        # if key already exists, move it to end (it's being updated = recently used)
        if key in self.cache:
            self.cache.move_to_end(key)

        # set the value
        self.cache[key] = value

        # if we're over capacity, evict the oldest (first item)
        # popitem(last=False) removes from the FRONT
        # in JS: const oldest = map.keys().next().value; map.delete(oldest)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


if __name__ == "__main__":
    cache = LRUCache(2)

    cache.put("q1", "answer1")
    cache.put("q2", "answer2")
    print("get q1:", cache.get("q1"))   # answer1 — q1 moves to end (most recent)

    cache.put("q3", "answer3")          # full! evicts q2 (oldest), NOT q1
    print("get q2:", cache.get("q2"))   # None — was evicted
    print("get q3:", cache.get("q3"))   # answer3

    cache.put("q4", "answer4")          # evicts q1 (now q1 is oldest)
    print("get q1:", cache.get("q1"))   # None — evicted
    print("get q4:", cache.get("q4"))   # answer4
