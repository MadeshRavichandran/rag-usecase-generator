import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def add(self, chunks):
        embeddings = self.model.encode([c["text"] for c in chunks])
        self.index.add(np.array(embeddings))
        self.texts.extend(chunks)

    def search(self, query, top_k=5):
        q_emb = self.model.encode([query])
        distances, indices = self.index.search(q_emb, top_k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            results.append({
                "text": self.texts[idx]["text"],
                "score": float(1 / (1 + dist))
            })
        return results
