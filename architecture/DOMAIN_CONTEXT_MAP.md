# Domain Context Map

## 1. Purpose

This document defines the relationships, dependencies, and interaction boundaries between BottomUp's business domains.

It establishes:

- Bounded-context relationships and dependency direction.
- Ownership of authoritative data and business rules.
- Cross-domain communication and integration patterns.
- Coordination of cross-domain workflows.
- Architectural coupling and potential change impacts.

This document complements:

- `DOMAIN_ARCHITECTURE.md` — defines domain structure, responsibilities, and architectural boundaries.
- `CROSS_DOMAIN_AUTHORIZATION.md` — defines authorization requirements for cross-domain interactions.
- Individual domain contracts — define domain capabilities, ownership, invariants, interfaces, and events.

Individual domain contracts remain authoritative for domain-specific implementation requirements.

## 2. Architectural Principles

### 2.1 Bounded Context Ownership

Each domain owns its business capabilities, authoritative data, and invariants. Other domains must interact through explicitly defined interfaces and must not bypass its business rules or directly modify its data.

### 2.2 Single Source of Truth

Every authoritative business entity has exactly one owning domain. Other domains may maintain references, projections, or snapshots, but these must not become competing sources of truth.

### 2.3 Explicit Domain Dependencies

Domain dependencies must be intentional and documented. Domains should depend on exposed capabilities rather than internal implementations, and circular dependencies must be avoided.

### 2.4 Contract-Driven Integration

Cross-domain interactions must follow explicit contracts defining relevant inputs, outputs, preconditions, postconditions, authorization, failure semantics, and consistency expectations.

### 2.5 Loose Coupling

Domains should minimize knowledge of one another's internal structures. Prefer domain interfaces and events over dependencies on internal models, database schemas, or implementation details.

### 2.6 Independent Evolution

Domains should be able to evolve independently without requiring unrelated domains to change. Changes to exposed contracts must account for compatibility and migration requirements.

### 2.7 Cross-Domain Authorization

All cross-domain interactions must comply with `CROSS_DOMAIN_AUTHORIZATION.md`.

Agents must execute operations under their own identities and delegated authority, not impersonate human users. The target domain must independently enforce authorization and business invariants.

## 3. Bounded Context Overview

BottomUp consists of sixteen bounded contexts.

| Domain | Primary Responsibility | Authoritative Ownership |
|---|---|---|
| Identity & Access | User identity, authentication, and access control | Users, credentials, identity-level permissions |
| Organization | Organizational identity, membership, and capabilities | Organizations, memberships, organizational capabilities |
| Candidate | Candidate profiles and professional information | Profiles, education, experience, skills, resumes |
| Agent Identity | Agent principals, identity, and delegation | Agent identities, delegation relationships |
| Assistant | AI assistant experiences and task orchestration | Conversations, assistant memory, assistant tasks |
| Tool Governance | Tool registration, policies, and execution authorization | Tool definitions, approval policies, execution governance |
| Opportunity | Employment opportunities and their lifecycle | Job opportunities and related records |
| Discovery | Opportunity discovery and matching | Discovery configurations, search and matching results |
| Application | Candidate applications and their lifecycle | Applications and application-related records |
| Career Services | Career centre operations and student support | Career service cases, programmes, and related records |
| Communication | Direct and contextual communications | Communication records and conversations |
| Integration | External system connectivity and synchronization | Integration configurations, credentials, synchronization state |
| Notification | User-facing notifications and delivery | Notification records and delivery state |
| Billing | Subscriptions, entitlements, and payments | Subscription, billing, and entitlement records |
| Analytics | Reporting, metrics, and analytical projections | Derived analytical datasets and reports |
| Compliance | Governance, audit, and regulatory oversight | Audit records, compliance policies, and evidence |

These ownership descriptions are high-level. Individual domain contracts define the precise entities, attributes, and invariants owned by each domain.

## 4. Domain Context Relationships

