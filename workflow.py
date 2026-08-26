# workflow.py
# -----------
# This file improves retrieval quality using multi-step AI workflows.
#
# The retrieval quality problem:
# The quality of a RAG answer depends heavily on what gets retrieved.
# And what gets retrieved depends on how similar the query embedding is
# to the document embeddings. If the user's query is vague or uses
# different vocabulary than the documents, retrieval suffers.
#
# Two solutions:
#
# 1. Query rewriting: Use an LLM to rewrite the user's question into a
#    version that will produce a better embedding for semantic search.
#    "tell me about that database thing" → "How do relational databases
#    store and query structured data using SQL?"
#
# 2. Query decomposition: Some questions are actually multiple questions.
#    Split them up and retrieve separately, then combine the results.
#    This is called "multi-hop retrieval."

from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL
from embeddings import embed_text
from vector_store import query_similar

_client = genai.Client(api_key=GEMINI_API_KEY)


def rewrite_query(original_query, conversation_context=""):
    """
    Use Gemini to rewrite the user's query for better semantic search.

    Args:
        original_query:      The user's original question.
        conversation_context: Recent conversation history (helps resolve
                              pronouns like "it" or "that").

    Returns:
        A rewritten query string, or the original if rewriting fails.
    """
    try:
        context_section = ""
        if conversation_context:
            context_section = f"\nPrevious conversation:\n{conversation_context}\n"

        prompt = f"""Rewrite the user's question to be clearer and more specific for semantic search.
Keep the same meaning, but make it more technical and self-contained.
{context_section}
Original question: {original_query}

Return only the rewritten question."""

        response = _client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1),
        )

        rewritten = response.text.strip()
        if rewritten and len(rewritten) <= 500:
            return rewritten
        return original_query
    except Exception:
        return original_query


def decompose_query(query):
    """
    Break a complex multi-part question into simpler sub-questions.

    Args:
        query: A question that may contain multiple distinct topics.

    Returns:
        A list of sub-question strings (up to 3), or [query] if it's
        already simple or if decomposition fails.
    """
    try:
        prompt = f"""If this question covers multiple topics, split it into 2-3 simpler sub-questions.
If it is already simple, return it unchanged.

Question: {query}

Return one sub-question per line."""

        response = _client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1),
        )

        sub_questions = [
            line.strip("- ").strip()
            for line in response.text.splitlines()
            if line.strip() and len(line.strip()) > 3
        ]

        return sub_questions[:3] if sub_questions else [query]
    except Exception:
        return [query]


def multi_hop_retrieve(query, n_per_hop=2):
    """
    Retrieve documents for each sub-question and combine the results.

    Steps:
      1. Decompose the query into sub-questions
      2. Embed and search for each sub-question independently
      3. Combine results, removing duplicates

    Args:
        query:     The original complex query.
        n_per_hop: Documents to retrieve per sub-question.

    Returns:
        A deduplicated list of relevant document strings.
    """
    sub_queries = decompose_query(query)

    all_documents = []
    seen_documents = set()

    for sub_query in sub_queries:
        embedding = embed_text(sub_query)
        results = query_similar(embedding, n_per_hop)

        for doc in results["documents"][0]:
            if doc not in seen_documents:
                seen_documents.add(doc)
                all_documents.append(doc)

    return all_documents
