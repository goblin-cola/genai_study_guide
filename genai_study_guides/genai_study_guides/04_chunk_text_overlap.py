"""Study Guide #4: Chunking Text with Overlap (RAG Preprocessing)

PROBLEM
-------
Split a long text into chunks of at most `size` characters, with `overlap`
characters shared between consecutive chunks.

WHY THIS SHOWS UP IN GENAI
--------------------------
LLMs have limited context windows. You can't feed a whole document in.
So you split it into chunks, embed each chunk, and store them for retrieval.

Overlap matters because without it, a sentence split across two chunks
loses its meaning in both. Overlap ensures context is preserved at boundaries.

HOW IT WORKS
------------
size=10, overlap=3 -> step=7 (advance 7 chars each time)

text: "abcdefghijklmnopqrstuvwxyz"

chunk0: [abcdefghij]              positions 0-9
chunk1:        [hijklmnopqr]      positions 7-16
                ^^^overlap^^^
chunk2:               [opqrstuvwx] positions 14-23
                       ^^^overlap^^^

The key formula: step = size - overlap

"""


def chunk_text(text, size, overlap):
    """Split text into overlapping chunks.

    size    = max characters per chunk
    overlap = how many characters to repeat between chunks
    Returns a list of strings.
    """
    chunks = []

    # step = how far forward we move each time
    # if size=10 and overlap=3, step=7
    # we move forward 7, but grab 10, so the last 3 chars overlap with the next chunk
    step = size - overlap

    start = 0
    while start < len(text):
        # grab a chunk from start to start+size
        # text[start:start+size] is like text.slice(start, start+size) in JS
        chunk = text[start:start + size]
        chunks.append(chunk)
        start += step  # advance by step, NOT by size (that's the trick)

    return chunks


if __name__ == "__main__":
    text = "abcdefghijklmnopqrstuvwxyz"
    size = 10
    overlap = 3

    chunks = chunk_text(text, size, overlap)

    print(f"Text: '{text}' (length={len(text)})")
    print(f"size={size}, overlap={overlap}, step={size - overlap}\n")

    for i, chunk in enumerate(chunks):
        print(f"  chunk{i}: '{chunk}'")

    # Expected:
    # chunk0: 'abcdefghij'   (0 to 10)
    # chunk1: 'hijklmnopqr'  (7 to 17)  — 'hij' overlaps with chunk0
    # chunk2: 'opqrstuvwxy'  (14 to 24) — 'opq' overlaps with chunk1
    # chunk3: 'vwxyz'        (21 to 26) — last chunk can be shorter
