---
id: opportunity
name: Opportunity
type: domain-contract
status: draft
version: 1.0.0
owner: opportunity
---

# Opportunity Domain Contract

## 1. Purpose

The Opportunity domain manages the creation, management, and publication lifecycle of career opportunities on Bottom Up.

It provides the platform's authoritative source of truth for opportunities such as:

- Internships
- Full-time jobs
- Part-time jobs
- Graduate programmes
- Other early-career opportunities supported by the platform

The domain enables employers to publish and manage opportunities while ensuring that students and other authorised users can access accurate, relevant, and trustworthy opportunity information.

The domain supports Bottom Up's initial product focus on discovery by making opportunity information structured, consistent, and available to the Discovery domain.

Its primary responsibility is to ensure that opportunities are properly managed throughout their lifecycle, from creation to closure or archival.

**Core principle: Opportunity owns the opportunity record and its lifecycle. Other domains consume opportunity information through defined interfaces and events.**

## 2. Scope & Responsibilities

### 2.1 In Scope

The Opportunity domain is responsible for:

- Creating and managing opportunity records.
- Supporting different opportunity types, including internships and jobs.
- Managing opportunity descriptions and structured attributes.
- Managing employment details, such as work arrangement, location, duration, and compensation information where applicable.
- Managing application-related information and requirements displayed on an opportunity.
- Managing opportunity ownership and organisational association.
- Managing opportunity publication and visibility.
- Managing opportunity lifecycle states.
- Publishing domain events when opportunities are created, updated, published, closed, or otherwise change lifecycle state.
- Providing authoritative opportunity information to other domains.
- Supporting validation of opportunity information before publication.
- Supporting authorised updates and withdrawal of opportunities.
- Maintaining the integrity and consistency of opportunity records.

### 2.2 Out of Scope

The following responsibilities belong to other domains:

| Responsibility | Owning domain |
|---|---|
| Employer organisation and membership management | Organization |
| User authentication and central permission evaluation | Identity & Access |
| Candidate profiles, resumes, skills, and preferences | Candidate |
| Agent identity and delegation lifecycle | Agent Identity |
| AI conversations and assistant orchestration | Assistant |
| Tool permissions, risk policies, and tool execution governance | Tool Governance |
| Opportunity search, indexing, ranking, and recommendations | Discovery |
| Application submissions and recruitment pipelines | Application |
| School career-centre workflows and career programmes | Career Services |
| Human-to-human conversations | Communication |
| External job-board connectors and synchronisation | Integration |
| Notification delivery | Notification |
| Subscription plans, entitlements, and usage limits | Billing |
| Analytical reporting and derived metrics | Analytics |
| Audit evidence, consent, and retention policies | Compliance |

### 2.3 Boundary Principles

1. Opportunity is the authoritative source of truth for opportunity records.
2. Other domains must not directly access or modify the Opportunity database.
3. Discovery may maintain its own search index or read model, but Opportunity remains authoritative.
4. Application may reference an opportunity, but does not own or modify its listing details.
5. Organization owns organisation records and memberships. Opportunity stores the relevant organisation reference rather than duplicating organisation ownership data.
6. Opportunity must not independently implement or replace the platform's central authorization service.
7. External opportunity sources must be handled through the Integration domain rather than introducing direct dependencies on external systems.

## 3. Domain Model

### 3.1 Core Entities

#### Opportunity

The primary aggregate root representing a job, internship, graduate programme, or other supported career opportunity.

Potential attributes:

- `id`
- `organization_id`
- `title`
- `description`
- `opportunity_type`
- `employment_type`
- `work_arrangement`
- `location`
- `department` (optional)
- `industry` (optional)
- `required_skills`
- `preferred_skills`
- `requirements`
- `responsibilities`
- `qualifications`
- `compensation` (optional)
- `start_date` (optional)
- `end_date` (optional)
- `application_deadline` (optional)
- `application_instructions`
- `application_method`
- `status`
- `published_at` (optional)
- `closed_at` (optional)
- `created_by`
- `updated_by`
- `created_at`
- `updated_at`

The exact attributes and data types should be finalised in the Opportunity data model specification.

#### Opportunity Type

A classification of the kind of career opportunity.

