"""Study Guide #5: Rate Limiter (Sliding Window)

PROBLEM
-------
Implement a per-user rate limiter:
    allow(user_id, timestamp) -> True or False

Each user can make at most N requests in the last W seconds.
If they exceed the limit, return False.

WHY THIS SHOWS UP IN GENAI
--------------------------
LLM APIs are expensive. You MUST rate limit per user/tenant to prevent
abuse and control costs. OpenAI, Anthropic, etc. all enforce rate limits.

This uses the exact same sliding window pattern as #02:
  1. Keep a queue of timestamps per user
  2. Drop expired ones from the front
  3. Check if the queue is full

EXAMPLE
-------
N=3, Window=60 seconds

allow("u1", 1000) -> True   queue: [1000]
allow("u1", 1001) -> True   queue: [1000, 1001]
allow("u1", 1002) -> True   queue: [1000, 1001, 1002]
allow("u1", 1003) -> False  queue is full! (3 items, max is 3)

"""

from collections import deque


class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # each user gets their own queue of timestamps
        # in JS: this.hits = new Map()  // userId -> []
        self.hits = {}

    def allow(self, user_id, now):
        """Returns True if the request is allowed, False if rate limited."""

        # get or create this user's queue
        if user_id not in self.hits:
            self.hits[user_id] = deque()
        q = self.hits[user_id]

        # remove timestamps outside the window
        # "now - window" = the oldest timestamp we still care about
        cutoff = now - self.window_seconds
        while q and q[0] <= cutoff:
            q.popleft()  # drop from front (oldest)

        # check if they've hit the limit
        if len(q) >= self.max_requests:
            return False  # too many requests, denied

        # allow it and record the timestamp
        q.append(now)
        return True


if __name__ == "__main__":
    rl = RateLimiter(max_requests=3, window_seconds=60)

    print("N=3, Window=60 seconds\n")

    # user1 makes 4 requests in quick succession
    for t in [1000, 1001, 1002, 1003]:
        result = rl.allow("u1", t)
        print(f"  allow('u1', {t}) -> {result}")

    # Expected: True, True, True, False

    # after the window expires, they can request again
    print()
    result = rl.allow("u1", 1061)  # 1061 - 60 = 1001, so t=1000 expired
    print(f"  allow('u1', 1061) -> {result}")
    # Expected: True (t=1000 fell outside the window)