### 4.1 Identity & Access

**Primary role:** Provides the platform's identity, authentication, and access-control foundation.

**Upstream dependencies:** None within the initial business-domain architecture.

**Downstream consumers:** Organization, Candidate, Agent Identity, Assistant, Tool Governance, and other domains requiring user identity or authentication.

**Responsibilities and boundaries:**

- Owns canonical user identities, credentials, authentication, and identity-level permissions.
- Provides stable user identifiers for other domains.
- Does not own organizational membership, agent delegation, or domain-specific business authorization.
- Existing Cookiecutter `users/` application remains the authentication foundation. Identity & Access owns broader identity and access policies without introducing a competing User implementation.

### 4.2 Organization

**Primary role:** Manages organizational identity, membership, and capabilities.

**Upstream dependencies:** Identity & Access.

**Downstream consumers:** Opportunity, Application, Discovery, Career Services, Communication, Analytics, and Compliance.

**Responsibilities and boundaries:**

- Owns organizational records, memberships, and organizational capabilities.
- Supports multiple capabilities through one canonical Organization, such as employer and career centre, rather than separate records for each business role.
- References canonical user identities through Identity & Access.
- Provides membership and capability information to consuming domains.
- Does not own resource-specific business authorization. Each consuming domain enforces its own operational rules.

For example, Opportunity determines whether an organization possesses the employer capability required to publish an opportunity.

### 4.3 Candidate

**Primary role:** Manages candidate profiles and professional information.

**Upstream dependencies:** Identity & Access.

**Downstream consumers:** Discovery, Application, Career Services, Assistant, Analytics, and Compliance.

**Responsibilities and boundaries:**

- Owns candidate profiles, education, experience, skills, and resumes.
- Associates candidate profiles with canonical user identities.
- Exposes candidate information through defined interfaces and events.
- Does not own application records, discovery results, or career service cases.
- Assistant may consume candidate information and initiate authorized updates but cannot independently modify candidate records.

### 4.4 Agent Identity

**Primary role:** Represents AI agents as independent principals within the platform's authorization model.

**Upstream dependencies:** Identity & Access.

**Downstream consumers:** Assistant, Tool Governance, Application, Opportunity, Candidate, Organization, Communication, Integration, and Compliance.

**Responsibilities and boundaries:**

- Owns agent principals, identities, and delegation relationships.
- Establishes the authority granted to agents by human users or other principals.
- Provides identity and delegation information to Assistant and Tool Governance.
- Enables business domains to evaluate requests against the requesting agent principal and its delegated authority.
- Does not authorize specific tool executions or replace business-domain authorization.

An agent remains a distinct executing principal even when acting on behalf of a human user.

### 4.5 Assistant

**Primary role:** Provides AI assistant capabilities and coordinates agent-driven workflows.

**Upstream dependencies:** Identity & Access, Agent Identity, Candidate, Organization, Opportunity, Discovery, Application, Career Services, Communication, Integration, Tool Governance, and Billing.

**Downstream consumers:** Tool Governance, Candidate, Opportunity, Discovery, Application, Career Services, Communication, Integration, Analytics, and Compliance.

**Responsibilities and boundaries:**

- Owns conversations, assistant memory, and assistant tasks.
- Provides user-facing and agent-facing orchestration.
- Coordinates business operations through the appropriate domain capabilities and governed execution paths.
- Does not own business records created or modified through its actions.
- May retain contextual references, summaries, and derived information from other domains, subject to authorization, provenance, freshness, and retention requirements.
- Must retrieve authoritative information from the owning domain when an operation requires current business state.

For example, Application remains the authoritative owner of an application submitted through Assistant.

Assistant memory must not become an alternative source of authoritative business data.

### 4.6 Tool Governance

**Primary role:** Governs tool availability, authorization, and execution.

**Upstream dependencies:** Identity & Access, Agent Identity, Billing, and tool definitions or execution capabilities provided through Integration where applicable.

