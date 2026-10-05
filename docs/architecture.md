# System Architecture (mirrors proposal Figure 01)

```
 Presentation (React + D3)          Gateway (FastAPI + JWT)         Simulation (SimPy, M05)
  upload · heatmap · quiz · auth  ◄──────────────►│◄────────── virtual students
                                             │
                       Agentic Engineering Core
   ┌─────────────────────────────────────────┼────────────────────────────────────────┐
   │  Deterministic NLP Pipeline (M01)   LangGraph Orchestrator (M03) ──► Cloud LLMs  │
   │  Graph Traversal / CAT (M03)        Statistical Modeling BKT·IRT (M03)           │
   │  Multilingual Terminology Layer (M03)                                            │
   └─────────────────────────────────────────┼────────────────────────────────────────┘
                                             │
                       Hybrid Data Persistence
            Neo4j (graph)   ·   ChromaDB (vectors)   ·   PostgreSQL (users/BKT)
```

## Data flow (ingestion — M01's pipeline)

1. PDF → text+layout (PyMuPDF/pdfplumber); image-only scans rejected.
2. Section segmentation via heading/numbering/font heuristics ⇒ `Section` tree ⇒ `PART_OF`.
3. spaCy: noun chunks + glossary `EntityRuler` + acronym tables ⇒ concepts.
4. Canonicalisation ⇒ `canonical_key` (synonyms.yaml).
5. Prerequisite mining: lexical cues (0.9) · dependency-parse cues (0.8) · cross-refs (0.7) ·
   ILO coupling (0.6) · structural prior (0.3); confidence-gated, evidence-stamped, DAG-checked.
6. Load: Neo4j `MERGE` batches + ChromaDB section chunks (MiniLM embeddings) with metadata
   `{doc_id, section_id, concept_keys, subject}` (ADR-0002).

## Downstream consumers

- **M03 CAT** traverses `PREREQUISITE_OF` to pick frontier questions; **BKT** writes Postgres;
  **GraphRAG** scopes Chroma retrieval by graph neighbourhood.
- **M04** renders graph-snapshot JSON (schema co-defined S6) + mastery overlay.
- **M02** wraps all of it in REST + JWT; owns fork ACLs (ADR-0001).
- **M05** drives the same ingest entry point with virtual students.

## Forking model (ADR-0001, summary)

Canonical curriculum graph shared; per-user mastery only in Postgres; per-user private vectors in
`user_{id}_private` collections; personal annotations as `PersonalNote` overlays; "fork" = ACL row.
