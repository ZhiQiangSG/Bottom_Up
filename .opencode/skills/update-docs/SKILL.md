---
name: update-docs
description: Audit codebase and sync README.md, AGENTS.md, docs/ARCHITECTURE.md, docs/INDEX.md, and docs/domains/** after major changes
---

# Update Docs

Audit the live repo state and sync user-facing + agent-facing docs to match reality. Never invent commands, versions, endpoints, or features.

Replaces the removed `update-readme` skill — README logic below is backward-compatible with it.

## When to use

Use when the user invokes `/update-docs` or asks to refresh docs after a major modification. Load via `skill({ name: "update-docs" })`, then follow this workflow.

Major modification means any of: new app under `bottom_up/`, model/API change, dependency or version bump, port/env change, command/CI/workflow change, new spec in `docs/domains/`.

## Workflow

### 1. Discover (read-only)

Inspect on disk — do not assume:

- Structure: `bottom_up/` apps, `config/settings/`, `config/urls.py`, `config/api_router.py`, `config/celery_app.py`, `manage.py`, `bottom_up/templates/`, `bottom_up/static/`
- Manifests: `pyproject.toml` (`[project]` name/version/description/dependencies, `[dependency-groups]` dev), `uv.lock`, `.python-version` (Python 3.14), `justfile`, `docker-compose.local.yml`, `.envs/.local/.postgres`
- Config: `config/settings/base.py` vs `local/test/production.py`, API prefix in `config/api_router.py`, `api/schema/` + `api/docs/` if present
- Tooling: `.opencode/commands/*.md`, `.opencode/agents/*.md`, `.opencode/skills/*/SKILL.md`, `.opencode/README.md` (canonical index), `opencode.json`, `.github/workflows/*`, `.pre-commit-config.yaml`
- Core targets (always read before writing): `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/INDEX.md`
- Conditional targets (read only if relevant change detected): `docs/domains/**` (domain contract or a feature spec (`<feature>.md`) added/renamed/removed), `CONTRIBUTING.md` + `.opencode/README.md` (tooling change: any `commands/|agents/|skills/` add/remove/rename, `opencode.json` perm change, pre-commit/CI change), `docs/VISION.md` (proposal-only, never auto-rewrite)
- Trigger rule: treat untracked `?? .opencode/**` in `git status --short` as a tooling-change trigger, never ignorable.
- History: `git log -n 20 --oneline` + `git status --short` + `git diff --stat main...HEAD`. If not a git repo, skip and note "history unavailable".

Preserve pass (always run before writing):

- Read every target file you intend to touch first via the `read` tool.
- Extract and carry over custom content: badges, logos (`<img>`/![logo]), mermaid/architecture diagrams, hand-written notes, ADRs, manual warnings — unless directly contradicted by live code truth.
- Never drop these silently. List kept items in your final summary.

Scoped update (`target=`, `focus=`, `path=`):

- `target=` selects files: `readme|agents|arch|docs|tooling|all` (default `all`). `target=docs` without `path=` covers `docs/*.md` + `docs/domains/**`; with `path=docs/<file>.md` covers that file only. `target=tooling` covers `.opencode/README.md` + `CONTRIBUTING.md` tooling table only.
- `focus=<section>` rewrites ONLY that section within the selected target(s). Preserve all other sections byte-for-byte from the version you just read.
- If the target section is missing, insert it in the template position without touching neighbors.
- Valid `focus` for `readme`: `title`, `stack`, `prerequisites`, `quickstart`, `config`, `commands`, `api`, `features`, `deployment`.
- Valid `focus` for `agents`: `layout`, `commands`, `env`, `conventions`, `workflow`.
- Valid `focus` for `arch`: `overview`, `stack`, `repomap`, `env`, `auth`, `data`, `celery`, `quality`, `workflow`, `recipes`, `pitfalls`, `status`.
- `path=` must stay inside `docs/`, or equal `.opencode/README.md` or `CONTRIBUTING.md`. Reject anything else.

### 2. Synthesize

- Prerequisites: Python from `.python-version`, `uv`, Docker + `just`, Postgres + Redis for native runs (`POSTGRES_HOST/PORT/DB/USER/PASSWORD`, `REDIS_URL=redis://localhost:6379/0`, `USE_DOCKER=no`, `DJANGO_SETTINGS_MODULE=config.settings.local`)
- Setup truth: `uv sync --group dev`, `docker compose -f docker-compose.local.yml up -d postgres redis mailpit`, `just build && just up`, `just manage migrate`, `uv run pytest` / `just pytest`
- Stack: Django 6, DRF + drf-spectacular, Celery + beat, Redis, Postgres (psycopg), uv, Docker, Mailpit `:8025`, Flower `:5555` — pin exact versions from `pyproject.toml`/`uv.lock` only
- Features/status: only what exists on disk + recent commits. Mark gaps as `> Status: not yet implemented`.
- ARCHITECTURE truth (§§1-12 in `docs/ARCHITECTURE.md`): system diagram + routing from `config/urls.py`, pinned stack, repo map + `LOCAL_APPS` + `router.register()`, env matrix (container vs native), auth/API conventions (`USERNAME_FIELD=email`, `IsAuthenticated` default, spectacular `IsAdminUser`, self-scoped ViewSets), migration rule (`makemigrations` + commit, CI `--check`), Celery (`config/celery_app.py`, tasks in `<app>/tasks.py`), quality-gate order `lint → typecheck → test`, agentic rules (`opencode.json` perms, specs `requires_specs`, lazy-load via `docs/INDEX.md`), recipes A/B/C, pitfalls, §12 status. Link to specs — never duplicate this file into specs.
- Spec truth: `docs/INDEX.md` domain + feature tables, `docs/domains/<domain>/domain.md` contracts (stable `##` headings that specs anchor to), `<feature>.md` specs with `requires_specs` frontmatter relative to `docs/`, and `docs/domains/TEMPLATE*.md` as the shape to copy. Keep tables, anchors, and `requires_specs` links in sync — never rename an anchored heading without updating consumers.
- Tooling truth: enumerate `.opencode/commands/*.md` × `.opencode/agents/*.md` × `.opencode/skills/*/SKILL.md`; all three must reconcile against `.opencode/README.md` Commands + Agents tables and the `CONTRIBUTING.md` agentic-tooling table (row counts plus runner/skill columns).

### 3. Rewrite (or propose)

Strict dry-run gate (check FIRST):

- If `--dry-run` is present in `$ARGUMENTS`: DO NOT call `write`, `edit`, or `apply_patch` under any circumstance.
- Output one ```markdown fenced block per touched file with `path:` header, followed by a bullet changelog.
- End response there. No file writes, no commits.

