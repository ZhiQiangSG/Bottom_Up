---
id: organization
name: Organization
type: domain-contract
status: draft
version: 0.1.0
owner: organization
---

# Organization Domain Contract

## 1. Purpose

The Organization domain manages the organizational identities and relationships that enable employers and educational institutions to participate in the Bottom Up career ecosystem.

Bottom Up connects students, employers, and schools through a shared platform. Organizations provide the institutional context through which users perform activities such as publishing opportunities, managing recruitment, supporting students, and coordinating career-related workflows.

The Organization domain provides a canonical representation of each participating organization, its enabled capabilities, its members, and their organizational roles.

Its purpose is to ensure that organizational relationships and responsibilities are consistently represented and enforced across the platform.

## 2. Scope & Responsibilities

Define the responsibilities owned by this domain.

### In Scope

- Organization registration and creation.
- Organization profile and information management.
- Organization status and lifecycle management.
- Organization capability management.
- Organization membership management.
- Membership invitations and activation.
- Organizational role assignment and management.
- Organizational membership status and lifecycle.
- Organization-level relationship and access context.
- Providing authoritative organizational information to other domains.

### Out of Scope

- User registration and authentication.
- User credentials and session management.
- Centralized permission definitions and authorization evaluation.
- Candidate profile management.
- Job and internship listing management.
- Recruitment and application processing.
- Career-centre programme and advising management.
- Subscription, billing, and entitlement management.
- AI agent identity and lifecycle management.
- Tool execution governance.
- Notification delivery.
- Audit and compliance record ownership.

## 3. Domain Model

Describe the conceptual model and important relationships.

### Entities

| Entity | Description |
|---|---|
| Organization | Canonical representation of an employer, educational institution, or other participating organization. |
| OrganizationMembership | Represents the relationship between a user and an organization. |
| OrganizationCapability | Represents a capability enabled for an organization, such as employer or career centre. |
| OrganizationalRole | Represents a role assigned to a user within an organization. |
| OrganizationInvitation | Represents an invitation for a user to join an organization. |

The exact entity boundaries and persistence model remain subject to detailed feature specifications.

### Value Objects

| Value Object | Description |
|---|---|
| OrganizationName | The official or display name of an organization. |
| OrganizationType | Classification of the organization, where applicable. |
| OrganizationIdentifier | A stable identifier for an organization. |
| OrganizationCapabilityType | Identifies a supported organizational capability. |
| MembershipStatus | Represents the status of an organizational membership. |
| OrganizationStatus | Represents the lifecycle status of an organization. |

### Aggregates & Aggregate Roots

**Organization Aggregate**

Aggregate root: `Organization`

Responsible for:
- Organization identity and core information.
- Organization status.
- Enabled organizational capabilities.
- Organization-level invariants.

**Organization Membership Aggregate**

Aggregate root: `OrganizationMembership`

Responsible for:
- User-to-organization membership.
- Membership status.
- Organizational role assignments.
- Membership lifecycle.

**Organization Invitation Aggregate**

Aggregate root: `OrganizationInvitation`

Responsible for:
- Invitation creation.
- Invitation recipient and target organization.
- Invitation expiry and status.
- Invitation acceptance or rejection.

The proposed aggregate boundaries should be validated against transactional requirements in the relevant feature specifications.

### Important Relationships

- One organization can have multiple users as members.
- One user can belong to multiple organizations.
- An organization can support multiple capabilities.
- A membership belongs to one organization and one user.
- A membership can have organizational role assignments.
- An organization can have multiple outstanding invitations.
- An organization capability does not automatically grant permissions to its members.

An organization is a canonical entity. Enabling employer and career-centre capabilities must not create separate organization identities.

## 4. Capabilities

List the capabilities belonging to this domain.

| Capability | Description |
|---|---|
| Organization Management | Create, retrieve, update, and manage organization records. |
| Organization Lifecycle Management | Manage organization status and lifecycle transitions. |
| Organization Capability Management | Enable and manage capabilities such as employer and career centre. |
| Membership Management | Manage user membership within organizations. |
| Membership Invitation | Invite users to join an organization and manage invitation outcomes. |
| Organizational Role Management | Assign and manage organizational roles within membership relationships. |

## 5. Commands (Write Operations)

Define the domain's supported write operations.

