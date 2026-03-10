"""PRACTICE: Top-K Cosine Similarity

Implement two functions:

1. cosine_similarity(a, b)
   - Takes two lists of numbers (same length)
   - Returns a float between -1 and 1
   - Formula: dot_product(a,b) / (magnitude(a) * magnitude(b))
   - If either vector is all zeros, return 0.0

2. top_k(query, docs, k)
   - query = list of floats (the embedding)
   - docs = list of (doc_id, embedding) tuples
   - k = how many results to return
   - Returns list of (doc_id, score) sorted by score descending

Run this file to check your answers: python 01_topk_cosine_work.py

INTERVIEW QUESTIONS (this topic):
1. "Given a search query embedding and a database of document embeddings, how would you
   find the most relevant documents? Write a function that returns the top K results
   ranked by similarity."
2. "Implement cosine similarity from scratch. How would you handle edge cases like
   zero vectors?"
3. "We have a recommendation system that needs to find the K nearest neighbors to a
   user's preference vector. How would you implement this efficiently?"
"""

from math import sqrt


def cosine_similarity(a, b):
    # YOUR CODE HERE
    dot = sum(x*y for x, y in zip(a,b))
    mag_a = sqrt(sum(x*x for x in a))
    mag_b = sqrt(sum(x*x for x in b))

    if mag_a == 0  or mag_b == 0:
        return 0.0

    return dot / (mag_a * mag_b)
    pass


def top_k(query, docs, k):
    #keep track of scores for each doc
    scored = []
    # for every doc score the doc against the query
    for doc_id, embedding in docs:
        score = cosine_similarity(query, embedding)
        scored.append((doc_id, score))

    # reorder the results with highest on top
    scored.sort(key=lambda x: x[1], reverse=True)
    # return the top k results
    return scored[:k]
    pass


# ============================================================
# TESTS — don't modify below this line
# ============================================================

def test_cosine_similarity():
    # identical vectors should return 1.0
    score = cosine_similarity([1, 0, 0], [1, 0, 0])
    assert score is not None, "cosine_similarity returned None — did you forget to return?"
    assert abs(score - 1.0) < 0.001, f"Same vector should be 1.0, got {score}"

    # perpendicular vectors should return 0.0
    score = cosine_similarity([1, 0], [0, 1])
    assert abs(score - 0.0) < 0.001, f"Perpendicular should be 0.0, got {score}"

    # known value
    score = cosine_similarity([1, 2, 3], [4, 5, 6])
    expected = 32 / (sqrt(14) * sqrt(77))  # dot=32, mag_a=sqrt(14), mag_b=sqrt(77)
    assert abs(score - expected) < 0.001, f"Expected {expected:.4f}, got {score:.4f}"

    # zero vector should return 0.0
    score = cosine_similarity([0, 0, 0], [1, 2, 3])
    assert abs(score - 0.0) < 0.001, f"Zero vector should be 0.0, got {score}"

    print("  cosine_similarity: ALL PASSED")


def test_top_k():
    query = [0.2, 0.5, 0.3]
    docs = [
        ("doc1", [0.1, 0.5, 0.4]),
        ("doc2", [0.9, 0.1, 0.2]),
        ("doc3", [0.2, 0.6, 0.2]),
    ]

    result = top_k(query, docs, 2)
    assert result is not None, "top_k returned None — did you forget to return?"
    assert len(result) == 2, f"Expected 2 results, got {len(result)}"

    # doc3 should be first (most similar), doc1 second
    assert result[0][0] == "doc3", f"First result should be doc3, got {result[0][0]}"
    assert result[1][0] == "doc1", f"Second result should be doc1, got {result[1][0]}"

    # scores should be floats between 0 and 1
    assert 0.9 < result[0][1] < 1.0, f"doc3 score should be ~0.978, got {result[0][1]}"
    assert 0.9 < result[1][1] < 1.0, f"doc1 score should be ~0.976, got {result[1][1]}"

    # k=1 should return only 1 result
    result = top_k(query, docs, 1)
    assert len(result) == 1, f"k=1 should give 1 result, got {len(result)}"

    print("  top_k: ALL PASSED")


if __name__ == "__main__":
    print("Testing 01: Top-K Cosine Similarity\n")
    try:
        test_cosine_similarity()
    except Exception as e:
        print(f"  cosine_similarity: FAILED - {e}")
    try:
        test_top_k()
    except Exception as e:
        print(f"  top_k: FAILED - {e}")