**Downstream consumers:** Assistant, Candidate, Organization, Opportunity, Discovery, Application, Career Services, Communication, Integration, and Compliance.

**Responsibilities and boundaries:**

- Owns tool definitions, approval policies, execution policies, and governance records.
- Evaluates execution requests against tool policies, delegated authority, entitlements, and approval requirements.
- Authorizes or rejects governed tool executions.
- Does not own the underlying business operations performed through tools.
- Requires target business domains to independently enforce authorization and validate their own invariants.

Tool Governance and Agent Identity have complementary responsibilities:

- Agent Identity establishes who the agent is and what authority has been delegated.
- Tool Governance determines whether a particular tool execution is permitted.
- The target business domain determines whether the requested business operation is valid and authorized.

Every agent-initiated business operation must pass through Tool Governance before execution.

Assistant may perform explicitly permitted read-only orchestration and access approved contextual interfaces, but must not bypass governed execution for operations that modify business state or access protected resources.

### 4.7 Opportunity

**Primary role:** Manages employment opportunities and their lifecycle.

**Upstream dependencies:** Organization and Identity & Access.

**Downstream consumers:** Discovery, Application, Assistant, Analytics, and Compliance.

**Responsibilities and boundaries:**

- Owns job listings and their lifecycle.
- Validates organizational eligibility and relevant permissions when opportunities are created or managed.
- Exposes opportunity information through defined interfaces and events.
- Does not delegate ownership of opportunity records to Discovery or Application.

Organizations with appropriate capabilities can create and manage opportunities.

### 4.8 Discovery

**Primary role:** Helps candidates discover and evaluate relevant opportunities.

**Upstream dependencies:** Candidate, Opportunity, Organization, and Identity & Access.

**Downstream consumers:** Assistant, Application, Analytics, and Compliance.

**Responsibilities and boundaries:**

- Owns discovery configurations and derived search and matching results.
- Consumes candidate and opportunity information through interfaces or approved projections.
- Provides search, filtering, matching, and ranking capabilities.
- Does not own underlying candidate or opportunity records.
- Treats discovery results as potentially stale and non-authoritative.
- Does not act as an authorization authority for accessing candidate or opportunity records.

Application must independently validate candidate and opportunity state when an application is created.

Search, filtering, matching, and ranking remain within Discovery initially. A separate ML domain may be introduced if model lifecycle management, feature infrastructure, experimentation, or model serving becomes an independently governed capability.

### 4.9 Application

**Primary role:** Manages the application lifecycle between candidates and organizations.

**Upstream dependencies:** Candidate, Opportunity, Organization, Identity & Access, and Agent Identity.

**Downstream consumers:** Communication, Notification, Analytics, Compliance, and Assistant.

**Responsibilities and boundaries:**

- Owns application records and their lifecycle.
- References candidate, opportunity, and organization records without taking ownership of them.
- Validates the conditions required to create, update, submit, and transition applications.
- Enforces its own authorization and business invariants, including for agent-initiated operations.
- Publishes relevant lifecycle events for downstream consumers.

Assistant may initiate application operations through approved capabilities, but Application remains responsible for their execution and validation.

### 4.10 Career Services

**Primary role:** Provides career centre operational capabilities and student support.

**Upstream dependencies:** Identity & Access, Organization, Candidate, Opportunity, and Application.

**Downstream consumers:** Assistant, Communication, Notification, Analytics, and Compliance.

**Responsibilities and boundaries:**

- Owns career service cases, programmes, and support activities.
- Consumes candidate, opportunity, and application information through their owning domains.
- Supports career centre operations and candidate assistance.
- Relies on Organization for membership and career centre capabilities.
- Does not own candidate profiles, opportunity records, or application records.

### 4.11 Communication

**Primary role:** Manages direct and contextual communications between platform participants.

**Upstream dependencies:** Identity & Access, Organization, Candidate, Application, and Career Services.