| Command | Description |
|---|---|
| CreateOrganization | Create a new organization. |
| UpdateOrganization | Update organization information. |
| ActivateOrganization | Activate an organization. |
| SuspendOrganization | Suspend an organization. |
| DeactivateOrganization | Deactivate an organization. |
| EnableOrganizationCapability | Enable a capability for an organization. |
| DisableOrganizationCapability | Disable a capability for an organization. |
| InviteOrganizationMember | Invite a user to join an organization. |
| AcceptOrganizationInvitation | Accept an organization invitation. |
| RejectOrganizationInvitation | Reject an organization invitation. |
| RevokeOrganizationInvitation | Revoke an outstanding invitation. |
| RemoveOrganizationMember | Remove a user's membership from an organization. |
| SuspendOrganizationMembership | Suspend an organization membership. |
| ReactivateOrganizationMembership | Reactivate an eligible membership. |
| AssignOrganizationalRole | Assign an organizational role to a member. |
| RevokeOrganizationalRole | Revoke an organizational role assignment. |

Reference the relevant feature specifications for detailed behaviour and validation rules.

## 6. Queries (Read Operations)

Define supported read operations.

| Query | Description |
|---|---|
| GetOrganization | Retrieve an organization by identifier. |
| SearchOrganizations | Search and discover organizations. |
| GetOrganizationMembers | Retrieve an organization's members. |
| GetOrganizationMembership | Retrieve a user's membership in an organization. |
| GetUserOrganizations | Retrieve organizations associated with a user. |
| GetOrganizationCapabilities | Retrieve enabled capabilities for an organization. |
| GetOrganizationRoles | Retrieve organizational roles and assignments. |
| GetOrganizationInvitations | Retrieve organization invitations. |
| CheckOrganizationMembership | Determine whether a user has an active membership. |
| GetOrganizationStatus | Retrieve an organization's current status. |

Queries expose organization-owned information and must not become substitutes for authorization decisions.

## 7. Business Rules & Invariants

Define rules that must always hold within the domain.

- Every organization must have a unique identifier.
- An organization must have a valid name.
- An organization may have multiple capabilities.
- Enabling a capability must not create a separate organization record.
- A user may belong to multiple organizations.
- An organization membership must reference an existing user and organization.
- A membership must belong to exactly one organization and one user.
- Membership status must be valid according to its lifecycle.
- Organizational role assignments must belong to a membership within the relevant organization.
- A user cannot grant themselves an organizational role that they are not authorized to assign.
- An inactive, suspended, or revoked membership must not be treated as an active organizational relationship.
- An organization capability does not independently grant a user permission to perform an operation.
- Organizational membership does not automatically grant unrestricted access to organization resources.
- Cross-organization access is denied by default unless an explicit relationship or grant permits it.
- Organization status and membership status must be considered independently.
- Disabling an organization capability must not silently delete the organization or its historical records.
- Organization-owned data must only be modified through authorized domain operations.

## 8. Domain Events

Define events produced by this domain.

The following are proposed events. Their final names, payloads, and publication conditions should be defined in the Domain Event Specification.

| Event | Trigger | Description |
|---|---|---|
| OrganizationCreated | Organization creation succeeds | A new organization was created. |
| OrganizationUpdated | Organization information changes | Organization information was updated. |
| OrganizationActivated | Organization becomes active | An organization was activated. |
| OrganizationSuspended | Organization is suspended | An organization was suspended. |
| OrganizationDeactivated | Organization is deactivated | An organization was deactivated. |
| OrganizationCapabilityEnabled | A capability is enabled | An organizational capability became available. |
| OrganizationCapabilityDisabled | A capability is disabled | An organizational capability became unavailable. |
| OrganizationMemberInvited | An invitation is created | A user was invited to join an organization. |
| OrganizationMembershipActivated | An invitation is accepted or membership activated | A user became an active organization member. |
| OrganizationMembershipSuspended | Membership is suspended | A membership became suspended. |
| OrganizationMembershipRemoved | Membership is removed | A user is no longer a member. |
| OrganizationalRoleAssigned | A role is assigned | An organizational role was assigned to a member. |
| OrganizationalRoleRevoked | A role is revoked | An organizational role assignment was revoked. |

Events should communicate completed domain state changes. Consumers must not assume that receiving an event grants authorization to perform an operation.

## 9. Authorization Requirements

Define:
- Actors and their access levels.
- Operations requiring authorization.
- Permission evaluation rules.
- Privileged operations and restrictions.
- Cross-domain authorization requirements.

Reference the Cross-Domain Authorization Specification.

### Actors

| Actor | Description | Authorization considerations |
|---|---|---|
| User | An authenticated platform user. | May create or interact with organizations where permitted. |
| Organization Member | A user with an organization membership. | Access is determined by membership status, assigned role, permissions, and resource scope. |
| Organization Administrator | A member with authorized organization-management responsibilities. | May manage permitted organization information and membership operations. |
| System Principal | A trusted system actor. | Restricted to explicitly defined system operations. |
| Agent Principal | An independently authenticated AI agent. | Must have explicit delegated authority and satisfy Tool Governance requirements. |

