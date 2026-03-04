"""Study Guide #12: Real-Time Feature Aggregation (Fraud Signals)

PROBLEM
-------
Given a stream of transactions, compute fraud features per transaction:
  - count: how many transactions this user made in the last W seconds
  - total: sum of amounts in the last W seconds
  - avg: average amount in the last W seconds
  - velocity_change: is current amount > 2x the user's recent average?

WHY THIS SHOWS UP IN FRAUD/OSCILAR
-----------------------------------
Fraud detection = real-time features. "User spent $5000 in the last 10 min"
or "this transaction is 3x their average" are classic fraud signals.

EXAMPLE
-------
events = [("user1", 100, 1000), ("user1", 50, 1001), ("user1", 500, 1002)]
window = 60

user1 at t=1002: count=3, total=650, avg=216, velocity_change=True
  (because 500 > 2 * average of previous [100, 50] = 150)

"""

from collections import deque


def compute_features(events, window):
    # each user gets their own sliding window (a deque of recent transactions)
    # deque = double-ended queue, like an array you can efficiently pop from the front
    # in JS: just an array with shift() and push()
    user_windows = {}
    results = []

    for user_id, amount, ts in events:

        # get or create this user's window
        if user_id not in user_windows:
            user_windows[user_id] = deque()
        q = user_windows[user_id]

        # add current transaction to the window
        q.append((ts, amount))

        # remove transactions that are too old
        # cutoff = "anything before this time is expired"
        cutoff = ts - window
        while q and q[0][0] < cutoff:
            q.popleft()  # drop from the front (oldest first)

        # --- compute features from whatever is left in the window ---

        # count: just how many transactions are in the window
        count = len(q)

        # total: add up all the amounts
        # sum(amt for _, amt in q) means "for each (timestamp, amount) in q, sum the amounts"
        # the _ means "I don't care about the timestamp here"
        total = sum(amt for _, amt in q)

        # avg: total / count (basic average)
        avg = total / count

        # velocity_change: is THIS transaction suspiciously large?
        # we compare it to the average of PREVIOUS transactions (not including this one)
        # formula: current_amount > 2 * average_of_previous_transactions
        prev_count = count - 1
        if prev_count > 0:
            prev_avg = (total - amount) / prev_count
            velocity_change = amount > 2 * prev_avg
        else:
            velocity_change = False  # first transaction ever, nothing to compare to

        results.append({
            "user_id": user_id,
            "amount": amount,
            "count": count,
            "total": total,
            "avg": avg,
            "velocity_change": velocity_change,
        })

    return results


if __name__ == "__main__":
    events = [
        ("user1", 100.0, 1000),   # first transaction
        ("user1",  50.0, 1001),   # normal
        ("user1",  75.0, 1002),   # normal
        ("user1", 500.0, 1003),   # big spike! should trigger velocity_change
        ("user2",  20.0, 1001),   # different user, separate window
        ("user2",  25.0, 1002),
    ]

    results = compute_features(events, window=60)

    for r in results:
        flag = " << SUSPICIOUS" if r["velocity_change"] else ""
        print(f'{r["user_id"]} amt=${r["amount"]:<6.0f} '
              f'count={r["count"]} total=${r["total"]:.0f} avg=${r["avg"]:.0f} '
              f'velocity_spike={r["velocity_change"]}{flag}')
