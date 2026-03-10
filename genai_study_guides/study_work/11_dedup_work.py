"""PRACTICE: Deduplicate Chunks by Similarity

Implement two functions:

1. jaccard(text_a, text_b)
   - Split each text into a set of lowercase words
   - Return |intersection| / |union|
   - (words in common) / (total unique words)

2. dedup_chunks(chunks, threshold=0.7)
   - chunks = [(chunk_id, text), ...] ranked by relevance (best first)
   - For each chunk, check if it's too similar to any already-kept chunk
   - If jaccard >= threshold, skip it (it's a duplicate)
   - Return the filtered list

Run this file to check: python 11_dedup_work.py

INTERVIEW QUESTIONS (this topic):
1. "Our retrieval system sometimes returns near-duplicate chunks. How would you filter
   out chunks that are too similar to ones already selected? Implement a deduplication
   function using Jaccard similarity."
2. "Implement Jaccard similarity between two text strings. Then use it to deduplicate a
   ranked list of search results, keeping the first occurrence when two items are above
   a similarity threshold."
"""


def jaccard(text_a, text_b):
    # YOUR CODE HERE
    pass


def dedup_chunks(chunks, threshold=0.7):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def test_jaccard_identical():
    score = jaccard("the cat sat", "the cat sat")
    assert score is not None, "Returned None — did you forget to return?"
    assert abs(score - 1.0) < 0.01, f"Identical text should be 1.0, got {score}"
    print("  jaccard_identical: PASSED")


def test_jaccard_partial():
    score = jaccard("the cat sat", "the cat slept")
    # common: {the, cat} = 2, union: {the, cat, sat, slept} = 4
    assert abs(score - 0.5) < 0.01, f"Expected 0.5, got {score}"
    print("  jaccard_partial: PASSED")


def test_jaccard_no_overlap():
    score = jaccard("hello world", "foo bar")
    assert abs(score - 0.0) < 0.01, f"No overlap should be 0.0, got {score}"
    print("  jaccard_no_overlap: PASSED")


def test_dedup_removes_similar():
    chunks = [
        ("c1", "RAG combines retrieval with generation to ground LLM responses"),
        ("c2", "RAG combines retrieval with generation to ground LLM outputs"),  # ~80% similar to c1
        ("c3", "Vector databases store embeddings for fast search"),
    ]
    result = dedup_chunks(chunks, threshold=0.7)
    assert result is not None, "Returned None — did you forget to return?"
    ids = [cid for cid, _ in result]
    assert "c1" in ids, "c1 should be kept (it's first)"
    assert "c2" not in ids, "c2 should be removed (too similar to c1)"
    assert "c3" in ids, "c3 should be kept (different topic)"
    print("  dedup_removes_similar: PASSED")


def test_dedup_keeps_all_if_different():
    chunks = [
        ("c1", "apples are red fruit"),
        ("c2", "dogs are loyal pets"),
        ("c3", "python is a programming language"),
    ]
    result = dedup_chunks(chunks, threshold=0.7)
    assert len(result) == 3, f"All different, should keep all 3, got {len(result)}"
    print("  dedup_keeps_all_if_different: PASSED")


if __name__ == "__main__":
    print("Testing 11: Dedup Chunks\n")
    for test in [test_jaccard_identical, test_jaccard_partial, test_jaccard_no_overlap,
                 test_dedup_removes_similar, test_dedup_keeps_all_if_different]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
