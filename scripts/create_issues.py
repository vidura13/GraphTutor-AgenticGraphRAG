#!/usr/bin/env python3
"""Bootstrap labels + issue backlog from scripts/issues.yaml using the GitHub CLI.

Usage:
    python scripts/create_issues.py --repo OWNER/REPO [--dry-run]
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent


def run(args: list[str], dry: bool) -> None:
    print("+", " ".join(args))
    if not dry:
        subprocess.run(args, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="OWNER/REPO")
    ap.add_argument("--dry-run", action="store_true")
    ns = ap.parse_args()

    if not ns.dry_run and shutil.which("gh") is None:
        print("error: GitHub CLI (gh) not found; install it or create issues manually.",
              file=sys.stderr)
        return 1

    data = yaml.safe_load((HERE / "issues.yaml").read_text())

    for lab in data["labels"]:
        run(["gh", "label", "create", lab["name"], "--repo", ns.repo,
             "--color", lab["color"], "--force"], ns.dry_run)

    for issue in data["issues"]:
        cmd = ["gh", "issue", "create", "--repo", ns.repo, "--title", issue["title"],
               "--body", issue["body"]]
        for lab in issue["labels"]:
            cmd += ["--label", lab]
        run(cmd, ns.dry_run)

    print(f"\nDone: {len(data['labels'])} labels, {len(data['issues'])} issues"
          + (" (dry run)" if ns.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
