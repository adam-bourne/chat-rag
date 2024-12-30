# chat-rag
A repo for demoing RAG apps with chat interface


## Setup
### 1. Get the data
Run the following script to download the data. This will create a `ConvFinQA` directory with the data in the root directory.
```bash
./scripts/unzip_data.sh
```

### 2. Build the vector DB
Run the following script to build the vector DB. This will create a `.my_db` directory in the root directory.
```bash
python scripts/build_local_vector_db.py
```
