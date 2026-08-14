from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from app.config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    DOCS_PATH,
    EMBEDDING_MODEL,
)

# Create persistent ChromaDB client
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Create or load collection
collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

# Load embedding model
model = SentenceTransformer(EMBEDDING_MODEL)

# Read all documents
doc_folder = Path(DOCS_PATH)

documents = []

for file in sorted(doc_folder.glob("*.txt")):
    text = file.read_text(encoding="utf-8")

    documents.append(
        {
            "id": file.stem,
            "text": text,
        }
    )

print(f"Loaded {len(documents)} documents.")

# Generate embeddings
texts = [doc["text"] for doc in documents]
embeddings = model.encode(texts).tolist()

# Clear existing collection (optional, avoids duplicates)
existing = collection.get()

if existing["ids"]:
    collection.delete(ids=existing["ids"])

# Store in ChromaDB
collection.add(
    ids=[doc["id"] for doc in documents],
    documents=texts,
    embeddings=embeddings,
)

print(f"Embedded and stored {len(documents)} documents in ChromaDB.")

if __name__ == "__main__":
    print("Ingestion complete!")