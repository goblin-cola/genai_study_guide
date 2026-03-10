"""PRACTICE: Rule Engine (Risk Decisioning)

Implement: evaluate(transaction, rules)

- transaction = dict with keys like "amount", "user_age_days", "device_new", etc.
- rules = list of dicts, each with:
    "name":  string label
    "level": "block" or "review"
    "check": function that takes transaction, returns True/False
- Run ALL rules against the transaction
- Return (decision, triggered_rule_names)
    decision: "block" if any block rule fired
              "review" if any review rule fired (but no blocks)
              "allow" if nothing fired

Run this file to check: python 13_rule_engine_work.py

INTERVIEW QUESTIONS (this topic):
1. "Design a simple rule engine where each rule has a name, a severity level (block or
   review), and a check function. Given a transaction, evaluate all rules and return
   the highest-severity decision along with which rules triggered."
2. "We need a configurable risk decisioning system. Business analysts define rules like
   'block if amount > 10000' or 'review if device is new.' How would you structure and
   evaluate these rules?"
"""


def evaluate(transaction, rules):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def make_rules():
    """Standard test rules."""
    return [
        {"name": "high_amount", "level": "block",
         "check": lambda tx: tx["amount"] > 10000},
        {"name": "new_user", "level": "review",
         "check": lambda tx: tx.get("user_age_days", 999) < 7},
        {"name": "new_device", "level": "review",
         "check": lambda tx: tx.get("device_new", False)},
    ]


def test_block():
    decision, names = evaluate({"amount": 15000, "user_age_days": 2}, make_rules())
    assert decision is not None, "Returned None — did you forget to return?"
    assert decision == "block", f"Expected block, got {decision}"
    assert "high_amount" in names, "high_amount should have triggered"
    print("  block: PASSED")


def test_review():
    decision, names = evaluate({"amount": 500, "user_age_days": 3, "device_new": True}, make_rules())
    assert decision == "review", f"Expected review, got {decision}"
    assert "new_user" in names, "new_user should have triggered"
    assert "new_device" in names, "new_device should have triggered"
    assert "high_amount" not in names, "high_amount should NOT have triggered"
    print("  review: PASSED")


def test_allow():
    decision, names = evaluate({"amount": 50, "user_age_days": 365, "device_new": False}, make_rules())
    assert decision == "allow", f"Expected allow, got {decision}"
    assert len(names) == 0, f"No rules should trigger, got {names}"
    print("  allow: PASSED")


def test_block_beats_review():
    """If both block and review rules fire, decision should be block."""
    decision, names = evaluate({"amount": 15000, "device_new": True}, make_rules())
    assert decision == "block", f"Block should beat review, got {decision}"
    print("  block_beats_review: PASSED")


if __name__ == "__main__":
    print("Testing 13: Rule Engine\n")
    for test in [test_block, test_review, test_allow, test_block_beats_review]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
