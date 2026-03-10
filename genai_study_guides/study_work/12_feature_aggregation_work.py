"""PRACTICE: Real-Time Feature Aggregation (Fraud)

Implement: compute_features(events, window)

- events = list of (user_id, amount, timestamp)
- window = seconds to look back
- For each event, compute:
    count:   how many transactions in the window
    total:   sum of amounts in the window
    avg:     average amount in the window
    velocity_change: is current amount > 2x the average of PREVIOUS transactions?
      (if first transaction, velocity_change = False)

- Return list of dicts: {"user_id", "amount", "count", "total", "avg", "velocity_change"}

This builds on the sliding window pattern from #02!

Run this file to check: python 12_feature_aggregation_work.py

INTERVIEW QUESTIONS (this topic):
1. "For each incoming transaction, we need to compute real-time features: count, total,
   and average spend in the last N seconds, plus a velocity flag if the current amount
   is more than 2x the running average. How would you implement this?"
2. "Design a feature engineering pipeline for fraud detection that computes sliding
   window aggregates per user in a single pass over an event stream."
3. "What is a velocity change indicator in fraud detection? Implement it as part of a
   real-time feature computation system."
"""

from collections import deque


def compute_features(events, window):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def test_basic_counts():
    events = [("u1", 100, 1000), ("u1", 50, 1001), ("u1", 75, 1002)]
    result = compute_features(events, 60)
    assert result is not None, "Returned None — did you forget to return?"
    assert len(result) == 3, f"Expected 3 results, got {len(result)}"
    assert result[0]["count"] == 1, f"First event count should be 1, got {result[0]['count']}"
    assert result[1]["count"] == 2, f"Second event count should be 2, got {result[1]['count']}"
    assert result[2]["count"] == 3, f"Third event count should be 3, got {result[2]['count']}"
    print("  basic_counts: PASSED")


def test_totals_and_avg():
    events = [("u1", 100, 1000), ("u1", 200, 1001)]
    result = compute_features(events, 60)
    assert result[1]["total"] == 300, f"Total should be 300, got {result[1]['total']}"
    assert result[1]["avg"] == 150, f"Avg should be 150, got {result[1]['avg']}"
    print("  totals_and_avg: PASSED")


def test_velocity_spike():
    events = [
        ("u1", 100, 1000),
        ("u1", 50, 1001),
        ("u1", 500, 1002),  # 500 > 2 * avg(100,50)=150 -> True
    ]
    result = compute_features(events, 60)
    assert result[0]["velocity_change"] == False, "First event should be False (no history)"
    assert result[1]["velocity_change"] == False, "50 is not > 2*100=200"
    assert result[2]["velocity_change"] == True, "500 > 2*75=150, should be True"
    print("  velocity_spike: PASSED")


def test_separate_users():
    events = [("u1", 100, 1000), ("u2", 200, 1001)]
    result = compute_features(events, 60)
    assert result[0]["count"] == 1, "u1 should have count 1"
    assert result[1]["count"] == 1, "u2 should have count 1 (separate window)"
    print("  separate_users: PASSED")


if __name__ == "__main__":
    print("Testing 12: Feature Aggregation\n")
    for test in [test_basic_counts, test_totals_and_avg, test_velocity_spike, test_separate_users]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
