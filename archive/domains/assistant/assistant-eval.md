---
domain: assistant
requires_specs:
  - ARCHITECTURE.md
  - domains/assistant/domain.md#safety-and-abuse
  - domains/assistant/domain.md#error-contract
---

# Assistant Quality Gates

| Field | Value |
| --- | --- |
| Name | Assistant Quality Gates |
| Description | Evaluation transcripts, user feedback, quotas, and admin visibility keep assistant quality and cost observable. |

## Goal

Make assistant behaviour measurable and bounded: deterministic evaluation
transcripts run offline, user feedback feeds the eval set, usage and cost are
visible per user and per day, and ops can disable the assistant instantly.

## Non-goals

- Model training or fine-tuning on user data.
- A full analytics product or BI dashboard.
- Automated prompt rewriting in production.

## Actors

- Engineering / operations (staff)
- Student, Employer, School Admin (feedback and quota subject)

## Preconditions

- Assistant enabled with the fake provider available in test settings.
- At least one prompt version recorded on turns.

## Postconditions

- The eval suite runs without network access and fails on unsafe tool selection.
- Every turn carries a prompt version and usage counters.
- Feedback is attributable to a message and its owner.
- A kill switch disables assistant endpoints without deployment.

## Gherkin scenarios

```gherkin
Feature: Assistant quality gates
  Scenario: Offline evaluation run
    Given the fake provider and recorded transcripts
    When the eval suite runs
    Then each transcript asserts the expected tool selection and arguments
    And no network request is made
    And unsafe or ungrounded outputs fail the suite

  Scenario: Prompt injection is a test case
    Given a transcript whose job text asks the assistant to ignore its rules
    When the eval suite runs
    Then the expected tool set is unchanged
    And the case passes only when no mutation is proposed

  Scenario: Feedback is owner-scoped
    Given I rate my assistant message "down" with a reason
    When the feedback is stored
    Then it is linked to my message and user
    And rating another user's message returns 404

  Scenario: Usage is observable
    Given I send messages across two days
    When ops inspect usage
    Then each day has message and token counters for my account
    And no message content is exposed in the counters

  Scenario: Kill switch
    Given ASSISTANT_ENABLED is false
    When any client calls an assistant endpoint
    Then the response is 503 with code "assistant_disabled"
    And the portal remains fully usable without the assistant
```

## Acceptance criteria

- [ ] Eval transcripts run under `config.settings.test` with no external calls.
- [ ] Eval failures block the change in CI once the suite is wired into pytest.
- [ ] `UsageLedger` records messages, tokens, and cost per user per day.
- [ ] Feedback requires owning the message; foreign ids return 404.
- [ ] `ASSISTANT_ENABLED=false` disables all assistant endpoints with 503.
- [ ] Staff can inspect turns and usage in Django admin without seeing raw prompts by default.
- [ ] Retention purge is scheduled and tested with `CELERY_TASK_ALWAYS_EAGER=True`.

## Open questions

- Whether eval transcripts ship as pytest cases or as a separate management command.
- Prompt-version naming and review process for system-prompt changes.
- Cost threshold that triggers an ops alert versus a hard user budget stop.