**Downstream consumers:** Notification, Analytics, and Compliance.

**Responsibilities and boundaries:**

- Owns communication records and conversations.
- May reference applications, candidates, organizations, and career service cases for contextual communication.
- Does not own the underlying business records associated with communications.
- Publishes relevant communication events for downstream consumers.

Notification may consume communication events to inform participants about new messages or communication activity.

### 4.12 Integration

**Primary role:** Provides connectivity and synchronization with external systems.

**Upstream dependencies:** Identity & Access and Agent Identity. Tool execution authorization is supplied through the governed execution context.

**Downstream consumers:** Candidate, Organization, Opportunity, Application, Career Services, Communication, Analytics, and Compliance.

**Responsibilities and boundaries:**

- Owns external connection configurations, credentials, external identifiers, synchronization state, and transport-level mapping infrastructure.
- Provides controlled connectivity to external services and systems.
- Does not automatically become the authoritative owner of imported or exported business information.
- Does not bypass Tool Governance for governed agent-initiated execution.
- Passes external data through receiving domains' approved interfaces.

The receiving business domain owns domain-specific validation and canonicalization rules.

### 4.13 Notification

**Primary role:** Manages notification creation and delivery.

**Upstream dependencies:** Identity & Access, Application, Communication, Career Services, Billing, and Integration.

**Downstream consumers:** Analytics and Compliance.

**Responsibilities and boundaries:**

- Owns notification records and delivery state.
- Consumes relevant domain events and generates notifications for intended recipients.
- Respects recipient preferences, authorization, and communication policies.
- Does not own the business events that trigger notifications.

Delivery failure must not automatically reverse or invalidate the underlying business operation.

### 4.14 Billing

**Primary role:** Manages subscriptions, payments, and platform entitlements.

**Upstream dependencies:** Identity & Access and Organization.

**Downstream consumers:** Assistant, Tool Governance, Notification, Analytics, and Compliance.

**Responsibilities and boundaries:**

- Owns subscription, payment, billing, and entitlement records.
- Maintains the canonical entitlement state.
- Exposes entitlement information to consuming domains.
- Does not directly enforce feature-specific restrictions within other domains.

Assistant and Tool Governance may consume entitlement information when evaluating available capabilities. Each consuming domain remains responsible for enforcing applicable entitlements alongside its own operational constraints.

### 4.15 Analytics

**Primary role:** Provides reporting, metrics, and analytical insights.

**Upstream dependencies:** All domains publishing relevant business events or exposing approved analytical interfaces.

**Downstream consumers:** Assistant, Organization, Candidate, Opportunity, Application, Career Services, Billing, and platform administration.

**Responsibilities and boundaries:**

- Owns derived analytical datasets, metrics, and reports.
- Consumes published events and approved data interfaces into a logically independent analytical store.
- Maintains projections that may be eventually consistent with upstream domains.
- Respects applicable access restrictions, privacy, and data-handling requirements.
- Must not serve as the source of truth for operational decisions requiring authoritative current state.
- Must not query operational database internals as its integration contract.

A dedicated event or analytical data platform may be introduced when volume and reporting requirements justify it.

### 4.16 Compliance

**Primary role:** Provides governance, auditability, and compliance oversight.

**Upstream dependencies:** Identity & Access, Organization, Agent Identity, Assistant, Tool Governance, Candidate, Opportunity, Discovery, Application, Career Services, Communication, Integration, Notification, Billing, and Analytics.

**Downstream consumers:** Platform administration and relevant business domains requiring compliance policies or audit evidence.

**Responsibilities and boundaries:**

- Owns audit records, compliance policies, and evidence required for oversight.
- Establishes governance requirements affecting relevant domains.
- Does not become the authoritative owner of the business entities being audited.
- Relies on business domains to enforce their own authorization and invariants.
- Provides centralized oversight while maintaining distributed enforcement at the appropriate domain boundaries.

## 5. Domain Dependency Map

