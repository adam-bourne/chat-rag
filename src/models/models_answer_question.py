from langchain_core.pydantic_v1 import BaseModel, Field

class AnswerRag(BaseModel):
    answer: str = Field(
        description="The most concise answer to the question",
        min_length=1,
        max_length=1000
    )
    chain_of_thought: str = Field(
        description="The chain of thought used to arrive at the answer",
        min_length=1,
        max_length=1000
    )