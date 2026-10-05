// GraphTutor ontology v0 — constraints & indexes (Neo4j 5.x)
// Apply with: cypher-shell -a bolt://localhost:7687 -u neo4j -p graphtutor_dev -f schema.cypher
// Keep in sync with docs/ontology.md.

CREATE CONSTRAINT concept_key_unique  IF NOT EXISTS FOR (c:Concept)  REQUIRE c.canonical_key IS UNIQUE;
CREATE CONSTRAINT subject_name_unique IF NOT EXISTS FOR (s:Subject)  REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT doc_hash_unique     IF NOT EXISTS FOR (d:Document) REQUIRE d.content_hash IS UNIQUE;

CREATE INDEX concept_aliases_idx IF NOT EXISTS FOR (c:Concept) ON (c.aliases);
CREATE INDEX section_doc_idx     IF NOT EXISTS FOR (s:Section) ON (s.doc_id);
