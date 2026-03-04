"""PRACTICE: Sliding Window Event Counts

Implement: sliding_window_counts(events, window_seconds)

- events = list of (user_id, amount, timestamp) sorted by timestamp
- window_seconds = how far back to look
- For each event, count how many events this user has in the window
- Return list of (user_id, timestamp, count)

Hint: use a deque per user. Add timestamps, remove expired ones from front.

Run this file to check: python 02_sliding_window_work.py
"""

from collections import deque


def sliding_window_counts(events, window_seconds):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def test_basic():
    events = [
        ("user1", 100, 1),
        ("user1",  50, 5),
        ("user1",  70, 7),
        ("user2", 200, 8),
    ]
    result = sliding_window_counts(events, 5)
    assert result is not None, "Returned None — did you forget to return?"
    assert len(result) == 4, f"Expected 4 results, got {len(result)}"

    # (user1, 1, 1) — first event, count=1
    assert result[0] == ("user1", 1, 1), f"Expected ('user1', 1, 1), got {result[0]}"
    # (user1, 5, 2) — t=1 and t=5 both in window
    assert result[1] == ("user1", 5, 2), f"Expected ('user1', 5, 2), got {result[1]}"
    # (user1, 7, 2) — t=1 expired (7-5=2 > 1), t=5 and t=7 remain
    assert result[2] == ("user1", 7, 2), f"Expected ('user1', 7, 2), got {result[2]}"
    # (user2, 8, 1) — different user, own window
    assert result[3] == ("user2", 8, 1), f"Expected ('user2', 8, 1), got {result[3]}"

    print("  basic: PASSED")


def test_single_user_all_in_window():
    events = [("u1", 10, 1), ("u1", 20, 2), ("u1", 30, 3)]
    result = sliding_window_counts(events, 100)
    assert result[2] == ("u1", 3, 3), f"All should be in window, got {result[2]}"
    print("  all_in_window: PASSED")


def test_window_zero():
    events = [("u1", 10, 1), ("u1", 20, 2)]
    result = sliding_window_counts(events, 0)
    # window=0 means only the exact same timestamp counts
    assert result[0][2] == 1, f"Window=0, first event count should be 1, got {result[0][2]}"
    print("  window_zero: PASSED")


if __name__ == "__main__":
    print("Testing 02: Sliding Window Counts\n")
    for test in [test_basic, test_single_user_all_in_window, test_window_zero]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
