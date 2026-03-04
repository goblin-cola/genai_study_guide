"""Study Guide #6: Citation Validation (Hallucination Guard)

PROBLEM
-------
In a RAG system:
  1. You retrieve a set of chunk IDs from the database
  2. The LLM generates an answer and claims to cite certain chunks

Problem: the LLM might hallucinate citations that don't exist!
Filter out any citation that wasn't in the retrieved set.

WHY THIS SHOWS UP IN GENAI
--------------------------
This is the simplest and most important guardrail against hallucinated
citations. If the LLM says "according to chunk c5" but you never retrieved
c5, that citation is fake and must be removed.

EXAMPLE
-------
retrieved = ["c1", "c2", "c3"]        (what we actually retrieved)
citations = ["c2", "c5", "c1"]        (what the LLM claims to cite)
-> ["c2", "c1"]                        (c5 was hallucinated, removed)

KEY INSIGHT
-----------
Convert retrieved to a set for O(1) lookups, then filter.
In JS: const allowed = new Set(retrieved); citations.filter(c => allowed.has(c))

"""


def validate_citations(retrieved, citations):
    """Keep only citations that exist in the retrieved set. Preserve order.

    retrieved = list of chunk IDs we actually fetched from the DB
    citations = list of chunk IDs the LLM claims to reference
    """

    # set() = like new Set() in JS
    # lookups in a set are O(1) — instant, no matter how big
    # lookups in a list are O(n) — slow, checks every item
    allowed = set(retrieved)

    # keep only citations that are in the allowed set
    # "if c in allowed" checks set membership — like allowed.has(c) in JS
    valid = []
    for c in citations:
        if c in allowed:
            valid.append(c)
    return valid

    # one-liner version (same thing, just shorter):
    # return [c for c in citations if c in allowed]


if __name__ == "__main__":
    retrieved = ["c1", "c2", "c3"]
    citations = ["c2", "c5", "c1", "c99"]

    result = validate_citations(retrieved, citations)

    print("Retrieved chunks:", retrieved)
    print("LLM citations:   ", citations)
    print("Valid citations: ", result)
    # Expected: ["c2", "c1"]
    # c5 and c99 were hallucinated — removed