### Permission Examples

The following are proposed domain-oriented permission names.

| Operation | Required permission | Resource scope |
|---|---|---|
| Create organization | organization.create | Individual |
| Read organization | organization.read | Organization / Resource |
| Update organization | organization.update | Organization |
| Activate organization | organization.activate | Organization |
| Suspend organization | organization.suspend | Organization |
| Enable capability | organization.capability.manage | Organization |
| Invite member | organization.member.invite | Organization |
| Remove member | organization.member.remove | Organization |
| Assign organizational role | organization.role.assign | Organization / Resource |
| Revoke organizational role | organization.role.revoke | Organization / Resource |
| Read membership | organization.membership.read | Organization / Resource |
| Manage membership | organization.membership.manage | Organization / Resource |

Final permission definitions and role mappings are owned by Identity & Access.

### Authorization Constraints

- Membership must be verified against authoritative Organization domain state.
- Organization membership does not automatically grant unrestricted organizational access.
- Organizational roles provide organizational context for authorization; they do not independently replace permission evaluation.
- Organization capabilities do not automatically grant their members permissions.
- Users must not be able to assign themselves privileged organizational roles.
- Role assignment and revocation require explicit authorization.
- Cross-organization access is denied by default.
- Organization resource ownership and membership must be validated where applicable.
- Agents must authenticate as independent principals.
- Agent operations must satisfy the agent's own permissions, delegation grant, delegator's eligible authority, resource scope, and Tool Governance requirements.
- An agent cannot create or extend its own delegation grant.
- Human approval does not change the acting principal from the agent to the human.
- Indeterminate authorization results must be treated as denial.
- Authorization must fail closed when required membership or organization context cannot be verified.

## 10. Cross-Domain Dependencies

Document interactions with other domains.

| Domain | Dependency | Purpose |
|---|---|---|
| Identity & Access | User identity and authorization evaluation | Resolve user identity and evaluate permissions for organization operations. |
| Candidate | Candidate association | Allow candidate-related workflows to reference user identities independently of organizational membership. |
| Opportunity | Organization information and capabilities | Validate the organizational context of opportunity creation and management. |
| Application | Organization context | Support employer-side recruitment and application workflows. |
| Career Services | Organization information and career-centre capability | Support school and career-centre workflows. |
| Agent Identity | Agent principal and delegation context | Establish agent identity and delegated authority for organization-related operations. |
| Tool Governance | Tool execution policies and approvals | Govern agent-initiated organization operations. |
| Billing | Subscription and entitlement evaluation | Determine whether organizational capabilities or paid operations are available. |
| Communication | Organization membership and identity context | Support organization-related conversations and communications. |
| Notification | Organization-related events | Request delivery of relevant membership and organization notifications. |
| Integration | External organization references and synchronization | Support integrations with external organizational systems. |
| Analytics | Organization information and lifecycle events | Support derived organizational reporting and metrics. |
| Compliance | Audit and compliance requirements | Support evidence and records for security-sensitive organizational operations. |

### Dependency Rules

- Organization is the authoritative source for organization records, capabilities, memberships, and organizational role assignments.
- Identity & Access is the authoritative source for user identity, authentication, and centralized authorization evaluation.
- Other domains must not directly access Organization's internal database or modify its records.
- Cross-domain interactions must use explicit contracts, APIs, or domain events.
- Other domains may maintain local projections of organization information where appropriate.
- Local projections must not be treated as authoritative Organization state.
- Organization must not own subscription or entitlement decisions.
- Organization must not directly deliver notifications or own audit records.
- Authorization decisions must use authoritative organization and membership context where relevant.

## 11. External Integrations

Document external systems and integration boundaries.

| Integration | Purpose | Direction |
|---|---|---|
| Organization Verification Provider | Potential verification of organization identity and legitimacy | Inbound / Outbound |
| External School Systems | Potential synchronization of school or institutional information | Inbound / Outbound |
| External Employer Systems | Potential synchronization of employer information | Inbound / Outbound |

These are potential integration boundaries rather than confirmed initial-release requirements.

External integration credentials, connector configuration, synchronization state, and transport are owned by Integration.

## 12. Data Ownership & Lifecycle

Define:

### Authoritative Data Owned

The Organization domain owns:

