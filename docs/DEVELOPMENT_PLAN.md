# BottomUp — Team Development Plan

Proposed engineering workflow · 5-person team · AI-assisted development

## 1. Objectives

Our objective is to develop BottomUp using an AI-first software engineering workflow.

We will first establish a shared architectural foundation, define clear domain ownership, and standardise how AI agents execute software development.

The intended outcomes are:

1. Establish a consistent architecture across all domains.
2. Give each team member clear ownership and responsibilities.
3. Use AI agents to handle the majority of documentation and software implementation.
4. Retain human oversight over important architectural and engineering decisions.
5. Ensure that independently developed features integrate into a coherent system.

## 2. Team structure and responsibilities

We will have five people, with myself coordinating the overall product vision and architecture.

| Role                      | Responsibilities                                                                                                                  |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Project architect (me)    | Establish initial domain contracts, resolve cross-domain conflicts, maintain architectural consistency and coordinate priorities. |
| Domain owners (4 members) | Own assigned domains, refine contracts, draft feature specifications, coordinate implementation and maintain documentation.       |
| All members               | Review specifications, approve implementation plans where assigned, review code and participate in integration testing.           |

Domain ownership does not mean exclusive implementation rights. Members can implement features outside their assigned domains, subject to the relevant domain owner's review.

## 3. Development phases

1. Phase 1 — Establish architectural foundation

   Project architect

   I will draft the initial domain contracts for all BottomUp domains.

   Deliverables:
   - Initial domain contracts.
   - Domain architecture.
   - Domain context map.
   - Cross-domain authorization specifications.
   - Identification of cross-domain dependencies and potential conflicts.
   The objective is to establish consistent domain boundaries before distributing domain ownership.
2. Phase 2 — Domain ownership and refinement

   All members

   Domains will be distributed among the four groupmates.

   Each domain owner will:
   - Review the initial domain contract.
   - Identify missing requirements and potential inconsistencies.
   - Propose refinements.
   - Coordinate with other domain owners on cross-domain interactions.
   - Finalise their assigned domain contracts.
   Significant architectural disagreements will be discussed and resolved centrally.
3. Phase 3 — Feature specification

   Domain owners

   Each domain owner will identify and document the features required for their domains.

   Deliverables:
   - `FEATURE.md` for individual features.
   - Relevant architectural decisions (ADRs).
   - Identified dependencies on other features or domains.
   - Acceptance criteria and open questions.
   Feature specifications should follow the established `FEATURE_TEMPLATE.md`.

   We will prioritise features based on dependencies and the minimum requirements for an end-to-end working product.

   We do not need to complete every feature specification before development begins.
4. Phase 4 — AI-assisted feature development

   All members

   Once a feature is sufficiently specified and its dependencies are ready, its development can begin.

   We will follow the standard development lifecycle outlined in Section 4 (refer below).

   Each member will be responsible for initiating development, reviewing AI-generated outputs and ensuring that completed features satisfy their specifications.
5. Phase 5 — Integration and system verification

   All members

   Features will be integrated incrementally rather than waiting until all domains are completed.

   Activities:
   - Cross-domain integration testing.
   - End-to-end testing of important user journeys.
   - Regression testing.
   - Resolving interface incompatibilities.
   - Verifying system-wide authorization and data integrity.
   The objective is to ensure that individually completed features work together as one system.

## 4. Standard AI-assisted development lifecycle

Every feature should follow the same development process.

| Step | Stage                    | Description                                                            | Responsibility |
| ---- | ------------------------ | ---------------------------------------------------------------------- | -------------- |
| 1    | Specification            | Define requirements and acceptance criteria in `FEATURE.md`.           | Human + AI     |
| 2    | Specification validation | Check completeness, ambiguities and consistency with domain contracts. | AI + Human     |
| 3    | Planning                 | AI analyses requirements and creates `IMPLEMENTATION.md`.              | AI             |
| 4    | Plan approval            | Review and approve the proposed implementation approach.               | Human          |
| 5    | Test development         | AI writes tests and verifies that they fail for the expected reasons.  | AI             |
| 6    | Test approval            | Verify that tests accurately represent the feature requirements.       | Human          |
| 7    | Implementation           | AI implements the feature incrementally and runs relevant tests.       | AI             |
| 8    | Independent review       | Another AI and a human independently review the implementation.        | AI + Human     |
| 9    | Corrections              | Address valid review findings and rerun relevant checks.               | AI             |
| 10   | Completion               | Verify, update documentation and tracking, and commit changes.         | AI + Human     |

