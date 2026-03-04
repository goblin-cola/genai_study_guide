from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable

# ----- Types -----
@dataclass(frozen=True)
class Auth:
    tenant_id: str
    user_id: str
    groups: Tuple[str, ...]

@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    meta: Dict[str, object]  # must include: tenant_id, visibility, owner_user_id, allowed_user_ids, allowed_group_ids

# ----- ACL check (defense-in-depth) -----
def allowed(auth: Auth, c: Chunk) -> bool:
    if c.meta.get("tenant_id") != auth.tenant_id:
        return False
    vis = c.meta.get("visibility", "private")
    if vis == "org":
        return True
    if c.meta.get("owner_user_id") == auth.user_id:
        return True
    if auth.user_id in set(c.meta.get("allowed_user_ids", []) or []):
        return True
    allowed_groups = set(c.meta.get("allowed_group_ids", []) or [])
    return any(g in allowed_groups for g in auth.groups)

# ----- Merge + dedupe candidates from BM25 + vector -----
def merge_dedupe(vec: List[Tuple[Chunk, float]], bm25: List[Tuple[Chunk, float]]) -> List[Chunk]:
    best: Dict[str, Tuple[Chunk, float]] = {}
    for src in (vec, bm25):
        for ch, score in src:
            prev = best.get(ch.chunk_id)
            if prev is None or score > prev[1]:
                best[ch.chunk_id] = (ch, score)
    # Sort by first-stage score (fast)
    return [ch for ch, _ in sorted(best.values(), key=lambda x: x[1], reverse=True)]

# ----- Stubs (in interview you say: "these are integrations") -----
def vector_search(query: str, filters: Dict[str, object], k: int) -> List[Tuple[Chunk, float]]:
    raise NotImplementedError

def bm25_search(query: str, filters: Dict[str, object], k: int) -> List[Tuple[Chunk, float]]:
    raise NotImplementedError

def rerank(query: str, chunks: List[Chunk]) -> List[Chunk]:
    # Stub: in real life a cross-encoder returns scores; here keep order.
    return chunks

def llm_generate(query: str, context: List[Chunk]) -> Dict[str, object]:
    # Stub: real LLM would return structured JSON w/ citations.
    return {
        "answer": "…",
        "citations": [{"doc_id": context[0].doc_id, "chunk_id": context[0].chunk_id, "quote": context[0].text[:120]}]
                     if context else [],
    }

# ----- Interview-sized "answer" function -----
def answer(auth: Auth, query: str) -> Dict[str, object]:
    # Mandatory tenant filter is derived from auth (never trust client-supplied tenant_id)
    filters = {"tenant_id": auth.tenant_id}

    vec = vector_search(query, filters=filters, k=30)
    kw = bm25_search(query, filters=filters, k=30)

    candidates = merge_dedupe(vec, kw)
    # Defense-in-depth: enforce ACL again even if stores filtered (prevents bugs/leaks)
    candidates = [c for c in candidates if allowed(auth, c)][:50]

    top = rerank(query, candidates)[:8]

    out = llm_generate(query, top)

    # Validate citations only reference provided context chunks
    allowed_ids = {c.chunk_id for c in top}
    out["citations"] = [c for c in out.get("citations", []) if c.get("chunk_id") in allowed_ids]

    if not out["citations"]:
        return {"answer": "I don't know based on the documents I have access to.", "citations": []}

    return out