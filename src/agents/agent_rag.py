from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from src.models import State
from src.nodes import (
    doc_assistant_node,
    retriever_node,
    reranker_node,
    answer_question_node,
)
from src.routing import route_doc_assistant

class RAGAgent:
    """Manages the graph which performs RAG"""

    def __init__(self, chat: bool = False):
        self.chat = chat
        self.thread = {"configurable": {"thread_id": "1"}} # for retrieving state 
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.graph = self.init_graph()
        self.chat_history = []

    def init_graph(self):
        
        workflow = StateGraph(State)

        # Set entry point depending on whether the system is conversational or not
        if self.chat:
            workflow.set_entry_point("doc_assistant")
            workflow.add_node("doc_assistant", doc_assistant_node)
            workflow.add_conditional_edges("doc_assistant", 
                                   route_doc_assistant,
                                   )
            workflow.add_edge("answer_question_node", "doc_assistant")
        else:
            workflow.set_entry_point("retriever_node")

        # Add nodes
        workflow.add_node("retriever_node", retriever_node)
        workflow.add_node("reranker_node", reranker_node)
        workflow.add_node("answer_question_node", answer_question_node)

        # Add edges
        workflow.add_edge("retriever_node", "reranker_node")
        workflow.add_edge("reranker_node", "answer_question_node")

        #TRY WITOUT MEMORY ONCE COMPLETE AND SEE IF IT WORKS
        graph = workflow.compile(checkpointer=self.memory)

        return graph
    
    def run(self, question: str) -> str:
        """Manages the graph execution"""

        # Add question to chat history
        messages = self.chat_history.copy()
        messages.append(HumanMessage(content=question))

        inputs = {
            "question": question,
            "messages": messages, 
            "chat": self.chat
        }

        final_state = self.graph.invoke(inputs, self.thread)

        answer = final_state["messages"][-1].content
        self.chat_history = final_state["messages"]

        return answer