### 5.1 Dependency Overview

The following relationships represent primary architectural dependencies and consumers, not every possible interaction.

| Upstream Domain | Downstream Domain | Dependency |
|---|---|---|
| Identity & Access | All relevant domains | User identity and access |
| Organization | Opportunity, Application, Discovery, Career Services, Communication | Organizational identity, membership, and capabilities |
| Candidate | Discovery, Application, Career Services, Assistant | Candidate information |
| Agent Identity | Assistant, Tool Governance, Application, Opportunity, Integration | Agent identity and delegated authority |
| Assistant | Tool Governance | Tool execution requests |
| Tool Governance | Integration and relevant business domains | Governed execution authorization |
| Opportunity | Discovery, Application, Assistant | Opportunity information |
| Discovery | Assistant, Application | Search and matching results |
| Application | Communication, Notification, Analytics | Application records and lifecycle events |
| Career Services | Communication, Notification, Analytics | Career service context and events |
| Communication | Notification | Communication events |
| Integration | Relevant business domains | External connectivity and synchronization |
| Billing | Assistant, Tool Governance | Entitlement information |
| All relevant domains | Analytics | Analytical information |
| All relevant domains | Compliance | Audit and compliance evidence |

A dependency does not necessarily imply a direct synchronous interaction. The relevant domain contracts and workflows determine the appropriate mechanism.

### 5.2 Dependency Direction

Dependencies should flow toward the domain owning the required capability or information.

For example:

- Application depends on Candidate for candidate information, not vice versa.
- Discovery depends on Opportunity for opportunity information, not vice versa.
- Notification consumes Application and Communication events without becoming an operational dependency of either.
- Analytics consumes domain information without becoming an operational dependency for authoritative business decisions.

This direction preserves ownership and limits coupling.

## 6. Cross-Domain Interaction Patterns

### 6.1 Synchronous Domain Interfaces

Use synchronous interfaces when a consuming domain requires an authoritative response before completing an operation.

Examples:

- Application validating candidate information and opportunity eligibility.
- Opportunity verifying organizational capabilities.
- Tool Governance evaluating execution permissions.
- Business domains validating incoming agent authorization.

Synchronous interactions should be limited to information or operations necessary for the current business transaction.

### 6.2 Domain Events

Use domain events to communicate completed business state changes to interested consumers.

Examples:

| Producing Domain | Event Example | Potential Consumers |
|---|---|---|
| Identity & Access | UserRegistered | Organization, Candidate, Notification, Compliance |
| Identity & Access | UserEmailVerified | Notification, Compliance |
| Organization | OrganizationCreated | Analytics, Compliance |
| Organization | MembershipChanged | Opportunity, Career Services, Compliance |
| Candidate | CandidateProfileUpdated | Discovery, Analytics, Compliance |
| Candidate | ResumeUpdated | Discovery, Assistant, Analytics |
| Agent Identity | AgentDelegationGranted | Assistant, Tool Governance, Compliance |
| Agent Identity | AgentDelegationRevoked | Assistant, Tool Governance, Compliance |
| Tool Governance | ToolExecutionAuthorized | Assistant, Compliance |
| Tool Governance | ToolExecutionDenied | Assistant, Compliance |
| Opportunity | OpportunityPublished | Discovery, Notification, Analytics |
| Opportunity | OpportunityClosed | Discovery, Application, Analytics |
| Application | ApplicationSubmitted | Communication, Notification, Analytics, Compliance |
| Application | ApplicationStatusChanged | Communication, Notification, Analytics |
| Career Services | CareerServiceCaseCreated | Notification, Analytics, Compliance |
| Communication | MessageSent | Notification, Analytics, Compliance |
| Integration | SynchronizationCompleted | Relevant business domains, Analytics, Compliance |
| Billing | SubscriptionChanged | Assistant, Tool Governance, Notification, Analytics |
| Billing | PaymentFailed | Notification, Analytics, Compliance |

