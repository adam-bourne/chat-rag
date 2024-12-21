from langgraph.graph import END

from src.models import State

def route_doc_assistant(state: State):
    """Decides whether to enter the RAG flow or respond directly to the user"""

    last_message = state["messages"][-1]
    if "tool_calls" not in last_message.additional_kwargs:
        return END
    else:
        return "retriever_node"