Initial proposed values:

- `INTERNSHIP`
- `FULL_TIME`
- `PART_TIME`
- `GRADUATE_PROGRAMME`

The domain should allow additional types to be introduced without requiring changes to unrelated domain logic.

#### Opportunity Location

Represents where an opportunity is based.

Potential attributes:

- Country
- State or region
- City
- Address (optional)
- Work arrangement

Work arrangement may be represented separately as an enumerated value:

- `ONSITE`
- `HYBRID`
- `REMOTE`

#### Compensation

Represents compensation information associated with an opportunity.

Potential attributes:

- Minimum amount
- Maximum amount
- Currency
- Compensation period (hourly, monthly, annually, or other supported period)
- Whether compensation is disclosed

Compensation should be optional because employers may choose not to disclose it.

#### Opportunity Requirement

Represents a requirement or qualification associated with an opportunity.

Potential information includes:

- Requirement description
- Requirement category
- Whether it is mandatory or preferred

The domain should distinguish required qualifications from preferred qualifications.

### 3.2 Proposed Aggregate Boundary

**Opportunity** should initially be the primary aggregate root.

An opportunity's core information, ownership reference, publication state, and lifecycle should be managed consistently through this aggregate.

Related information should only become separate aggregates when independent lifecycle or consistency requirements justify doing so.

For the initial implementation, avoid unnecessary aggregate complexity.

### 3.3 Value Objects

Potential value objects include:

- `OpportunityTitle`
- `OpportunityDescription`
- `Compensation`
- `OpportunityLocation`
- `ApplicationDeadline`
- `EmploymentPeriod`
- `OpportunityRequirement`

Value objects should enforce their own validation rules where appropriate.

## 4. Capabilities

### 4.1 Opportunity Creation

Allows authorised employer representatives to create new opportunities.

Capabilities include:

- Creating an opportunity.
- Associating it with an organisation.
- Specifying the opportunity type.
- Providing the job description and requirements.
- Providing employment and location details.
- Specifying application instructions and deadlines.

### 4.2 Opportunity Management

Allows authorised users to manage existing opportunities.

Capabilities include:

- Retrieving opportunity details.
- Updating opportunity information.
- Updating employment details.
- Updating application requirements and instructions.
- Updating deadlines.
- Withdrawing opportunities.
- Closing opportunities.

### 4.3 Opportunity Publication

Manages whether an opportunity is visible and available to the platform.

Capabilities include:

- Validating publication requirements.
- Publishing an opportunity.
- Unpublishing or withdrawing an opportunity.
- Managing opportunity visibility.
- Recording publication timestamps.
- Preventing invalid opportunities from being published.

### 4.4 Opportunity Lifecycle Management

Manages the transition of an opportunity between lifecycle states.

Capabilities include:

- Managing draft opportunities.
- Publishing opportunities.
- Closing opportunities.
- Archiving opportunities.
- Handling expired opportunities.
- Preventing invalid lifecycle transitions.

### 4.5 Opportunity Information Retrieval

Provides authoritative opportunity information to authorised users and consuming domains.

Capabilities include:

- Retrieving an opportunity by ID.
- Retrieving opportunities belonging to an organisation.
- Retrieving published opportunities.
- Retrieving opportunities by lifecycle state.
- Providing opportunity information to Discovery and Application through defined interfaces.

## 5. Commands

Commands represent requests to change the state of the Opportunity domain.

| Command | Description |
|---|---|
| `CreateOpportunity` | Creates a new opportunity. |
| `UpdateOpportunity` | Updates an existing opportunity's details. |
| `DeleteDraftOpportunity` | Deletes an opportunity that has not been published, subject to lifecycle rules. |
| `PublishOpportunity` | Publishes an eligible opportunity. |
| `UnpublishOpportunity` | Removes an opportunity from public visibility without necessarily closing it. |
| `CloseOpportunity` | Closes an opportunity and prevents further applications through supported platform workflows. |
| `ArchiveOpportunity` | Archives an opportunity that is no longer active. |
| `ExtendApplicationDeadline` | Changes the application deadline where permitted. |
| `ReopenOpportunity` | Reopens a previously closed opportunity if permitted by policy. |

