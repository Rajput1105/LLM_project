import chromadb
from sentence_transformers import SentenceTransformer


chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("financial_docs")
embedding_model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


# Query ChromaDB
query_text = "What is Since Inception?"
query_embedding = embedding_model.encode(query_text)

results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=1)


# Display retrieved documents
for i, doc in enumerate(results["documents"]):
    print(f"\n🔹 Retrieved Document {i+1}:")
    print(doc[:500])  # Print first 500 characters
    print("Metadata:", results["metadatas"][i])

