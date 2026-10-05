"""S0 sanity checks: design artifacts exist, parse, and satisfy the ontology contract."""
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[2]
ONTO = ROOT / "src" / "graphtutor" / "ontology"


def test_glossary_parses_and_keys_are_unique():
    data = yaml.safe_load((ONTO / "glossary.yaml").read_text())
    assert data["version"] == 0
    keys = [c["key"] for s in data["subjects"] for c in s["concepts"]]
    assert len(keys) == len(set(keys)), "duplicate canonical keys in glossary"
    assert len(keys) >= 40, "glossary seed too small"


def test_synonyms_parse():
    data = yaml.safe_load((ONTO / "synonyms.yaml").read_text())
    assert "acronyms" in data and "synonyms" in data


def test_schema_has_required_constraints():
    schema = (ONTO / "schema.cypher").read_text()
    for token in ("concept_key_unique", "subject_name_unique", "doc_hash_unique"):
        assert token in schema


def test_package_imports():
    import graphtutor

    assert graphtutor.__version__ == "0.1.0"
