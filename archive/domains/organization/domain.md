# Organizations — Domain Contract

**Last Modified**: 08/11/2026

## 1. Domain purpose

The Organization domain owns the identity, lifecycle, capabilities, verification, approval and membership of organizations participating in BottomUp.

It supports organizations operating in one or more business capacities, including:

- Employers.
- Educational institutions and career centres.

An organization has one canonical identity regardless of the number of capabilities it operates.

For example, a university may operate both as:
- An employer recruiting employees.
- A career centre providing career services to students and alumni.

Both capabilities belong to the same Organization record.

The domain is responsible for:

- Organization registration and onboarding.
- Organization profiles.
- Organization lifecycle and status.
- Organization capabilities.
- Organization verification and approval.
- Organization memberships.
- Staff roles and permissions.
- Staff invitations.
- Organization-level access management.
- Organization-related audit events.

It does not own user accounts, candidate profiles, education affiliations, job listings, applications or career-centre entitlements.

---

## 2. Ubiquitous language

| Term | Definition |
|---|---|
| Organization | A canonical entity representing a participating employer, institution or other organization. |
| Organization capability | A business function enabled for an organization, such as employer or career centre. |
| Organization status | The organization's operational lifecycle state. |
| Verification | The process of establishing that an organization is legitimate and its submitted information is credible. |
| Approval | Permission granted by BottomUp to use a particular platform capability. |
| Organization membership | A relationship between an account and an organization. |
| Member | An account with an organization membership. |
| Membership role | A named set of permissions assigned to a member within an organization. |
| Permission | An individual action that a member is authorized to perform. |
| Invitation | An offer to establish an organization membership. |
| Organization administrator | A member authorized to manage organization settings and memberships. |
| Capability restriction | A restriction preventing an organization from using a particular business function. |
| Organization context | The organization currently selected in a user's interface. It does not grant authorization. |

### Important distinctions

1. Organization identity is independent of organization capabilities.
2. Organization verification is independent of platform approval.
3. Organization capabilities do not automatically grant individual members permissions.
4. Membership is independent of account-level capabilities.
5. An organization may have multiple members with different permissions.
6. A single account may belong to multiple organizations.
7. Organization membership does not automatically imply candidate access.

---

## 3. Entities and aggregates

### 3.1 Organization aggregate

**Aggregate root:** Organization

The Organization aggregate owns its identity, operational status and enabled capabilities.

#### Organization

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique organization identifier |
| legal_name | String | Registered legal name |
| display_name | String | Public-facing organization name |
| slug | String | Unique organization URL identifier |
| website_url | URL / nullable | Official website |
| description | Text / nullable | Organization description |
| logo | File reference / nullable | Organization logo |
| status | Enum | pending, active, suspended, rejected, closed |
| verification_status | Enum | unverified, pending, verified, rejected |
| created_at | Datetime | Creation timestamp |
| updated_at | Datetime | Last modification timestamp |
| created_by | Account ID | Creating account |
| closed_at | Datetime / nullable | Closure timestamp |

Organization records should distinguish legal identity from public-facing identity.

The display name may change without changing the organization's canonical identity.

#### OrganizationCapability

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique capability record |
| organization_id | FK | Associated organization |
| capability | Enum | employer, career_center |
| status | Enum | pending, enabled, suspended, revoked |
| enabled_at | Datetime / nullable | Activation timestamp |
| enabled_by | Account ID / nullable | Approving actor |
| revoked_at | Datetime / nullable | Revocation timestamp |

Capabilities are additive.

An organization may possess both employer and career-centre capabilities.

A capability must not be inferred from an organization's name, domain or email address.

### 3.2 Organization profile

**Owner:** Organizations

Organization profiles contain public-facing information that may be displayed to candidates and other platform users.

Possible information includes:

- Description.
- Industry.
- Organization size.
- Headquarters location.
- Website.
- Logo.
- Contact information.
- Social media links.

The profile should be separate from verification records so that public-facing content can evolve independently of verification evidence.

### 3.3 Organization verification

**Owner:** Organizations

Verification establishes the legitimacy of an organization.

#### OrganizationVerification

