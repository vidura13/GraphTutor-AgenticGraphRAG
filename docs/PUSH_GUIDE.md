# One-time GitHub bootstrap (for Member 01)

Run from the folder containing this scaffold, on **your** machine.
Git newcomers: read `docs/GIT_CRASH_COURSE.md` first (10 min) — it explains every command below.

## 0. One-time auth setup (HTTPS)

GitHub rejects account passwords for git. Either let Git Credential Manager open a browser
sign-in, or use a fine-grained PAT (Settings → Developer settings → Tokens → Contents: R/W on
this repo) as the "password". If you see `Invalid username or token`, Windows is replaying a
stale saved credential — clear it first:

```bash
cmdkey /delete:git:https://github.com
```

## 1. Push the initial commit

```bash
git init -b main
git add -A
git commit -m "chore(ops): S0 initial scaffold — docs, ontology v0, CI, templates"

git remote add origin https://github.com/<USERNAME>/<REPO>.git   # your existing private repo
git fetch origin                                                 # triggers the login; proves auth works

# Repo created with GitHub's placeholder README/.gitignore? Those commits contain no human
# work and nobody else has cloned: republish safely (see GIT_CRASH_COURSE §6).
git push -u origin main --force-with-lease

git switch -c develop
git push -u origin develop
git switch main
```

## 2. Branch protection (Settings → Branches → "Add branch rule", or via CLI)

Rules for **both** `main` and `develop`:
- Require a pull request before merging, **1 approval**, dismiss stale reviews.
- Require status checks to pass: `unit` (and `integration` on push workflows).
- No force pushes, no deletions. Include administrators.

CLI equivalent (run once per branch, replace OWNER/REPO):

```bash
gh api repos/<OWNER>/<REPO>/branches/main/protection -X PUT --input scripts/protection.json
gh api repos/<OWNER>/<REPO>/branches/develop/protection -X PUT --input scripts/protection.json
```

## 3. Labels & issue backlog

```bash
python scripts/create_issues.py --repo <OWNER>/<REPO>          # creates labels + all S0/US issues
python scripts/create_issues.py --repo <OWNER>/<REPO> --dry-run   # preview first
```

## 4. Invite the team

Settings → Collaborators → add Members 02–05 with **Write** access.
Share `docs/TEAM_WORKFLOW.md` (onboarding checklist) in the group chat.

## 5. Create the Projects board

New project (table view) with columns `Backlog · In sprint · Review · Done`,
link the repo, and add all issues. Set milestone `S0-bootstrap`.
