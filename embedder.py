from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

EMBEDDING_DIMENSION = 512  # Match Pinecone index dimension
_model = None  # Lazy-load model

def _get_model():
    """Lazy-load the embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def _pad_embedding(embedding: List[float], target_dim: int = EMBEDDING_DIMENSION) -> List[float]:
    """Pad embedding to match Pinecone index dimension."""
    # Convert numpy array to list if needed
    if isinstance(embedding, np.ndarray):
        embedding = embedding.tolist()
    
    current_dim = len(embedding)
    if current_dim < target_dim:
        padding = np.zeros(target_dim - current_dim)
        return np.concatenate([np.array(embedding), padding]).tolist()
    return embedding[:target_dim]

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """Embed chunks using sentence-transformers model."""
    model = _get_model()
    embeddings = model.encode(chunks, convert_to_tensor=False)
    # Pad embeddings to match Pinecone dimension
    padded_embeddings = [_pad_embedding(emb) for emb in embeddings]
    print(f"Embedded {len(chunks)} chunks successfully")
    return padded_embeddings

def embed_User_query(query: str) -> List[float]:
    """Embed a user query to create a vector representation."""
    model = _get_model()
    embedding = model.encode(query, convert_to_tensor=False)
    return _pad_embedding(embedding)