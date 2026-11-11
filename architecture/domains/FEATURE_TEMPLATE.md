# `<Feature Name>`

## 1. Overview

### 1.1 Feature ID

`<DOMAIN>-<CAPABILITY>-<NUMBER>`

### 1.2 Goal

Describe the business outcome this feature is intended to achieve.

### 1.3 Description

Provide a concise explanation of the feature, its behaviour and its role within the owning domain.

### 1.4 Priority

- [ ] P0 — Critical
- [ ] P1 — High
- [ ] P2 — Medium
- [ ] P3 — Low

### 1.5 Specification Status

- [ ] Draft
- [ ] Under Review
- [ ] Approved
- [ ] Deprecated

---

## 2. Scope

### 2.1 In Scope

List the functionality and behaviours covered by this feature.

### 2.2 Non-Goals

Explicitly identify functionality that this feature does not implement.

### 2.3 Domain Ownership

**Owning domain:** `<domain_name>`

**Owning capability:** `<capability_name>`

Identify the authoritative entities and business rules owned by this feature.

### 2.4 Domain Boundaries

Describe responsibilities that belong to other domains.

| Responsibility | Owning domain | Interaction |
|---|---|---|
| `<Responsibility>` | `<Domain>` | `<How this feature interacts with it>` |

---

## 3. Actors and Permissions

### 3.1 Actors

| Actor | Description | Role in this feature |
|---|---|---|
| `<Actor>` | `<Description>` | `<Interaction>` |

### 3.2 Authorization Requirements

Specify the permissions required to perform each operation.

| Operation | Required permission | Resource scope |
|---|---|---|
| `<Operation>` | `<Permission>` | `<Scope>` |

### 3.3 Authorization Constraints

- Identify applicable ownership restrictions.
- Identify organizational membership requirements.
- Identify resource-level access restrictions.
- Identify applicable agent delegation requirements.
- Identify whether human approval is required for agent-initiated operations.

Do not assume authentication implies authorization.

---

## 4. Preconditions

List the conditions that must be satisfied before the feature can execute.

| ID | Precondition | Failure behaviour |
|---|---|---|
| PRE-001 | `<Condition>` | `<Expected behaviour if unmet>` |

---

## 5. Functional Requirements

Define the required system behaviours.

| ID | Requirement | Expected behaviour | Priority |
|---|---|---|---|
| FR-001 | `<Requirement>` | `<Expected behaviour>` | P0 |
| FR-002 | `<Requirement>` | `<Expected behaviour>` | P1 |

Requirements must be specific, independently understandable and testable.

Avoid implementation-specific decisions unless they are necessary architectural constraints.

---

## 6. Business Rules

Define the business rules governing the feature.

| ID | Business rule | Description |
|---|---|---|
| BR-001 | `<Rule>` | `<Explanation>` |

Business rules should describe what must be true, regardless of implementation.

---

## 7. Inputs and Outputs

### 7.1 Inputs

| Field | Type | Required | Validation | Description |
|---|---|---|---|---|
| `<field>` | `<type>` | Yes/No | `<Rule>` | `<Description>` |

### 7.2 Outputs

| Field | Type | Description |
|---|---|---|
| `<field>` | `<type>` | `<Description>` |

### 7.3 Side Effects

Identify any state changes or external effects caused by this feature.

- Database records created or updated.
- Domain events published.
- External services invoked.
- Notifications requested.
- Audit evidence generated.

---

## 8. State and Lifecycle

### 8.1 States

Define the states relevant to this feature.

| State | Description |
|---|---|
| `<State>` | `<Description>` |

### 8.2 State Transitions

| Current state | Trigger | Next state | Conditions |
|---|---|---|---|
| `<State>` | `<Trigger>` | `<State>` | `<Conditions>` |

### 8.3 Invalid Transitions

Specify prohibited transitions and their expected handling.

---

## 9. Gherkin Scenarios

Define the expected behaviour using Given-When-Then scenarios.

### Scenario 1: Successful operation

**Given** `<initial conditions>`

**And** `<additional conditions>`

**When** `<actor performs action>`

**Then** `<expected outcome>`

**And** `<additional outcome>`

### Scenario 2: Authorization failure

**Given** `<actor without required permission>`

**When** `<actor attempts operation>`

**Then** `<operation is rejected>`

**And** `<no unauthorized state change occurs>`

### Scenario 3: Validation failure

**Given** `<invalid input or state>`

**When** `<operation is performed>`

