"""PRACTICE: Graph-Based Risk Scoring

Implement: score_users(edges, known_fraudsters)

- edges = list of (user_a, user_b, shared_attribute)
- known_fraudsters = set of user IDs
- Build a graph from edges (adjacency list)
- BFS from all known fraudsters to compute distances
- Return dict: {user_id: (risk_level, hops)}
    0 hops = "known_fraud"
    1 hop  = "high"
    2 hops = "medium"
    3+ or no connection = "low"

Hint: use a deque for BFS. Start all fraudsters at distance 0.

Run this file to check: python 14_graph_scoring_work.py
"""

from collections import deque


def score_users(edges, known_fraudsters):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def test_basic():
    edges = [
        ("bad1", "user2", "same_device"),
        ("user2", "user3", "same_ip"),
    ]
    result = score_users(edges, {"bad1"})
    assert result is not None, "Returned None — did you forget to return?"

    level, hops = result["bad1"]
    assert level == "known_fraud", f"bad1 should be known_fraud, got {level}"
    assert hops == 0, f"bad1 should be 0 hops, got {hops}"

    level, hops = result["user2"]
    assert level == "high", f"user2 should be high (1 hop), got {level}"

    level, hops = result["user3"]
    assert level == "medium", f"user3 should be medium (2 hops), got {level}"

    print("  basic: PASSED")


def test_disconnected():
    edges = [
        ("bad1", "user2", "same_device"),
        ("user5", "user6", "same_ip"),  # no connection to bad1
    ]
    result = score_users(edges, {"bad1"})

    level, _ = result["user5"]
    assert level == "low", f"user5 is disconnected, should be low, got {level}"
    level, _ = result["user6"]
    assert level == "low", f"user6 is disconnected, should be low, got {level}"
    print("  disconnected: PASSED")


def test_multiple_fraudsters():
    edges = [
        ("bad1", "user2", "same_device"),
        ("bad2", "user3", "same_ip"),
        ("user2", "user3", "same_email"),
    ]
    result = score_users(edges, {"bad1", "bad2"})

    # both user2 and user3 are 1 hop from a fraudster
    assert result["user2"][0] == "high", f"user2 should be high, got {result['user2'][0]}"
    assert result["user3"][0] == "high", f"user3 should be high, got {result['user3'][0]}"
    print("  multiple_fraudsters: PASSED")


def test_3_hops_is_low():
    edges = [
        ("bad1", "u2", "x"),
        ("u2", "u3", "x"),
        ("u3", "u4", "x"),  # 3 hops from bad1
    ]
    result = score_users(edges, {"bad1"})
    level, hops = result["u4"]
    assert level == "low", f"3 hops should be low, got {level}"
    assert hops == 3, f"Should be 3 hops, got {hops}"
    print("  3_hops_is_low: PASSED")


if __name__ == "__main__":
    print("Testing 14: Graph Risk Scoring\n")
    for test in [test_basic, test_disconnected, test_multiple_fraudsters, test_3_hops_is_low]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