- Organization records and identifiers.
- Organization names and core information.
- Organization status and lifecycle.
- Organization capabilities.
- Organization membership records.
- Membership status and lifecycle.
- Organizational role assignments.
- Organization invitations and their lifecycle.

### Data Creation and Update Rules

- Organizations are created through authorized organization operations.
- Organization information is modified through Organization domain commands.
- Memberships are created through approved membership or invitation workflows.
- Membership status changes must follow defined lifecycle rules.
- Organizational role assignments must be explicitly authorized.
- Organization capability changes must be performed through authorized operations.
- Other domains must request changes through Organization's exposed contracts.

### Data Retention and Deletion

- Organization records should retain a stable identity throughout their lifecycle.
- Deactivation or suspension should not automatically erase historical organizational relationships.
- Membership removal should preserve the historical record where required for auditability and business history.
- Retention, deletion, anonymization, and legal requirements must follow Compliance policies.
- Detailed retention and deletion behaviour remains subject to the Data Ownership and Compliance specifications.

### Data Exposure to Other Domains

The Organization domain may expose:

- Organization identifier and name.
- Organization status.
- Enabled organization capabilities.
- Membership status.
- Organizational role assignments.
- Relevant organization profile information.

Sensitive or unnecessary membership information must not be exposed to unrelated domains.

### Data Consistency Requirements

- Organization-owned state must remain authoritative within this domain.
- Changes must be reflected in relevant domain events.
- Consumers must tolerate asynchronous event delivery and maintain idempotent event handling.
- Cross-domain projections may be eventually consistent.
- Authorization-sensitive operations must not rely solely on stale membership projections.
- Revocation or suspension must be reflected in subsequent authorization checks.

## 13. Non-Functional Requirements

Define relevant requirements for:

### Security
- Enforce authorization on all organization-management operations.
- Protect membership and organizational role information.
- Prevent unauthorized cross-organization access.
- Apply least-privilege principles.
- Preserve agent identity and delegated authority context.

### Performance
- Organization and membership queries should support normal platform workflows without unnecessary cross-domain calls.
- Specific latency targets remain to be established.

### Availability
- Organization operations must fail safely when required authorization or authoritative state cannot be verified.
- Failure of non-critical downstream consumers should not reverse successfully committed organization operations.

### Scalability
- Support organizations with multiple members and multiple enabled capabilities.
- Support users who belong to multiple organizations.
- Support growth in organizations, memberships, and organizational activity.

### Reliability
- Commands must preserve domain invariants.
- Duplicate or retried requests must not create unintended duplicate state.
- Domain event publication must support reliable downstream processing.

### Privacy
- Expose only the organizational and membership information required by consuming domains.
- Follow applicable consent, retention, and data protection policies.

## 14. Testing Requirements

Define:

### Domain Invariant Tests
- Organization identifiers are unique.
- Organizations can support multiple capabilities.
- Enabling a capability does not create another organization.
- Memberships reference valid organizations and users.
- A user can belong to multiple organizations.
- Organizational role assignments belong to the correct membership.
- Invalid organization and membership lifecycle transitions are rejected.

### Unit Tests
- Organization creation and update validation.
- Organization capability management.
- Membership lifecycle rules.
- Invitation lifecycle rules.
- Organizational role assignment and revocation.
- Organization status transitions.

### Integration Tests
- Identity & Access user identity and authorization interactions.
- Opportunity and Application organization-context interactions.
- Career Services capability checks.
- Billing entitlement checks where required.
- Notification requests and event consumers.
- Domain event publication and consumption.

### Security and Authorization Tests
- Users without the required permission cannot manage organizations.
- Organization members cannot access another organization's resources without explicit authorization.
- Suspended or removed members cannot exercise membership-dependent access.
- Users cannot assign themselves privileged roles.
- Agents cannot operate outside their delegated authority.
- Expired or revoked delegation grants cannot authorize subsequent operations.
- Indeterminate authorization results are denied.

### Edge Cases
- Duplicate organization creation requests.
- Duplicate membership invitations.
- Invitation expiry and revocation.
- Concurrent membership and role updates.
- Organization suspension while members are active.
- Capability removal while dependent workflows exist.
- Membership revocation during a long-running agent task.
- Downstream event delivery failures and retries.

## 15. Domain Acceptance Criteria

The Organization domain contract is considered implemented when:

