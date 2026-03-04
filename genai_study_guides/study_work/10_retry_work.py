"""PRACTICE: Retry with Exponential Backoff

Implement: call_with_retry(fn, max_retries=3, base_delay=1.0, retry_on=(Exception,))

- Call fn()
- If it raises an error that matches retry_on, wait and retry
- Wait time = base_delay * (2 ** attempt)  -> 1s, 2s, 4s, 8s...
- After max_retries retries, raise the last error
- If the error type is NOT in retry_on, raise immediately (no retry)

NOTE: For testing, use base_delay=0 so tests run instantly.

Run this file to check: python 10_retry_work.py
"""

import time


def call_with_retry(fn, max_retries=3, base_delay=1.0, retry_on=(Exception,)):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def test_succeeds_first_try():
    def ok():
        return "hello"
    result = call_with_retry(ok, max_retries=3, base_delay=0)
    assert result == "hello", f"Expected 'hello', got {result}"
    print("  succeeds_first_try: PASSED")


def test_succeeds_after_retries():
    counter = [0]
    def flaky():
        counter[0] += 1
        if counter[0] <= 2:
            raise TimeoutError("timeout")
        return "finally"

    result = call_with_retry(flaky, max_retries=3, base_delay=0, retry_on=(TimeoutError,))
    assert result == "finally", f"Expected 'finally', got {result}"
    assert counter[0] == 3, f"Should have taken 3 attempts, took {counter[0]}"
    print("  succeeds_after_retries: PASSED")


def test_all_retries_fail():
    def always_fails():
        raise TimeoutError("broken")

    try:
        call_with_retry(always_fails, max_retries=2, base_delay=0, retry_on=(TimeoutError,))
        assert False, "Should have raised TimeoutError"
    except TimeoutError:
        pass  # expected
    print("  all_retries_fail: PASSED")


def test_non_retryable_error():
    """If the error type isn't in retry_on, it should raise immediately."""
    counter = [0]
    def bad_input():
        counter[0] += 1
        raise ValueError("bad")

    try:
        call_with_retry(bad_input, max_retries=3, base_delay=0, retry_on=(TimeoutError,))
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # expected
    assert counter[0] == 1, f"Should NOT retry ValueError, but called {counter[0]} times"
    print("  non_retryable_error: PASSED")


if __name__ == "__main__":
    print("Testing 10: Retry with Backoff\n")
    for test in [test_succeeds_first_try, test_succeeds_after_retries,
                 test_all_retries_fail, test_non_retryable_error]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
