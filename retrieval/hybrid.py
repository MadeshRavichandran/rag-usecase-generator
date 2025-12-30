def hybrid_search(vector_results, keyword_results, top_k=5):
    seen = set()
    combined = []

    for r in vector_results + keyword_results:
        key = r["text"][:200]
        if key not in seen:
            seen.add(key)
            combined.append(r)

    combined.sort(key=lambda x: x["score"], reverse=True)
    return combined[:top_k]