**Then** `<validation failure is returned>`

### Scenario 4: Boundary condition

**Given** `<boundary conditions>`

**When** `<operation is performed>`

**Then** `<expected behaviour>`

### Additional scenarios

Include relevant cases for:

- Missing or invalid inputs.
- Duplicate requests.
- Concurrent operations.
- Invalid state transitions.
- Resource ownership violations.
- Unauthorized access.
- Expired or revoked permissions.
- External service failures.
- Agent-initiated operations.
- Retry and recovery behaviour.

Only include scenarios relevant to the feature.

---

## 10. Error Handling

Define expected failure conditions and system behaviour.

| Error ID | Condition | Expected response | State impact |
|---|---|---|---|
| ERR-001 | `<Condition>` | `<Response>` | `<Impact>` |

Specify whether failures are:

- Validation failures.
- Authorization failures.
- Business rule violations.
- Resource conflicts.
- External dependency failures.
- Unexpected system failures.

---

## 11. Domain Events

### 11.1 Events Published

| Event | Trigger | Payload | Consumers |
|---|---|---|---|
| `<EventName>` | `<Trigger>` | `<Relevant fields>` | `<Domains>` |

### 11.2 Events Consumed

| Event | Producer | Purpose | Resulting behaviour |
|---|---|---|---|
| `<EventName>` | `<Domain>` | `<Purpose>` | `<Behaviour>` |

If the feature does not publish or consume domain events, explicitly state `None`.

---

## 12. Cross-Domain Dependencies

Identify dependencies on other domains or capabilities.

| Dependency | Owning domain | Required operation | Failure behaviour |
|---|---|---|---|
| `<Dependency>` | `<Domain>` | `<Operation>` | `<Expected behaviour>` |

Specify whether the dependency is synchronous or asynchronous.

Do not directly access another domain's internal implementation or database tables.

---

## 13. Security and Privacy

Specify relevant security and privacy requirements.

- Authentication requirements.
- Authorization requirements.
- Resource ownership restrictions.
- Sensitive data handling.
- Data minimization.
- Audit requirements.
- Consent requirements.
- Data retention requirements.
- Protection against unauthorized disclosure.
- Agent delegation and execution restrictions, where applicable.

Reference applicable domain policies rather than duplicating their full specifications.

---

## 14. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-001 | Performance | `<Requirement>` |
| NFR-002 | Reliability | `<Requirement>` |
| NFR-003 | Security | `<Requirement>` |
| NFR-004 | Scalability | `<Requirement>` |
| NFR-005 | Observability | `<Requirement>` |

Include measurable thresholds where they are known. Do not invent performance targets.

---

## 15. Acceptance Criteria

Define the conditions required for the feature to be considered complete.

- [ ] All functional requirements are implemented.
- [ ] All applicable business rules are enforced.
- [ ] All Gherkin scenarios pass.
- [ ] Authorization is enforced correctly.
- [ ] Invalid operations are handled correctly.
- [ ] Domain boundaries are respected.
- [ ] Relevant domain events are published or consumed correctly.
- [ ] Security and privacy requirements are satisfied.
- [ ] Automated tests cover relevant success and failure cases.
- [ ] Documentation is updated where necessary.

Additional feature-specific acceptance criteria:

- [ ] `<Acceptance criterion>`

---

## 16. Testing Requirements

### 16.1 Unit Tests

Specify the business logic and validation rules requiring unit tests.

### 16.2 Integration Tests

Specify interactions with external domains, services and persistence layers.

### 16.3 Authorization Tests

Specify relevant permission, ownership and delegation tests.

### 16.4 Edge Cases

Identify boundary conditions, concurrency cases and failure scenarios.

### 16.5 Regression Tests

Identify existing behaviour that must remain unaffected.

---

## 17. Dependencies and Related Specifications

| Specification | Type | Relationship |
|---|---|---|
| `<Specification>` | Feature / Domain / Workflow | `<Relationship>` |

---

## 18. Open Questions

| ID | Question | Impact | Resolution |
|---|---|---|---|
| Q-001 | `<Question>` | `<Impact>` | Pending |

Do not silently assume answers to unresolved questions that materially affect system behaviour.

---

## 19. Implementation Notes

Optional section for approved technical constraints or implementation guidance.

This section must not replace functional requirements or prescribe unnecessary implementation details.

---

## 20. Change History

| Version | Date | Changes | Author |
|---|---|---|---|
| 0.1 | `<Date>` | Initial draft | `<Author>` |