"""Misc utils for the repo"""
import os

import lancedb
from langchain_openai import ChatOpenAI
from gliner import GLiNER
from src.constants import DB_NAME, LANGCHAIN_PROJECT

# set up tracing on langsmith if using
if os.getenv("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT

_db_table = None
_ner_model = None

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

    # Load environment variables explicitly
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    llm = ChatOpenAI(
        api_key=api_key,
        model=model,
        temperature=0,
        streaming=True,
        max_retries=3,
        model_kwargs=kwargs
    )

    return llm

def get_ner_model():
    global _ner_model

    if _ner_model is None:
        _ner_model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

    return _ner_model