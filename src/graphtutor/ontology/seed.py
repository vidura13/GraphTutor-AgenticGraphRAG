"""OOP mini-graph seed: the team's shared dev fixture (and M05's smallest sim input).

Usage:  python -m graphtutor.ontology.seed
Every write goes through MERGE + the DAG gate (dogfooding dag.assert_acyclic).
"""
from ..graph.dag import assert_acyclic
from ..graph.db import get_driver

SUBJECT = "Object-Oriented Programming"

# (canonical_key, name, level)
CONCEPTS: list[tuple[str, str, int]] = [
    ("oop-foundations", "OOP Foundations", 1),
    ("oop-advanced", "Advanced OOP", 2),
    ("class", "Class", 1),
    ("object", "Object", 1),
    ("constructor", "Constructor", 1),
    ("encapsulation", "Encapsulation", 1),
    ("access-modifier", "Access Modifier", 1),
    ("abstraction", "Abstraction", 1),
    ("inheritance", "Inheritance", 1),
    ("polymorphism", "Polymorphism", 2),
    ("method-overloading", "Method Overloading", 2),
    ("method-overriding", "Method Overriding", 2),
    ("abstract-class", "Abstract Class", 2),
    ("interface", "Interface", 2),
    ("composition", "Composition", 2),
    ("exception-handling", "Exception Handling", 2),
    ("uml-class-diagram", "UML Class Diagram", 2),
    ("solid-principles", "SOLID Principles", 3),
]

# (from_key, to_key): from is a prerequisite of to
PREREQS: list[tuple[str, str]] = [
    ("class", "object"),
    ("class", "constructor"),
    ("class", "encapsulation"),
    ("access-modifier", "encapsulation"),
    ("class", "inheritance"),
    ("inheritance", "polymorphism"),
    ("inheritance", "method-overriding"),
    ("method-overloading", "polymorphism"),
    ("abstraction", "abstract-class"),
    ("abstraction", "interface"),
    ("inheritance", "abstract-class"),
    ("class", "composition"),
    ("class", "uml-class-diagram"),
    ("polymorphism", "solid-principles"),
    ("abstraction", "solid-principles"),
    ("class", "exception-handling"),
]

# (child_key, parent_key): hierarchy topics
PART_OF: list[tuple[str, str]] = [
    ("class", "oop-foundations"),
    ("object", "oop-foundations"),
    ("encapsulation", "oop-foundations"),
    ("abstraction", "oop-foundations"),
    ("polymorphism", "oop-advanced"),
    ("inheritance", "oop-advanced"),
    ("solid-principles", "oop-advanced"),
]

SEED_CONCEPT_KEYS = [k for k, _, _ in CONCEPTS]

MERGE_CONCEPT = """
MERGE (c:Concept {canonical_key: $key})
ON CREATE SET c.name = $name, c.level = $level, c.seed = true, c.source_count = 1
"""
MERGE_SUBJECT = """
MERGE (s:Subject {name: $name})
ON CREATE SET s.seed = true
"""
# MERGE the endpoints too: avoids the disconnected-pattern (cartesian) warning and
# stays idempotent; endpoints already exist with full properties at this point.
MERGE_PREREQ = """
MERGE (a:Concept {canonical_key: $from})
MERGE (b:Concept {canonical_key: $to})
MERGE (a)-[r:PREREQUISITE_OF]->(b)
ON CREATE SET r.confidence = 1.0, r.method = 'seed', r.evidence = 'docs/ontology.md seed graph'
"""
MERGE_PART_OF = """
MERGE (a:Concept {canonical_key: $child})
MERGE (b:Concept {canonical_key: $parent})
MERGE (a)-[:PART_OF]->(b)
"""
MERGE_BELONGS = """
MERGE (c:Concept {canonical_key: $key})
MERGE (s:Subject {name: $subject})
MERGE (c)-[:BELONGS_TO]->(s)
"""


def load_seed(driver=None) -> dict:
    """Idempotently load subject + concepts + edges; returns counts."""
    driver = driver or get_driver()
    with driver.session() as session:
        session.run(MERGE_SUBJECT, {"name": SUBJECT})
        for key, name, level in CONCEPTS:
            session.run(MERGE_CONCEPT, {"key": key, "name": name, "level": level})
            session.run(MERGE_BELONGS, {"key": key, "subject": SUBJECT})
        for frm, to in PREREQS:
            assert_acyclic(session, frm, to)
            session.run(MERGE_PREREQ, {"from": frm, "to": to})
        for child, parent in PART_OF:
            session.run(MERGE_PART_OF, {"child": child, "parent": parent})
    return {
        "concepts": len(CONCEPTS),
        "prereqs": len(PREREQS),
        "part_of": len(PART_OF),
    }


def clear_seed(driver=None) -> None:
    """Delete seed nodes/edges only (safe cleanup for tests)."""
    driver = driver or get_driver()
    with driver.session() as session:
        session.run(
            "MATCH (c:Concept {seed: true}) DETACH DELETE c"
        )
        session.run("MATCH (s:Subject {seed: true}) DETACH DELETE s")


if __name__ == "__main__":
    counts = load_seed()
    print(f"seeded {SUBJECT}: {counts}")
