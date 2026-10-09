# GraphTutor

**An Agentic GraphRAG System with Probabilistic Mastery Tracking for Computing Exam Preparation.**

A model-agnostic, adaptive study platform for Sri Lankan IT/SE undergraduates. Uploaded course
materials become a deterministic knowledge graph (Neo4j) + vector chunks (ChromaDB); diagnostic
quizzes route via graph-based CAT; mastery is traced with BKT and rolled into an IRT exam-readiness
score; a LangGraph agent generates guarded, multilingual (Sinhala/Tamil) remediation; peers share
curricula via graph-forking. Validated by SimPy discrete-event simulation with virtual students.

> **Design principle:** the graph + probabilistic models are the source of truth.
> The LLM only *words* explanations, behind JSON guardrails, after the cognitive state is fixed.

## Team & ownership

| Member | Role | Primary area |
|---|---|---|
| 01 | Project Leader & Knowledge Graph Engineer | Ontology/Neo4j schema, AKGC ingestion pipeline, requirements |
| 02 | Backend & Systems Engineer | FastAPI, JWT, graph-forking ACLs, semantic cache |
| 03 | AI/ML Engineer | BKT/IRT/CAT, LangGraph agents, GraphRAG, multilingual layer |
| 04 | Frontend & Visualization Engineer | React + D3 dashboard, force-directed heatmap |
| 05 | Research, QA & Validation Engineer | SimPy simulation, testing strategy, documentation |

## Repository layout

```
docs/            SRS, ontology, architecture, ADRs, team workflow
src/graphtutor/  Python package (ontology/, ingestion/, graph/, eval/)
web/             React app (added by M04)
tests/           unit + integration (pytest)
scripts/         ops helpers (issue bootstrap, DB setup)
.github/         CI workflow + PR/issue templates
```

## Local development quickstart

```bash
# 1. services (Neo4j for M01/M03, Postgres for M02)
docker compose up -d

# 2. python env
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m spacy download en_core_web_md
cp .env.example .env                                   # adjust if needed

# 3. verify
pytest tests/unit -q

# 4. database schema + shared dev fixture (S1)
python -m graphtutor.graph.schema       # apply constraints/indexes (idempotent)
python -m graphtutor.ontology.seed      # load the OOP mini-graph
```

Neo4j Browser: http://localhost:7474 (user `neo4j`, password `graphtutor_dev`).

## Workflow (read before your first PR)

- Branch model, PR rules, commit conventions, sprint cadence → [`docs/TEAM_WORKFLOW.md`](docs/TEAM_WORKFLOW.md)
- Requirements as user stories → [`docs/SRS.md`](docs/SRS.md); backlog bootstrap → `scripts/create_issues.py`
- One-time push/protection/invite commands for the lead → [`docs/PUSH_GUIDE.md`](docs/PUSH_GUIDE.md)

## Documentation index

| Doc | Purpose |
|---|---|
| [`docs/SRS.md`](docs/SRS.md) | Software Requirements Specification (user stories + acceptance criteria) |
| [`docs/ontology.md`](docs/ontology.md) | IT-education ontology & Neo4j schema (M01 deliverable 1) |
| [`docs/architecture.md`](docs/architecture.md) | System architecture & data flow |
| [`docs/adr/`](docs/adr/) | Architecture Decision Records (forking model, embeddings, question nodes) |

## Status

S0 (bootstrap). Implementation sprints S1–S6 are tracked in `planning/member01_workflow.md`
(M01 working document, pre-repo) and mirrored to GitHub milestones.
