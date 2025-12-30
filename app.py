import argparse
import json
import os

from ingestion.loader import load_text_from_file
from ingestion.chunker import chunk_text
from retrieval.vector_store import VectorStore
from retrieval.keyword_store import KeywordStore
from retrieval.hybrid import hybrid_search
from guards.confidence import has_sufficient_evidence
from generation.generator import generate_use_cases


def main(debug=False):
    query = "Create use cases for user signup"

    text = load_text_from_file("data/PRD_Signup.md")
    chunks = chunk_text(text)
    vector_store = VectorStore()
    keyword_store = KeywordStore()

    vector_store.add(chunks)
    keyword_store.add(chunks)

    v_results = vector_store.search(query)
    k_results = keyword_store.search(query)

    results = hybrid_search(v_results, k_results)

    if debug:
        print("\nRetrieved Chunks:")
        for r in results:
            print("Score:", round(r["score"], 3))
            print(r["text"][:200], "\n---")

    if not has_sufficient_evidence(results):
        print("Insufficient context. Please provide more details.")
        return

    output = generate_use_cases(query, results)

    
    os.makedirs("outputs", exist_ok=True)
    output_path = "outputs/use_cases.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\n Use cases generated and saved to {output_path}\n")

    if debug:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    main(debug=args.debug)
