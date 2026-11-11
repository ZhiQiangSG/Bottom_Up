---
name: domain-contract
description: Write or rewrite a Full DDD domain.md contract (ubiquitous language, entities, state machine, invariants, authz matrix, events, error contract) per TEMPLATE_DOMAIN.md. Use when creating a new domain contract or refreshing an existing one.
---

# Domain Contract (Writing: Full DDD + Anchor Stability)

Write one new or rewrite one existing domain contract as an executable Full DDD
spec. Requires `domain=<name>` and `mode=new|rewrite` before starting.

Source of truth: `docs/domains/TEMPLATE_DOMAIN.md` (section structure),
`docs/INDEX.md` (lazy-load rule + validator), `docs/ARCHITECTURE.md`
(technical truth — link it, do not duplicate it).

## When to use

Use when the user invokes `/domain-contract` (runs in the `domain-architect`
subagent). Load via `skill({ name: "domain-contract" })`, then follow this
workflow.

## Prerequisites (check FIRST)

- `domain=<name>` present in `$ARGUMENTS`, plus `mode=new|rewrite`. If either
  is missing, stop and ask — do not guess the domain.
- `mode=new`: confirm `docs/domains/<domain>/` does not already exist (or ask
  whether to overwrite). `mode=rewrite`: confirm the target `domain.md` exists.
- If `--dry-run` appears in the request, make ZERO `write`/`edit` calls.
  Output the full draft in fenced blocks instead.

## Workflow

### 1. Discover (read-only)

- Read `docs/INDEX.md` first to locate the domain.
- `mode=rewrite`: read ONLY `docs/domains/<domain>/domain.md`, then all
  feature specs (`<feature>.md`, excluding `domain.md`) in that domain, then follow ONLY their `requires_specs`
  frontmatter transitively (sibling domains, `ARCHITECTURE.md`). Do not load
  all domains eagerly.
- `mode=new`: read `docs/domains/TEMPLATE_DOMAIN.md`, `docs/INDEX.md`, and
  `docs/ARCHITECTURE.md` §12 (open decisions). Skim at most the sibling
  domain contracts the new domain will reference — never the full tree.
- Inspect on disk, do not assume: read `LOCAL_APPS` in `config/settings/base.py`,
  then `glob bottom_up/*/models.py` but read only `bottom_up/<domain>/models.py`
  + `bottom_up/users/models.py` (`USERNAME_FIELD=email`,
  `username/first_name/last_name=None`) + `router.register()` entries in
  `config/api_router.py`.

### 2. Anchor audit (mode=rewrite, before touching the file)

List every `##` heading in the existing `domain.md` that is referenced by any
`requires_specs` anchor (e.g. `#search-contract`, `#job-lifecycle`), including
anchors from OTHER domains' feature specs (`<feature>.md`). These headings must survive the
rewrite byte-for-byte in slug form. New sections are additive only — never
rename or delete an anchored heading.

### 3. Draft the 8 Full DDD sections

Copy `docs/domains/TEMPLATE_DOMAIN.md` and fill in, in this order:

1. `## Ubiquitous language` — glossary table. Every status/state word used in
   a Gherkin `Then` step must appear here or in `## State machine`.
2. `## Entities & aggregates` — entity, key fields with types, relations.
   Mark proposed models/fields with `(proposed)` until the migration is
   committed. FK to `settings.AUTH_USER_MODEL`; never import `User` directly.
   New apps live under `bottom_up/<app>/` + `LOCAL_APPS` + `router.register()`
   (see `ARCHITECTURE.md` §3, §5, §6).
3. `## State machine` — states table + allowed transitions, using the
   canonical enum values consumed by API responses and dashboard UI. If the
   domain is stateless, write "No lifecycle — stateless." instead of a table.
4. `## Invariants` — numbered `INV-01`, … rules, each API/UI-observable and
   each mapped to at least one Gherkin `Then` in a feature spec (`<feature>.md`).
5. `## Authorization matrix` — role × action → allow/deny. Roles are Student,
   Employer, School Admin unless the domain narrows them. Permission shape
   follows `ARCHITECTURE.md` §5 (`IsAuthenticated`, scoped querysets).
6. `## Domain events & side effects` — event name, JSON-serializable payload,
   producer, consumer. Celery args must be JSON-serializable
   (see `ARCHITECTURE.md` §7). Emails via Mailpit locally (`:8025`).
7. `## Error contract` — condition → HTTP status or UI message, no partial
   state change. Every row maps to a Gherkin error scenario. Never leak
   existence details on auth failures (generic messages).
8. `## Open decisions` — unresolved choices linked to
   `docs/decisions/NN<feature>.md` once decided (create the directory if absent).

Preserve any domain-specific `##` sections the existing file already has
(e.g. `## Search Contract`, `## Job Lifecycle`) with their meaning intact —
extend them with concrete rules underneath rather than replacing them.

### 4. Verify

- Re-run the anchor audit: every pre-existing anchor resolves to a `##` slug.
  Suggested check: extract `##` headings, slugify
  (lowercase, strip non-`[a-z0-9 -]`, spaces → `-`), and compare against every
  `domain.md#<anchor>` in all feature-spec `requires_specs`.
- Confirm `docs/INDEX.md` validator compliance: template sections present,
  `(proposed)` marking on unmigrated models/endpoints, `##` headings stable.
- Hygiene: final newline, no trailing whitespace. (`pre-commit` cannot run
  without a git repo — if `git status` fails, note it and rely on the manual
  check above.)

### 5. Report

Summarize: file written, sections added/changed, anchors preserved (count),
open decisions recorded, and verification performed. Do NOT commit, push, or
open a PR unless explicitly asked.

## Flags ($ARGUMENTS)

- `domain=<name>` — required, single-domain scope (e.g. `domain=postings`).
- `mode=new|rewrite` — required; `new` scaffolds from the template,
  `rewrite` refreshes while preserving anchors.
- `--dry-run` — print the full draft in fenced blocks, make zero
  `write`/`edit` calls.

## Boundaries

- NEVER invent endpoints, env vars, ports, or versions — read them.
- NEVER commit secrets (`.env`, `.envs/.production/`, credentials in `.envs/.local/`).
- NEVER run destructive commands (`just prune`, `down -v`, `rm -rf`, `push`)
  unless explicitly asked.
- NEVER break `docs/INDEX.md` links, `domain.md` anchors, or spec `requires_specs` links.
- `docs/VISION.md` is proposal-only — never rewrite it directly.
