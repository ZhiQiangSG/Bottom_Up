# Cross-Domain Authorization

## 1. Purpose & Scope

### 1.1 Purpose

This document defines the system-wide authorization architecture for BottomUp.

It establishes a consistent authorization model across bounded contexts, covering:

- Human users and their personas.
- Organizational memberships and roles.
- Individual and organizational resources.
- AI agents acting as independent principals.
- Delegated authority granted to agents.
- System-level principals and internal service operations.
- Tool execution policies and approval requirements.

The objective is to ensure that protected operations are consistently authorized, resource ownership and business rules remain within their respective domains, and authorization decisions are auditable.

### 1.2 Scope

This document defines:

- Authorization principles and responsibilities.
- Principal, permission, and authorization models.
- Individual and organizational authorization scopes.
- Cross-domain authorization and enforcement.
- Agent identity, delegation, and execution authority.
- Tool Governance integration.
- Revocation, failure handling, and audit requirements.

It does not define:

- Authentication protocols or credential storage details.
- The complete permission catalogue for each domain.
- Individual domain resource models.
- Tool-specific execution policies.
- Detailed approval workflows.
- Billing plans or entitlement definitions.

These concerns are specified in their respective domain contracts and feature specifications.

## 2. Core Principles

### 2.1 Explicit Authorization

Every protected operation must be authorized against an explicit permission and applicable resource context.

Authorization must not be inferred solely from authentication, account ownership, persona selection, organizational affiliation, agent ownership, or previous authorization decisions.

### 2.2 Deny by Default

Access is denied unless explicitly permitted.

Missing, invalid, or indeterminate authorization context must fail closed.

### 2.3 Separation of Responsibilities

Authorization responsibilities are distributed across domains:

- Identity & Access owns centralized authorization evaluation and delegation management.
- Resource-owning domains define resource-specific authorization requirements and enforce business invariants.
- Organization owns organizational memberships and role assignments.
- Agent Identity owns agent identities and lifecycle.
- Tool Governance owns tool execution policies, risk classification, and approval requirements.
- Compliance owns audit and compliance requirements.

No domain may bypass another domain's authoritative responsibilities.

### 2.4 Least Privilege

Users, agents, and system principals receive only the permissions necessary for their intended operations.

Permissions must be constrained by applicable resource, organizational, delegation, and execution contexts.

### 2.5 Independent Agent Identity

An AI agent acts under its own identity and permissions, not by impersonating its owner.

The agent is the acting principal. Its owner or delegating user is attributed separately where relevant.

Agent ownership does not automatically confer the owner's permissions upon the agent.

### 2.6 Contextual Authorization

Authorization decisions must consider the principal, action, resource, scope, and applicable contextual restrictions.

These may include delegation validity, organizational membership, approval status, consent, privacy, and entitlement requirements.

### 2.7 Auditability

Authorization decisions and protected operations must produce sufficient information to reconstruct:

- Who or what initiated the operation.
- Which authority permitted the operation.
- Which resource was accessed or modified.
- Which policy version was applied.
- Whether approval was required and obtained.

## 3. Authorization Model

### 3.1 Principal

A principal is an identifiable actor that can initiate an operation.

BottomUp supports:

| Principal | Description |
|---|---|
| User | An authenticated human user. |
| Agent | An independently identified AI agent. |
| System | An explicitly registered system-level principal. |

Every authorization request must identify its acting principal. A principal must not be silently replaced during authorization evaluation or cross-domain execution.

### 3.2 Action

An action represents an operation a principal intends to perform.

Examples:

- `candidate.profile.read`
- `candidate.profile.update`
- `organization.member.read`
- `organization.member.invite`
- `opportunity.create`
- `application.submit`
- `application.withdraw`
- `tool.execute`

Permissions must follow a consistent, domain-oriented naming convention. Each domain owns the definition and documentation of its permissions.

### 3.3 Resource

A resource is the object or data targeted by an operation.

