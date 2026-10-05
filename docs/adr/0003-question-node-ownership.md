# ADR-0003: Question nodes — schema reserved, population owned by M03

- **Status**: PROPOSED (sign-off: M01+M03)
- **Context**: CAT needs an item bank with IRT params; past papers *could* be mined
  deterministically, but parameter estimation is M03's statistical territory.
- **Decision**: ontology reserves `(:Question {id, text, kind})` + `(:Question)-[:TESTS]->(:Concept)`;
  M03 extends with IRT params (`a`, `b`, `c`) and generation logic. M01 does **not** build question
  ingestion in MVP unless the team re-prioritises.
- **Consequences**: keeps M01's MVP scope on concepts/topology; item-bank bootstrap is an M03+S3 task.
