import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def add(self, chunks):
        if not chunks:
            return

        texts = [c["text"] for c in chunks if c.get("text", "").strip()]
        if not texts:
            return

        embeddings = self.model.encode(texts)
        embeddings = np.array(embeddings)

        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        self.index.add(embeddings)
        self.texts.extend(texts)

    def search(self, query, top_k=5):
        if self.index.ntotal == 0:
            return []

        q_emb = self.model.encode([query])
        q_emb = np.array(q_emb)

        distances, indices = self.index.search(q_emb, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.texts):
                results.append({
                    "text": self.texts[idx],
                    "score": float(1 / (1 + dist))
                })

        return results
