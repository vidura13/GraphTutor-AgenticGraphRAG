# ADR-0002: ChromaDB collections & embedding model

- **Status**: PROPOSED (confirm with M03)
- **Context**: GraphRAG retrieval needs deterministic, keyless, local embeddings; collections must
  isolate shared vs private content for the forking model.
- **Decision**: ChromaDB embedded (local persist dir); default embedding
  `all-MiniLM-L6-v2` (ONNX, local, deterministic); collections `curriculum_{id}` (shared chunks)
  and `user_{id}_private`; chunk = one `Section`, metadata
  `{doc_id, section_id, concept_keys, subject}`.
- **Consequences**: no API cost in ingestion; M03 queries with concept-scoped `where` filters;
  swap embedding later = re-index script (M01 provides).
