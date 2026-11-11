# Assistant — Domain Contract

> How each user's AI agent helps them use Bottom Up.
> Owns conversations, the agent loop, the tool allowlist, confirmation of
> proposed actions, per-user memory, usage budgets, and turn-level audit.
> Does not own job data (`domains/postings/domain.md#job-lifecycle`), search
> semantics (`domains/discovery/domain.md#search-contract`), application
> tracking (`domains/applications/domain.md#outbound-tracking`), or alert
> delivery (`domains/notifications/domain.md#watch-contract`).

## Ubiquitous language

| Term | Definition |
| --- | --- |
| Assistant | The per-user agent bound to exactly one account and role; it has no privileges of its own. |
| Conversation | Ordered thread of turns owned by one user; the only unit a user can list, read, or delete. |
| Turn | One user request plus the assistant reply, tool calls, and usage counters; created atomically. |
| Tool | A named, allowlisted, typed server-side capability; the only way the agent reads or changes data. |
| Read tool | A tool that only reads data already visible to the requesting user. |
| Proposal | A mutating tool call recorded as a `PendingAction`; inert until confirmed. |
| Confirmation | An explicit user action authorising exactly one pending action; single-use and expiring. |
| Grounded answer | A reply whose factual claims come from tool results in the same turn, never from model memory. |
| Memory | User-visible, user-editable preferences the agent may use; never inferred silently. |
| Budget | Server-enforced per-user daily ceiling on messages and tokens. |
| Fallback | The manual portal UI offered when the assistant is disabled, over budget, or unavailable. |
| Kill switch | A deployment setting that disables the assistant without a code change. |

## Entities & aggregates

| Entity | Key fields (type) | Relations | Notes |
| --- | --- | --- | --- |
| `Conversation` (proposed) | `user: FK settings.AUTH_USER_MODEL`, `title: str(200)`, `status: enum(open, archived)`, `created_at`, `last_message_at` | `related_name="assistant_conversations"` | Indexed `(user, -last_message_at)`. Foreign access returns 404. |
| `Turn` (proposed) | `conversation: FK`, `request_id: uuid unique`, `status: enum(pending, completed, failed, blocked)`, `model: str`, `prompt_version: str`, `tokens_in/tokens_out: int`, `latency_ms: int`, `error_code: str` | `related_name="turns"` | One row per request; supplies idempotency and cost audit. |
| `Message` (proposed) | `turn: FK`, `role: enum(user, assistant, tool)`, `content: text`, `citations: json` | `related_name="messages"` | Assistant markdown is sanitised by the client renderer. |
| `ToolCall` (proposed) | `turn: FK`, `name: str`, `args: json`, `args_hash: str(64)`, `result_summary: json`, `status: enum(ok, denied, error)`, `duration_ms: int` | `related_name="tool_calls"` | Audit trail; raw PII is not stored in `result_summary`. |
| `PendingAction` (proposed) | `user: FK`, `conversation: FK nullable`, `tool_name: str`, `payload: json`, `state: enum(proposed, confirmed, executed, expired, cancelled)`, `expires_at`, `idempotency_key: uuid unique` | FK to user and conversation | The only path to a mutation. |
| `Memory` (proposed) | `user: OneToOne`, `facts: json`, `updated_at` | One-to-one with user | User-visible and editable via the API. |
| `UsageLedger` (proposed) | `user: FK`, `day: date`, `messages: int`, `tokens_in/tokens_out: int`, `cost_micros: bigint` | Unique `(user, day)` | Backs the budget invariant; keeps no content. |
| `Feedback` (proposed) | `user: FK`, `message: FK`, `rating: enum(up, down)`, `reason: text blank` | FK to user and message | Feeds the evaluation set. |

New app `bottom_up/assistant/`; registered in `LOCAL_APPS` and exposed through
`router.register("assistant", ...)` (`ARCHITECTURE.md` §3, §5, §6).

## Conversation contract

Every request is idempotent per `request_id`; replaying the same id returns the
existing turn without calling the provider again. History is bounded
(`ASSISTANT_HISTORY_MESSAGES`) and always scoped to the owning user. Deleting a
conversation is a hard delete for the user and leaves only aggregate usage
counters.

## Tool contract

Tools are declared with a name, description, and JSON-schema parameters. The
server validates arguments with serializers and executes handlers under the
caller's own queryset scoping; the model never supplies identity or role.

| Tool | Kind | Backing domain | Rule |
| --- | --- | --- | --- |
| `search_jobs` | read | discovery `#search-contract` | Accepts only the documented query params; returns active listings plus a shareable URL. |
| `get_job` | read | postings `#job-lifecycle` | `live` with a future deadline only; expired returns an explanatory payload. |
| `list_my_applications` | read | applications `#outbound-tracking` | Self-scoped only. |
| `get_my_profile` | read | identity-access `#rbac-roles` | Returns display fields only; never email, tokens, or password material. |
| `navigate` | ui | — | Whitelisted route map; emits a structured `ui_action`, never a free-form URL. |
| `propose_watch` | mutate (proposed) | notifications `#watch-contract` | Serialises discovery params, creates a `PendingAction`, executes only on confirmation. |

Tools not listed here are unreachable, regardless of what the model emits.

## Confirmation flow

`proposed` → `confirmed` → `executed`, with `proposed` → `cancelled`/`expired`
and `confirmed` → `expired`. Confirmation binds to
`(user, pending_action, payload_hash)`; any payload change invalidates it.
Actions expire after `ASSISTANT_ACTION_TTL_SECONDS`; a replay returns the
recorded outcome rather than executing twice.