### 5.1 Command Behaviour

Commands should:

- Validate the requested state transition.
- Enforce domain business rules.
- Verify the actor's authority through Identity & Access.
- Verify resource ownership and organisational context.
- Persist changes within the Opportunity domain.
- Emit appropriate domain events after successful state changes.
- Support idempotency where commands may be retried.
- Record relevant actor and correlation information for auditability.

A command must not report success if its state change has failed.

## 6. Queries

Queries retrieve information without changing domain state.

| Query | Description |
|---|---|
| `GetOpportunity` | Retrieves an opportunity by ID. |
| `GetOpportunitiesByOrganization` | Retrieves opportunities associated with an organisation. |
| `GetPublishedOpportunity` | Retrieves an opportunity that is currently published and visible. |
| `GetOpportunitiesByStatus` | Retrieves opportunities filtered by lifecycle status. |
| `GetOpportunityDetails` | Retrieves the full authorised opportunity details. |
| `GetOpportunityPublicationStatus` | Retrieves the current publication state. |

Queries should respect access-control rules. Draft and unpublished opportunities must not be exposed to unauthorised users.

Discovery may use a separate projection or search index for search and filtering. It should not use the Opportunity database as a directly accessible search store.

## 7. Business Rules & Invariants

### 7.1 Opportunity Creation

1. Every opportunity must have a unique identifier.
2. Every opportunity must be associated with a valid organisation or another explicitly supported owner.
3. An opportunity must have a title and sufficient descriptive information.
4. An opportunity must have a recognised opportunity type.
5. An opportunity must be created by an authenticated and authorised principal.
6. The organisation associated with an opportunity must be valid and accessible within the actor's authorised organisational context.

### 7.2 Opportunity Updates

1. Only authorised principals may modify an opportunity.
2. An actor must have the appropriate permissions within the organisation associated with the opportunity.
3. Updating an opportunity must not silently change its ownership.
4. Updates must preserve the integrity of required fields.
5. Changes to published opportunities must be reflected in downstream consumers through domain events.
6. An update must not bypass lifecycle restrictions.

### 7.3 Publication

1. An opportunity must satisfy publication requirements before it can be published.
2. A draft opportunity must not be publicly discoverable.
3. Only authorised principals may publish an opportunity.
4. A published opportunity must contain sufficient information for a student to understand the role and its requirements.
5. Publication must record the relevant publication timestamp.
6. Unpublishing an opportunity must remove it from active discovery without necessarily deleting its record.
7. A published opportunity must not remain discoverable after it has been closed or expired.

### 7.4 Opportunity Lifecycle

The following is a proposed initial lifecycle:

`DRAFT → PUBLISHED → CLOSED → ARCHIVED`

Additional transitions:

- `PUBLISHED → DRAFT` through unpublishing, if permitted.
- `CLOSED → PUBLISHED` through reopening, if permitted.
- `DRAFT → DELETED` where deletion rules allow it.

Lifecycle rules:

1. Only valid state transitions are permitted.
2. A closed opportunity must not accept new applications through the platform.
3. An archived opportunity must not be publicly discoverable.
4. Expired opportunities must not remain active.
5. Lifecycle transitions must be recorded.
6. Historical opportunity information should be retained according to the platform's retention and compliance requirements.

The exact lifecycle and reopening rules require confirmation before implementation.

### 7.5 Application-Related Rules

1. Opportunity owns the application instructions and requirements displayed on the listing.
2. Application owns the actual application submission and recruitment process.
3. Opportunity must provide Application with the relevant opportunity information through defined interfaces or events.
4. Closing an opportunity must be communicated to Application so that its application workflow can enforce the appropriate restrictions.
5. Opportunity must not directly create, modify, or manage application records.

### 7.6 Data Integrity

1. Opportunity is the authoritative source for its own records.
2. Downstream projections must not become alternative sources of truth.
3. Domain events must reflect successfully committed state changes.
4. Repeated event processing must not cause unintended duplicate effects.
5. Invalid or unauthorised updates must fail without partially changing the aggregate.

## 8. Domain Events

Domain events communicate meaningful changes in Opportunity state to other domains.