Examples include candidate profiles, organizations, memberships, opportunities, applications, career service records, agent configurations, and tool execution records.

The resource-owning domain defines resource-specific authorization requirements and supplies authoritative resource context.

### 3.4 Authorization Scope

Initial supported scopes are:

| Scope | Description |
|---|---|
| Individual | Access to resources within an individual's permitted context. |
| Organization | Access to resources within an organization for which the principal has appropriate authority. |
| Resource | Explicit access to a specific resource where required. |
| System | Narrowly defined system-level operations. |

The initial implementation should prioritize individual and organizational scopes, while supporting explicit resource-level grants where necessary.

### 3.5 Permission

A permission represents an explicitly defined capability to perform an action.

Permissions are assigned through controlled role and grant configurations rather than arbitrary user-defined permission sets.

Initial requirements:

- Use predefined roles and permission mappings.
- Maintain role and permission definitions through controlled configuration or system-managed records.
- Exclude custom roles initially.
- Support explicit resource-level grants where required.

### 3.6 Authorization Decision

Identity & Access returns a structured authorization decision:

| Outcome | Meaning |
|---|---|
| Permit | The operation is authorized. |
| Deny | The operation is explicitly unauthorized. |
| Indeterminate | Authorization cannot be established. |

Indeterminate decisions must be treated as denials by enforcement points.

The decision must contain:

- Outcome and standardized reason code.
- Applicable policy reference and version.
- Relevant authorization context.
- Internal diagnostic information where appropriate.

Sensitive policy details must not be exposed to external clients.

## 4. Domain Responsibilities

| Domain | Responsibilities |
|---|---|
| Identity & Access | Centralized authorization evaluation, permission definitions and mappings, individual grants, agent delegation grants, policy enforcement and versioning. |
| Organization | Organization records and capabilities, memberships, membership status, organizational roles and assignments. |
| Resource-owning domains | Resource-specific authorization requirements, authoritative resource context, business invariants and data protection. |
| Agent Identity | Agent principals, identity status, ownership relationships, lifecycle and agent-specific permissions. |
| Assistant | Agent task orchestration, execution context, identity preservation, authorized operation requests and approval handling. |
| Tool Governance | Approved tool definitions, risk classification, execution constraints, approval workflows and tool-specific enforcement. |
| Compliance | Audit requirements, audit records, compliance investigations, retention and access requirements. |

### 4.1 Architectural Boundaries

Identity & Access must not become the owner of domain-specific business rules or resource data.

Organization remains the authoritative source of organizational membership and role assignments. Membership alone does not grant access to every organizational resource; applicable permissions, roles, resources, and context must still be evaluated.

Resource-owning domains must not assume that authentication or possession of a resource identifier establishes authorization.

Assistant must not bypass Identity & Access or Tool Governance.

Tool Governance does not replace general authorization evaluation. An operation permitted by Identity & Access may still be prohibited by Tool Governance.

## 5. Roles, Permissions & Organizational Access

### 5.1 Role Management

Roles provide reusable permission groupings.

Examples include:

- Candidate.
- Organization Owner.
- Organization Administrator.
- Organization Member.
- Career Centre Administrator.
- Career Centre Staff.

The precise role catalogue and role-to-permission mappings are maintained by the relevant domain.

Initial requirements:

- Use predefined roles and controlled permission mappings.
- Assign roles within their applicable individual or organizational scopes.
- Exclude custom roles.
- Ensure role and permission changes affect subsequent authorization decisions.

A user may hold different roles across different organizations.

A user's primary persona is not an authorization role. Persona selection determines the primary product context but must not independently grant permissions.

### 5.2 Organizational Context

Organizational operations must identify the relevant organization context.

A client-provided organization identifier represents a requested context, not proof of membership or authorization.

Before granting organizational access, the system must verify:

- The organization exists and is in an applicable state.
- The principal has an active membership or another explicit authorization basis.
- The membership grants the required role or permissions.
- The requested operation is permitted within the organization's scope.
- Resource-specific restrictions are satisfied.

