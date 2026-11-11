---
domain: notifications
requires_specs:
  - ARCHITECTURE.md
  - domains/notifications/domain.md#watch-contract
  - domains/discovery/domain.md#search-contract
---

# Watch Alerts

| Field | Value |
| --- | --- |
| Name | Watch Alerts |
| Description | Saved searches are evaluated on a cadence and deliver only genuinely new, active matches. |

## Goal

Turn active watches into a low-noise digest: evaluated on schedule, filtered to
active listings, deduplicated against everything already alerted, and delivered
over the user's chosen channel.

## Non-goals

- Real-time push or websockets.
- Ranking or recommendations inside a digest.
- Cross-user or employer-side alerts.

## Actors

- Student (watch owner)
- Celery beat worker (system actor)

## Preconditions

- At least one `active` watch exists.
- Discovery search is available.

## Postconditions

- Each active watch has at most one run per cadence window.
- A digest contains only new matches, or nothing when the policy is silent.
- Delivery status is recorded and retryable on failure.

## Gherkin scenarios

```gherkin
Feature: Watch alerts
  Scenario: New match produces a digest
    Given an active watch for "fintech internships"
    And a new matching listing went live since the last run
    When the digest task runs
    Then the run records new_count=1
    And one delivery is sent over the watch channel
    And the listing is recorded in SeenListing

  Scenario: Repeat run sends nothing new
    Given the same matching listing was already alerted
    When the digest task runs again
    Then new_count=0
    And no duplicate delivery is sent

  Scenario: Expired listing never alerts
    Given a matching listing is expired or a draft
    When the digest task runs
    Then it is excluded from matches

  Scenario: Paused watch is skipped
    Given my watch is paused
    When the digest task runs
    Then no run delivers and no email is sent

  Scenario: Delivery failure is retryable
    Given the email backend raises a timeout
    When the digest task runs
    Then the delivery is marked "failed" with an error code
    And a later retry does not duplicate already-seen matches

  Scenario: Foreign watch
    Given another user owns the watch
    When I pause or delete it
    Then I receive 404
```

## Acceptance criteria

- [ ] Beat schedule evaluates active watches at most once per cadence window.
- [ ] Digest matches come only from active listings (`live` and future deadline).
- [ ] `SeenListing` uniqueness prevents duplicate alerts per watch.
- [ ] Paused and deleted watches produce no deliveries.
- [ ] Delivery rows record `pending`/`sent`/`failed` with an error code.
- [ ] Pause, resume, and delete are self-scoped; foreign ids return 404.
- [ ] Emails render in Mailpit locally; production uses Mailgun.

## Open questions

- Silent vs explicit "no new matches" digest.
- Digest send time and per-user timezone handling.
- Retention of `SeenListing` rows after listings expire.