These are illustrative event names, not a finalized event catalog.

Individual domain contracts and the centralized event catalog must define event schemas, ownership, delivery guarantees, versioning, and consumers.

### 6.3 Read Models and Projections

Domains may maintain local read models when information from other contexts is required for performance, availability, or operational purposes.

Examples:

- Discovery maintains searchable candidate and opportunity representations.
- Analytics maintains cross-domain analytical datasets.
- Assistant maintains contextual references and relevant memory.
- Career Services may maintain operational views of candidates and applications.

Each projection must define:

- Authoritative source domain.
- Synchronization mechanism and freshness expectations.
- Handling of missing, stale, or deleted records.
- Authorization and data-retention requirements.
- Deletion and lifecycle behaviour.

Projections remain non-authoritative. Operations requiring current business state must validate against the owning domain.

### 6.4 Avoiding Direct Database Access

Domains must not directly query or modify another domain's internal database tables as an integration mechanism.

Cross-domain interactions must use:

- Explicit domain interfaces.
- Published domain events.
- Approved read APIs or query interfaces.
- Well-defined projections.

Internal database structures must not become implicit integration contracts.

## 7. Cross-Domain Workflow Examples

The following workflows illustrate how bounded contexts collaborate to deliver BottomUp's primary capabilities. Detailed business processes belong in individual workflow specifications.

### 7.1 User Registration and Onboarding

**Participating domains:** Identity & Access, Organization, Candidate, Notification, Compliance.

**Interaction sequence:**

1. Identity & Access receives and validates the registration request.
2. Identity & Access creates the user and associated authentication credentials.
3. Identity & Access records required policy acceptance.
4. Identity & Access initiates email verification.
5. Notification delivers the verification message.
6. Identity & Access activates the user after successful verification.
7. The relevant profile or organizational onboarding process proceeds according to the selected persona.

**Ownership boundaries:**

- Identity & Access owns registration, authentication, and user activation.
- Organization owns organizational onboarding and membership.
- Candidate owns candidate profile creation and management.
- Compliance owns relevant audit evidence.

### 7.2 Candidate Profile Management

**Participating domains:** Identity & Access, Candidate, Assistant, Discovery, Analytics, Compliance.

**Interaction sequence:**

1. Identity & Access establishes the authenticated user.
2. Candidate identifies the corresponding candidate profile.
3. Candidate validates and persists profile changes.
4. Candidate publishes relevant profile update events.
5. Discovery updates its candidate representations.
6. Analytics updates applicable analytical projections.
7. Compliance retains required audit evidence.

Assistant may help candidates prepare or improve profile information through authorized operations.

Candidate remains the sole authoritative owner of the profile.

### 7.3 Opportunity Creation and Publication

**Participating domains:** Identity & Access, Organization, Opportunity, Notification, Discovery, Analytics, Compliance.

**Interaction sequence:**

1. Identity & Access establishes the requesting principal.
2. Organization establishes the relevant membership and capabilities.
3. Opportunity validates the operation and organizational eligibility.
4. Opportunity creates and manages the opportunity record.
5. Opportunity publishes an event when the opportunity becomes available.
6. Discovery updates its searchable opportunity representation.
7. Notification informs relevant recipients where appropriate.
8. Analytics updates relevant reporting data.

### 7.4 Opportunity Discovery and Matching

**Participating domains:** Candidate, Opportunity, Organization, Discovery, Assistant, Analytics.

**Interaction sequence:**

1. Discovery obtains candidate information through Candidate interfaces or approved projections.
2. Discovery obtains opportunity information through Opportunity interfaces or approved projections.
3. Discovery performs search, filtering, and matching.
4. Discovery returns results to the requesting user or Assistant.
5. Assistant may use the results to support subsequent actions.
6. Analytics records relevant discovery activity where permitted.

Discovery owns the search and matching process, not the underlying records.

### 7.5 Job Application Submission

