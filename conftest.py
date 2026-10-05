"""Make `src/` importable without installation (CI installs properly via pip)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
