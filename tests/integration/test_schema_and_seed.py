"""S1 integration: schema applies, seed loads, cycle gate holds against live Neo4j.

Skips when no Neo4j is reachable locally; runs in CI via the neo4j service container.
"""
import pytest

pytest.importorskip("neo4j")

from graphtutor.graph.dag import CycleError, assert_acyclic
from graphtutor.graph.db import get_driver
from graphtutor.graph.schema import apply_schema
from graphtutor.ontology.seed import (
    PREREQS,
    SEED_CONCEPT_KEYS,
    SUBJECT,
    clear_seed,
    load_seed,
)


@pytest.fixture(scope="module")
def driver():
    d = get_driver()
    try:
        d.verify_connectivity()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Neo4j not reachable: {exc}")
    yield d
    d.close()


@pytest.fixture(autouse=True)
def clean(driver):
    clear_seed(driver)
    yield
    clear_seed(driver)


def test_schema_applies_idempotently(driver):
    assert apply_schema(driver) >= 5
    assert apply_schema(driver) >= 5  # second run must not fail
    with driver.session() as s:
        names = {r["name"] for r in s.run("SHOW CONSTRAINTS").data()}
    assert {"concept_key_unique", "subject_name_unique", "doc_hash_unique"} <= names


def test_seed_loads_and_counts_match(driver):
    counts = load_seed(driver)
    assert counts == {"concepts": 18, "prereqs": 16, "part_of": 7}
    with driver.session() as s:
        n = s.run(
            "MATCH (c:Concept {seed: true})-[:BELONGS_TO]->(s:Subject {name: $sub}) "
            "RETURN count(c) AS n",
            {"sub": SUBJECT},
        ).single()["n"]
    assert n == len(SEED_CONCEPT_KEYS)


def test_seed_is_idempotent(driver):
    load_seed(driver)
    load_seed(driver)
    with driver.session() as s:
        n = s.run("MATCH (c:Concept {seed: true}) RETURN count(c) AS n").single()["n"]
    assert n == len(SEED_CONCEPT_KEYS)  # MERGE, never duplicate


def test_cycle_gate_rejects_on_live_graph(driver):
    load_seed(driver)
    with driver.session() as s:
        # object -> class would close the seeded class -> object edge
        with pytest.raises(CycleError):
            assert_acyclic(s, "object", "class")
        # a genuinely new edge passes
        assert_acyclic(s, "exception-handling", "solid-principles")


def test_prereq_edges_present(driver):
    load_seed(driver)
    with driver.session() as s:
        n = s.run(
            "MATCH (:Concept {seed: true})-[r:PREREQUISITE_OF]->(:Concept {seed: true}) "
            "RETURN count(r) AS n"
        ).single()["n"]
    assert n == len(PREREQS)
