import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mock mode (default = True)
MOCK_LLM = os.getenv("MOCK_LLM", "1") == "1"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ChromaDB settings
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "zepto_docs"

# Corpus folder
DOCS_PATH = "./docs"