| Field | Type | Description |
|---|---|---|
| id | UUID | Verification record identifier |
| organization_id | FK | Associated organization |
| status | Enum | pending, verified, rejected, expired |
| verification_method | Enum / string | Verification mechanism |
| submitted_at | Datetime | Submission timestamp |
| reviewed_at | Datetime / nullable | Review timestamp |
| reviewed_by | Account ID / nullable | Reviewing administrator |
| rejection_reason | Text / nullable | Reason for rejection |
| expires_at | Datetime / nullable | Expiry timestamp |

Verification evidence should be stored securely and separately from public organization profile information.

Verification methods may include:

- Official-domain email verification.
- Business registration documentation.
- Institutional documentation.
- Manual platform review.
- Other approved verification mechanisms.

The verification process may differ according to organization type and capability.

### 3.4 Organization approval

Verification and approval must remain independent.

For example, an organization may be verified but still require approval before publishing jobs.

#### CapabilityApproval

| Field | Type | Description |
|---|---|---|
| id | UUID | Approval record identifier |
| organization_id | FK | Associated organization |
| capability | Enum | employer, career_center |
| status | Enum | pending, approved, rejected, suspended, revoked |
| reviewed_at | Datetime / nullable | Review timestamp |
| reviewed_by | Account ID / nullable | Reviewing administrator |
| reason | Text / nullable | Decision rationale |

Approval is capability-specific.

An organization may be approved to operate as an employer but still have a pending career-centre approval.

The exact approval requirements are governed by platform policy.

### 3.5 Organization membership aggregate

**Aggregate root:** OrganizationMembership

Memberships are organization-scoped.

An account may have memberships in multiple organizations, and may have different permissions in each.

#### OrganizationMembership

| Field | Type | Description |
|---|---|---|
| id | UUID | Membership identifier |
| organization_id | FK | Organization |
| account_id | Account ID | Associated account |
| role | Enum | recruiter, hiring_manager, counsellor, org_admin |
| status | Enum | pending, active, suspended, revoked |
| granted_at | Datetime / nullable | Activation timestamp |
| granted_by | Account ID / nullable | Granting actor |
| revoked_at | Datetime / nullable | Revocation timestamp |

Constraints:

- A membership belongs to exactly one organization.
- A membership belongs to exactly one account.
- An account may have multiple memberships.
- A user may have different roles in different organizations.
- Membership permissions apply only within the associated organization.
- Revoked memberships remain auditable.
- An inactive membership cannot authorize business operations.

A user may hold multiple memberships within the same organization only if there is a clear business requirement. The initial implementation should prefer one membership with an explicitly assigned role and permission set.

### 3.6 Membership permissions

**Owner:** Organizations

Permissions define the actions an individual member may perform.

Initial permission groups:

| Role | Intended permissions |
|---|---|
| recruiter | Create and manage job listings; view and manage assigned recruitment workflows |
| hiring_manager | Review applicants; participate in recruitment decisions |
| counsellor | Manage permitted career-centre services and candidate interactions |
| org_admin | Manage organization profile, memberships, invitations and organization settings |

These are initial role templates, not immutable permission boundaries.

The application should evaluate permissions explicitly rather than relying solely on role-name comparisons.

Permission examples:

- `jobs.create`
- `jobs.update`
- `jobs.publish`
- `applications.view`
- `applications.review`
- `career_services.manage`
- `memberships.invite`
- `memberships.revoke`
- `organization.profile.update`
- `organization.settings.manage`

Role templates may be expanded as BottomUp introduces more organizational workflows.

### 3.7 OrganizationInvitation

**Owner:** Organizations

#### OrganizationInvitation

| Field | Type | Description |
|---|---|---|
| id | UUID | Invitation identifier |
| organization_id | FK | Target organization |
| email | Email address | Intended recipient |
| role | Enum | Proposed membership role |
| status | Enum | pending, accepted, rejected, expired, revoked |
| invited_by | Account ID | Inviting member |
| invited_at | Datetime | Invitation timestamp |
| expires_at | Datetime | Expiration timestamp |
| accepted_at | Datetime / nullable | Acceptance timestamp |

Rules:

- Invitations must be issued by authorized organization members.
- Invitations must specify the target organization and proposed role.
- Invitations are single-use.
- Invitations expire.
- Acceptance requires authentication.
- Acceptance must establish a membership only after verifying the intended recipient.
- Invitations must not grant access to unrelated organizations.
- An existing active membership should not be duplicated through invitation acceptance.

---

## 4. Organization lifecycle

### 4.1 Organization status

