"""PRACTICE: Merge Ranked Results

Implement: merge_results(list_a, list_b)

- Each list = [(doc_id, score), ...]
- Merge into one list, deduplicated by doc_id
- If a doc appears in both, keep the HIGHER score
- Return sorted by score descending

Run this file to check: python 03_merge_results_work.py
"""


def merge_results(list_a, list_b):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def test_basic_merge():
    vec = [("docA", 0.90), ("docB", 0.80)]
    kw = [("docB", 0.95), ("docC", 0.70)]
    result = merge_results(vec, kw)
    assert result is not None, "Returned None — did you forget to return?"
    assert len(result) == 3, f"Expected 3 results, got {len(result)}"
    assert result[0] == ("docB", 0.95), f"First should be docB=0.95, got {result[0]}"
    assert result[1] == ("docA", 0.90), f"Second should be docA=0.90, got {result[1]}"
    assert result[2] == ("docC", 0.70), f"Third should be docC=0.70, got {result[2]}"
    print("  basic_merge: PASSED")


def test_no_overlap():
    a = [("d1", 0.9)]
    b = [("d2", 0.8)]
    result = merge_results(a, b)
    assert len(result) == 2, f"Expected 2, got {len(result)}"
    assert result[0][0] == "d1", f"d1 should be first (higher score)"
    print("  no_overlap: PASSED")


def test_full_overlap():
    a = [("d1", 0.5), ("d2", 0.3)]
    b = [("d1", 0.8), ("d2", 0.9)]
    result = merge_results(a, b)
    assert len(result) == 2, f"Expected 2, got {len(result)}"
    assert result[0] == ("d2", 0.9), f"d2=0.9 should be first, got {result[0]}"
    assert result[1] == ("d1", 0.8), f"d1=0.8 should be second, got {result[1]}"
    print("  full_overlap: PASSED")


def test_empty_lists():
    result = merge_results([], [("d1", 0.5)])
    assert len(result) == 1, f"Expected 1, got {len(result)}"
    result = merge_results([], [])
    assert len(result) == 0, f"Expected 0, got {len(result)}"
    print("  empty_lists: PASSED")


if __name__ == "__main__":
    print("Testing 03: Merge Ranked Results\n")
    for test in [test_basic_merge, test_no_overlap, test_full_overlap, test_empty_lists]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
