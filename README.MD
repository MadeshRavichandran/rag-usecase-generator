# File-Based Multimodal RAG for Use-Case / Test-Case Generation

## Overview
This project implements a file-based Retrieval-Augmented Generation (RAG) system that generates grounded use cases and test cases from uploaded documents such as PRDs, notes, and specifications.

The system prioritizes retrieval accuracy, hallucination prevention, modular design, and structured JSON output, while keeping the UI intentionally lightweight.

## Key Capabilities
- File-based knowledge ingestion (no external database required)
- Hybrid retrieval (Vector + Keyword search)
- Context-grounded LLM generation
- Strong guardrails against hallucination
- Debug and observability support
- Deterministic, structured JSON output
- Persistent output storage
- Streamlit UI for demonstration

## Architecture
Input Files
↓
Parsing & Chunking
↓
Hybrid Retrieval (Vector + Keyword)
↓
Evidence Threshold Check
↓
LLM Generation (Context-Only)
↓
JSON Normalization & ID Injection
↓
Saved Output + Debug View


## Supported Input Files
- .txt, .md
- .pdf
- Extensible for .docx and images via OCR

All files are parsed, chunked, embedded, and indexed locally.

## Retrieval Strategy
- Vector Search: Semantic similarity using embeddings
- Keyword Search: SQLite FTS5
- Hybrid Merge: Deduplicated, ranked results
- Minimum Evidence Threshold: Prevents low-confidence generation

If evidence is insufficient, the system refuses to generate output.

## Generation Strategy
- Uses free LLM inference (Groq – LLaMA 3.1)
- Strict system prompt:
  - Context-only generation
  - No hallucinated features
  - JSON-only output
- Robust JSON parsing:
  - Handles malformed LLM responses
  - Extracts first valid JSON object
- Schema normalization:
  - Automatically injects stable use-case IDs (UC-01, UC-02, ...)

## Safety and Guardrails
- No generation without sufficient evidence
- No feature invention outside documents
- Explicit handling of missing information
- Prompt-injection resilience
- Deterministic output schema

## Debug and Observability
- Debug mode shows:
  - Retrieved chunks
  - Similarity scores
- Evidence threshold control
- Output persisted to:


## Streamlit UI
Run the UI:
-streamlit run streamlit_app.py


Features:
- File upload
- Query input
- Debug toggle
- Evidence threshold control
- JSON output viewer

## CLI Usage
python app.py