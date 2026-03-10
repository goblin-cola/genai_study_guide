"""PRACTICE: Prompt Builder with Token Budget

Implement two functions:

1. estimate_tokens(text)
   - Returns len(text) // 4  (rough: 1 token ~ 4 chars)

2. build_prompt(system, query, chunks, max_tokens)
   - system and query are always included
   - Pack as many chunks as fit (best first, greedy)
   - Format: "System: {system}\n\nContext:\n[1] chunk1\n[2] chunk2\n\nUser: {query}"
   - Return (prompt_string, num_chunks_used)

Run this file to check: python 08_prompt_builder_work.py

INTERVIEW QUESTIONS (this topic):
1. "You have a system prompt, a user query, and a list of retrieved context chunks, but
   a fixed token budget. How would you greedily pack as many chunks as possible into
   the prompt without exceeding the limit?"
2. "Design a prompt construction function for a RAG system that respects a max token
   count. How would you estimate token usage without calling the tokenizer?"
"""


def estimate_tokens(text):
    # YOUR CODE HERE
    pass


def build_prompt(system, query, chunks, max_tokens):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def test_estimate_tokens():
    assert estimate_tokens("") == 0, "Empty string should be 0 tokens"
    assert estimate_tokens("abcd") == 1, "4 chars should be 1 token"
    assert estimate_tokens("abcdefgh") == 2, "8 chars should be 2 tokens"
    print("  estimate_tokens: PASSED")


def test_all_chunks_fit():
    prompt, used = build_prompt("sys", "q", ["short"], max_tokens=100)
    assert prompt is not None, "Returned None — did you forget to return?"
    assert used == 1, f"Expected 1 chunk used, got {used}"
    assert "[1] short" in prompt, "Chunk should appear in prompt"
    assert "System: sys" in prompt, "System prompt should appear"
    assert "User: q" in prompt, "Query should appear"
    print("  all_chunks_fit: PASSED")


def test_budget_limits_chunks():
    chunks = ["A" * 100, "B" * 100, "C" * 100]  # each ~25 tokens
    prompt, used = build_prompt("sys", "q", chunks, max_tokens=35)
    assert used < 3, f"Budget is tight, shouldn't fit all 3 chunks (used {used})"
    assert used >= 1, f"Should fit at least 1 chunk (used {used})"
    print("  budget_limits_chunks: PASSED")


def test_no_chunks_fit():
    # system + query alone use up the budget
    prompt, used = build_prompt("A" * 80, "B" * 80, ["chunk1"], max_tokens=40)
    assert used == 0, f"No room for chunks, expected 0, got {used}"
    print("  no_chunks_fit: PASSED")


def test_empty_chunks():
    prompt, used = build_prompt("sys", "q", [], max_tokens=100)
    assert used == 0, f"No chunks given, expected 0, got {used}"
    print("  empty_chunks: PASSED")


if __name__ == "__main__":
    print("Testing 08: Prompt Builder\n")
    for test in [test_estimate_tokens, test_all_chunks_fit, test_budget_limits_chunks,
                 test_no_chunks_fit, test_empty_chunks]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