### 5.3 Cross-Organization Access

Cross-organization access is denied by default.

A principal must not access another organization's resources merely because it belongs to a different organization.

Access requires an explicit relationship or resource-level grant recognized by the applicable authorization policy.

### 5.4 Organization Capabilities

An Organization may support multiple capabilities, such as Employer and Career Centre.

Authorization must consider the relevant organization, capability, role, and resource context.

A capability does not independently grant a user access to organizational resources.

## 6. Agent Authorization & Delegation

### 6.1 Agent Identity

Each agent is an independent authorization principal with:

- A unique agent identifier.
- An identifiable owner relationship.
- An independent permission set.
- An applicable lifecycle status.
- A verifiable execution identity.

For agent-initiated operations:

| Context | Purpose |
|---|---|
| `principal_id` | Identifies the acting agent. |
| `principal_type` | Identifies the principal as an agent. |
| `owner_user_id` | Identifies the agent's owner where relevant. |
| `delegation_grant_id` | Identifies the authority granted to the agent. |
| Execution context | Identifies the task and applicable constraints. |

The owner identifier provides attribution and delegation context. It must never replace the agent as the acting principal.

### 6.2 Independent Agent Permissions

Agents have permission sets independent of their owners' permissions.

An agent must not automatically inherit all permissions held by its owner.

Two separate concepts govern agent authority:

- **Agent permissions:** What the agent is technically permitted to do as a principal.
- **Delegation:** Which authority the agent is allowed to exercise on behalf of a human user.

### 6.3 Delegation Grants

A delegation grant explicitly authorizes an agent to exercise specified authority on behalf of a human user.

Each grant must identify:

- Agent principal.
- Delegating user.
- Permitted actions or predefined capability groups.
- Applicable resource or organizational scope.
- Contextual restrictions.
- Grant status.
- Validity period, where applicable.
- Creation and revocation information.

Initial restrictions:

- Only human users may create delegation grants.
- Agents cannot create or extend their own grants.
- Nested delegation and agent-to-agent delegated execution are prohibited.

Delegation grants should support explicit permissions and reusable predefined capability groups rather than arbitrary user-defined permission expressions.

### 6.4 Effective Agent Authority

An agent's effective authority is the intersection of all applicable constraints:

1. The agent's own permissions.
2. The delegating user's authority eligible for delegation.
3. Permissions or predefined capability groups specified in the delegation grant.
4. Applicable resource and organizational scope.
5. Delegation and execution restrictions.
6. Identity & Access authorization policies.
7. Tool Governance policies and execution constraints.
8. Required approval conditions.
9. Applicable consent, privacy, and entitlement restrictions.

The agent may perform an operation only when all applicable requirements are satisfied.

A delegation grant cannot expand the delegating user's authority or override the agent's own permission restrictions.

### 6.5 Agent Authentication

Agents must authenticate independently when making internal API calls.

Agent authentication must use short-lived, cryptographically verifiable credentials.

The receiving service must validate:

- Agent identity.
- Credential validity and authenticity.
- Agent lifecycle status.
- Relevant execution context.
- Delegation context where the operation relies on delegated authority.

An owner's session or credentials must not be reused as the agent's identity.

Authentication establishes which agent is making the request; it does not establish authorization.

### 6.6 Agent Lifecycle and Revocation

Initial requirements:

- Suspending an agent immediately prevents protected execution.
- Deleting an agent revokes its associated delegation grants.
- Ownership transfer is not supported initially.
- Reconfiguring an agent must not silently expand its authority.
- Changes to agent permissions must affect subsequent authorization decisions.

Revoking a delegation grant must prevent subsequent operations relying on that grant.

### 6.7 Execution and Long-Running Tasks

Authorization at task initiation is insufficient for long-running tasks.

The system must revalidate authorization before every consequential operation.

