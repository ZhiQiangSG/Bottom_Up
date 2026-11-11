---
domain: assistant
requires_specs:
  - ARCHITECTURE.md
  - domains/assistant/domain.md#conversation-contract
  - domains/assistant/domain.md#safety-and-abuse
  - domains/identity-access/domain.md#rbac-roles
---

# Assistant Conversation Shell

| Field | Value |
| --- | --- |
| Name | Assistant Conversation Shell |
| Description | A logged-in user starts a conversation, sends a message, and receives a grounded reply with visible history. |

## Goal

Give every user a persistent, private assistant conversation with an auditable
turn record, budget enforcement, and a graceful fallback to the manual UI when
the assistant is unavailable.

## Non-goals

- Job search tools, watch proposals, and any database mutation.
- Token-level streaming; the transport ships as turn replay (see Open questions).
- Multi-agent orchestration or long-running background reasoning.

## Actors

- Student, Employer, School Admin

## Preconditions

- The user is authenticated and verified.
- `ASSISTANT_ENABLED` is on and the user is under their daily budget.

## Postconditions

- A `Conversation` exists for the user and is listed only for that user.
- The sent turn is persisted with model, prompt version, latency, and token counters.
- An assistant message is stored, or the turn is recorded as `failed`/`blocked` with no partial reply.

## Gherkin scenarios

```gherkin
Feature: Assistant conversation shell
  Scenario: Start a conversation and receive a reply
    Given I am a logged-in student with no assistant conversation
    When I POST /api/assistant/conversations/ and then send "help me get started"
    Then a conversation is created for me
    And the turn status is "completed"
    And I can read both my message and the assistant reply in history

  Scenario: History is private
    Given another student owns a conversation
    When I GET that conversation by id
    Then I receive 404 and no message content

  Scenario: Idempotent retry
    Given I already sent a message with request_id "abc"
    When I resend the same request_id
    Then I receive the persisted turn
    And the provider is not called a second time

  Scenario: Provider unavailable
    Given the provider times out
    When I send a message
    Then the turn status is "failed" with code "provider_unavailable"
    And no assistant message is stored
    And the response offers the manual search fallback

  Scenario: Budget exhausted
    Given my usage ledger has reached the daily message limit
    When I send a message
    Then I receive 429 with code "budget_exceeded"
    And no turn or provider call is made

  Scenario: Assistant disabled by kill switch
    Given ASSISTANT_ENABLED is false
    When I open any assistant endpoint
    Then I receive 503 with code "assistant_disabled"
    And the manual portal UI remains usable

  Scenario: Delete a conversation
    Given I own a conversation
    When I DELETE /api/assistant/conversations/{id}/
    Then the conversation and its messages are removed
    And my usage counters remain
```

## Acceptance criteria

- [ ] `POST /api/assistant/conversations/` returns 201 with `id`, `title`, `status`, `url`.
- [ ] `GET /api/assistant/conversations/` returns only the caller's conversations.
- [ ] `POST /api/assistant/conversations/{id}/turns/` returns 201 with the turn, messages, and tool calls.
- [ ] Foreign conversation ids return 404 for retrieve, delete, and turn creation.
- [ ] Duplicate `request_id` returns the persisted turn and providers are called once.
- [ ] Provider failure returns 502/504 with `retryable: true` and a fallback hint; no assistant message exists.
- [ ] Over-budget returns 429 with reset time; no turn row and no provider call.
- [ ] Kill switch returns 503 for every assistant endpoint.
- [ ] `DELETE` removes content but leaves `UsageLedger` counters intact.
- [ ] `GET /api/schema/` exposes all assistant endpoints.

## Open questions

- Token-level streaming: keep sync send + SSE replay, or move to provider-streamed deltas?
- Should unverified accounts be allowed a read-only assistant, or blocked entirely?
- Retention window (default 30 days) and PDPA sign-off.
