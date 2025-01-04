from src.models.state import State
from src.utils import load_table, get_ner_model
from src.constants import TABLE_NAME, RETRIEVAL_TOP_N

def retriever_node(state: State) -> State:
    """Node to perform vector retrieval and full text search
    over the corpus of documents and return the top n relevant documents"""
    
    question = state["question"]
    metadata_filtering = state["metadata_filtering"]

    table = load_table(TABLE_NAME)

    retrieved_docs = table.search(question, query_type="hybrid").limit(RETRIEVAL_TOP_N)

    if metadata_filtering:
        year_range = get_range(question)
        if len(year_range) == 2: # only filter if we have valid year range
            retrieved_docs = retrieved_docs.where(f"year IN {year_range}", prefilter=True)

    return {"retrieved_docs": retrieved_docs.to_list()}


def get_range(question: str) -> tuple:
    """Takes a question, extracts the years mentioned, and takes the latest year.
    Then will create a year containing the latest year and the next year.
    This should encompass a lot of the documts."""

    model = get_ner_model()
    labels = ["Year"]
    entities = model.predict_entities(question, labels, threshold=0.5)
    
    try:
        # sometimes we get errors if the entraction doesn't convert to an int
        years = (int(entity['text']) for entity in entities)
        max_year = max(years)
        return (max_year + 1, max_year)
    except:
        return ()