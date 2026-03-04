"""Study Guide #9: Streaming Response Aggregator

PROBLEM
-------
An LLM streams back tokens one at a time (like ChatGPT typing).
Collect them into a final string, but stop early if:
  1. A stop phrase appears (e.g., "[DONE]")
  2. You hit a max token limit

Return the final text and WHY you stopped.

WHY THIS SHOWS UP IN GENAI
--------------------------
Production GenAI systems use streaming (stream=True) to show results as
they arrive instead of waiting for the full response. You need to handle
the stream correctly: collect tokens, detect stop conditions, enforce limits.

EXAMPLE
-------
tokens = ["Hello", " world", "!", " [DONE]", " extra"]
-> ("Hello world!", "stop_phrase")     — stopped at [DONE], ignored "extra"

tokens = ["one", "two", "three", "four"]
-> ("onetwothree", "max_tokens")       — stopped after 3 tokens

"""


def aggregate_stream(token_iterator, max_tokens=500, stop_phrase="[DONE]"):
    """Collect streamed tokens into a string.

    token_iterator = something you can loop over that gives you one token at a time
                     in JS: an async iterator you'd use with `for await (const token of stream)`

    Returns (text, stop_reason)
    stop_reason is: "stop_phrase", "max_tokens", or "end_of_stream"
    """

    parts = []   # collect tokens here — like an array we'll .join("") at the end
    count = 0    # how many tokens we've seen

    # "for token in token_iterator" is like "for (const token of iterator)" in JS
    for token in token_iterator:

        # check if this token contains the stop phrase
        # "in" checks if a substring exists — like token.includes(stop_phrase) in JS
        if stop_phrase in token:
            # grab any text BEFORE the stop phrase
            # "Hello [DONE]".split("[DONE]") -> ["Hello ", ""]
            before = token.split(stop_phrase)[0]
            if before:
                parts.append(before)
            # .strip() removes whitespace from both ends — like .trim() in JS
            return "".join(parts).strip(), "stop_phrase"

        parts.append(token)
        count += 1

        # check if we've hit the max token limit
        if count >= max_tokens:
            return "".join(parts).strip(), "max_tokens"

    # if we get here, the stream ended naturally (no stop phrase, no limit)
    return "".join(parts).strip(), "end_of_stream"


if __name__ == "__main__":
    # Case 1: stop phrase
    tokens1 = ["Hello", " world", "!", " [DONE]", " this should not appear"]
    text, reason = aggregate_stream(iter(tokens1))
    print(f"Case 1: '{text}' (reason: {reason})")
    # -> "Hello world!" (stop_phrase)

    # Case 2: max tokens hit
    tokens2 = ["one ", "two ", "three ", "four ", "five "]
    text, reason = aggregate_stream(iter(tokens2), max_tokens=3)
    print(f"Case 2: '{text}' (reason: {reason})")
    # -> "one two three" (max_tokens)

    # Case 3: stream ends naturally
    tokens3 = ["This ", "is ", "complete."]
    text, reason = aggregate_stream(iter(tokens3))
    print(f"Case 3: '{text}' (reason: {reason})")
    # -> "This is complete." (end_of_stream)

    # Case 4: empty stream
    text, reason = aggregate_stream(iter([]))
    print(f"Case 4: '{text}' (reason: {reason})")
    # -> "" (end_of_stream)
