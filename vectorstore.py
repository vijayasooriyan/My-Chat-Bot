from pinecone import Pinecone
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pinecone_client.Index(os.getenv("PINECONE_INDEX_NAME"))

def store_in_pinecone(chunks: List[str], embeddings: List[List[float]],namespace : str =""):
    vectors_to_upsert =[]
    for i,(chunk,embedding) in enumerate(zip(chunks,embeddings)):
        vector_data={
            "id": f"chunk_{i}",
            "values": embedding,
            "metadata": {
                "text": chunk,
                "chunk_index": i
                }
        }
        vectors_to_upsert.append(vector_data)

    batch_size = 100
    for i in range(0, len(vectors_to_upsert), batch_size):
        batch = vectors_to_upsert[i:i + batch_size]
        index.upsert(vectors=batch,namespace=namespace)

def search_in_pinecone(query_vector: List[float], top_k: int = 3, namespace: str = "") -> str:
    """Search for similar chunks in Pinecone using a query vector."""
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )
    
    # Extract and combine the metadata text from matched chunks
    matched_chunks = []
    for match in results.matches:
        if match.metadata.get("text"):
            matched_chunks.append(match.metadata["text"])
    
    return "\n\n".join(matched_chunks)
        