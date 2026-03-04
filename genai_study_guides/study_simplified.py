c"""Simplified GenAI interview problems — Python version
No type hints, no imports you don't need. Just the logic.
"""

from math import sqrt
from collections import deque, OrderedDict


# ============================================================
# 1) TOP-K COSINE SIMILARITY
# Core of vector search in RAG
# ============================================================

def cosine_sim(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sqrt(sum(x * x for x in a))
    mag_b = sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def top_k(query, docs, k):
    """docs = [(id, embedding), ...] -> returns [(id, score), ...] top k"""
    scored = [(doc_id, cosine_sim(query, emb)) for doc_id, emb in docs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


# ============================================================
# 2) RATE LIMITER (sliding window)
# Same pattern as sliding window counts — deque per user
# ============================================================

class RateLimiter:
    def __init__(self, max_req, window):
        self.max_req = max_req
        self.window = window
        self.hits = {}  # user_id -> deque of timestamps

    def allow(self, user_id, now):
        if user_id not in self.hits:
            self.hits[user_id] = deque()
        q = self.hits[user_id]

        # drop expired
        while q and q[0] <= now - self.window:
            q.popleft()

        if len(q) >= self.max_req:
            return False
        q.append(now)
        return True


# ============================================================
# 3) CHUNK TEXT WITH OVERLAP
# RAG preprocessing — split docs into overlapping windows
# ============================================================

def chunk_text(text, size, overlap):
    """Returns list of string chunks."""
    chunks = []
    step = size - overlap
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += step
    return chunks


# ============================================================
# 4) MERGE + DEDUPE RANKED RESULTS
# Hybrid retrieval: combine vector + keyword search
# ============================================================

def merge_results(list_a, list_b):
    """Each list = [(doc_id, score), ...]. Keep highest score per doc."""
    best = {}
    for doc_id, score in list_a + list_b:
        if doc_id not in best or score > best[doc_id]:
            best[doc_id] = score
    return sorted(best.items(), key=lambda x: x[1], reverse=True)


# ============================================================
# 5) LRU CACHE (bonus — comes up a lot)
# Cache repeated queries to avoid redundant LLM calls
# ============================================================

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)  # mark as recently used
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # evict oldest


# ============================================================
# QUICK TESTS — run with: python study_simplified.py
# ============================================================

if __name__ == "__main__":
    # 1) Top-K
    q = [0.2, 0.5, 0.3]
    docs = [("doc1", [0.1, 0.5, 0.4]), ("doc2", [0.9, 0.1, 0.2]), ("doc3", [0.2, 0.6, 0.2])]
    print("=== Top-K Cosine ===")
    print(top_k(q, docs, 2))
    # Expected: doc3 and doc1 (most similar to query)

    # 2) Rate Limiter
    print("\n=== Rate Limiter ===")
    rl = RateLimiter(max_req=3, window=60)
    for t in [1000, 1001, 1002, 1003]:
        print(f"  t={t}: {rl.allow('user1', t)}")
    # Expected: True, True, True, False

    # 3) Chunking
    print("\n=== Chunking ===")
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunk_text(text, size=10, overlap=3)
    for i, c in enumerate(chunks):
        print(f"  chunk{i}: '{c}'")

    # 4) Merge Results
    print("\n=== Merge Results ===")
    vec = [("A", 0.9), ("B", 0.8)]
    kw = [("B", 0.95), ("C", 0.7)]
    print(merge_results(vec, kw))
    # Expected: [('B', 0.95), ('A', 0.9), ('C', 0.7)]

    # 5) LRU Cache
    print("\n=== LRU Cache ===")
    cache = LRUCache(2)
    cache.put("q1", "answer1")
    cache.put("q2", "answer2")
    print(f"  get q1: {cache.get('q1')}")  # answer1
    cache.put("q3", "answer3")             # evicts q2
    print(f"  get q2: {cache.get('q2')}")  # None (evicted)
    print(f"  get q3: {cache.get('q3')}")  # answer3
