"""Apply ontology constraints/indexes from ontology/schema.cypher.

Usage:  python -m graphtutor.graph.schema
Idempotent: every statement uses IF NOT EXISTS.
"""
from pathlib import Path

from .db import get_driver

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "ontology" / "schema.cypher"


def apply_schema(driver=None) -> int:
    """Run every schema statement; returns the number applied."""
    driver = driver or get_driver()
    # strip comment lines FIRST, then split statements (comments may sit above a statement)
    text = "\n".join(
        ln for ln in SCHEMA_PATH.read_text().splitlines()
        if not ln.strip().startswith("//")
    )
    statements = [s.strip() for s in text.split(";") if s.strip()]
    with driver.session() as session:
        for stmt in statements:
            session.run(stmt)
    return len(statements)


if __name__ == "__main__":
    n = apply_schema()
    print(f"applied {n} schema statements from {SCHEMA_PATH.name}")