**Participating domains:** Identity & Access, Agent Identity, Candidate, Opportunity, Organization, Application, Assistant, Tool Governance, Communication, Notification, Analytics, Compliance.

**Interaction sequence:**

1. A user or agent initiates an application operation.
2. Agent Identity establishes the requesting principal and delegated authority for agent-initiated operations.
3. Tool Governance evaluates the requested execution, including policy and approval requirements.
4. Application receives the request with the appropriate principal and authorization context.
5. Application validates candidate information, opportunity eligibility, and its own business invariants.
6. Application creates and submits the application.
7. Application publishes relevant lifecycle events.
8. Communication and Notification process downstream interactions.
9. Analytics updates application metrics.
10. Compliance retains required audit evidence.

Application remains responsible for validating and executing the application operation.

### 7.6 Agent-Executed Operations

**Participating domains:** Assistant, Agent Identity, Tool Governance, Integration, relevant business domains, Compliance.

**Interaction sequence:**

1. Assistant determines the requested operation.
2. Agent Identity establishes the agent principal and delegation context.
3. Tool Governance evaluates the tool, policies, permissions, entitlements, and approval requirements.
4. Approved execution is dispatched through the relevant tool or Integration capability.
5. The target business domain receives the request under the agent's identity.
6. The target domain independently validates authorization and business invariants.
7. The target domain executes or rejects the operation.
8. The result is returned to Assistant.
9. Relevant execution and business events are recorded for auditability.

**Authorization boundary:**

The human user and executing agent are distinct principals. The agent must not impersonate the user or inherit unrestricted user permissions.

The user's delegated authority establishes the basis for permitted actions, but the agent remains the executing identity.

### 7.7 Career Centre Operations

**Participating domains:** Identity & Access, Organization, Candidate, Opportunity, Application, Career Services, Communication, Notification, Analytics, Compliance.

**Interaction sequence:**

1. Identity & Access establishes the user.
2. Organization establishes membership and relevant career centre capabilities.
3. Career Services provides the relevant operational capabilities.
4. Career Services consumes candidate, opportunity, and application information through their owning domains.
5. Career Services manages its own cases, programmes, and support activities.
6. Communication supports contextual interactions.
7. Notification delivers relevant updates.
8. Analytics provides operational reporting.

Career Services does not assume ownership of candidate or application records because career centre personnel can access them.

### 7.8 Subscription and Entitlement Management

**Participating domains:** Identity & Access, Organization, Billing, Assistant, Tool Governance, Notification, Analytics, Compliance.

**Interaction sequence:**

1. Identity & Access establishes the user or requesting principal.
2. Organization establishes the relevant organizational context where applicable.
3. Billing manages subscription and payment operations.
4. Billing determines the applicable entitlements.
5. Assistant and Tool Governance consume entitlement information when evaluating available capabilities.
6. Notification delivers relevant subscription and payment updates.
7. Analytics updates billing metrics.
8. Compliance retains relevant audit evidence.

Billing owns entitlement records. Consuming domains enforce restrictions applicable to their own capabilities.

## 8. Data Ownership and Reference Rules

### 8.1 Authoritative Ownership and References

Each domain owns and maintains its authoritative business records.

Consuming domains may reference externally owned records through globally unique identifiers.

Cross-domain identifiers must:

- Be globally unique within the platform.
- Be treated as opaque references.
- Not expose assumptions about another domain's internal identifier format.

Examples:

- Application references Candidate and Opportunity identifiers.
- Opportunity references an Organization identifier.
- Candidate references a User identifier.
- Agent Identity references an associated User identifier where applicable.
- Communication may reference an Application or Career Service case identifier.

### 8.2 Denormalized Information

Domains may retain snapshots or projections of external information for performance, historical accuracy, or operational resilience.

Such information must have a defined purpose, authoritative source, and lifecycle.

The owning domain remains authoritative for current state. Historical snapshots must not silently become current authoritative records.

### 8.3 Deletion and Retention