| Event | Description | Potential consumers |
|---|---|---|
| `OpportunityCreated` | An opportunity has been created. | Analytics, Compliance |
| `OpportunityUpdated` | An opportunity's details have changed. | Discovery, Application, Analytics |
| `OpportunityPublished` | An opportunity has been published and is available for discovery. | Discovery, Notification, Analytics |
| `OpportunityUnpublished` | An opportunity has been removed from public visibility. | Discovery, Analytics |
| `OpportunityClosed` | An opportunity has been closed. | Discovery, Application, Notification, Analytics |
| `OpportunityArchived` | An opportunity has been archived. | Discovery, Analytics |
| `OpportunityDeadlineChanged` | An opportunity's application deadline has changed. | Discovery, Application, Notification |
| `OpportunityReopened` | A previously closed opportunity has been reopened. | Discovery, Application, Notification |

### 8.1 Event Requirements

Events should include the relevant metadata:

- Event ID
- Event type
- Event version
- Opportunity ID
- Organisation ID
- Timestamp
- Actor principal ID and principal type, where applicable
- Correlation ID
- Causation ID, where applicable

Events should include sufficient information for consumers to understand the change or retrieve the authoritative record.

Events must not expose sensitive or unnecessary information.

### 8.2 Event Delivery

1. Events should be emitted only after successful state changes.
2. Event delivery should support retries.
3. Consumers must handle duplicate delivery idempotently.
4. Event ordering should be considered for lifecycle transitions.
5. Failed downstream processing must not corrupt the Opportunity domain's transactional state.
6. An outbox pattern is a proposed approach for reliable publication of events alongside database transactions.

## 9. Authorization Requirements

Opportunity follows the platform-wide Cross-Domain Authorization Specification.

### 9.1 Principals

Supported principal types:

- User
- Agent
- System

The acting principal must remain explicit throughout every operation.

An agent must not impersonate the human who delegated authority to it.

### 9.2 Permission Requirements

Proposed permission identifiers:

| Permission | Description |
|---|---|
| `opportunity.create` | Create opportunities. |
| `opportunity.read` | Read opportunity information. |
| `opportunity.update` | Update opportunity information. |
| `opportunity.delete` | Delete eligible draft opportunities. |
| `opportunity.publish` | Publish opportunities. |
| `opportunity.unpublish` | Unpublish opportunities. |
| `opportunity.close` | Close opportunities. |
| `opportunity.archive` | Archive opportunities. |
| `opportunity.reopen` | Reopen closed opportunities. |
| `opportunity.manage.organization` | Manage opportunities within an authorised organisation scope. |

These are proposed identifiers and must be aligned with the central permission registry.

### 9.3 Resource Scope

Opportunity operations may use the following scopes:

- **Individual scope:** A user accesses opportunities they are explicitly permitted to manage.
- **Organization scope:** An authorised organisation member manages opportunities belonging to that organisation.
- **Resource scope:** Access is evaluated against a specific opportunity.
- **System scope:** Narrowly authorised system operations, such as scheduled lifecycle processing.

### 9.4 Authorization Rules

1. An employer representative must have appropriate permissions within the organisation associated with the opportunity.
2. Organisation membership and role assignments are owned by Organization.
3. Opportunity must not maintain its own competing source of truth for organisational roles or memberships.
4. A user must not gain access to another organisation's opportunities merely by knowing an opportunity ID.
5. Publicly published opportunities may be readable by users who are permitted to access public listings.
6. Draft, unpublished, and restricted opportunities require appropriate access.
7. Agent operations require valid agent identity, delegation authority, scope, and any applicable Tool Governance approval.
8. Authorization must be evaluated again before consequential operations.
9. Indeterminate authorization decisions must fail closed.
10. System principals must have narrowly scoped permissions.

### 9.5 Resource-Level Enforcement

Identity & Access evaluates central permissions, while Opportunity enforces resource-specific business rules.

For example, having `opportunity.update` does not automatically allow a user to update every opportunity. The domain must verify that the target opportunity belongs to an organisation within the actor's authorised scope.

## 10. Cross-Domain Dependencies

