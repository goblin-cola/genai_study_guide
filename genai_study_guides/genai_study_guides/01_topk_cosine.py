"""Study Guide #1: Top-K Similar Documents (Cosine Similarity)

PROBLEM
-------
Given a query embedding and a list of document embeddings, return the
K most similar documents.

WHY THIS SHOWS UP IN GENAI
--------------------------
This is the core of vector search in RAG: "find the most relevant chunks."
In production you'd use a vector DB (FAISS, Pinecone, pgvector), but you
should understand the underlying math.

FORMULA
-------
cosine_similarity(a, b) = dot_product(a, b) / (magnitude(a) * magnitude(b))

dot_product = multiply each pair of elements and sum them
magnitude   = sqrt of sum of squares (the "length" of the vector)

Result is between -1 and 1:
  1  = identical direction (very similar)
  0  = perpendicular (unrelated)
  -1 = opposite direction

EXAMPLE
-------
query = [0.2, 0.5, 0.3]
docs  = [("doc1", [0.1, 0.5, 0.4]), ("doc2", [0.9, 0.1, 0.2]), ("doc3", [0.2, 0.6, 0.2])]
k = 2
-> [("doc3", 0.978), ("doc1", 0.976)]   (doc3 and doc1 are most similar to query)

"""

from math import sqrt


def cosine_similarity(a, b):
    """Cosine similarity between two vectors (lists of numbers)."""

    # dot product: multiply matching elements and sum
    # [1, 2, 3] dot [4, 5, 6] = (1*4) + (2*5) + (3*6) = 32
    # zip(a, b) pairs them up: (1,4), (2,5), (3,6)
    # in JS: a.reduce((sum, x, i) => sum + x * b[i], 0)
    dot = sum(x * y for x, y in zip(a, b))

    # magnitude: the "length" of each vector
    # mag([3, 4]) = sqrt(3*3 + 4*4) = sqrt(9 + 16) = sqrt(25) = 5
    mag_a = sqrt(sum(x * x for x in a))
    mag_b = sqrt(sum(x * x for x in b))

    # avoid dividing by zero (if a vector is all zeros)
    if mag_a == 0 or mag_b == 0:
        return 0.0

    # the formula: dot / (mag_a * mag_b)
    return dot / (mag_a * mag_b)


def top_k(query, docs, k):
    """Return the k most similar docs to the query.

    docs = list of (doc_id, embedding) pairs
    Returns list of (doc_id, score) sorted by score descending
    """

    # score every doc against the query
    # this is the same as: docs.map(([id, emb]) => [id, cosineSim(query, emb)]) in JS
    scored = []
    for doc_id, embedding in docs:
        score = cosine_similarity(query, embedding)
        scored.append((doc_id, score))

    # sort by score, highest first
    # key=lambda x: x[1] means "sort by the second element" (the score)
    # reverse=True means descending (highest first)
    # in JS: scored.sort((a, b) => b[1] - a[1])
    scored.sort(key=lambda x: x[1], reverse=True)

    # take only the top k
    # in JS: scored.slice(0, k)
    return scored[:k]


if __name__ == "__main__":
    query = [0.2, 0.5, 0.3]
    docs = [
        ("doc1", [0.1, 0.5, 0.4]),
        ("doc2", [0.9, 0.1, 0.2]),
        ("doc3", [0.2, 0.6, 0.2]),
    ]

    results = top_k(query, docs, k=2)

    print("Query:", query)
    print(f"\nTop {2} results:")
    for doc_id, score in results:
        print(f"  {doc_id}: {score:.4f}")

    # Expected: doc3 (0.978) and doc1 (0.976) — most similar to query
    # doc2 (0.659) is least similar because its vector points in a different direction