| State | Meaning | Allowed transitions |
|---|---|---|
| pending | Organization registered but onboarding incomplete | active, rejected, closed |
| active | Organization permitted to operate subject to capability approvals | suspended, closed |
| suspended | Organization access blocked | active, closed |
| rejected | Organization registration rejected | pending, closed |
| closed | Organization permanently closed | No normal transition |

### 4.2 Organization verification lifecycle

| State | Meaning | Allowed transitions |
|---|---|---|
| unverified | Verification not submitted | pending |
| pending | Verification under review | verified, rejected |
| verified | Verification completed successfully | expired, rejected |
| rejected | Verification failed | pending |
| expired | Verification validity expired | pending |

A verification rejection or expiry does not necessarily require immediate organization closure.

The platform may restrict specific capabilities according to verification policy.

### 4.3 Capability lifecycle

| State | Meaning | Allowed transitions |
|---|---|---|
| pending | Capability requested | enabled, revoked |
| enabled | Capability available subject to approval and business rules | suspended, revoked |
| suspended | Temporarily disabled | enabled, revoked |
| revoked | Capability removed | pending through a new request |

### 4.4 Membership lifecycle

| State | Meaning | Allowed transitions |
|---|---|---|
| pending | Membership awaiting acceptance or activation | active, revoked |
| active | Member has access according to assigned permissions | suspended, revoked |
| suspended | Membership temporarily blocked | active, revoked |
| revoked | Membership terminated | New invitation required |

Membership suspension must not suspend the underlying account.

Likewise, account suspension must block access even if the organization membership remains active.

---

## 5. Organization business rules

### 5.1 Organization identity

- One real-world organization should have one canonical BottomUp identity.
- Multiple capabilities must not create duplicate organization records.
- Legal name and display name are separate.
- Organization identifiers must remain stable when public-facing information changes.
- Duplicate organization registration must be detected using available evidence and reviewed where necessary.

Exact duplicate-detection rules should account for subsidiaries, campuses and legally distinct entities.

### 5.2 Multiple capabilities

- Organizations may enable multiple capabilities.
- Each capability has an independent lifecycle.
- Each capability may have separate verification and approval requirements.
- Disabling one capability must not automatically disable another.
- Capability changes must not silently delete associated memberships or business records.
- Members must possess the relevant permissions for the capability they are operating under.

### 5.3 Verification and approval

- Verification must use an approved process.
- Verification decisions must be auditable.
- Approval must be evaluated independently for each capability.
- Rejected organizations must not operate restricted functionality.
- Verification expiry must trigger applicable restrictions.
- Organization status must be checked during authorization.

### 5.4 Membership

- Memberships are organization-scoped.
- Memberships cannot be self-granted.
- Members may only perform actions allowed by their assigned permissions.
- Members cannot grant permissions they do not possess.
- Organization administrators may manage memberships within their organization subject to platform restrictions.
- Organization membership does not grant platform-wide administrative privileges.
- Membership revocation must take effect on subsequent authorization checks.

### 5.5 Invitations

- Invitations must be created by authorized members.
- Invitation acceptance must verify recipient identity.
- Expired or revoked invitations cannot be accepted.
- Duplicate active invitations for the same account, organization and proposed role should be prevented.
- Invitation acceptance must be idempotent.

---

## 6. Authorization policies

### 6.1 Organization authorization model

Organization authorization evaluates:

1. Account authentication and status.
2. Organization status.
3. Organization capability.
4. Capability approval.
5. Active organization membership.
6. Membership permissions.
7. Resource-level authorization.
8. Applicable business rules.

No single check is sufficient.

### 6.2 Authorization matrix

| Principal | Action | Rule |
|---|---|---|
| Anonymous | Register organization | Allow subject to registration policy |
| Authenticated account | Create organization | Allow subject to registration eligibility |
| Organization admin | Update organization profile | Own organization only |
| Organization admin | Invite staff | Own organization only |
| Organization admin | Revoke membership | Own organization only, subject to safeguards |
| Recruiter | Create job listing | Employer capability and applicable approval required |
| Recruiter | Publish job listing | Employer capability, approval and publishing permission required |
| Hiring manager | Review applicants | Authorized recruitment scope only |
| Counsellor | Manage career services | Career-centre capability and permission required |
| Platform admin | Verify organization | Platform-wide administrative permission |
| Platform admin | Approve capability | Platform-wide administrative permission |
| Any member | Access unrelated organization | Deny |

