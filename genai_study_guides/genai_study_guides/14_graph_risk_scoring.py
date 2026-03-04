"""Study Guide #14: Graph-Based Risk Scoring (Connected Fraudsters)

PROBLEM
-------
Users are connected by shared attributes (same device, same IP, same card).
Some users are known fraudsters.

Find how "close" each user is to a known fraudster:
  - 0 hops = known fraudster
  - 1 hop  = directly shares a device/IP with a fraudster -> high risk
  - 2 hops = connected through one person -> medium risk
  - 3+ or no connection -> low risk

This is BFS (breadth-first search) starting from the bad guys.

WHY THIS SHOWS UP IN FRAUD/OSCILAR
-----------------------------------
Fraud rings share devices, IPs, and payment methods. Start from a known
bad actor, walk the graph, and flag nearby accounts.

EXAMPLE
-------
bad1 --same_device-- user2 --same_ip-- user3 --same_email-- user4

bad1:  known_fraud (0 hops)
user2: high risk   (1 hop from bad1)
user3: medium risk (2 hops from bad1)
user4: low risk    (3 hops)

"""

from collections import deque


def score_users(edges, known_fraudsters):
    """BFS from known fraudsters to score all connected users.

    edges = list of (user_a, user_b, shared_attribute)
    known_fraudsters = set of user IDs we know are bad

    Returns dict: {user_id: (risk_level, hops)}
    """

    # --- Step 1: Build the graph ---
    # an adjacency list = for each user, store who they're connected to
    # in JS this would be: const graph = new Map()  // userId -> Set of neighbors
    graph = {}
    all_users = set()

    for a, b, _attribute in edges:
        # _attribute: the underscore means "i'm not using this variable"
        # we only care about WHO is connected, not WHY (for scoring)

        # add both directions (if A connects to B, then B connects to A)
        if a not in graph:
            graph[a] = set()  # set = like Set in JS, no duplicates
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)

        all_users.add(a)
        all_users.add(b)

    # --- Step 2: BFS from all known fraudsters ---
    # BFS = explore layer by layer (all 1-hops, then all 2-hops, etc.)
    # we start from ALL fraudsters at once (multi-source BFS)

    distances = {}  # user_id -> how many hops from nearest fraudster
    queue = deque()  # the BFS queue

    # seed the queue with known fraudsters at distance 0
    for f in known_fraudsters:
        distances[f] = 0
        queue.append(f)

    # process the queue
    while queue:
        user = queue.popleft()  # take next user from front of queue

        # look at everyone they're connected to
        for neighbor in graph.get(user, set()):
            # only visit each user once (first visit = shortest path)
            if neighbor not in distances:
                distances[neighbor] = distances[user] + 1
                queue.append(neighbor)  # add to back of queue

    # --- Step 3: Convert hop counts to risk levels ---
    results = {}
    for user in all_users:
        hops = distances.get(user)  # None if not connected to any fraudster

        if hops is None:
            results[user] = ("low", -1)
        elif hops == 0:
            results[user] = ("known_fraud", 0)
        elif hops == 1:
            results[user] = ("high", 1)
        elif hops == 2:
            results[user] = ("medium", 2)
        else:
            results[user] = ("low", hops)

    return results


if __name__ == "__main__":
    edges = [
        ("bad1", "user2", "same_device"),           # bad1 shares device with user2
        ("user2", "user3", "same_ip"),               # user2 shares IP with user3
        ("user3", "user4", "same_email_domain"),     # user3 shares email with user4
        ("user5", "user6", "same_device"),           # separate cluster, no fraud link
        ("bad1", "user7", "same_payment_method"),    # bad1 shares payment with user7
    ]

    known_fraudsters = {"bad1"}

    results = score_users(edges, known_fraudsters)

    print("=== Graph Risk Scores ===")
    for user in sorted(results):
        level, hops = results[user]
        hop_str = f"{hops} hops" if hops >= 0 else "no connection"
        print(f"  {user:>8}: {level:<12} ({hop_str})")
