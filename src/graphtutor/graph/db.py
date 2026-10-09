"""Env-driven Neo4j driver helper."""
import os
from functools import lru_cache

from dotenv import load_dotenv
from neo4j import GraphDatabase


@lru_cache(maxsize=1)
def get_driver():
    """Singleton driver from .env / environment (see .env.example)."""
    load_dotenv()
    return GraphDatabase.driver(
        os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        auth=(
            os.environ.get("NEO4J_USER", "neo4j"),
            os.environ.get("NEO4J_PASSWORD", "graphtutor_dev"),
        ),
    )
