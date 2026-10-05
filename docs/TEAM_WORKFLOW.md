# Team Workflow — GitHub + Agile (fast-track)

## Branching model

| Branch | Purpose | Protection |
|---|---|---|
| `main` | always releasable; tagged releases | PR + ≥1 review + CI green; no force push/delete |
| `develop` | integration | same as main |
| `feature/<area>-<slug>` | e.g. `feature/kg-neo4j-schema` | cut from `develop`, PR back to `develop` |

Area prefixes: `kg-` (M01) `be-` (M02) `ai-` (M03) `fe-` (M04) `qa-` (M05) `ops-`.
**No direct pushes to `develop`/`main`** — enforced by branch protection, not politeness.

## Commits & PRs

- Conventional commits: `feat(kg): …`, `fix(nlp): …`, `docs(srs): …`, `chore(ops): …`.
- PR template is mandatory; every PR links an issue (`Closes #n`) and states how it was tested.
- Review rule: a *different* member approves (cross-area reviews catch contract breaks early).

## Requirements & sprints

- Requirements live in `docs/SRS.md`; the issue backlog is created once via `scripts/create_issues.py`.
- Board: GitHub Projects (zero extra tooling). Trello only if the team votes for it.
- **Fast-track cadence: 3–4 day sprints** (compressed Gantt). Sprint end = runnable demo +
  retro note committed to `docs/retros/`.
- Milestones = S0..S6 from `planning/member01_workflow.md`.

## CI

- Every PR: `ruff check` + `pytest tests/unit`.
- Push to `develop`/`main`: + integration job with `neo4j:5` service container.

## Onboarding checklist (each member, ~30 min)

1. Accept GitHub invite (Write access).
2. `git clone` + `docker compose up -d` + venv + `pip install -e ".[dev]"` +
   `python -m spacy download en_core_web_md` + `pytest tests/unit -q` (green).
3. Add yourself to `CONTRIBUTORS.md` on a `feature/ops-onboarding-<you>` branch → first PR.
   (This proves the whole loop: branch → CI → review → merge.)
4. Subscribe to repo notifications; pick up your P0 issues.

## Meetings

- Kickoff: sign SRS v0 + ontology v0 + ADR-0001 (forking) — see issue backlog.
- Per sprint: 15-min planning + demo/retro. Notes in `docs/retros/`.