| Domain | Dependency | Interaction |
|---|---|---|
| Identity & Access | Authorization evaluation and permission definitions | Authorization interface |
| Organization | Organisation records, memberships, and roles | Organisation references and domain interfaces/events |
| Agent Identity | Agent principal identity and lifecycle | Agent identity and delegation context |
| Tool Governance | Tool execution policies and approvals | Authorization/governance decisions for agent-initiated actions |
| Discovery | Published opportunity information for search and recommendations | Domain events and read projections |
| Application | Opportunity information and availability for application workflows | Domain interfaces and events |
| Candidate | No direct ownership dependency | Candidate information is not stored as part of Opportunity |
| Integration | External opportunity imports and synchronisation | Integration-owned connectors and validated inbound data |
| Notification | Publication, deadline, and closure notifications | Domain events |
| Analytics | Opportunity lifecycle and outcome-related reporting | Domain events and analytical projections |
| Compliance | Audit evidence, privacy, and retention requirements | Audit events and compliance interfaces |
| Billing | Applicable publication entitlements or usage limits, if required | Entitlement evaluation through Billing |

### 10.1 Dependency Rules

1. Opportunity must not access another domain's database directly.
2. Opportunity must not own organisation membership, candidate profile, application, or billing data.
3. Cross-domain interactions must use defined interfaces, events, or projections.
4. Dependencies must be explicit and documented.
5. Downstream consumers must tolerate eventual consistency.
6. Opportunity must remain operationally isolated from failures in non-critical downstream consumers.
7. Where an external dependency is required to authorise a consequential operation, failure must not silently grant permission.

## 11. External Integrations

### 11.1 External Job Platforms

Opportunity does not directly own external platform connections.

External job listing imports and synchronisation should be handled by Integration.

Potential workflows:

- Importing opportunities from external sources.
- Mapping external fields to Bottom Up's opportunity model.
- Validating imported opportunity information.
- Tracking external source identifiers.
- Updating or retiring imported listings.
- Handling duplicate opportunities.

Imported opportunities must pass the relevant validation and publication rules before becoming publicly discoverable.

### 11.2 AI and Agent-Assisted Opportunity Management

Agents may assist employers with:

- Drafting opportunity descriptions.
- Suggesting improvements to listing completeness.
- Preparing structured opportunity information.
- Updating opportunity details when authorised.

However:

1. The agent must act as its own principal.
2. Delegated authority must be valid and within scope.
3. Tool Governance must evaluate applicable tool policies and risk.
4. Opportunity must independently enforce its business rules.
5. Publishing, closing, or otherwise consequential actions must receive the required authorization and approvals.
6. The agent must not bypass the normal opportunity lifecycle.

Agent-assisted workflows are a future capability and should not complicate the initial implementation unnecessarily.

## 12. Data Ownership & Lifecycle

### 12.1 Ownership

Opportunity owns:

- Opportunity records.
- Opportunity descriptions and structured details.
- Opportunity type classifications.
- Employment and location details recorded on opportunities.
- Opportunity requirements.
- Opportunity publication status.
- Opportunity lifecycle state.
- Opportunity-specific metadata and timestamps.

Opportunity references but does not own:

- Organisation records and memberships.
- User and agent identities.
- Candidate profiles.
- Application records.
- External connector credentials.
- Subscription entitlements.

### 12.2 Data Lifecycle

Proposed lifecycle:

1. An authorised actor creates an opportunity.
2. The opportunity is stored as a draft.
3. The employer completes and validates the listing.
4. An authorised actor publishes it.
5. Opportunity emits a publication event.
6. Discovery updates its search projection.
7. The opportunity remains active until it is closed, withdrawn, or expires.
8. The opportunity is eventually archived according to lifecycle and retention rules.

### 12.3 Data Retention

Opportunity records should not be physically deleted by default after publication.

Historical information may be required for:

- Application records.
- Employer reporting.
- Analytics.
- Audit and compliance.
- Platform integrity.

Retention and deletion policies must follow Compliance requirements.

## 13. Non-Functional Requirements

### 13.1 Security

- All protected operations must require authorization.
- Sensitive information must be protected in transit and at rest.
- Resource-level access must be enforced.
- Agent actions must retain explicit principal and delegation context.
- Unauthorized cross-organisation access must be denied.

