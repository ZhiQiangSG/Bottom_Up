---
description: Write or rewrite a Full DDD domain contract in the domain-architect subagent
agent: domain-architect
subtask: true
---

Load and execute the `domain-contract` skill using the `skill` tool.

Targets:
- @docs/INDEX.md
- @docs/domains/TEMPLATE_DOMAIN.md
- @docs/ARCHITECTURE.md
- @CONTRIBUTING.md
- @AGENTS.md
- @bottom_up/users/models.py # exemplar only: AUTH_USER_MODEL shape
- @config/settings/base.py # LOCAL_APPS: where new apps are discovered
- @config/api_router.py # choke point: single file, router.register() grows in place

Context overrides: $ARGUMENTS

Instructions:

1. Call `skill({ name: "domain-contract" })` and follow it exactly.
2. Parse `$ARGUMENTS` for `domain=<name>` (required) and `mode=new|rewrite` (required). If either is missing, stop and ask.
3. Lazy-load only that domain plus its `requires_specs` transitively. Never load all specs eagerly.
4. `mode=new`: scaffold `docs/domains/<domain>/domain.md` from `docs/domains/TEMPLATE_DOMAIN.md`, then update the `docs/INDEX.md` domains table.
5. `mode=rewrite`: audit existing `requires_specs` anchors first, preserve every anchored `##` heading, refresh the 8 Full DDD sections, then re-audit.
6. If `--dry-run` is present, print the full draft in fenced blocks and make zero `write`/`edit` calls.
7. Summarize file written, anchors preserved, open decisions recorded, and verification performed. Do NOT commit/push unless explicitly asked.

Usage:
- `/domain-contract domain=postings mode=rewrite`
- `/domain-contract domain=shipping mode=new`
- `/domain-contract domain=postings mode=rewrite --dry-run`
