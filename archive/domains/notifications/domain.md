# Notifications — Domain Contract

> How saved searches become alerts.
> Owns `Watch`, watch runs, digests, and delivery state.
> Does not own search semantics (`domains/discovery/domain.md#search-contract`),
> whose query contract a watch stores verbatim, or conversation state
> (`domains/assistant/domain.md#conversation-contract`), which may only propose
> a watch.

## Ubiquitous language

| Term | Definition |
| --- | --- |
| Watch | A user-owned saved discovery query with a cadence; stores discovery params verbatim. |
| Cadence | How often a watch is evaluated: `daily` or `weekly`. |
| Watch run | One evaluation of a watch at a point in time; records what matched. |
| Digest | One message summarising a watch run's new matches. |
| Delivery | The attempt to send a digest over a channel (`email`, `in_app`) with a status. |
| New match | An active listing matching the watch that has not appeared in a previous digest for that watch. |
| Paused watch | A watch that is retained but not evaluated and sends nothing. |

## Entities & aggregates

| Entity | Key fields (type) | Relations | Notes |
| --- | --- | --- | --- |
| `Watch` (proposed) | `user: FK settings.AUTH_USER_MODEL`, `title: str(120)`, `query: json`, `cadence: enum(daily, weekly)`, `channel: enum(email, in_app)`, `state: enum(active, paused, deleted)`, `last_run_at: datetime nullable`, `created_at` | `related_name="watches"` | `query` accepts only discovery's documented params. |
| `WatchRun` (proposed) | `watch: FK`, `started_at`, `finished_at`, `matched_count: int`, `new_count: int`, `status: enum(running, completed, failed)` | `related_name="runs"` | Idempotent per `(watch, window_start)`. |
| `Delivery` (proposed) | `watch_run: FK`, `channel: enum(email, in_app)`, `status: enum(pending, sent, failed)`, `sent_at nullable`, `error_code: str` | `related_name="deliveries"` | At most one successful delivery per run per channel. |
| `SeenListing` (proposed) | `watch: FK`, `listing_id: int`, `first_seen_at` | Unique `(watch, listing_id)` | Suppresses duplicate alerts; references postings by id. |

`SeenListing` stores an opaque listing id, not a cross-app FK, so the
notifications app does not import another domain's model.

## Watch contract

A watch is created from the portal UI or from an assistant proposal. Its
`query` is validated against discovery's parameter schema at creation; unknown
or unsafe keys are rejected. Evaluation runs on the Celery beat schedule, reads
only active listings (`status == live AND deadline > now()`), and records a
`SeenListing` row per matched listing so later runs alert only on new matches.

## State machine

| State | Meaning | Allowed next states |
| --- | --- | --- |
| `active` | Evaluated on cadence and delivers digests | `paused`, `deleted` |
| `paused` | Retained, not evaluated, no delivery | `active`, `deleted` |
| `deleted` | Hidden from the user; retained for audit | — (terminal) |
| `running` (run) | Evaluation in progress | `completed`, `failed` |
| `pending` (delivery) | Digest queued | `sent`, `failed` |

## Invariants

- [ ] INV-01: A watch's `query` contains only discovery parameters; unknown keys are rejected at creation.
- [ ] INV-02: Only active listings are considered; drafts, queued, and expired rows never produce a digest.
- [ ] INV-03: A listing alerts at most once per watch (`SeenListing` uniqueness).
- [ ] INV-04: A paused or deleted watch is never evaluated and never delivers.
- [ ] INV-05: A watch belongs to exactly one user; foreign access returns 404.
- [ ] INV-06: A failed delivery never marks the digest as sent and is retryable without duplicating matches.
- [ ] INV-07: An empty digest sends nothing (or one explicit "no new matches" message per cadence, per the chosen policy).

## Authorization matrix

| Role | Action | Rule |
| --- | --- | --- |
| student | Create, list, pause, resume, delete own watches | Allow; query validated against discovery schema |
| employer, school_admin | Same | Allow; no cross-user visibility |
| anonymous | Any watch endpoint | Deny — `IsAuthenticated` |
| assistant | Propose a watch for the requesting user | Allow only through the assistant confirmation flow (`domains/assistant/domain.md#confirmation-flow`) |
| staff | Inspect runs and delivery failures | Allow via Django admin |

## Domain events & side effects

| Event | Payload (JSON-serializable) | Produced by | Consumed by |
| --- | --- | --- | --- |
| `watch.created` | `{"user_id": "int", "watch_id": "int"}` | Watch view / action executor | Audit log |
| `watch.run_completed` | `{"watch_id": "int", "new_count": "int"}` | Digest beat task | Delivery task |
| `watch.digest_sent` | `{"user_id": "int", "watch_id": "int", "delivery_id": "int"}` | Delivery task | Analytics, email via Mailpit/Mailgun |
| `watch.digest_failed` | `{"watch_id": "int", "delivery_id": "int", "error_code": "str"}` | Delivery task | Retry backoff, ops log |

## Error contract

| Condition | Observable outcome |
| --- | --- |
| Unknown or unsafe query key | 400 field error; no watch created |
| Cadence outside `daily`/`weekly` | 400 field error; no watch created |
| Foreign watch id | 404 with a generic body |
| Duplicate create (same query and cadence) | 200 with the existing watch; no duplicate row |
| Delivery failure | Digest marked `failed` with `error_code`; retried with backoff; no duplicate matches |
| Paused watch evaluated by mistake | No delivery; run recorded as skipped |

## Open decisions

- Whether "no new matches" sends an explicit digest or stays silent (INV-07).
- Digest time-of-day and timezone per user (default `Asia/Singapore`).
- In-app channel storage (notification table vs derived feed) for v1.1.
- Retention of `SeenListing` rows after a listing expires.
