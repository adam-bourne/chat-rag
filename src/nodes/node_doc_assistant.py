import json
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate

from src.models import State, RAGTool
from src.utils import get_llm
from src.prompts import DOC_ASSISTANT_SYSTEM
from src.constants import LLM_MODEL

today = datetime.now().strftime("%B %d %Y")

llm = get_llm(LLM_MODEL)

def doc_assistant_node(state: State):
    """Node for a friendly doc assistant to act as a chat wrapper over the RAG agent"""

    messages = state["messages"]
    question = state["question"]

    doc_assistant_prompt = ChatPromptTemplate.from_messages(
        [("system", DOC_ASSISTANT_SYSTEM), ("placeholder", "{messages}")]
    ).partial(date=today)

    doc_assistant_chain = doc_assistant_prompt | llm.bind_tools([RAGTool])

    response = doc_assistant_chain.invoke({"messages": messages})

    # check if the LLM has used the RAGTool
    # If so, then we should use the reformatted question
    tool_calls = response.additional_kwargs.get("tool_calls", [])
    if tool_calls:
        question = json.loads(tool_calls[0]["function"]["arguments"])["question"]

    return {"messages": [response], "question": question}
