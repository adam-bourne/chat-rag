import sys
import json
import os
import lancedb

from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

# Add the project root directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.formatting import format_data
from src.constants import SENTENCE_TRANSFORMER, DB_NAME

# Initialize embedding model
sentence_model = get_registry().get("sentence-transformers").create(
    name=SENTENCE_TRANSFORMER
)

class Document(LanceModel):
    """Schema for the vector DB"""
    id: str
    text: str = sentence_model.SourceField()
    vector: Vector(384) = sentence_model.VectorField() # type: ignore
    year: int

def create_vector_db(data_path: str, db_path: str, table_name: str = "financial_docs"):
    """Create a vector database from financial documents.
    
    Args:
        data_path: Path to the JSON data file
        db_path: Path where the LanceDB should be created
        table_name: Name of the table to create
    """
    # Load data
    with open(data_path, 'r') as f:
        train_data = json.load(f)
    
    # Format documents
    docs = [format_data(chunk) for chunk in train_data]

    # Connect to DB
    db = lancedb.connect(db_path)
    
    table = db.create_table(
        table_name,
        data=docs,
        schema=Document,
        mode="overwrite"
    )
    
    # Add full text search index
    table.create_fts_index("text", replace=True)
    
    return table

if __name__ == "__main__":
    # Set paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "ConvFinQA", "data")
    db_path = os.path.join(script_dir, "..", f".{DB_NAME}")
    
    data_file = os.path.join(data_dir, "train.json")
    
    # Create the vector DB
    table = create_vector_db(data_file, db_path)
    print(f"Vector database created successfully at {db_path}")