Full rewrite (no `focus=`, no `path=`, no `--dry-run`, `target=all` or omitted):

- `README.md` — write complete file using this structure:

```markdown
# <name from pyproject.toml>
<concise description> + badges + License
## Tech Stack & Architecture
## Prerequisites
## Quickstart (native + Docker)
## Configuration / Env
## Basic Commands (users, test, lint, typecheck, celery)
## API / Usage Examples
## Key Features & Current Status
## Deployment
## Contributing / License
```

- `AGENTS.md` — concise ops reference only (<~60 lines): Layout, Commands (verify order: lint → typecheck → test), Env/services gotchas, Conventions, Workflow. Update only sections whose truth changed. Never mirror README prose.
- `docs/ARCHITECTURE.md` — update §§1-12 in place, preserving section numbers and lazy-load rule. Never rename sections without updating cross-refs in specs.
- `docs/INDEX.md` + `docs/domains/**` — keep the Domains/Features tables accurate; when a spec is added/renamed/removed update its row and every consumer's `requires_specs`; keep `##` heading slugs in `domain.md` stable (specs anchor to them). New specs copy `docs/domains/TEMPLATE.md`; new domains copy `TEMPLATE_DOMAIN.md`.
- Conditional: `CONTRIBUTING.md` + `.opencode/README.md` only when tooling changed (any `commands/|agents/|skills/` add/remove/rename, `opencode.json` perm change, pre-commit/CI change); `target=tooling` syncs `.opencode/README.md` tables + `CONTRIBUTING.md` tooling table; `docs/INDEX.md` only when a domain/spec file was added, renamed, or removed; `docs/VISION.md` proposal-only via `--dry-run`, never direct rewrite.
- Keep code blocks copy-pasteable. Prefer `uv run` / `just <cmd>` over bare `python`.
- Do NOT commit unless explicitly asked.

## Flags ($ARGUMENTS)

- `target=readme|agents|arch|docs|tooling|all` — file scope (default `all`).
- `focus=<section>` — scoped rewrite within target, preserve rest byte-for-byte (see Step 1). Valid `focus` for `tooling`: `commands`, `agents`, `flags`, `permissions`.
- `path=docs/<file>.md`, `path=docs/domains/<d>/<file>.md` — single-file scope; must stay inside allowlist above.
- `branch=<name>` — use `git log <name> -n 20 --oneline` for history.
- `--dry-run` — proposal only, zero file tool calls (see Step 3).

## Boundaries

- NEVER hallucinate endpoints, env vars, ports, or versions — read them.
- NEVER delete License/badges/diagrams/notes without replacement.
- NEVER commit secrets (`.env`, `.envs/.production/`, credentials in `.envs/.local/`).
- NEVER run destructive commands (`just prune`, `down -v`, `rm`, `push`, `commit`).
- NEVER reintroduce Sphinx or `.rst` docs unasked.
- NEVER break `docs/INDEX.md` links, `domain.md` anchors, or spec `requires_specs` links.
- NEVER leave `.opencode/README.md` Commands/Agents tables vs `commands/` + `agents/` + `skills/` on disk vs `CONTRIBUTING.md` tooling table out of sync.
- NEVER dismiss untracked `?? .opencode/**` as a non-trigger — it is a tooling change.
- NEVER auto-rewrite `docs/VISION.md` — proposal only.
- NEVER duplicate `docs/ARCHITECTURE.md` into specs or create a second root `ARCHITECTURE.md` — link to the canonical file.
