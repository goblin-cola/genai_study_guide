"""Study Guide #2: Sliding Window Event Counts (per User)

PROBLEM
-------
Given a time-ordered stream of events: (user_id, amount, timestamp)

For each event, count how many events that user has had in the last W seconds.

WHY THIS SHOWS UP IN FRAUD/GENAI
---------------------------------
"How many transactions has this user made in the last 60 seconds?"
This is the #1 fraud velocity feature. Also used for rate limiting API calls.
This same pattern is the foundation of #5 (rate limiter) and #12 (feature aggregation).

EXAMPLE (window = 5 seconds)
-----------------------------
("user1", 100, 1)  -> count=1   window has: [1]
("user1",  50, 5)  -> count=2   window has: [1, 5]
("user1",  70, 7)  -> count=2   window has: [5, 7]     (t=1 expired, 7-5=2 > 1)
("user2", 200, 8)  -> count=1   window has: [8]         (different user, own window)

THE PATTERN
-----------
For each user, keep a queue of their recent timestamps.
When a new event comes in:
  1. Add it to the queue
  2. Remove anything too old from the front
  3. The queue length = your count

This is O(n) because each timestamp is added once and removed once.

"""

from collections import deque


def sliding_window_counts(events, window_seconds):
    """For each event, compute how many events this user has in the window.

    events = list of (user_id, amount, timestamp), sorted by timestamp
    window_seconds = how far back to look

    Returns list of (user_id, timestamp, count)
    """

    # each user gets their own deque (queue) of timestamps
    # deque = double-ended queue, efficient to add/remove from both ends
    # in JS: just an array, but shift() is O(n) — deque is O(1) for popleft
    per_user = {}
    results = []

    for user_id, _amount, ts in events:
        # _amount: underscore means "I'm ignoring this value"
        # we only need the user and timestamp for counting

        # get or create this user's queue
        if user_id not in per_user:
            per_user[user_id] = deque()
        q = per_user[user_id]

        # add the current timestamp
        q.append(ts)

        # remove timestamps that have fallen outside the window
        # cutoff = "anything before this time is too old"
        # example: ts=7, window=5 -> cutoff=2 -> remove anything < 2
        cutoff = ts - window_seconds
        while q and q[0] < cutoff:
            q.popleft()  # remove from front (oldest)

        # whatever is left in the queue = events in the window
        count = len(q)
        results.append((user_id, ts, count))

    return results


if __name__ == "__main__":
    events = [
        ("user1", 100, 1),
        ("user1",  50, 5),
        ("user1",  70, 7),
        ("user2", 200, 8),
    ]
    window_seconds = 5

    print(f"Window: {window_seconds} seconds\n")

    results = sliding_window_counts(events, window_seconds)
    for user_id, ts, count in results:
        print(f"  {user_id} at t={ts} -> {count} events in window")

    # Expected:
    # user1 at t=1 -> 1 events in window
    # user1 at t=5 -> 2 events in window
    # user1 at t=7 -> 2 events in window  (t=1 expired)
    # user2 at t=8 -> 1 events in window  (separate user)
