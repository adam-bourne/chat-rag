from langchain_core.pydantic_v1 import BaseModel, Field

class RAGTool(BaseModel):
    """Select this tool when the user's question must be answered by querying the database"""

    question: str = Field(
        description="The users specific question, including context and scope.",
        min_length=1,
        max_length=1000
    )