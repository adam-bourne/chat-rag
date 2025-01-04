from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage, AIMessage

from src.models import State, AnswerRag
from src.formatting import format_ranked_docs
from src.utils import get_llm
from src.prompts import ANSWER_QUESTION_PROMPT
from src.constants import LLM_MODEL

llm = get_llm(LLM_MODEL)

def answer_question_node(state: State):
    """Node to answer the question using the rerieved and ranked documents"""

    question = state["question"]
    reranked_docs = state["reranked_docs"]

    # Format the ranked documents
    formatted_reranked_docs = format_ranked_docs(reranked_docs)

    # Create the chain
    answer_question_prompt_template = ChatPromptTemplate.from_messages([
        ("system", ANSWER_QUESTION_PROMPT),
    ])
    answer_question_chain = answer_question_prompt_template | llm.with_structured_output(AnswerRag)

    answer_rag = answer_question_chain.invoke({"question": question, "context": formatted_reranked_docs}).dict()

    # if in chat mode, this is a tool call, so need to return a tool message
    if state["chat"]:
        last_tool_call = state["messages"][-1].additional_kwargs["tool_calls"][-1]
        response = ToolMessage(
            content=answer_rag["answer"],
            name="rag_tool",
            tool_call_id=last_tool_call["id"]
        )

    # if not, just return an AI message
    else:
        response = AIMessage(content=answer_rag["answer"])

    return {"messages": [response], "answer": answer_rag["answer"]}