Changes to agent permissions, delegation grants, owner authority, resource access, or applicable policies must affect subsequent protected operations.

An agent must not continue performing consequential operations based solely on an authorization decision obtained when the task began.

### 6.8 Agent-to-Agent Operations

Agent-to-agent delegated execution is prohibited initially.

An agent may not transfer its delegation grant or authority to another agent.

If one agent requests another agent to perform an operation, the second agent must independently establish its identity, permissions, and any required delegation. It cannot rely on the first agent's authority.

### 6.9 Resource Ownership and Access

Resource ownership and acting principal identity must remain separate.

An agent accessing a user-owned or organization-owned resource must satisfy the applicable authorization requirements.

Neither agent ownership nor the owner's organizational membership automatically authorizes the agent to access those resources.

Explicit delegation and applicable resource authorization are required.

### 6.10 Human Approval

Human approval does not change the acting principal.

When an agent operation requires approval:

- The agent remains the acting principal.
- The approving human is recorded separately.
- Approval is associated with the specific operation or approval scope.
- Approval must not be interpreted as a general permission grant.
- The agent must still satisfy all other authorization and execution requirements.

Approval cannot override missing permissions, invalid delegation, or resource restrictions.

## 7. Tool Execution Governance

### 7.1 Independent Evaluations

Tool execution requires separate evaluation of:

1. General authorization by Identity & Access.
2. Tool-specific governance by Tool Governance.
3. Applicable approval requirements.
4. Other contextual restrictions, including consent, privacy, and entitlement.

A successful result from one evaluation does not imply success in the others.

### 7.2 Risk Classification

Tool operations must be classified according to their risk and potential impact.

Classification should distinguish:

- Read-only retrieval.
- Reversible modifications.
- External communications.
- Financial or contractual commitments.
- Irreversible or high-impact operations.

Tool Governance owns the classification and associated policies.

### 7.3 Approval Requirements

Consequential operations require approval according to their risk classification and applicable policy.

Approval must be enforced before execution and associated with the relevant operation and execution context.

Approval must not be treated as unrestricted authorization for future operations.

### 7.4 Execution Enforcement

All tool execution must pass through approved execution interfaces.

Agents and Assistant must not directly bypass Tool Governance to invoke protected integrations or external operations.

## 8. Authorization Evaluation & Cross-Domain Enforcement

### 8.1 Centralized Evaluation

Identity & Access provides the centralized authorization application service.

Domains must request authorization through the approved service interface rather than implementing independent, inconsistent cross-domain permission evaluation.

Resource-owning domains remain responsible for supplying authoritative resource context and enforcing their business invariants.

### 8.2 Authorization Request Context

An authorization request must contain the information required to evaluate the operation:

- Principal identifier and type.
- Requested action.
- Resource identifier and type.
- Individual or organizational scope.
- Relevant organization context.
- Delegation grant identifier, where applicable.
- Execution context, where applicable.
- Relevant contextual attributes.

The precise request contract is defined by Identity & Access.

### 8.3 Authorization Decision

The authorization service must return a structured decision rather than a bare boolean.

The result must include:

- Permit, Deny, or Indeterminate.
- Standardized reason code.
- Applicable policy reference and version.
- Internal diagnostic context where appropriate.

External clients receive standardized, non-sensitive denial codes. Detailed policy reasoning and internal diagnostics remain restricted.

### 8.4 Policy Precedence and Missing Context

Authorization follows a deny-overrides model.

- Explicit denial takes precedence over a permission grant.
- Conflicting policies result in denial unless the policy model explicitly defines a valid resolution.
- Indeterminate decisions are treated as denials.
- Missing or invalid authorization context must never be interpreted as permission.

Examples of missing or invalid context include:

- Missing principal identity.
- Missing resource ownership or scope information.
- Unverifiable organizational membership.
- Missing delegation information for a delegated operation.
- Invalid or incomplete execution context.

Such requests must fail closed.

