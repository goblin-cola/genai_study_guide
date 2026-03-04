"""GenAI / ML Coding Interview Practice Snippets

This file contains clean, copy-friendly reference implementations for
common "problem solving & coding" interview tasks that show up in GenAI,
search/RAG, and fraud/streaming contexts.

Each section includes:
  - a function implementation
  - a small example in __main__ you can run

All code is standard-library only.
"""

from __future__ import annotations

from collections import defaultdict, deque
from heapq import nlargest
from math import sqrt
from time import time
from typing import Deque, Dict, Iterable, List, Sequence, Tuple, Optional


# ============================================================
# 1) Top-K Similar Documents (Cosine similarity)
# ============================================================
#This mimics the vector retrieval step in RAG.

#Prompt
#You are given a query embedding and a list of document embeddings.
#Return the k most similar documents using cosine similarity.
# ============================================================

def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute cosine similarity between vectors a and b."""
    if len(a) != len(b):
        raise ValueError("Vectors must have the same dimension.")
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    denom = sqrt(na) * sqrt(nb)
    return 0.0 if denom == 0.0 else dot / denom


def top_k_cosine(
    query: Sequence[float],
    docs: Sequence[Tuple[str, Sequence[float]]],
    k: int,
) -> List[Tuple[str, float]]:
    """Return top-k document IDs by cosine similarity to query."""
    if k <= 0:
        return []
    scored: List[Tuple[str, float]] = []
    for doc_id, emb in docs:
        scored.append((doc_id, cosine_similarity(query, emb)))
    return nlargest(k, scored, key=lambda x: x[1])


# ============================================================
# 2) Sliding Window Event Features (count in last W seconds)
# ============================================================

def sliding_window_counts(
    events: Sequence[Tuple[str, float, int]],
    window_seconds: int,
) -> List[Tuple[str, int, int]]:
    """For each event (user_id, amount, ts), output (user_id, ts, count_in_window).

    Assumptions:
      - events are ordered by timestamp ascending
      - timestamps are integers (seconds)
    Complexity: O(n) time, O(users * window) space.
    """
    if window_seconds < 0:
        raise ValueError("window_seconds must be >= 0")

    per_user: Dict[str, Deque[int]] = defaultdict(deque)
    out: List[Tuple[str, int, int]] = []

    for user_id, _amount, ts in events:
        q = per_user[user_id]
        q.append(ts)
        cutoff = ts - window_seconds
        while q and q[0] < cutoff:
            q.popleft()
        out.append((user_id, ts, len(q)))

    return out


# ============================================================
# 3) Merge Ranked Results (hybrid retrieval merge + dedupe)
# ============================================================

def merge_ranked_results(
    a: Sequence[Tuple[str, float]],
    b: Sequence[Tuple[str, float]],
) -> List[Tuple[str, float]]:
    """Merge two ranked lists, dedupe by doc_id, keep highest score, sort desc."""
    best: Dict[str, float] = {}
    for doc_id, score in a:
        prev = best.get(doc_id)
        if prev is None or score > prev:
            best[doc_id] = score
    for doc_id, score in b:
        prev = best.get(doc_id)
        if prev is None or score > prev:
            best[doc_id] = score

    return sorted(best.items(), key=lambda x: x[1], reverse=True)


# ============================================================
# 4) Chunking Documents (fixed size with overlap)
# ============================================================

def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split text into chunks with max chunk_size and overlap characters.

    Example: chunk_size=100, overlap=20
      chunk1: [0:100]
      chunk2: [80:180]
      chunk3: [160:260]
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be < chunk_size")

    chunks: List[str] = []
    start = 0
    n = len(text)
    step = chunk_size - overlap

    while start < n:
        end = min(start + chunk_size, n)
        chunks.append(text[start:end])
        if end == n:
            break
        start += step

    return chunks


# ============================================================
# 5) Rate Limiter (N requests per window seconds)
# ============================================================

class SlidingWindowRateLimiter:
    """Per-user sliding window rate limiter.

    allow(user_id, now_ts) returns True if allowed else False.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        if max_requests <= 0:
            raise ValueError("max_requests must be > 0")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.hits: Dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, user_id: str, now_ts: Optional[float] = None) -> bool:
        if now_ts is None:
            now_ts = time()
        q = self.hits[user_id]
        cutoff = now_ts - self.window_seconds

        while q and q[0] <= cutoff:
            q.popleft()

        if len(q) >= self.max_requests:
            return False

        q.append(now_ts)
        return True


# ============================================================
# 6) Citation Validation (LLM citations must be subset of retrieved)
# ============================================================

def validate_citations(
    retrieved_chunk_ids: Iterable[str],
    citations: Iterable[str],
) -> List[str]:
    """Return only citations that exist in retrieved_chunk_ids, preserving order."""
    allowed = set(retrieved_chunk_ids)
    out: List[str] = []
    for c in citations:
        if c in allowed:
            out.append(c)
    return out


# ============================================================
# Quick run examples
# ============================================================

if __name__ == "__main__":
    # 1) Top-K cosine
    query = [0.2, 0.5, 0.3]
    docs = [
        ("doc1", [0.1, 0.5, 0.4]),
        ("doc2", [0.9, 0.1, 0.2]),
        ("doc3", [0.2, 0.6, 0.2]),
    ]
    print("Top-k cosine:", top_k_cosine(query, docs, k=2))

    # 2) Sliding window counts
    events = [
        ("user1", 100, 1),
        ("user1", 50, 5),
        ("user1", 70, 7),
        ("user2", 200, 8),
    ]
    print("Sliding window counts:", sliding_window_counts(events, window_seconds=5))

    # 3) Merge ranked results
    vector_results = [("docA", 0.9), ("docB", 0.8)]
    keyword_results = [("docB", 0.95), ("docC", 0.7)]
    print("Merged:", merge_ranked_results(vector_results, keyword_results))

    # 4) Chunking
    text = "abcdefghijklmnopqrstuvwxyz" * 10
    chunks = chunk_text(text, chunk_size=20, overlap=5)
    print("Chunks:", len(chunks), "first:", chunks[0], "second:", chunks[1])

    # 5) Rate limiter
    rl = SlidingWindowRateLimiter(max_requests=3, window_seconds=60)
    t0 = 1000.0
    print("Rate limiter:", [rl.allow("u1", t0 + i) for i in range(4)])

    # 6) Citation validation
    retrieved = ["c1", "c2", "c3"]
    cites = ["c2", "c5", "c1"]
    print("Valid citations:", validate_citations(retrieved, cites))
