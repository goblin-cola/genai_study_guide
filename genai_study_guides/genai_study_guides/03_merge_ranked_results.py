"""Study Guide #3: Merge Ranked Results (Hybrid Retrieval)

PROBLEM
-------
You have two ranked lists from different search methods:
  - vector search results:  [(doc_id, score), ...]
  - keyword search results: [(doc_id, score), ...]

Merge them into one list:
  - if a doc appears in both, keep the HIGHER score
  - sort by score descending

WHY THIS SHOWS UP IN GENAI
--------------------------
Hybrid retrieval = vector search + keyword search (BM25).
Vector search is good at meaning, keyword search is good at exact matches.
Combining them gives better results than either alone.

EXAMPLE
-------
vector  = [("docA", 0.90), ("docB", 0.80)]
keyword = [("docB", 0.95), ("docC", 0.70)]

docB appears in both — keep 0.95 (the higher score)
-> [("docB", 0.95), ("docA", 0.90), ("docC", 0.70)]

"""


def merge_results(list_a, list_b):
    """Merge two ranked lists, dedupe by doc_id, keep highest score.

    Returns list of (doc_id, score) sorted by score descending.
    """

    # use a dict to track the best score per doc
    # in JS: const best = new Map()
    best = {}

    # go through both lists
    # list_a + list_b just concatenates them into one list
    # in JS: [...listA, ...listB]
    for doc_id, score in list_a + list_b:
        # .get(key, default) returns the value if key exists, else default
        # in JS: best.get(doc_id) ?? -1
        if doc_id not in best or score > best[doc_id]:
            best[doc_id] = score

    # convert dict to list of tuples and sort by score
    # best.items() gives [(doc_id, score), ...] — like [...best.entries()] in JS
    # sorted() returns a new sorted list (doesn't modify the original)
    result = sorted(best.items(), key=lambda x: x[1], reverse=True)
    return result


if __name__ == "__main__":
    vector_results = [("docA", 0.90), ("docB", 0.80)]
    keyword_results = [("docB", 0.95), ("docC", 0.70)]

    merged = merge_results(vector_results, keyword_results)

    print("Vector results: ", vector_results)
    print("Keyword results:", keyword_results)
    print("\nMerged:")
    for doc_id, score in merged:
        print(f"  {doc_id}: {score}")

    # Expected: docB=0.95, docA=0.90, docC=0.70
    # docB got 0.95 (from keyword) instead of 0.80 (from vector)