### 6.3 Administrative safeguards

- An organization must not be left without an authorized administrator unless explicitly permitted by platform policy.
- An organization administrator cannot grant themselves platform administrator privileges.
- Organization administrators cannot bypass platform-level verification or approval.
- High-impact administrative changes must be auditable.
- Platform administrators retain the ability to override organization-level access where authorized.

---

## 7. Domain invariants

### Organization invariants

- INV-01: Every organization has one stable canonical identifier.
- INV-02: One organization may have multiple capabilities.
- INV-03: Organization capabilities must have independent lifecycle states.
- INV-04: Organization verification and capability approval are separate.
- INV-05: A rejected or closed organization cannot perform restricted business operations.
- INV-06: A suspended organization cannot perform organization operations.
- INV-07: Capability changes must not silently delete organizational data.
- INV-08: An organization must not receive capabilities through client-side manipulation.

### Membership invariants

- INV-09: Every membership belongs to exactly one account and one organization.
- INV-10: Every active membership must have an assigned permission set.
- INV-11: Membership permissions apply only within the associated organization.
- INV-12: An inactive or revoked membership cannot authorize operations.
- INV-13: Membership changes must be auditable.
- INV-14: Organization administrators cannot grant privileges beyond their own authority.
- INV-15: Account suspension overrides all organization memberships.
- INV-16: Organization suspension overrides all organization memberships.

### Invitation invariants

- INV-17: Invitations must be associated with an organization and intended recipient.
- INV-18: Invitations are single-use and time-limited.
- INV-19: An invitation cannot be accepted by an unrelated account.
- INV-20: Repeated invitation acceptance must not create duplicate memberships.

### Cross-domain invariants

- INV-21: Organization operations must not directly modify Identity & Access account records.
- INV-22: Organization operations must not directly modify Candidate records.
- INV-23: Organization capabilities must not automatically grant candidate or staff permissions.
- INV-24: Organization identifiers supplied by clients must always be checked against authoritative membership and resource ownership.

---

## 8. Domain events

### 8.1 Events produced by Organizations

| Event | Payload | Consumers |
|---|---|---|
| organization.created | organization_id, created_by | Notifications, analytics |
| organization.updated | organization_id, changed_fields | Search, analytics |
| organization.activated | organization_id | Relevant domains |
| organization.suspended | organization_id, reason | Jobs, Candidates, Notifications |
| organization.reactivated | organization_id | Relevant domains |
| organization.closed | organization_id | Relevant domains |
| organization.verification_submitted | organization_id | Review workflow |
| organization.verified | organization_id, verification_id | Relevant domains |
| organization.verification_rejected | organization_id, reason | Notifications |
| organization.capability_requested | organization_id, capability | Review workflow |
| organization.capability_enabled | organization_id, capability | Relevant domains |
| organization.capability_suspended | organization_id, capability | Relevant domains |
| organization.capability_revoked | organization_id, capability | Relevant domains |
| organization.capability_approved | organization_id, capability | Jobs or Career Services |
| membership.invited | organization_id, invitation_id | Notifications |
| membership.created | organization_id, account_id, role | Identity & Access, audit |
| membership.role_changed | organization_id, account_id, old_role, new_role | Audit |
| membership.suspended | organization_id, account_id | Audit |
| membership.revoked | organization_id, account_id | Identity & Access, audit |
| invitation.expired | organization_id, invitation_id | Notifications |

### 8.2 Event ownership

Organizations is the sole producer of organization and membership lifecycle events.

Identity & Access consumes membership events where session or account-level behaviour requires them.

Jobs & Recruitment consumes organization capability and approval events.

Candidates consumes organization events where institution availability or career-centre functionality is affected.

Consumers must not treat asynchronous events as a substitute for current authorization checks.

### 8.3 Event delivery

Use the transactional outbox pattern.

Requirements:

- Persist events in the same transaction as aggregate changes.
- Publish asynchronously.
- Support retry and failure recovery.
- Require idempotent consumers.
- Preserve event identifiers and versions.
- Avoid publishing sensitive verification evidence in event payloads.

---

## 9. Application workflows

