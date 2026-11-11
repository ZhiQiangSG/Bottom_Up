---
description: Audit repo and sync README + AGENTS + ARCHITECTURE + docs via update-docs skill
agent: docs-maintainer
subtask: true
---

Load and execute the `update-docs` skill using the `skill` tool.

Targets:
- @README.md
- @AGENTS.md
- @docs/ARCHITECTURE.md
- @docs/INDEX.md
- @CONTRIBUTING.md
- @.opencode/README.md (conditional: read on tooling scope or when `.opencode/**` changed)
- @docs/domains/ (conditional: read when a domain/spec changed)

Manifests: @pyproject.toml @justfile @docker-compose.local.yml @opencode.json
Tooling: @.opencode/commands/ @.opencode/agents/ @.opencode/skills/
Router: @config/api_router.py
Context overrides: $ARGUMENTS

Instructions:

1. Call `skill({ name: "update-docs" })` and follow it exactly.
2. Parse `$ARGUMENTS` for optional flags:
   - `target=readme|agents|arch|docs|tooling|all` (default `all`) — file scope (`tooling` = `.opencode/README.md` + `CONTRIBUTING.md` tooling table).
   - `focus=<section>` (e.g. `focus=quickstart`, `focus=env`, `focus=status`, `focus=commands` with `target=tooling`) — scoped rewrite only.
   - `path=docs/<file>.md`, `path=docs/domains/<d>/<file>.md`, `path=.opencode/README.md`, or `path=CONTRIBUTING.md` — single-file scope.
   - `branch=<name>` — use that branch for history.
   - `--dry-run` — print proposals, make zero write/edit calls.
   - No args → full audit + sync of core targets (`README`, `AGENTS`, `docs/ARCHITECTURE.md`) plus `docs/INDEX.md` when specs changed.
3. Conditional targets: touch `CONTRIBUTING.md` + `.opencode/README.md` only on tooling changes (any `commands/|agents/|skills/` add/remove/rename, `opencode.json` perm change, pre-commit/CI change — including untracked `?? .opencode/**`); touch `docs/INDEX.md` only when a domain/spec file was added, renamed, or removed; `docs/VISION.md` is proposal-only, never direct rewrite.
4. Prefer `read`/`glob`/`grep` tools and `@file` refs above. Use shell injection ONLY for git (no pipes):
   Recent commits: !`git log -n 20 --oneline`
   Status: !`git status --short`
   Change stat: !`git diff --stat main...HEAD`
5. If git commands fail (no repo), continue with filesystem audit and note it.
6. After rewrite (or dry-run output), summarize what changed per file and what custom content was preserved.

Usage:
- `/update-docs`
- `/update-docs target=readme focus=api`
- `/update-docs target=arch --dry-run`
- `/update-docs target=docs path=docs/INDEX.md`
- `/update-docs target=tooling --dry-run`
- `/update-docs branch=feat/auth --dry-run`
