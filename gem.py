# prompt: !curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=x" \
# -H 'Content-Type: application/json' \
# -X POST \
# -d '{
#   "contents": [{
#     "parts":[{"text": "Explain how AI works"}]
#     }]
#    }'
# convert above in python code 

import os
import requests
import json
import chromadb
from sentence_transformers import SentenceTransformer

# 🔹 Set up Google Gemini API Key
api_key = ""  # Replace with your actual API key
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

# 🔹 Load embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 🔹 Connect to ChromaDB running on port 2000
chroma_client = chromadb.HttpClient(host="localhost", port=2000)
collection = chroma_client.get_or_create_collection("financial_docs")
def query_rag(question):
    # Step 1️⃣: Convert question into an embedding
    query_embedding = embedding_model.encode(question)

    # Step 2️⃣: Search relevant documents in ChromaDB
    results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=3)  # Fetch 3 relevant docs

    # Step 3️⃣: Extract the retrieved documents (Flatten the list)
    retrieved_docs = [doc[0] for doc in results["documents"] if doc]  # Extract strings from lists

    if retrieved_docs:
        retrieved_text = "\n\n".join(retrieved_docs)  # Combine multiple docs for better context
    else:
        retrieved_text = "No relevant data found in the database."

    # Step 4️⃣: Create a structured prompt for Gemini
    prompt = f"""Use the following information to answer the question:
    {retrieved_text}

    Question: {question}
    Answer:
    """

    # Step 5️⃣: Make an API call to Gemini
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

    # Step 6️⃣: Extract response from Gemini
    if response.status_code == 200:
        result = response.json()
        try:
            output_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return output_text
        except KeyError:
            return "⚠️ Unexpected response format from Gemini."
    else:
        return f"❌ API Error ({response.status_code}): {response.text}"

# 🔹 Example Query
question = "What was investment on 13-Mar-25 turned into Invested?"
answer = query_rag(question)
print("🤖 Gemini's Answer:", answer)