| Workflow | Description |
|---|---|
| Organization registration | Create canonical organization identity |
| Organization onboarding | Complete organization profile and required checks |
| Organization verification | Verify legitimacy and submitted evidence |
| Capability request | Request employer or career-centre functionality |
| Capability approval | Approve or reject a capability |
| Organization suspension | Restrict organization operations |
| Organization reactivation | Restore organization operations |
| Organization closure | Terminate organization participation |
| Staff invitation | Invite an account to join an organization |
| Invitation acceptance | Establish an organization membership |
| Membership management | Assign or modify staff permissions |
| Membership revocation | Terminate organization access |
| Organization switching | Select an organization context in the interface |

---

## 10. Error contract

| Condition | Expected outcome |
|---|---|
| Duplicate organization registration | Conflict or manual review |
| Invalid organization information | 400 validation error |
| Unauthorized organization update | 403 or concealed 404 |
| Organization suspended | Organization access blocked |
| Capability not enabled | Capability unavailable |
| Capability not approved | Approval required |
| Verification rejected | Verification failure |
| Verification expired | Re-verification required |
| Unauthorized invitation | 403 |
| Expired invitation | Invitation expired |
| Invitation already accepted | Idempotent response or conflict |
| Invitation recipient mismatch | 403 |
| Duplicate active membership | Conflict or existing membership response |
| Revoked membership | 403 |
| Unauthorized role assignment | 403 |
| Invalid organization context | Context change rejected |

---

## 11. Acceptance criteria

### Organization identity

- Given a university operating as both an employer and career centre, both capabilities exist under one organization identity.
- Given an organization with multiple capabilities, disabling one does not automatically disable the others.
- Given an organization name change, its canonical identifier remains unchanged.

### Verification and approval

- Given an unverified organization, restricted operations cannot be performed.
- Given a verified but unapproved employer capability, job publication is denied.
- Given an organization approved for employer functionality, career-centre functionality is not automatically approved.
- Given a suspended organization, all organization operations are blocked.

### Membership

- Given an account with active membership in Organization A, it cannot access Organization B without a separate membership.
- Given a recruiter membership, the user cannot perform counsellor-only operations.
- Given a revoked membership, subsequent requests are denied.
- Given an account suspension, all organization memberships become ineffective for authorization.

### Invitations

- Given a valid invitation, the intended recipient can accept it after authentication.
- Given an expired invitation, acceptance is rejected.
- Given an already accepted invitation, repeated requests do not create additional memberships.
- Given an invitation intended for another email address, acceptance is rejected.

---

## 12. Open decisions

| Decision | Recommendation |
|---|---|
| Organization uniqueness | Use legal identifiers and verification evidence where available; manual review for ambiguous matches. |
| Organization hierarchy | Defer parent/sub-organization support until a real business requirement emerges. |
| Organization capabilities | Relational capability records rather than a fixed organization type. |
| Capability approval | Separate approval records per capability. |
| Verification frequency | Define renewal requirements according to verification method. |
| Membership roles | Begin with four role templates and explicit permissions. |
| Custom permissions | Defer custom role builders until justified by usage. |
| Multiple memberships per organization | Prefer one active membership per account per organization initially. |
| Last administrator removal | Require another administrator or platform intervention. |
| Invitation expiry | Define a standard configurable expiration period. |
| Organization closure | Define associated job, application and historical record handling. |
| Organization suspension | Define which existing recruitment and career-centre records remain visible. |
| Organization discovery | Determine whether all organizations are publicly searchable. |
| Organization registration | Determine whether self-registration is allowed for all capabilities. |
| Verification evidence | Define secure storage and retention policies. |

---

## 13. Architectural principles

1. **Canonical identity:** One organization has one BottomUp identity regardless of its capabilities.
2. **Capability independence:** Employer and career-centre functionality have independent lifecycles.
3. **Verification is not approval:** Establishing legitimacy does not automatically authorize every platform operation.
4. **Membership is scoped:** Organization permissions apply only to their respective organization.
5. **Least privilege:** Members receive only the permissions required for their responsibilities.
6. **Explicit ownership:** Organizations owns organization and membership aggregates.
7. **Revocation is effective:** Suspended or revoked access must be enforced on subsequent authorization checks.
8. **Auditability:** Administrative decisions and membership changes must be traceable.
9. **No implicit privilege escalation:** Organization administrators cannot grant permissions beyond their authority.
10. **Business-first modelling:** Organization capabilities should represent actual business functions, not merely UI categories.

---

**End of Organizations Domain Contract v1.0**