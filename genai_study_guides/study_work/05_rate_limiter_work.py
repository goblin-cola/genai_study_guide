"""PRACTICE: Rate Limiter

Implement class RateLimiter with:

    __init__(self, max_requests, window_seconds)
    allow(self, user_id, now) -> True or False

- Each user can make at most max_requests in the last window_seconds
- Uses a sliding window (deque of timestamps per user)
- Same pattern as sliding window counts!

Run this file to check: python 05_rate_limiter_work.py

INTERVIEW QUESTIONS (this topic):
1. "Design a rate limiter that allows at most N requests per user in a sliding time
   window. What's the time complexity of each request check?"
2. "We're seeing abuse on our API. Implement a per-user rate limiter using a sliding
   window approach. How would you handle concurrent requests in production?"
3. "How is a sliding window rate limiter different from a fixed window one? Implement
   the sliding window version."
"""

from collections import deque


class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        # YOUR CODE HERE
        pass

    def allow(self, user_id, now):
        # YOUR CODE HERE
        pass


# ============================================================
# TESTS
# ============================================================

def test_basic():
    rl = RateLimiter(max_requests=3, window_seconds=60)
    assert rl.allow("u1", 1000) == True, "1st request should be allowed"
    assert rl.allow("u1", 1001) == True, "2nd request should be allowed"
    assert rl.allow("u1", 1002) == True, "3rd request should be allowed"
    assert rl.allow("u1", 1003) == False, "4th request should be denied (limit=3)"
    print("  basic: PASSED")


def test_window_expiry():
    rl = RateLimiter(max_requests=2, window_seconds=10)
    assert rl.allow("u1", 100) == True
    assert rl.allow("u1", 105) == True
    assert rl.allow("u1", 108) == False  # 2 in window, denied

    # at t=111, the t=100 request expires (111-10=101, and 100 <= 101)
    assert rl.allow("u1", 111) == True, "Old request should have expired"
    print("  window_expiry: PASSED")


def test_separate_users():
    rl = RateLimiter(max_requests=1, window_seconds=60)
    assert rl.allow("u1", 100) == True
    assert rl.allow("u2", 100) == True, "Different users should have separate limits"
    assert rl.allow("u1", 101) == False, "u1 should be rate limited"
    assert rl.allow("u2", 101) == False, "u2 should be rate limited"
    print("  separate_users: PASSED")


if __name__ == "__main__":
    print("Testing 05: Rate Limiter\n")
    for test in [test_basic, test_window_expiry, test_separate_users]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
