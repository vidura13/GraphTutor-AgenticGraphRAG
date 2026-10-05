# Software Requirements Specification — GraphTutor (v0, for team sign-off)

Traceable requirements: every story below becomes a GitHub issue (see `scripts/create_issues.py`)
and later a test. Owners per proposal §5.2. Priorities: **P0** = MVP, **P1** = stretch.

## 1. Scope

In scope: deterministic AKGC ingestion; Neo4j ontology; ChromaDB chunking; CAT diagnostics;
BKT mastery; IRT readiness; LangGraph remediation with guardrails; Sinhala/Tamil mapping;
graph-forking sharing; React dashboard + heatmap; SimPy validation.
Out of scope (proposal §4.2): scanned/image-only papers, complex formula parsing, code execution,
certified exam prediction.

## 2. User stories & acceptance criteria

### US-01 — Upload study materials (owner M01/M02) · P0
*As a student, I want to upload PDF slides/notes/past papers so that my syllabus graph is built.*
- AC1: Accepts text-based PDFs; rejects image-only scans with a clear error.
- AC2: Ingestion is idempotent — re-uploading the same file changes nothing (`content_hash`).
- AC3: Produces `Concept`, `Section`, `Document` nodes + `PART_OF` hierarchy + Chroma chunks.

### US-02 — Deterministic concept & prerequisite extraction (owner M01) · P0
*As the system, I want concepts and prerequisite edges extracted deterministically so that the
graph is reproducible and hallucination-free.*
- AC1: Concept **recall ≥ 0.90** against the hand-annotated gold set (proposal objective).
- AC2: Every `PREREQUISITE_OF` edge stores `confidence`, `method`, `evidence`.
- AC3: The prerequisite relation never contains a cycle (DAG enforced).
- AC4: Edges with confidence 0.40–0.75 land in a human review queue, not the live graph.

### US-03 — Share curriculum via graph-forking (owner M02) · P1
*As a student, I want to share my curriculum map with my study group without duplicating storage.*
- AC1: Peers reference the same canonical `Concept` nodes (no subgraph copy).
- AC2: Each member's BKT state stays isolated (PostgreSQL, per-user rows).
- AC3: Sharing is revocable via an ACL entry.

### US-04 — Diagnostic quiz via CAT graph search (owner M03) · P0
*As a student, I want the quiz to adaptively hunt my knowledge boundary so diagnosis is fast.*
- AC1: Next question targets a concept on the prerequisite frontier of current mastery.
- AC2: Session ends by a stopping rule (max items or confidence threshold).

### US-05 — BKT mastery update (owner M03) · P0
*As a student, I want every answer to update my per-concept mastery probability.*
- AC1: Update uses BKT parameters (pL0, pT, pG, pS) persisted per user in PostgreSQL.
- AC2: Update is monotone-consistent: repeated correct answers raise p(L).

### US-06 — Misconception remediation via LangGraph agent (owner M03) · P1
*As a student who answered wrongly, I want a guided hint — not the answer — targeting my misconception.*
- AC1: Cyclic state machine with a max-loop bound; output validated by Pydantic JSON schema.
- AC2: Retrieval is scoped to the weak concept's graph neighbourhood (GraphRAG).

### US-07 — Sinhala/Tamil terminology mapping (owner M03) · P1
*As a student facing a language barrier, I want IT terms glossed in Sinhala/Tamil.*
- AC1: Mapping layer is a reviewable table (YAML/DB), not free-form LLM translation.

### US-08 — Progress heatmap (owner M04) · P0
*As a student, I want a force-directed graph coloured by mastery so my weak spots are visible.*
- AC1: Renders graph snapshot JSON (schema co-defined by M01/M04) + per-user mastery overlay.
- AC2: Updates in real time after each answer submission.

### US-09 — Exam readiness score (owner M03) · P1
*As a student, I want an IRT-based readiness probability as a progress indicator.*
- AC1: Computed from interaction history only; labelled as an indicator, not a certification.

### US-10 — Simulation validation (owner M05) · P0
*As the team, we want virtual students with known blind spots to prove BKT/CAT converge.*
- AC1: SimPy engine ingests through the same pipeline entry point as real users.
- AC2: Reports convergence steps & routing efficiency vs known baseline on 3 subjects.

## 3. Non-functional requirements

- **Security**: JWT-authenticated sessions; per-user data isolation (M02).
- **Determinism**: same input ⇒ identical graph (M01 pipeline is pure functions + stored rules).
- **Model-agnosticism**: LLM provider swappable via config; no provider-specific logic in core.
- **Performance**: ingestion of a 30-page PDF < 60 s on a laptop; heatmap render < 1 s.
- **Auditability**: every extracted edge traceable to evidence sentence (review queue UX later).
