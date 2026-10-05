# IT-Education Ontology & Neo4j Schema — v0 (M01 deliverable 1)

Status: **PROPOSED** — sign-off in S0 (see issue backlog). Implementation lives in
`src/graphtutor/ontology/schema.cypher` (constraints) + `glossary.yaml` / `synonyms.yaml`.

## 1. Node labels

| Label | Properties | Notes |
|---|---|---|
| `Subject` | `name` (UNIQUE), `code` | OOP, DBMS, Performance Modelling |
| `Concept` | `canonical_key` (UNIQUE), `name`, `aliases[]`, `level` (1–3), `definition?`, `source_count`, `created_at` | atom of the system; dedup via `canonical_key` |
| `Document` | `content_hash` (UNIQUE), `title`, `kind` ∈ {slides, notes, past_paper}, `subject`, `uploaded_by`, `uploaded_at` | re-upload dedup |
| `Section` | `doc_id`, `number`, `title`, `text_hash`, `chunk_id` | provenance anchor; `chunk_id` links ChromaDB |
| `PersonalNote` | `owner`, `text` | per-user overlay (forking model, ADR-0001) |
| `Question` *(reserved, ADR-0003)* | `id`, `text`, `kind` | M03 extends with IRT params |

## 2. Relationship types

| Type | Meaning | Properties |
|---|---|---|
| `(Concept)-[:PART_OF]->(Concept)` | concept hierarchy (from heading numbering) | `via` = "structural" |
| `(Concept)-[:BELONGS_TO]->(Subject)` | subject membership | — |
| `(Concept)-[:PREREQUISITE_OF]->(Concept)` | **the topology** | `confidence`, `method`, `evidence` |
| `(Section)-[:MENTIONS]->(Concept)` | occurrence w/ frequency | `count` |
| `(Document)-[:HAS_SECTION]->(Section)` | document structure | — |
| `(PersonalNote)-[:ATTACHED_TO]->(Concept)` | private overlay | — |

## 3. Constraints & indexes (dedup backbone)

```cypher
CREATE CONSTRAINT concept_key_unique  IF NOT EXISTS FOR (c:Concept)  REQUIRE c.canonical_key IS UNIQUE;
CREATE CONSTRAINT subject_name_unique IF NOT EXISTS FOR (s:Subject)  REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT doc_hash_unique     IF NOT EXISTS FOR (d:Document) REQUIRE d.content_hash IS UNIQUE;
CREATE INDEX concept_aliases_idx IF NOT EXISTS FOR (c:Concept) ON (c.aliases);
CREATE INDEX section_doc_idx     IF NOT EXISTS FOR (s:Section) ON (s.doc_id);
```

All writes use `MERGE` ⇒ idempotent ingestion; cross-document concept recurrence increments
`source_count` instead of duplicating nodes.

## 4. Integrity rules (enforced in code before write — S1)

1. **DAG**: reject any `PREREQUISITE_OF` edge creating a cycle.
2. **Confidence gate**: ≥0.75 auto-commit · 0.40–0.75 review queue · <0.40 dropped+logged.
3. **Orphan report**: concepts with no hierarchy parent and no mentions are flagged, not silently kept.

## 5. Canonicalisation contract (feeds `canonical_key`)

lowercase → lemmatise → singularise → synonym/acronym map (`synonyms.yaml`) → slug.
All mappings reviewable in PRs. Glossary (`glossary.yaml`) seeds the spaCy `EntityRuler`.

## 6. Open questions for sign-off

- Hierarchy depth cap (currently 3 levels) — enough for SL syllabi?
- Should `MENTIONS.count` be normalised per document length?
- Past-paper questions: ingest deterministically now, or wait for M03's IRT schema?
