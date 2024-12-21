import os

import cohere

from src.models.state import State
from src.constants import RERANKER_MODEL, RERANKER_TOP_N

cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

def reranker_node(state: State) -> State:
    """Node to rerank the retrieved documents"""

    question = state["question"]
    retrieved_docs = state["retrieved_docs"]

    unranked_results = [
        {"text": result['text'], "id": result['id']} for result in retrieved_docs
    ]

    ranked_results = cohere_client.rerank(
        model=RERANKER_MODEL,
        query=question,
        documents=unranked_results,
        top_n=RERANKER_TOP_N,
    )

    ranked_docs = []
    for result in ranked_results.results:
        idx = result.index
        doc = unranked_results[idx]
        ranked_docs.append({
            "text": doc["text"],
            "id": doc["id"],
        })

    return {"ranked_docs": ranked_docs}