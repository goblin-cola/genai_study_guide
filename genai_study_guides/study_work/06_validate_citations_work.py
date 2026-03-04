"""PRACTICE: Citation Validation

Implement: validate_citations(retrieved, citations)

- retrieved = list of chunk IDs we actually fetched
- citations = list of chunk IDs the LLM claims to cite
- Return only citations that exist in retrieved
- Preserve the LLM's citation order

Hint: convert retrieved to a set for fast lookups.

Run this file to check: python 06_validate_citations_work.py
"""


def validate_citations(retrieved, citations):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def test_basic():
    result = validate_citations(["c1", "c2", "c3"], ["c2", "c5", "c1"])
    assert result is not None, "Returned None — did you forget to return?"
    assert result == ["c2", "c1"], f"Expected ['c2', 'c1'], got {result}"
    print("  basic: PASSED")


def test_all_valid():
    result = validate_citations(["c1", "c2"], ["c1", "c2"])
    assert result == ["c1", "c2"], f"All valid, expected ['c1', 'c2'], got {result}"
    print("  all_valid: PASSED")


def test_all_hallucinated():
    result = validate_citations(["c1", "c2"], ["c99", "c100"])
    assert result == [], f"All fake, expected [], got {result}"
    print("  all_hallucinated: PASSED")


def test_preserves_order():
    result = validate_citations(["c1", "c2", "c3"], ["c3", "c1"])
    assert result == ["c3", "c1"], f"Should preserve LLM's order, got {result}"
    print("  preserves_order: PASSED")


def test_empty():
    assert validate_citations([], ["c1"]) == [], "Empty retrieved should give empty"
    assert validate_citations(["c1"], []) == [], "Empty citations should give empty"
    print("  empty: PASSED")


if __name__ == "__main__":
    print("Testing 06: Citation Validation\n")
    for test in [test_basic, test_all_valid, test_all_hallucinated, test_preserves_order, test_empty]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