- [ ] Organizations have a canonical identity and authoritative record.
- [ ] Organization information can be created, retrieved, and updated through defined operations.
- [ ] Organizations support multiple capabilities without duplicate organization records.
- [ ] Organization lifecycle is explicitly managed.
- [ ] Users can belong to multiple organizations.
- [ ] Memberships have defined status and lifecycle behaviour.
- [ ] Organization invitations follow defined lifecycle rules.
- [ ] Organizational roles can be assigned and revoked through authorized operations.
- [ ] Organization membership and capabilities are available to relevant consuming domains.
- [ ] Authorization is evaluated using authoritative organization context.
- [ ] Cross-organization access is denied by default.
- [ ] Agent operations respect independent identity, delegation, and Tool Governance requirements.
- [ ] Organization-owned data is not directly modified by other domains.
- [ ] Relevant domain events are published reliably.
- [ ] Security, privacy, and audit requirements are satisfied.
- [ ] Automated tests cover relevant business rules and failure conditions.

## 16. Open Questions

The following decisions require further clarification before the contract can be finalized.

| ID | Question | Impact | Resolution |
|---|---|---|---|
| Q-001 | What organization types should be supported initially? | Determines organization classification and registration workflows. | Pending |
| Q-002 | What organization capabilities are supported in the initial release? | Determines capability management and dependent workflows. | Pending |
| Q-003 | Can organizations be self-registered, or must they be created or verified through an administrative process? | Affects onboarding, verification, and trust. | Pending |
| Q-004 | What information is mandatory when creating an organization? | Determines organization profile validation. | Pending |
| Q-005 | What are the permitted organization lifecycle states and transitions? | Affects access, visibility, and downstream workflows. | Pending |
| Q-006 | Can one user hold multiple organizational roles within the same organization? | Affects membership and role-assignment modelling. | Pending |
| Q-007 | Are organizational roles standardized by the platform, or can organizations configure their own roles? | Affects role management and authorization mappings. | Pending |
| Q-008 | Who can invite members and assign or revoke organizational roles? | Determines organization administration permissions. | Pending |
| Q-009 | Can an organization have multiple administrators, and must at least one remain active? | Affects organization governance and lifecycle safeguards. | Pending |
| Q-010 | What happens to existing memberships and dependent workflows when an organization is suspended or deactivated? | Affects access enforcement and business continuity. | Pending |
| Q-011 | Can organization capabilities be disabled while dependent records or workflows still exist? | Affects lifecycle and consistency across domains. | Pending |
| Q-012 | What organization verification requirements apply to employers and educational institutions? | Affects trust, onboarding, and publishing privileges. | Pending |
| Q-013 | Should organization creation and management be available to all users or restricted to specific account conditions? | Affects onboarding and authorization. | Pending |
| Q-014 | What invitation expiry, re-invitation, and acceptance rules should apply? | Affects membership lifecycle. | Pending |

## 17. Related Specifications

| Specification | Type | Relationship |
|---|---|---|
| Domain Context Map | Architecture | Defines Organization's bounded-context boundaries and relationships. |
| Bottom Up Domain Map (Summarised) | Domain Architecture | Defines Organization responsibilities, ownership, and capabilities. |
| Cross-Domain Authorization Specification | Security / Architecture | Defines principal identity, permissions, scopes, delegation, and authorization enforcement. |
| Domain Event Specification | Architecture | Defines event naming, payloads, and delivery requirements. |
| Data Ownership Specification | Architecture | Defines authoritative data ownership and cross-domain data access. |
| Identity & Access Domain Contract | Domain Contract | Defines user identity and centralized authorization responsibilities. |
| Opportunity Domain Contract | Domain Contract | Defines employer opportunity ownership and organization dependencies. |
| Application Domain Contract | Domain Contract | Defines recruitment workflow ownership and organization dependencies. |
| Career Services Domain Contract | Domain Contract | Defines school and career-centre workflow ownership. |
| Billing Domain Contract | Domain Contract | Defines subscription and entitlement ownership. |
| Compliance Domain Contract | Domain Contract | Defines audit, privacy, retention, and compliance responsibilities. |

## 18. Implementation Notes

- Maintain one canonical organization record regardless of the number of enabled capabilities.
- Treat employer and career-centre participation as capabilities of an organization rather than mutually exclusive organization types.
- Keep organization membership separate from user identity.
- Keep organizational roles separate from centralized permission definitions.
- Do not use organization capabilities as a substitute for authorization.
- Keep organization state authoritative within this domain.
- Expose explicit contracts for other domains rather than sharing internal database access.
- Use domain events to communicate organization and membership lifecycle changes.
- Ensure organization and membership changes can be traced to the acting principal.

Implementation details such as persistence technology, API framework, event transport, and database schema should be specified separately.

## 19. Change History

| Version | Date | Changes | Author |
|---|---|---|---|
| 0.1.0 | 2026-11-11 | Initial draft | Pending |