### 8.5 Cross-Domain Enforcement

Every domain must enforce authorization before exposing protected data or performing protected state changes.

Authorization must be checked at the appropriate service boundary, not solely in the user interface.

A domain must not trust a previous authorization decision unless its scope, context, and validity demonstrably apply to the current operation.

### 8.6 Principal Propagation

Cross-domain calls must preserve the original acting principal and relevant authorization context.

For agent-initiated operations, the execution context must preserve:

- Agent principal identifier and type.
- Owner or delegating user identifier, where relevant.
- Delegation grant identifier.
- Relevant execution context.
- Correlation identifier.

The owner identifier is carried for attribution and delegation validation. It must never silently replace the agent as the acting principal.

### 8.7 Internal Service Calls

Internal service-to-service calls must use explicitly identified system principals where appropriate.

System principals must have narrow, predefined permissions.

A service must not use an unrestricted system identity to bypass authorization requirements on behalf of a user or agent.

### 8.8 Authoritative Resource Context

The resource-owning domain must provide or validate authoritative resource context.

A caller must not establish its own resource ownership, organization membership, or access scope merely by supplying request parameters.

## 9. Consent, Privacy & Entitlements

Authorization is distinct from consent, privacy, and entitlement evaluation.

A principal may possess the required permission but still be prohibited from performing an operation due to another applicable restriction.

### 9.1 Consent and Privacy

Consent and privacy requirements are separate policy inputs that may restrict an otherwise authorized operation.

Consent must not be treated as a substitute for authorization, and authorization must not be treated as proof of consent.

### 9.2 Entitlements

Billing and Entitlements determine whether an account or organization has access to a particular product capability or usage allowance.

An entitlement does not independently grant access to a resource. Likewise, a permission does not override a missing entitlement.

### 9.3 Combined Evaluation

Protected operations must satisfy all applicable conditions:

- Authentication.
- Authorization.
- Delegation, where applicable.
- Consent and privacy restrictions, where applicable.
- Entitlement requirements, where applicable.
- Tool Governance and approval requirements, where applicable.
- Domain-specific business invariants.

The relevant domain or application workflow is responsible for orchestrating these checks.

## 10. Lifecycle, Revocation & Failure Handling

### 10.1 Authorization Freshness

Authorization decisions may become invalid when permissions, memberships, delegation grants, policies, or resource states change.

The initial implementation should avoid long-lived authorization caches.

For consequential operations:

- Perform an authoritative authorization check before execution.
- Revalidate relevant delegation and membership state.
- Do not rely solely on authorization obtained at task initiation.
- Ensure revocation affects subsequent protected operations.

If caching is introduced later, it must have explicit expiration and invalidation mechanisms.

### 10.2 Revocation Requirements

The following changes must affect subsequent protected operations:

| Change | Required behavior |
|---|---|
| Role or permission revocation | Subsequent decisions reflect the updated permissions. |
| Membership suspension or revocation | Operations relying on that membership are denied. |
| Delegation revocation | The agent cannot perform subsequent operations relying on that grant. |
| Agent suspension | Protected agent execution is immediately blocked. |
| Agent deletion | Associated delegation grants are revoked. |
| Agent permission changes | Subsequent decisions reflect the updated permissions. |

Authorization must be revalidated before every consequential operation, including operations within long-running workflows.

An operation already dispatched to an external system is governed by the relevant domain and integration workflow. Revocation cannot be assumed to reverse an external action that has already completed.

### 10.3 Failure Handling

Authorization failures must result in denial.

This includes:

- Authorization service unavailability.
- Invalid principal credentials.
- Missing authorization context.
- Unverifiable resource context.
- Indeterminate policy evaluation.
- Invalid or revoked delegation.
- Unavailable authoritative membership information when required.

External-facing error responses must use standardized, non-sensitive reason codes. Detailed internal policy information must not be exposed to users or agents.

### 10.4 Retry Behavior

