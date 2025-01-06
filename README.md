# chat-rag
A RAG application built on top of the ConvFinQA dataset: https://github.com/czyssrs/ConvFinQA. 

This dataset contains 3000+ question/answer pairs for financial documents, and serves as a benchmark for examining the performance of RAG applications and LLM numerical reasoning.

This repo uses LangGraph to build the RAG architecture, and has an optional chat interface. Evaluation results are available in the `eval_data/` directory.

## Setup

### 1. Prerequisites
- Python 3.12

### 2. Environment variables
The RAG application uses OpenAI and Cohere as standard, and LangSmith for optional tracing. API keys are required for each, and `.env` file in the root directory should store them as follows:
```bash
OPENAI_API_KEY=<your_openai_api_key>
COHERE_API_KEY=<your_cohere_api_key>
LANGCHAIN_API_KEY=<your_langchain_api_key>
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get the data
Run the following script to download the data. This will create a `ConvFinQA` directory with the data in the root directory.
```bash
./scripts/unzip_data.sh
```

### 5. Build the vector DB
Run the following script to build the vector DB. This will create a `.my_db` directory in the root directory.
```bash
python scripts/build_local_vector_db.py
```

## Using the application
### Running the chat application
This will enable you to have back and forth conversations with the RAG agent.

This can take a minute to load on the first run.
```bash
streamlit run app.py
```

### Evaluating performance
To see evaluations, go to `notebooks/03_evaluation.ipynb`.