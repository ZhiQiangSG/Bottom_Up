---
domain: assistant
requires_specs:
  - ARCHITECTURE.md
  - domains/assistant/domain.md#confirmation-flow
  - domains/assistant/domain.md#tool-contract
  - domains/notifications/domain.md#watch-contract
---

# Confirmed Watch Proposal

| Field | Value |
| --- | --- |
| Name | Confirmed Watch Proposal |
| Description | The assistant proposes a saved search; the user confirms before the notification domain creates it. |

## Goal

Let a student say "keep an eye out for fintech internships" and, after an
explicit confirmation step, have a watch created with the exact discovery
parameters the assistant resolved.

## Non-goals

- Delivering alerts or deciding cadence policy (owned by notifications).
- Any mutation that is not `propose_watch` (apply, profile edits, job posting).
- Auto-confirming proposals from conversation context.

## Actors

- Student (Employer and School Admin may propose watches in the same flow)

## Preconditions

- Authenticated user with an active conversation.
- The assistant has resolved a valid discovery query.
- The user has not exhausted their pending-action limit.

## Postconditions

- A `PendingAction` exists in `proposed` state with a payload hash and TTL.
- On confirmation, exactly one watch exists and the action is `executed`.
- On cancel or expiry, no watch is created.

## Gherkin scenarios

```gherkin
Feature: Confirmed watch proposal
  Scenario: Propose a watch
    Given I ask "keep an eye out for fintech internships"
    When the assistant resolves the query
    Then a pending action "propose_watch" is created in "proposed" state
    And no watch exists yet
    And the reply asks me to confirm

  Scenario: Confirm creates exactly one watch
    Given a proposed watch action exists
    When I POST /api/assistant/pending-actions/{id}/confirm/
    Then the action state is "executed"
    And exactly one watch exists with my query and cadence
    And replaying the confirmation returns the recorded outcome

  Scenario: Cancel creates nothing
    Given a proposed watch action exists
    When I cancel it
    Then the action state is "cancelled"
    And no watch exists

  Scenario: Expired action
    Given the action TTL has elapsed
    When I confirm it
    Then I receive 409 with code "action_expired"
    And no watch is created

  Scenario: Payload cannot be swapped
    Given a proposed action for query A
    When a client confirms with payload B
    Then I receive 409 with code "action_invalid"
    And no watch is created

  Scenario: Foreign action
    Given another user owns the pending action
    When I confirm it
    Then I receive 404
    And nothing changes
```

## Acceptance criteria

- [ ] Proposing returns a pending action with `id`, `tool_name`, `state`, `expires_at`, and the hash-bound payload.
- [ ] Confirmation executes the registered handler once and records `executed_at`.
- [ ] Replayed confirmation returns the same outcome without a second write.
- [ ] Cancel and expiry both leave zero watches.
- [ ] Payload mismatch is rejected with 409 `action_invalid`.
- [ ] Foreign actions return 404 for confirm and cancel.
- [ ] No mutation path exists outside `POST .../confirm/`.

## Open questions

- Maximum pending actions per user and per conversation.
- Whether confirmation may be granted by a typed "yes" in chat or only by the API button.
