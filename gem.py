
import os
import requests
import json
import chromadb
from sentence_transformers import SentenceTransformer

api_key = ""  
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

chroma_client = chromadb.HttpClient(host="localhost", port=2000)
collection = chroma_client.get_or_create_collection("financial_docs")
def query_rag(question):
    query_embedding = embedding_model.encode(question)

    results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=3)  

    retrieved_docs = [doc[0] for doc in results["documents"] if doc]  
    if retrieved_docs:
        retrieved_text = "\n\n".join(retrieved_docs)  
    else:
        retrieved_text = "No relevant data found in the database."

   
    prompt = f"""Use the following information to answer the question:
    {retrieved_text}

    Question: {question}
    Answer:
    """

    
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(
        f"{api_url}?key={api_key}",
        headers=headers,
        json=payload
    )

    
    if response.status_code == 200:
        result = response.json()
        try:
            output_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return output_text
        except KeyError:
            return "⚠️ Unexpected response format from Gemini."
    else:
        return f"❌ API Error ({response.status_code}): {response.text}"


question = "What was investment on 13-Mar-25 turned into Invested?"
answer = query_rag(question)
print("🤖 Gemini's Answer:", answer)
