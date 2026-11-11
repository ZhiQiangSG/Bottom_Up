# Plans Index

> Read this first. Locate the domain or feature you need, load only that file, then follow its `requires_specs` frontmatter transitively. Do not load all specs eagerly.

Paths below are relative to `docs/`.

## Domains

| Domain | Contract | What it covers |
| --- | --- | --- |
| identity-access | domains/identity-access/domain.md | Roles, password policy, sessions, and email verification for all three roles. |
| discovery | domains/discovery/domain.md | Job search, filters, sorting, and shareable result URLs. |
| applications | domains/applications/domain.md | External-apply redirect with outbound tracking and dashboard status. |
| postings | domains/postings/domain.md | Job lifecycle, drafts, approval queue, and company verification. |
| assistant | domains/assistant/domain.md | Per-user AI agent: conversations, allowlisted tools, confirmation flow, memory, and budgets. |
| notifications | domains/notifications/domain.md | Saved-search watches, scheduled evaluation, digests, and delivery state. |

## Features

| File | Description |
| --- | --- |
| domains/identity-access/register.md | Role-aware registration with conditional fields, policy checkboxes, and email verification. |
| domains/identity-access/login.md | Email/password plus Google OAuth login with role-based dashboard redirect. |
| domains/identity-access/logout.md | Confirmed logout that invalidates the server session and clears local tokens. |
| domains/discovery/search-filter-jobs.md | Filtered and sorted job discovery with shareable URLs and an empty state. |
| domains/applications/apply-job.md | External “Apply Now” redirect that stays open with a tracking overlay modal. |
| domains/postings/post-job.md | Multi-step job posting with draft/publish flow and optional school approval. |
| domains/assistant/assistant-chat.md | Private conversation shell with turn audit, budget enforcement, and manual fallback. |
| domains/assistant/assistant-search.md | Natural-language job search resolved into discovery filters with shareable results. |
| domains/assistant/assistant-watch.md | Assistant proposes a saved search; user confirmation creates it exactly once. |
| domains/assistant/assistant-eval.md | Offline evaluation, feedback, usage observability, and the kill switch. |
| domains/notifications/watch-alerts.md | Scheduled watch evaluation with deduplicated, active-only digests. |

## Lazy-loading workflow

1. Start here to find the domain or feature file.
2. Read that single file.
3. Follow only the `requires_specs` paths listed in its frontmatter.

## Spec validator (Definition of Ready)

New `domains/<domain>/domain.md` files must copy `domains/TEMPLATE_DOMAIN.md`:

- Sections: Ubiquitous language, Entities & aggregates, State machine,
  Invariants (`INV-NN`), Authorization matrix, Domain events & side effects,
  Error contract, Open decisions. Keep `##` headings stable once feature specs (`<feature>.md`)
  files anchor to them.
- Mark proposed models/fields/endpoints with `(proposed)` until migrated/routed.

New feature specs (`domains/<domain>/<feature>.md`, never `domain.md`) must copy
`domains/TEMPLATE.md`:

- Frontmatter: `domain`, `requires_specs[]` (paths relative to `docs/`, always include `ARCHITECTURE.md` plus the domain contract anchor, e.g. `domains/discovery/domain.md#search-contract`).
- Sections: Goal, Non-goals, Actors, Preconditions, Postconditions, Gherkin `Feature:` with `Given/When/Then` scenarios, Acceptance criteria (checkboxes, API/UI-observable), Open Questions.
- Reject if: no Gherkin block, no acceptance checkboxes, `requires_specs` missing `ARCHITECTURE.md`, or anchor does not match a `##` heading slug in the target `domain.md`.
