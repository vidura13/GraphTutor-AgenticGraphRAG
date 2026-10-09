"""Cycle safety for PREREQUISITE_OF — the graph's integrity law (SRS US-02 AC3).

Pure-stdlib reachability so unit tests need no database; the Cypher twin
checks the live graph right before a write.
"""

CYCLE_CHECK_CYPHER = """
MATCH (to:Concept {canonical_key: $to})
      -[:PREREQUISITE_OF*0..50]->
      (anc:Concept {canonical_key: $from})
RETURN count(anc) > 0 AS creates_cycle
"""


class CycleError(ValueError):
    """Raised when adding a PREREQUISITE_OF edge would break the DAG invariant."""


def would_create_cycle(edges: list[tuple[str, str]], new_edge: tuple[str, str]) -> bool:
    """True iff adding `new_edge` (a -> b) creates a cycle in `edges`.

    Adding a->b closes a loop exactly when b can already reach a
    (or a == b, a self-loop).
    """
    a, b = new_edge
    if a == b:
        return True
    adj: dict[str, list[str]] = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
    seen: set[str] = set()
    stack = [b]
    while stack:
        node = stack.pop()
        if node == a:
            return True
        if node in seen:
            continue
        seen.add(node)
        stack.extend(adj.get(node, []))
    return False


def assert_acyclic(session, from_key: str, to_key: str) -> None:
    """Raise CycleError if writing (from)-[:PREREQUISITE_OF]->(to) would cycle."""
    rec = session.run(CYCLE_CHECK_CYPHER, {"from": from_key, "to": to_key}).single()
    if rec and rec["creates_cycle"]:
        raise CycleError(
            f"PREREQUISITE_OF {from_key} -> {to_key} rejected: would create a cycle"
        )
