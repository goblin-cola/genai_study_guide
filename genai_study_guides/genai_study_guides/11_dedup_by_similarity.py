"""Study Guide #11: Deduplicate Retrieved Chunks by Similarity

PROBLEM
-------
After retrieval, you often get near-duplicate chunks (same info, slightly
different wording). Remove duplicates to avoid wasting tokens.

Given a ranked list of chunks, keep each chunk ONLY if it's not too similar
to any chunk you've already kept.

WHY THIS SHOWS UP IN GENAI
--------------------------
If you stuff near-duplicate context into a prompt, you waste tokens and
the LLM gets confused. Dedup is a standard post-retrieval step.

JACCARD SIMILARITY (the simple version)
-----------------------------------------
Split each text into a set of words, then:

  jaccard = (words in common) / (total unique words)

Example:
  A = "the cat sat"       -> {"the", "cat", "sat"}
  B = "the cat slept"     -> {"the", "cat", "slept"}

  in common (intersection): {"the", "cat"}           = 2 words
  total unique (union):     {"the", "cat", "sat", "slept"} = 4 words
  jaccard = 2 / 4 = 0.5

If jaccard >= threshold, they're "too similar" = duplicate.

"""


def jaccard(text_a, text_b):
    """Word-level Jaccard similarity between two strings.

    Returns a number from 0.0 (completely different) to 1.0 (identical words).
    """

    # .lower() = lowercase everything
    # .split() = split on whitespace into a list of words
    # set()    = remove duplicates, like new Set() in JS
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())

    # & = intersection (words in BOTH sets) — like setA.intersection(setB)
    # | = union (words in EITHER set) — like new Set([...setA, ...setB])
    common = words_a & words_b
    total = words_a | words_b

    # avoid divide by zero if both texts are empty
    if not total:
        return 1.0

    return len(common) / len(total)


def dedup_chunks(chunks, threshold=0.7):
    """Remove near-duplicate chunks. Keep the first (most relevant) version.

    chunks = [(chunk_id, text), ...] ordered by relevance (best first)
    threshold = similarity cutoff (0.7 = 70% similar words = duplicate)

    Returns filtered list of (chunk_id, text).
    """

    kept = []  # chunks we're keeping

    for chunk_id, text in chunks:
        # check if this chunk is too similar to any chunk we already kept
        is_dupe = False
        for _, kept_text in kept:
            # _ means "I don't care about the chunk_id of the kept chunk"
            if jaccard(text, kept_text) >= threshold:
                is_dupe = True
                break  # found a match, no need to check the rest

        if not is_dupe:
            kept.append((chunk_id, text))

    return kept


if __name__ == "__main__":
    chunks = [
        ("c1", "RAG combines retrieval with generation to ground LLM responses"),
        ("c2", "RAG combines retrieval with generation to ground LLM outputs"),   # near-dupe of c1
        ("c3", "Fine tuning updates model weights on domain-specific data"),
        ("c4", "Fine tuning updates the model weights on specific domain data"),  # near-dupe of c3
        ("c5", "Vector databases store embeddings for fast similarity search"),
    ]

    print("=== Before dedup ===")
    for cid, text in chunks:
        print(f"  {cid}: {text}")

    result = dedup_chunks(chunks, threshold=0.7)

    print(f"\n=== After dedup (threshold=0.7) ===")
    for cid, text in result:
        print(f"  {cid}: {text}")

    # Show why: c1 and c2 are 80% similar (over threshold), so c2 is dropped
    print(f"\n=== Similarity scores ===")
    print(f"  c1 vs c2: {jaccard(chunks[0][1], chunks[1][1]):.2f}  (>= 0.7, dupe!)")
    print(f"  c3 vs c4: {jaccard(chunks[2][1], chunks[3][1]):.2f}  (< 0.7, kept)")
    print(f"  c1 vs c3: {jaccard(chunks[0][1], chunks[2][1]):.2f}  (totally different)")
