from src.models.state import State
from src.utils import load_table
from src.constants import TABLE_NAME, RETRIEVAL_TOP_N

def retriever_node(state: State) -> State:
    """Node to perform vector retrieval and full text search
    over the corpus of documents and return the top n relevant documents"""
    
    question = state["question"]

    table = load_table(TABLE_NAME)

    retrieved_docs = (
        table.search(question, query_type="hybrid")
        .limit(RETRIEVAL_TOP_N)
        .to_list()
    )

    return {"retrieved_docs": retrieved_docs}