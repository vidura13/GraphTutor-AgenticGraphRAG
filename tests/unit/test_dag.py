"""DAG gate: pure-logic cycle rejection (no DB needed)."""
from graphtutor.graph.dag import would_create_cycle

EDGES = [("class", "object"), ("class", "inheritance"), ("inheritance", "polymorphism")]


def test_fresh_edge_ok():
    assert not would_create_cycle(EDGES, ("polymorphism", "solid"))


def test_self_loop_rejected():
    assert would_create_cycle(EDGES, ("class", "class"))


def test_reverse_edge_rejected():
    # object -> class would close the loop class -> object -> class
    assert would_create_cycle(EDGES, ("object", "class"))


def test_transitive_cycle_rejected():
    # polymorphism -> class closes class -> inheritance -> polymorphism -> class
    assert would_create_cycle(EDGES, ("polymorphism", "class"))


def test_unrelated_edge_ok():
    assert not would_create_cycle(EDGES, ("abstraction", "interface"))