Cross-domain deletion must respect ownership, dependencies, legal obligations, and retention requirements.

- A domain must not independently delete records owned by another domain.
- The owning domain controls deletion, deactivation, and lifecycle transitions.
- Where changes affect other domains, the owner should publish appropriate events or expose controlled operations.
- Consumers must define how they handle resulting changes.
- Prefer deactivation or soft deletion where historical references must remain valid.
- Hard deletion must respect applicable privacy and retention obligations.

## 9. Consistency and Failure Handling

### 9.1 Strong Consistency

Maintain transactional consistency within a domain wherever its business invariants require it.

Distributed operations across multiple domains must not be assumed to form a single database transaction.

### 9.2 Eventual Consistency

Cross-domain projections and asynchronous consumers may be eventually consistent.

Consumers must account for propagation delays. Operations requiring authoritative current state must validate against the owning domain.

### 9.3 Idempotency

Retryable cross-domain operations must define idempotency behaviour, particularly:

- Application submission.
- Payment processing.
- External synchronization.
- Notification delivery.
- Agent tool execution.

### 9.4 Failure Isolation

A downstream failure must not automatically invalidate a successfully completed upstream business operation.

For example:

- Notification failure must not reverse application submission.
- Analytics failure must not block candidate profile updates.
- Delayed Discovery projections must not invalidate opportunity publication.

### 9.5 Distributed Workflows

Cross-domain workflows involving multiple independent operations must define:

- Execution sequence and preconditions.
- Success and failure conditions.
- Retry and timeout behaviour.
- Compensation where necessary.
- Audit requirements.

Use explicit orchestration for workflows requiring important sequencing, conditional branching, authorization checkpoints, or compensation.

Use event-driven choreography for simpler downstream reactions, such as analytics updates and notification generation.

Avoid introducing a universal workflow orchestrator that becomes a central owner of business logic.

## 10. Architectural Constraints

The following constraints apply to all domains:

1. Every authoritative entity must have exactly one owning domain.
2. Domains must not directly modify another domain's authoritative data.
3. Cross-domain dependencies and interfaces must be explicitly defined.
4. Circular domain dependencies must be avoided.
5. Cross-domain interactions must follow defined contracts.
6. Domain events must be published by the domain owning the underlying business state.
7. Consumers must account for asynchronous delivery and eventual consistency.
8. Projections and snapshots must not become competing sources of truth.
9. Authorization must be enforced by the domain responsible for the requested operation.
10. Agent operations must use agent identity and delegated authority, not human-user impersonation.
11. Tool Governance approval does not replace target-domain authorization.
12. Integration must not bypass domain ownership or business invariants.
13. Analytics must remain non-authoritative and use approved data interfaces.
14. Compliance must not become the owner of business data simply because it audits that data.
15. Receiving domains own their business validation and canonicalization rules.
16. Cross-domain workflows must define consistency, failure recovery, and audit requirements.
17. Internal database schemas and implementation details must not become implicit integration contracts.
18. Entitlement restrictions must be enforced within the consuming domain.

## 11. Evolution and Maintenance

Update this document when:

- A bounded context is introduced, split, merged, or reorganized.
- Domain responsibilities or authoritative ownership change.
- Cross-domain dependencies are introduced or removed.
- Domain interfaces or event contracts change materially.
- Architectural decisions change the integration model.

Cross-domain changes must be reflected in affected domain contracts and architectural decision records.

Domain owners must identify downstream consumers before changing exposed contracts.

The architecture owner is responsible for resolving cross-domain ownership conflicts and maintaining consistency across architectural documents.

**Document status:** Draft

**Related documents:**
- `DOMAIN_ARCHITECTURE.md`
- `CROSS_DOMAIN_AUTHORIZATION.md`
- `domains/DOMAIN_CONTRACT_TEMPLATE.md`
- `domains/FEATURE_TEMPLATE.md`
- `decisions/TEMPLATE.md`