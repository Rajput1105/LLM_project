import chromadb 
from sentence_transformers import SentenceTransformer
import os 
from loguru import logger

logger.add("app.log", rotation="10 MB", level="INFO")

embedding_model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

file_path='./Data/MHD1150.md'

with open(file_path,'r',encoding='utf-8') as f:
    markdown_text=f.read()


embedding=embedding_model.encode(markdown_text)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("financial_docs")
chroma_client = chromadb.HttpClient(host="localhost", port=2000)
# Add Markdown text + embedding to ChromaDB
collection.add(
    documents=[markdown_text],
    embeddings=[embedding.tolist()],
    metadatas=[{"file_name": os.path.basename(file_path), "format": "markdown"}],
    ids=["financial_report_001"]
)
logger.info("Markdown file embedded & stored in ChromaDB ✅")
print("Markdown file embedded & stored in ChromaDB ✅")