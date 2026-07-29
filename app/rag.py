import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(BASE_DIR, "knowledge_base", "health_topics.json")

_model = None
_index = None
_kb_data = None

def _load():
    global _model, _index, _kb_data
    if _model is not None:
        return  # already loaded

    with open(KB_PATH, "r", encoding="utf-8") as f:
        _kb_data = json.load(f)

    _model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [f"{item['topic']}: {item['content']}" for item in _kb_data]
    embeddings = _model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)  # cosine similarity via inner product on normalized vecs
    _index.add(embeddings)

def retrieve(query: str, top_k: int = 2, threshold: float = 0.35):
    """
    Returns a list of relevant KB entries above similarity threshold.
    Empty list if nothing is relevant enough (avoids forcing irrelevant context).
    """
    _load()
    query_vec = _model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    scores, indices = _index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if score >= threshold and idx != -1:
            entry = _kb_data[idx]
            results.append({**entry, "score": float(score)})
    return results