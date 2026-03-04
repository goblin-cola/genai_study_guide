"""Study Guide #8: Prompt Builder with Token Budget

PROBLEM
-------
You have:
  - a system prompt (always included)
  - a user query (always included)
  - a list of context chunks, ranked by relevance (best first)
  - a max token budget

Build the final prompt by fitting as many chunks as possible.

WHY THIS SHOWS UP IN GENAI
--------------------------
Every LLM has a context window (e.g., 128k tokens). You MUST fit within it.
You usually have more retrieved chunks than can fit, so you greedily pack
the best ones first and stop when you run out of room.

TOKEN ESTIMATION
----------------
Rough rule: 1 token ~ 4 characters. Not exact, but good enough for interviews.
In production you'd use a real tokenizer (tiktoken for OpenAI, etc.)

KEY INSIGHT
-----------
This is a greedy algorithm: try chunks in order (best first), add if it fits.

"""


def estimate_tokens(text):
    """Rough estimate: 1 token ~ 4 characters."""
    # len("hello world") = 11 chars -> ~2 tokens
    # this is the standard interview approximation
    return len(text) // 4


def build_prompt(system, query, chunks, max_tokens):
    """Assemble a prompt that fits within the token budget.

    system = system prompt string (always included)
    query  = user's question (always included)
    chunks = list of context strings, best first
    max_tokens = total budget

    Returns (prompt_string, num_chunks_used)
    """

    # these are mandatory — always part of the prompt
    header = f"System: {system}\n\n"
    footer = f"\nUser: {query}"

    # count how many tokens the fixed parts use
    used = estimate_tokens(header) + estimate_tokens(footer)

    # greedily add chunks, best first, until we run out of room
    context_parts = []
    for i, chunk in enumerate(chunks):
        # format each chunk with a number label
        # f"..." is like `template literals` in JS
        chunk_line = f"[{i + 1}] {chunk}\n"
        chunk_tokens = estimate_tokens(chunk_line)

        # would adding this chunk go over budget?
        if used + chunk_tokens > max_tokens:
            break  # no room, stop adding

        context_parts.append(chunk_line)
        used += chunk_tokens

    # assemble the final prompt
    context_section = ""
    if context_parts:
        # "".join(list) concatenates all strings — like list.join("") in JS
        context_section = "Context:\n" + "".join(context_parts) + "\n"

    prompt = header + context_section + footer
    return prompt, len(context_parts)


if __name__ == "__main__":
    system = "You are a helpful assistant. Answer using only the provided context."
    query = "What is retrieval augmented generation?"

    chunks = [
        "RAG combines a retrieval step with LLM generation. Documents are embedded and stored in a vector database.",
        "At query time, relevant chunks are retrieved via similarity search and injected into the LLM prompt.",
        "This grounds the LLM's response in real data, reducing hallucinations significantly.",
        "RAG was introduced in a 2020 paper by Lewis et al. at Facebook AI Research.",
        "Alternative approaches include fine-tuning, but RAG is cheaper and more flexible for most use cases.",
    ]

    # tight budget — can't fit all chunks
    prompt, num_used = build_prompt(system, query, chunks, max_tokens=100)
    print(f"=== Budget: 100 tokens ===")
    print(f"Chunks used: {num_used} / {len(chunks)}")
    print()
    print(prompt)

    print("=" * 50)

    # bigger budget — fits more
    prompt, num_used = build_prompt(system, query, chunks, max_tokens=250)
    print(f"\n=== Budget: 250 tokens ===")
    print(f"Chunks used: {num_used} / {len(chunks)}")
    print()
    print(prompt)
