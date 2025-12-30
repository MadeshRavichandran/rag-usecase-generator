from typing import List
import hashlib

def chunk_text(text: str, chunk_size=500, overlap=100) -> List[dict]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        chunk_hash = hashlib.md5(chunk_text.encode()).hexdigest()
        chunks.append({
            "text": chunk_text,
            "hash": chunk_hash
        })

        start += chunk_size - overlap

    return chunks