### 13.2 Performance

- Opportunity retrieval should support responsive user experiences.
- Publication and update operations should avoid unnecessary synchronous dependencies.
- Search and filtering workloads should be handled primarily by Discovery rather than placing excessive query load on Opportunity.

### 13.3 Availability

- Core opportunity creation, retrieval, and lifecycle operations should remain available independently of non-critical downstream consumers where possible.
- Downstream event delivery failures must not invalidate successfully committed opportunity changes.

### 13.4 Scalability

- Opportunity records should support growth in employers, listings, and listing updates.
- Event publication should support increasing numbers of downstream consumers.
- Read-heavy discovery workloads should be served through appropriate projections.

### 13.5 Reliability

- Commands should support safe retries where appropriate.
- Events should be delivered reliably.
- Consumers should process duplicate events safely.
- Lifecycle transitions must be consistent.
- Partial failures must not leave opportunities in invalid states.

### 13.6 Privacy

- Only necessary personal information should be stored.
- Opportunity records should not contain candidate personal data.
- Data retention and deletion must comply with Compliance requirements.

## 14. Testing Requirements

### 14.1 Unit Tests

Test:

- Opportunity creation validation.
- Opportunity update validation.
- Opportunity type validation.
- Publication requirements.
- Lifecycle transitions.
- Deadline validation.
- Ownership and organisation association rules.
- Invalid state transitions.

### 14.2 Integration Tests

Test:

- Identity & Access authorization integration.
- Organization membership and scope validation.
- Opportunity event publication.
- Discovery projection updates.
- Application integration when an opportunity is closed or reopened.
- Billing entitlement evaluation, if required.
- Integration workflows for externally imported opportunities.

### 14.3 Contract Tests

Test:

- Command and query interfaces.
- Domain event schemas.
- Event version compatibility.
- Consumer expectations.
- Authorization context propagation.
- Cross-domain interface compatibility.

### 14.4 Security Tests

Test:

- Unauthorized opportunity creation.
- Cross-organisation access attempts.
- Unauthorized updates and publication.
- Access to unpublished opportunities.
- Agent actions outside delegated scope.
- Revoked or expired delegation.
- Indeterminate authorization decisions.
- Attempts to bypass lifecycle restrictions.

### 14.5 Reliability Tests

Test:

- Duplicate event delivery.
- Event delivery retries.
- Out-of-order event handling.
- Downstream consumer failure.
- Repeated command execution.
- Concurrent opportunity updates.

## 15. Acceptance Criteria

The Opportunity domain is considered ready for its initial release when:

1. An authorised employer representative can create an opportunity.
2. An opportunity can be associated with a valid organisation.
3. An authorised employer representative can update an opportunity.
4. An opportunity can be saved as a draft.
5. An opportunity must satisfy defined validation requirements before publication.
6. An authorised employer representative can publish an opportunity.
7. Published opportunities can be retrieved by authorised consumers.
8. Draft and unpublished opportunities are not publicly discoverable.
9. An authorised employer representative can close an opportunity.
10. Closed opportunities are no longer available for new applications through the platform.
11. Opportunity lifecycle changes produce the appropriate domain events.
12. Discovery can consume opportunity events and maintain its own projection.
13. Application can obtain authoritative opportunity information.
14. Cross-organisation access is prevented.
15. Agent actions are subject to delegated authority and applicable tool governance.
16. The domain does not directly access or modify another domain's database.
17. Core business rules and authorization requirements are covered by automated tests.

## 16. Open Questions

Each question includes a proposed approach to guide further discussion. These proposals are working recommendations and should not be treated as confirmed requirements until agreed.

### 16.1 Opportunity Ownership

**Question:** Who should be allowed to own and create opportunities? Should opportunities be exclusively owned by employer organisations, or should schools also be able to create and manage opportunities?

**Proposed approach:** Start with employer organisations as the primary owners of opportunities. If schools need to manage opportunities on behalf of employers, introduce an explicit authorised relationship or delegated management capability rather than treating schools as automatic owners.

### 16.2 Application Method

**Question:** Will every opportunity use Bottom Up's internal application workflow, or should employers also be able to direct students to external application links?

