"""PRACTICE: Chunk Text with Overlap

Implement: chunk_text(text, size, overlap)

- Split text into chunks of at most `size` characters
- Each chunk overlaps with the next by `overlap` characters
- step = size - overlap (how far to advance each time)
- Return list of strings

Run this file to check: python 04_chunk_text_work.py

INTERVIEW QUESTIONS (this topic):
1. "Our documents are too long to fit in the LLM's context window. How would you split
   text into fixed-size chunks with overlap so we don't lose context at chunk boundaries?"
2. "Implement a text chunking function that takes a max size and an overlap amount.
   Why is overlap important in a RAG pipeline?"
"""


def chunk_text(text, size, overlap):
    # YOUR CODE HERE
    pass


# ============================================================
# TESTS
# ============================================================

def test_basic():
    text = "abcdefghijklmnopqrstuvwxyz"
    result = chunk_text(text, 10, 3)
    assert result is not None, "Returned None — did you forget to return?"
    assert result[0] == "abcdefghij", f"chunk0 should be 'abcdefghij', got '{result[0]}'"
    assert result[1] == "hijklmnopq", f"chunk1 should be 'hijklmnopq', got '{result[1]}'"
    # overlap check: last 3 chars of chunk0 == first 3 chars of chunk1
    assert result[0][-3:] == result[1][:3], "Overlap not working — last 3 of chunk0 should equal first 3 of chunk1"
    print("  basic: PASSED")


def test_no_overlap():
    text = "abcdefghij"
    result = chunk_text(text, 5, 0)
    assert len(result) == 2, f"Expected 2 chunks, got {len(result)}"
    assert result[0] == "abcde", f"chunk0 should be 'abcde', got '{result[0]}'"
    assert result[1] == "fghij", f"chunk1 should be 'fghij', got '{result[1]}'"
    print("  no_overlap: PASSED")


def test_short_text():
    text = "hi"
    result = chunk_text(text, 10, 3)
    assert len(result) == 1, f"Short text should give 1 chunk, got {len(result)}"
    assert result[0] == "hi", f"Should be 'hi', got '{result[0]}'"
    print("  short_text: PASSED")


def test_last_chunk_shorter():
    text = "abcdefghijklm"  # 13 chars
    result = chunk_text(text, 5, 0)
    assert result[-1] == "klm", f"Last chunk should be 'klm', got '{result[-1]}'"
    print("  last_chunk_shorter: PASSED")


if __name__ == "__main__":
    print("Testing 04: Chunk Text with Overlap\n")
    for test in [test_basic, test_no_overlap, test_short_text, test_last_chunk_shorter]:
        try:
            test()
        except Exception as e:
            print(f"  {test.__name__}: FAILED - {e}")
