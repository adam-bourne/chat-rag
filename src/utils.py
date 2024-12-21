"""Misc utils for the repo"""
import os

import lancedb
from langchain_openai import ChatOpenAI

from src.constants import DB_NAME

# set up tracing on langsmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "FINANCIAL_RAG"

_db_table = None

def load_table(table_name: str):
    """Loads a LanceDB table, creating the connection only once"""
    global _db_table

    if _db_table is None:
        # Get the current file's directory and construct path to project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        db_path = os.path.join(root_dir, f".{DB_NAME}")
        
        db = lancedb.connect(db_path)
        _db_table = db.open_table(table_name)

    return _db_table

def get_llm(model: str, **kwargs) -> ChatOpenAI:
    """Creates a ChatOpenAI instance from a given model name"""

    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=model,
        temperature=0,
        streaming=True,
        max_retries=3,
        model_kwargs=kwargs
    )

    return llm