## State machine

| State | Meaning | Allowed next states |
| --- | --- | --- |
| `pending` (turn) | Provider call in flight | `completed`, `failed`, `blocked` |
| `completed` | Reply and usage recorded | — (terminal) |
| `failed` | Provider/validation error; no partial reply | — (terminal; retry = new turn) |
| `blocked` | Guardrail refused the request | — (terminal) |
| `proposed` (action) | Awaiting user confirmation | `confirmed`, `cancelled`, `expired` |
| `confirmed` | User authorised one execution | `executed`, `expired` |
| `executed` | Handler succeeded; outcome recorded | — (terminal) |
| `expired` | TTL elapsed or replay after success | — (terminal) |
| `open` (conversation) | Accepting turns | `archived` |
| `archived` | Read-only history | — (terminal unless undeclared) |

## Invariants

- [ ] INV-01: No tool executes with broader privilege than the requesting user; authorization is re-derived server-side from `request.user`.
- [ ] INV-02: No mutating tool runs without a recorded, single-use, unexpired confirmation tied to the payload hash.
- [ ] INV-03: Content read from the database (job text, company copy) is data only; it can never add tools, alter the allowlist, or trigger an unconfirmed mutation.
- [ ] INV-04: Every turn stores model, prompt version, tool calls, latency, and tokens; job claims trace to tool results in the same turn.
- [ ] INV-05: Conversations, messages, and actions are visible only to their owner; foreign identifiers return 404.
- [ ] INV-06: Budget is checked before the provider call; over-budget returns 429 and spends nothing.
- [ ] INV-07: Provider failure or timeout leaves no partial assistant message and no orphan state.
- [ ] INV-08: Replaying a `request_id` returns the persisted turn without a second provider call.
- [ ] INV-09: Deletion removes message content within the retention window; `UsageLedger` keeps counters only.
- [ ] INV-10: Assistant output is treated as untrusted markdown; no raw HTML, script, or non-allowlisted link reaches the DOM.
- [ ] INV-11: Memory is only what the user wrote; the agent never invents or silently persists preferences.

## Authorization matrix

| Role | Action | Rule |
| --- | --- | --- |
| student | Chat, read own history, confirm own actions | Allow; assistant inherits student scope |
| employer, school_admin | Chat, read own history | Allow read tools scoped to their role; no privileged rows, no admin tools |
| anonymous | Any assistant endpoint | Deny — `IsAuthenticated`; 401/403, never a guest conversation |
| any user | Read another user's conversation/action/message | Deny — 404, no existence leak |
| staff | Inspect turns and usage | Allow via Django admin (counts and metadata; message content only with retention policy) |

## Domain events & side effects

| Event | Payload (JSON-serializable) | Produced by | Consumed by |
| --- | --- | --- | --- |
| `assistant.turn_completed` | `{"user_id": "int", "turn_id": "int", "tool_calls": "int", "tokens": "int"}` | Turn service | Usage ledger, analytics |
| `assistant.action_proposed` | `{"user_id": "int", "action_id": "int", "tool": "str"}` | Turn service | Audit log |
| `assistant.action_executed` | `{"user_id": "int", "action_id": "int", "tool": "str"}` | Confirmation view | Audit log, notifications create |
| `assistant.turn_blocked` | `{"user_id": "int", "reason": "str"}` | Guardrail | Security log |

Celery tasks: retention purge, usage rollup, and evaluation runs. Task arguments
are JSON-serializable and tested with `CELERY_TASK_ALWAYS_EAGER=True`
(`ARCHITECTURE.md` §7).

## Error contract

| Condition | Observable outcome |
| --- | --- |
| Assistant disabled (kill switch) | 503 with `code="assistant_disabled"` and the manual fallback hint; no turn created |
| Over budget | 429 with `code="budget_exceeded"`, reset time, and fallback hint; no provider call |
| Empty or oversized message (> `ASSISTANT_MAX_MESSAGE_CHARS`) | 400 field error; no turn created |
| Duplicate `request_id` | 200/201 with the persisted turn; no second provider call |
| Foreign conversation or action | 404 with a generic body; no existence leak |
| Provider timeout / upstream error | 504/502 with `code="provider_unavailable"`, `retryable=true`; turn `failed`, no assistant message |
| Guardrail block (prompt injection, unsafe request) | 200 with a blocked turn and refusal text; nothing executed |
| Action TTL elapsed | 409 with `code="action_expired"`; no execution |
| Confirmation payload mismatch / replay | 409 with `code="action_invalid"`; no execution |

## Safety and Abuse

- Untrusted retrieved content is delimited and labelled as data; system
  instructions never include raw job text.
- Tool arguments are allowlisted by schema; free-form URLs, SQL, shell, and
  outbound HTTP are not tool parameters.
- No passwords, tokens, or full emails enter prompts; logs store `args_hash`
  and summaries.
- Per-user rate limits (messages/minute), daily budgets, and a global kill
  switch are enforced server-side.
- Assistant markdown is sanitised at render; links are limited to the portal
  and `Job.external_url` values.
- Prompt-injection and data-exfiltration attempts are logged as
  `assistant.turn_blocked` and counted for abuse review.

## Open decisions

- Provider and data-processing terms (hosted API vs self-hosted) — record in
  `docs/decisions/0001-assistant-provider.md` once chosen.
- Whether employers and school admins receive write proposals in v1.1.
- Message retention window default (30 days proposed) and PDPA review.
- Token-level streaming transport (SSE deltas vs sync + replay) for the UI.
