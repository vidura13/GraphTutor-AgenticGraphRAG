"""Deterministic AKGC pipeline (implemented S2–S5; design in docs/architecture.md §data flow).

Planned modules (stubs only at S0):
    extract.py       PDF -> text+layout (PyMuPDF/pdfplumber); reject image-only scans
    segment.py       heading/numbering/font heuristics -> Section tree
    concepts.py      spaCy noun chunks + glossary EntityRuler + acronym tables
    canonicalize.py  synonyms.yaml-driven canonical_key production
    prereq.py        weighted cue mining + DAG gate + review queue
    load.py          Neo4j MERGE batches + ChromaDB chunk upserts
    cli.py           `graphtutor-ingest` entry point (also used by M05 simulation)
"""
