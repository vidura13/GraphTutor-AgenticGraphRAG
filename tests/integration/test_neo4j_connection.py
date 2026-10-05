"""Skips gracefully when Neo4j is not running locally; runs in CI (service container)."""
import os

import pytest

pytest.importorskip("neo4j")

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "graphtutor_dev")


def _reachable() -> bool:
    from neo4j import GraphDatabase

    try:
        with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)) as d:
            d.verify_connectivity(timeout=3)
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _reachable(), reason="Neo4j not running locally")
def test_connectivity():
    assert _reachable()