### Important rules

1\. Specifications are the source of truth.

`FEATURE.md` defines what needs to be built. `IMPLEMENTATION.md` defines how it will be built.

If implementation reveals missing or incorrect requirements, update the specification rather than silently changing the intended behaviour.

2\. AI agents cannot approve their own work.

The implementation agent cannot approve its own implementation plan, tests or code.

3\. Tests must verify requirements, not merely implementation assumptions.

Human reviewers must verify that tests cover the actual acceptance criteria.

4\. Independent reviews must be independent.

The reviewing AI should assess the specification, approved plan, tests and code diff rather than simply agreeing with the implementation agent.

5\. No feature is complete without verification.

Passing tests, linting, type checking, relevant integration tests and resolution of review findings are required before completion.

## 5. Documentation and engineering standards

We will maintain a consistent documentation structure.

```
/architecture
├── DOMAIN_ARCHITECTURE.md
├── DOMAIN_CONTEXT_MAP.md
├── CROSS_DOMAIN_AUTHORIZATION.md
├── domains/
│   ├── DOMAIN_CONTRACT_TEMPLATE.md
│   ├── FEATURE_TEMPLATE.md
│   └── <domain>/
│       ├── DOMAIN_CONTRACT.md
│       └── features/
│           └── <feature>/
│               └── FEATURE.md
├── decisions/
│   └── <decision>.md
├── workflows/
    └── WORKFLOW_TEMPLATE.md
```

Implementation plans and other temporary working documents should follow the agreed workflow conventions.

We will also maintain:

- Consistent naming conventions and terminology.
- Explicit domain ownership.
- Traceability between requirements, tests and implementation.
- Architecture Decision Records for significant decisions.
- A shared feature tracking mechanism.
- Automated CI checks.

## 6. Collaboration and review guidelines

To prevent development from becoming siloed, we will establish the following practices.

| Activity                | Guideline                                                        |
| ----------------------- | ---------------------------------------------------------------- |
| Domain contract changes | Domain owner proposes; affected owners review.                   |
| Cross-domain conflicts  | Discuss with affected owners; architect resolves.                |
| Feature specification   | Domain owner maintains; another member reviews when appropriate. |
| Implementation plan     | Must receive human approval before implementation.               |
| Test suite              | Must be checked against acceptance criteria.                     |
| Pull requests           | Must receive an independent human review.                        |
| Architectural changes   | Must be documented through ADRs.                                 |
| Integration             | Must pass relevant automated checks before merging.              |

We should also use a rotating code-review arrangement so that everyone participates in understanding the wider codebase.

## 7. Initial priorities

We should not attempt to develop all domains simultaneously.

Instead, we will prioritise features based on dependencies and build an end-to-end working product incrementally.

For example, an initial development sequence could be:
- Account registration feature
- Log in, Log out features
- Password setting feature

Some work can proceed in parallel once its dependencies are established.

## 8. Immediate next steps

Our immediate focus should be architectural preparation rather than coding.

Initial checklist

1 of 8 completed

12.5%

[x] Establish the complete list of BottomUp domains.

[ ] Draft initial domain contracts for all domains.

[ ] Review and resolve cross-domain conflicts.

[ ] Distribute domain ownership among the four groupmates.

[ ] Refine and finalise assigned domain contracts.

[ ] Identify and prioritise the initial features.

[ ] Draft FEATURE.md for the first development milestone.

[ ] Begin AI-assisted implementation of the first end-to-end features.

## 9. Guiding principles

1. Architecture before implementation: Establish clear domain boundaries before building features.
2. Progressive documentation: Document sufficiently before implementation, but do not over-document features that have not been prioritised.
3. Ownership with collaboration: Every domain has an owner, but the system belongs to the entire team.
4. AI-first execution: Delegate repetitive engineering work to AI agents wherever practical.
5. Human accountability: Humans remain responsible for requirements, architectural decisions and approving deliverables.
6. Verification over trust: AI-generated outputs must be independently verified.
7. Incremental integration: Continuously integrate completed features instead of postponing integration until the end.

The end goal is to establish a repeatable engineering process where we spend our time making product and architectural decisions, while AI agents handle the bulk of the implementation work.