/**
 * Simplified GenAI interview problems — JavaScript version
 * Same logic as the Python file, in the language you know.
 * Use this to understand the pattern, then translate to Python.
 */

// ============================================================
// 1) TOP-K COSINE SIMILARITY
// Core of vector search in RAG
// ============================================================

function cosineSim(a, b) {
  // dot product: multiply each pair of elements and sum them
  // [0.2, 0.5] dot [0.1, 0.6] = (0.2*0.1) + (0.5*0.6) = 0.32
  const dot = a.reduce((sum, x, i) => sum + x * b[i], 0);

  // magnitude: sqrt of sum of squares (length of each vector)
  // mag([3, 4]) = sqrt(9 + 16) = sqrt(25) = 5
  const magA = Math.sqrt(a.reduce((sum, x) => sum + x * x, 0));
  const magB = Math.sqrt(b.reduce((sum, x) => sum + x * x, 0));

  // cosine = dot / (magA * magB)
  // result is between -1 (opposite) and 1 (identical direction)
  // 0 means perpendicular / unrelated
  // if either vector is all zeros, return 0 to avoid divide-by-zero
  return magA * magB === 0 ? 0 : dot / (magA * magB);
}

function topK(query, docs, k) {
  return docs
    .map(([id, emb]) => [id, cosineSim(query, emb)])  // score every doc against the query
    .sort((a, b) => b[1] - a[1])                       // sort by score, highest first
    .slice(0, k);                                       // take the top k
}

// ============================================================
// 2) RATE LIMITER (sliding window)
// Same pattern as sliding window counts
// ============================================================

class RateLimiter {
  constructor(maxReq, window) {
    this.maxReq = maxReq;
    this.window = window;
    this.hits = new Map(); // userId -> [timestamps]
  }

  allow(userId, now) {
    // get or create this user's timestamp queue
    if (!this.hits.has(userId)) this.hits.set(userId, []);
    const q = this.hits.get(userId);

    // slide the window: remove timestamps that are too old
    // e.g. window=60, now=1003 -> drop anything <= 943
    while (q.length && q[0] <= now - this.window) {
      q.shift();  // remove from front (oldest first)
    }

    // if queue is full, deny the request
    if (q.length >= this.maxReq) return false;

    // otherwise allow it and record the timestamp
    q.push(now);
    return true;
  }
}

// ============================================================
// 3) CHUNK TEXT WITH OVERLAP
// RAG preprocessing
// ============================================================

function chunkText(text, size, overlap) {
  const chunks = [];
  const step = size - overlap;  // how far to advance each time
  // e.g. size=10, overlap=3 -> step=7
  // chunk0: [0..10], chunk1: [7..17], chunk2: [14..24]
  //          ^^^overlap^^^

  let start = 0;
  while (start < text.length) {
    chunks.push(text.slice(start, start + size));  // grab a chunk
    start += step;                                  // advance by step (not size!)
  }
  return chunks;
}

// ============================================================
// 4) MERGE + DEDUPE RANKED RESULTS
// Hybrid retrieval: combine vector + keyword search
// ============================================================

function mergeResults(listA, listB) {
  const best = new Map();  // doc_id -> highest score seen

  // loop through both lists combined
  for (const [id, score] of [...listA, ...listB]) {
    // only keep the higher score if we've seen this doc before
    if (!best.has(id) || score > best.get(id)) {
      best.set(id, score);
    }
  }

  // convert map back to array and sort by score descending
  return [...best.entries()].sort((a, b) => b[1] - a[1]);
}

// ============================================================
// 5) LRU CACHE (bonus — comes up a lot)
// Cache repeated queries to avoid redundant LLM calls
// ============================================================

class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map(); // Map preserves insertion order in JS
  }

  get(key) {
    if (!this.cache.has(key)) return null;
    const val = this.cache.get(key);
    // trick: delete and re-set to move it to the END of the Map
    // Map keeps insertion order, so "end" = most recently used
    this.cache.delete(key);
    this.cache.set(key, val);
    return val;
  }

  put(key, value) {
    // if key exists, delete first so re-inserting moves it to the end
    if (this.cache.has(key)) this.cache.delete(key);
    this.cache.set(key, value);

    // if over capacity, evict the OLDEST (first item in the Map)
    if (this.cache.size > this.capacity) {
      const oldest = this.cache.keys().next().value;  // first key = least recently used
      this.cache.delete(oldest);
    }
  }
}

// ============================================================
// QUICK TESTS — run with: node study_simplified.js
// ============================================================

// 1) Top-K
const q = [0.2, 0.5, 0.3];
const docs = [["doc1", [0.1, 0.5, 0.4]], ["doc2", [0.9, 0.1, 0.2]], ["doc3", [0.2, 0.6, 0.2]]];
console.log("=== Top-K Cosine ===");
console.log(topK(q, docs, 2));

// 2) Rate Limiter
console.log("\n=== Rate Limiter ===");
const rl = new RateLimiter(3, 60);
for (const t of [1000, 1001, 1002, 1003]) {
  console.log(`  t=${t}: ${rl.allow("user1", t)}`);
}

// 3) Chunking
console.log("\n=== Chunking ===");
const chunks = chunkText("abcdefghijklmnopqrstuvwxyz", 10, 3);
chunks.forEach((c, i) => console.log(`  chunk${i}: '${c}'`));

// 4) Merge Results
console.log("\n=== Merge Results ===");
const vec = [["A", 0.9], ["B", 0.8]];
const kw = [["B", 0.95], ["C", 0.7]];
console.log(mergeResults(vec, kw));

// 5) LRU Cache
console.log("\n=== LRU Cache ===");
const cache = new LRUCache(2);
cache.put("q1", "answer1");
cache.put("q2", "answer2");
console.log(`  get q1: ${cache.get("q1")}`);  // answer1
cache.put("q3", "answer3");                    // evicts q2
console.log(`  get q2: ${cache.get("q2")}`);  // null (evicted)
console.log(`  get q3: ${cache.get("q3")}`);  // answer3
