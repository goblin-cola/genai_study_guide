"""Study Guide #13: Simple Rule Engine (Risk Decisioning)

PROBLEM
-------
Evaluate a transaction against a list of rules.
Each rule has a name, a severity level, and a check function.

Return a decision:
  - "block"  if ANY blocking rule triggers
  - "review" if ANY review rule triggers (but no blocks)
  - "allow"  if nothing triggers

WHY THIS SHOWS UP IN FRAUD/OSCILAR
-----------------------------------
Oscilar is a "risk decisioning platform." This is literally their product:
rules like "block if amount > $10k" or "review if new device + high amount."

EXAMPLE
-------
transaction = {"amount": 15000, "user_age_days": 2}
-> decision: "block", reasons: ["amount_over_10k"]

"""


def evaluate(transaction, rules):
    """Run every rule against a transaction. Return (decision, list of triggered rule names).

    rules = list of dicts, each with:
      "name":  string label for the rule
      "level": "block" or "review"
      "check": a function that takes the transaction and returns True/False
    """

    triggered = []

    # run every single rule (we always run ALL of them for audit purposes)
    for rule in rules:
        # rule["check"] is a function — call it with the transaction
        # in JS this would be: rule.check(transaction)
        if rule["check"](transaction):
            triggered.append(rule)

    # pick the harshest decision
    # "block" beats "review" beats "allow"
    #
    # any() checks if at least one item matches — like .some() in JS
    if any(r["level"] == "block" for r in triggered):
        decision = "block"
    elif any(r["level"] == "review" for r in triggered):
        decision = "review"
    else:
        decision = "allow"

    # return the decision + which rules fired (for logging / auditing)
    triggered_names = [r["name"] for r in triggered]
    return decision, triggered_names


if __name__ == "__main__":
    # --- define the rules ---
    # each rule is just a dict with a name, level, and check function
    # "lambda tx:" is Python's arrow function: (tx) => in JS
    rules = [
        {
            "name": "amount_over_10k",
            "level": "block",
            "check": lambda tx: tx["amount"] > 10000,
        },
        {
            "name": "new_user_high_amount",
            "level": "review",
            # .get("key", default) is like (tx.key ?? default) in JS
            "check": lambda tx: tx.get("user_age_days", 999) < 7 and tx["amount"] > 500,
        },
        {
            "name": "new_device",
            "level": "review",
            "check": lambda tx: tx.get("device_new", False),
        },
        {
            "name": "suspicious_country",
            "level": "block",
            # "in" checks membership — like ["XX","YY"].includes(tx.country) in JS
            "check": lambda tx: tx.get("country") in ("XX", "YY"),
        },
    ]

    # --- test transactions ---
    transactions = [
        {"amount": 15000, "user_age_days": 2, "device_new": True, "country": "US"},
        {"amount": 200, "user_age_days": 365, "device_new": False, "country": "US"},
        {"amount": 800, "user_age_days": 3, "device_new": True, "country": "US"},
        {"amount": 50, "user_age_days": 100, "device_new": False, "country": "XX"},
    ]

    for i, tx in enumerate(transactions):
        decision, reasons = evaluate(tx, rules)
        print(f"TX{i+1} amt=${tx['amount']:>6} -> {decision:>6}  rules: {reasons}")
