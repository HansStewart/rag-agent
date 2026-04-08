import faiss
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

index = None
chunks = []
chunk_sources = []

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

def chunk_text(text, source_name, chunk_size=500, overlap=50):
    words = text.split()
    chunks_list = []
    sources_list = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks_list.append(chunk)
            sources_list.append(source_name)
    return chunks_list, sources_list

def add_document(text, source_name):
    global index, chunks, chunk_sources
    new_chunks, new_sources = chunk_text(text, source_name)
    embeddings = []
    for chunk in new_chunks:
        embedding = get_embedding(chunk)
        embeddings.append(embedding)
    embeddings_array = np.array(embeddings, dtype=np.float32)
    if index is None:
        dimension = embeddings_array.shape[1]
        index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_array)
    chunks.extend(new_chunks)
    chunk_sources.extend(new_sources)
    return len(new_chunks)

def search_documents(query, top_k=5):
    global index, chunks, chunk_sources
    if index is None or len(chunks) == 0:
        return []
    query_embedding = get_embedding(query)
    query_array = np.array([query_embedding], dtype=np.float32)
    distances, indices = index.search(query_array, min(top_k, len(chunks)))
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:
            results.append({
                "chunk": chunks[idx],
                "source": chunk_sources[idx],
                "score": float(distances[0][i])
            })
    return results

def get_store_stats():
    return {
        "total_chunks": len(chunks),
        "documents": list(set(chunk_sources)),
        "index_ready": index is not None
    }