A failed authorization decision must not be converted into permission through automatic retries or fallback logic.

Retries may recover from transient service failures, but the operation must remain blocked until a valid authorization decision is obtained.

## 11. Audit & Compliance

### 11.1 Audit Requirements

Protected operations and relevant authorization decisions must be auditable.

Audit records should capture:

- Acting principal identifier and type.
- Owner or delegating user identifier, where applicable.
- Delegation grant identifier, where applicable.
- Requested action.
- Target resource identifier and type.
- Organization context, where applicable.
- Authorization outcome.
- Relevant policy identifier and version.
- Approval identifier and approving human, where applicable.
- Timestamp.
- Correlation identifier.
- Execution or tool context, where applicable.

### 11.2 Agent Attribution

For agent-initiated operations:

- The agent is recorded as the actor.
- The owner or delegating user is recorded separately.
- The delegation grant is recorded where applicable.
- The approving human is recorded separately when approval is required.

Audit records must not misrepresent an agent operation as a direct human operation.

### 11.3 Policy Versioning

Authorization policies must be versioned.

Audit records must reference the policy version used for the relevant authorization decision, supporting historical reconstruction and compliance investigations.

### 11.4 Sensitive Information

Audit records must not unnecessarily retain sensitive information.

Retention, access, and disclosure requirements are governed by Compliance and applicable privacy policies.

## 12. Implementation Priorities

The initial implementation should follow this sequence:

### Phase 1: Core Authorization

- Establish principal and permission concepts.
- Implement centralized authorization evaluation in Identity & Access.
- Establish predefined roles and permission mappings.
- Support individual and organizational scopes.
- Establish structured authorization outcomes.
- Implement deny-by-default and fail-closed behavior.
- Integrate authoritative organization membership information.

### Phase 2: Cross-Domain Enforcement

- Define authorization interfaces and contracts.
- Integrate authorization checks into resource-owning domains.
- Establish principal and execution-context propagation.
- Introduce standardized denial codes.
- Establish policy versioning and audit references.

### Phase 3: Agent Authorization

- Establish independent agent principals.
- Implement agent authentication.
- Establish independent agent permission sets.
- Implement explicit delegation grants.
- Enforce effective-authority intersection.
- Implement delegation revocation and agent lifecycle behavior.
- Preserve agent identity and delegation context across domain boundaries.

### Phase 4: Tool Governance Integration

- Integrate tool execution authorization.
- Implement risk-based operation classification.
- Introduce approval requirements for consequential operations.
- Preserve agent attribution and approval records.
- Enforce authorization revalidation before consequential execution.

### Phase 5: Hardening

- Review authorization caching and invalidation.
- Test revocation and long-running execution scenarios.
- Validate cross-organization isolation.
- Test failure and indeterminate outcomes.
- Review audit completeness and policy-version traceability.

## 13. Open Questions & Related Documents

### 13.1 Open Questions

There are no outstanding architecture-level open questions for the initial authorization model.

Detailed implementation decisions remain to be specified in the relevant domain contracts and feature specifications. These include:

- Exact permission identifiers and role-to-permission mappings.
- Agent credential format, issuance, rotation, and validation mechanisms.
- Delegation grant persistence and lifecycle transitions.
- Exact resource-level grant representation.
- Authorization service request and response schemas.
- Tool risk classifications and approval workflows.
- Audit event schemas and retention policies.
- External operation cancellation and reconciliation behavior.

These implementation details must remain consistent with the architectural decisions in this document.

### 13.2 Related Documents

This document should be read alongside:

- `DOMAIN_ARCHITECTURE.md`
- `DOMAIN_CONTEXT_MAP.md`
- `domains/DOMAIN_CONTRACT_TEMPLATE.md`
- Relevant domain contracts.
- Relevant feature specifications.
- Relevant workflow specifications.

Changes affecting domain responsibilities, principal identity, delegation, or cross-domain authorization must be reflected in the relevant domain contracts.