**Proposed approach:** Support both internal and external application methods. Opportunity stores the application method and relevant instructions, while Application owns internal application submissions and recruitment workflows.

### 16.3 Publication Approval

**Question:** Can employers publish opportunities immediately, or should opportunities go through a review or approval process before becoming publicly visible?

**Proposed approach:** Start with employer self-publication after basic validation. Support draft and published states initially, while keeping the lifecycle extensible for a future review or approval state. Introduce mandatory review only if moderation, trust, or school-partner requirements justify it.

### 16.4 Opportunity Visibility and Audience Restrictions

**Question:** Should published opportunities be visible to all eligible students on Bottom Up, or should employers and schools be able to restrict opportunities to specific audiences, such as students from selected institutions?

**Proposed approach:** Keep opportunity ownership separate from visibility and audience rules. Start with generally discoverable published opportunities for eligible platform users, while allowing an explicit audience or access policy to be introduced for school-specific or targeted opportunities. Coordinate any such restrictions with Identity & Access and Organization; do not assume every published opportunity is globally visible.

### 16.5 Opportunity Expiry

**Question:** Should opportunities automatically close when their application deadline passes, or should employers be responsible for manually closing them?

**Proposed approach:** Automatically close opportunities with an expired application deadline through a scheduled lifecycle process. Opportunities without deadlines remain active until manually closed or otherwise made inactive according to lifecycle rules.

### 16.6 Opportunity Types

**Question:** Should Bottom Up support only internships and jobs initially, or should graduate programmes and part-time opportunities be supported from the first release?

**Proposed approach:** Design the opportunity type model to support all four categories, but prioritise internships and full-time jobs for the initial product experience. Confirm which types are enabled at launch.

### 16.7 Publication Requirements

**Question:** What fields are mandatory before an opportunity can be published?

**Proposed approach:** Require a title, description, opportunity type, organisation, location or work arrangement, and sufficient application instructions. Keep compensation and other non-essential fields optional. Finalise the validation rules with the product requirements.

### 16.8 Editing Published Opportunities

**Question:** Can employers freely edit published opportunities, or should certain changes require republication or review?

**Proposed approach:** Allow normal edits while retaining an audit trail and emitting `OpportunityUpdated`. Reserve review or republication requirements for future policy decisions involving material changes.

### 16.9 Reopening Closed Opportunities

**Question:** Should employers be able to reopen closed opportunities?

**Proposed approach:** Support reopening as a controlled operation, requiring authorization and validation. Reopening should emit a separate event so Discovery and Application can update their projections and workflows.

### 16.10 Duplicate Opportunities

**Question:** How should the platform identify duplicate opportunities, especially when employers or external sources publish the same listing?

**Proposed approach:** Begin with organisation-scoped duplicate detection using relevant listing attributes. Treat automated duplicate detection as a validation or moderation aid rather than silently merging records.

### 16.11 External Opportunity Sources

**Question:** Will Bottom Up aggregate opportunities from external job platforms during the initial release?

**Proposed approach:** Keep the Opportunity model independent of external providers. If external sourcing is introduced, Integration should own connector logic and source synchronisation, while Opportunity remains responsible for the platform's authoritative listing lifecycle.

### 16.12 Billing and Publication Limits

**Question:** Will employers have subscription-based limits on the number of opportunities they can publish?

**Proposed approach:** If required, Billing should own the entitlement and usage rules. Opportunity should request entitlement evaluation through a defined interface and must not duplicate subscription logic.

### 16.13 Opportunity Versioning

**Question:** Should the platform maintain historical versions of opportunity descriptions and requirements?

**Proposed approach:** At minimum, retain update metadata and an auditable change history. Introduce full version snapshots if needed for application integrity, employer disputes, or compliance.

## 17. Related Specifications

- BottomUp Domain Context Map
- BottomUp Domain Map (Summarised)
- Cross-Domain Authorization Specification
- Domain Event Specification
- Data Ownership Specification
- Discovery Domain Contract
- Application Domain Contract
- Organization Domain Contract
- Identity & Access Domain Contract
- Agent Identity Domain Contract
- Tool Governance Domain Contract
- Integration Domain Contract

---

**End of Opportunity Domain Contract**
