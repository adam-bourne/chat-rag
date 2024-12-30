import operator
from typing import Annotated, Sequence, TypedDict, List
from langchain_core.messages import BaseMessage

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    question: str
    chat: bool
    retrieved_docs: List[dict]
    ranked_docs: List[dict]
