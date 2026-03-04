"""Study Guide #10: Retry with Exponential Backoff

PROBLEM
-------
LLM APIs fail sometimes (rate limits, timeouts). Write a function that:
  - Calls an API function
  - If it fails, wait and retry
  - Each retry waits longer: 1s, 2s, 4s, 8s... (exponential backoff)
  - Only retry certain error types (e.g., TimeoutError, not ValueError)
  - Give up after max_retries attempts

WHY THIS SHOWS UP IN GENAI
--------------------------
Every production GenAI system needs retry logic. OpenAI returns 429 (rate
limit) errors constantly. If you don't handle them, your app breaks.

BACKOFF FORMULA
---------------
wait_time = base_delay * (2 ^ attempt)

attempt 0: 1 * (2^0) = 1 second
attempt 1: 1 * (2^1) = 2 seconds
attempt 2: 1 * (2^2) = 4 seconds

This prevents hammering the API when it's already overloaded.

NOTE ON DECORATORS
------------------
The @retry syntax is a Python "decorator" — it wraps a function with extra behavior.
Think of it like a higher-order function in JS:

    Python:                           JavaScript:
    @retry(max_retries=3)             const callLLM = withRetry(
    def call_llm(prompt):                 (prompt) => api.call(prompt),
        return api.call(prompt)           { maxRetries: 3 }
                                      );

"""

import time


def call_with_retry(fn, max_retries=3, base_delay=1.0, retry_on=(Exception,)):
    """Call fn(). If it fails with a retryable error, retry with backoff.

    fn         = the function to call (takes no arguments)
    max_retries = how many times to retry after the first failure
    base_delay  = starting wait time in seconds
    retry_on    = tuple of exception types to retry on

    Returns the function's result, or raises the last error.
    """

    last_error = None

    # range(max_retries + 1) = [0, 1, 2, 3] if max_retries=3
    # attempt 0 is the first try, attempts 1-3 are retries
    for attempt in range(max_retries + 1):
        try:
            # try calling the function
            return fn()

        except retry_on as e:
            # the function raised an error we should retry on
            last_error = e

            if attempt < max_retries:
                # exponential backoff: 1s, 2s, 4s, 8s...
                # ** is Python's exponent operator — like Math.pow() in JS
                wait = base_delay * (2 ** attempt)
                print(f"  Attempt {attempt + 1} failed: {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  Attempt {attempt + 1} failed: {e}. No retries left.")

    # all retries exhausted — raise the last error
    # "raise" is like "throw" in JS
    raise last_error


if __name__ == "__main__":
    # --- simulate a flaky API that fails twice then works ---
    # we use a list [0] instead of a plain number because Python closures
    # can READ outer variables but can't REASSIGN them without "nonlocal"
    # using a list is a simple workaround — we mutate the list, not reassign it
    # in JS you wouldn't need this trick — closures just work
    counter = [0]

    def fake_llm_call():
        counter[0] += 1
        if counter[0] <= 2:
            raise TimeoutError("API timed out")
        return "Success! Response from LLM"

    # Case 1: succeeds on 3rd attempt
    print("=== Case 1: Flaky API (succeeds on attempt 3) ===")
    counter[0] = 0
    result = call_with_retry(fake_llm_call, max_retries=3, base_delay=0.1,
                             retry_on=(TimeoutError,))
    print(f"  Result: {result}")

    # Case 2: non-retryable error — fails immediately
    print("\n=== Case 2: Non-retryable error ===")
    def bad_input():
        raise ValueError("bad input")

    try:
        call_with_retry(bad_input, max_retries=3, base_delay=0.1,
                        retry_on=(TimeoutError,))  # only retry TimeoutError
    except ValueError as e:
        print(f"  Caught immediately (no retry): {e}")

    # Case 3: all retries fail
    print("\n=== Case 3: All retries fail ===")
    def always_fails():
        raise TimeoutError("still broken")

    try:
        call_with_retry(always_fails, max_retries=2, base_delay=0.1,
                        retry_on=(TimeoutError,))
    except TimeoutError as e:
        print(f"  Final error: {e}")
