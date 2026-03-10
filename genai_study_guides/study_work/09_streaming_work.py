"""PRACTICE: Streaming Response Aggregator

Implement: aggregate_stream(token_iterator, max_tokens=500, stop_phrase="[DONE]")

- Collect tokens into a string
- Stop if stop_phrase appears in a token (keep text before it)
- Stop if max_tokens tokens have been consumed
- Return (text, stop_reason)
  - stop_reason: "stop_phrase", "max_tokens", or "end_of_stream"
- Strip whitespace from the final text

Run this file to check: python 09_streaming_work.py

INTERVIEW QUESTIONS (this topic):
1. "Our LLM streams tokens one at a time. Write a function that collects them into a
   final string, stopping when it sees a stop phrase or hits a max token count. Return
   the text and the reason it stopped."
2. "How would you handle consuming a streaming LLM response where you need to enforce
   both a stop sequence and a max output length?"
"""


def aggregate_stream(token_iterator, max_tokens=500, stop_phrase="[DONE]"):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def test_stop_phrase():
    tokens = ["Hello", " world", "!", " [DONE]", " extra"]
    text, reason = aggregate_stream(iter(tokens))
    assert reason == "stop_phrase", f"Expected stop_phrase, got {reason}"
    assert text == "Hello world!", f"Expected 'Hello world!', got '{text}'"
    print("  stop_phrase: PASSED")


def test_max_tokens():
    tokens = ["one ", "two ", "three ", "four ", "five "]
    text, reason = aggregate_stream(iter(tokens), max_tokens=3)
    assert reason == "max_tokens", f"Expected max_tokens, got {reason}"
    assert "one" in text and "three" in text, f"Should have first 3 tokens, got '{text}'"
    assert "four" not in text, f"Should NOT have 4th token, got '{text}'"
    print("  max_tokens: PASSED")


def test_end_of_stream():
    tokens = ["This ", "is ", "complete."]
    text, reason = aggregate_stream(iter(tokens))
    assert reason == "end_of_stream", f"Expected end_of_stream, got {reason}"
    assert text == "This is complete.", f"Expected 'This is complete.', got '{text}'"
    print("  end_of_stream: PASSED")


def test_empty():
    text, reason = aggregate_stream(iter([]))
    assert reason == "end_of_stream", f"Expected end_of_stream, got {reason}"
    assert text == "", f"Expected empty string, got '{text}'"
    print("  empty: PASSED")


if __name__ == "__main__":
    print("Testing 09: Streaming Aggregator\n")
    for test in [test_stop_phrase, test_max_tokens, test_end_of_stream, test_empty]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
