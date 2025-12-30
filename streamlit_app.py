import streamlit as st
import json
import os
import tempfile

from ingestion.loader import load_text_from_file
from ingestion.chunker import chunk_text
from retrieval.vector_store import VectorStore
from retrieval.keyword_store import KeywordStore
from retrieval.hybrid import hybrid_search
from guards.confidence import has_sufficient_evidence
from generation.generator import generate_use_cases

st.set_page_config(
    page_title="File-Based RAG – Use Case Generator",
    layout="wide"
)

st.title("📄 File-Based Multimodal RAG")
st.caption("Generate grounded use cases / test cases from uploaded files")


st.sidebar.header("⚙️ Settings")
debug_mode = st.sidebar.checkbox("Enable Debug Mode", value=False)
confidence_threshold = st.sidebar.slider(
    "Evidence Threshold",
    min_value=0.1,
    max_value=0.5,
    value=0.2,
    step=0.05
)

st.subheader("📂 Upload Input Files")
uploaded_files = st.file_uploader(
    "Upload PRD / Notes (TXT, MD, PDF)",
    type=["txt", "md", "pdf"],
    accept_multiple_files=True
)

st.subheader("❓ Query")
query = st.text_input(
    "Enter your query",
    value="Create use cases for user signup"
)

generate_btn = st.button("🚀 Generate Use Cases")

if generate_btn:
    if not uploaded_files:
        st.warning("Please upload at least one input file.")
        st.stop()
    with st.spinner("Processing files and retrieving context..."):
        all_chunks = []

        with tempfile.TemporaryDirectory() as tmpdir:
            for file in uploaded_files:
                path = os.path.join(tmpdir, file.name)
                with open(path, "wb") as f:
                    f.write(file.read())

                text = load_text_from_file(path)
                chunks = chunk_text(text)
                all_chunks.extend(chunks)

        vector_store = VectorStore()
        keyword_store = KeywordStore()

        vector_store.add(all_chunks)
        keyword_store.add(all_chunks)

        v_results = vector_store.search(query)
        k_results = keyword_store.search(query)
        results = hybrid_search(v_results, k_results)

    if debug_mode:
        st.subheader("🔍 Retrieved Chunks")
        for r in results:
            st.markdown(f"**Score:** `{round(r['score'], 3)}`")
            st.code(r["text"][:500])

    if not has_sufficient_evidence(results, threshold=confidence_threshold):
        st.error("❌ Insufficient context to generate use cases.")
        st.stop()

    with st.spinner("Generating structured use cases..."):
        output = generate_use_cases(query, results)

    st.subheader("✅ Generated Output (JSON)")
    st.json(output)

    # Save output
    os.makedirs("outputs", exist_ok=True)
    output_path = "outputs/use_cases.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    st.success(f"Output saved to `{output_path}`")
