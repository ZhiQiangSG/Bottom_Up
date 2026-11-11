# Identity & Access — Domain Contract

> Roles, credentials, sessions, and verification shared by all features in this domain.
> Owns who a user is and what they may do. Does not own jobs, search, or tracking.
> Co-owns organization identity and candidate segmentation with the `organizations` and `candidates` domains (see Open decisions).

## Ubiquitous language

| Term | Definition |
| --- | --- |
| Account | A `users.User` row. Owns credentials, verification, suspension, and one or more account roles. |
| Account role | One of `candidate`, `employer_member`, `school_admin_member`, `platform_admin`. A user may hold **multiple** roles. Roles are granted at registration, by invitation, or by admin action; users cannot self-grant roles. |
| Active role | The single account role a user is currently acting under, chosen per session after login. Authorization and dashboard routing resolve against the active role. |
| Candidate | The canonical job-seeker entity. Present when the account holds the `candidate` role. |
| Candidate segment | One of `student`, `professional`. Used for UI routing, filters, and analytics. Not a security boundary. |
| Student segment | Candidate currently enrolled at an institution; drives campus UX and career-centre access eligibility. Can coexist with prior or current work experience. |
| Professional segment | Candidate not currently using student status; includes employed, unemployed, returning, career-changing, and gig/trade workers. |
| Education affiliation | A candidate's relationship to an institution: `current_student`, `alumni`, `not_enrolled`; carries verification status. |
| Career-centre entitlement | Institution-scoped permission for a candidate to use a career centre's services. Distinct from segment; may apply to students and alumni. |
| Organization | A career centre or employer. Owns company/profile data. Has many staff members. |
| Organization membership | Links a user account to an organization with a role (`recruiter`, `hiring_manager`, `counsellor`, `org_admin`). Required for every `employer_member` / `school_admin_member` role. |
| Unverified account | Newly registered account with `User.is_verified=False`; must confirm email before full access. |
| Suspended account | Account flagged `User.is_suspended=True` by an admin; login is blocked entirely. |
| Temporary session | Authenticated but unverified session issued at registration; limited to onboarding/verification pages. |
| Verification email | Email carrying a single-use token that flips `User.is_verified` to `True`. |

## Entities & aggregates

| Entity | Key fields (type) | Relations | Notes |
| --- | --- | --- | --- |
| `users.User` (exists; needs added fields) | `email: EmailField unique`, `name: CharField`, `password: hashed`, `USERNAME_FIELD=email`, `username=None`, `first_name=None`, `last_name=None`, **`is_verified: bool=False`**, **`is_suspended: bool=False`** | — | See `ARCHITECTURE.md` §5; Argon2 hasher. Verification and suspension are **account-level**, not role-level, so they cannot diverge across roles. |
| `AccountRole` (proposed; replaces `Role`) | `user: FK settings.AUTH_USER_MODEL`, `role: enum(candidate, employer_member, school_admin_member, platform_admin)`, `granted_at: datetime`, `granted_by: FK User nullable` | **Many-to-one** with user; `unique_together(user, role)` | A user may hold several roles (e.g., `candidate` + `employer_member` for a working recruiter). |
| `CandidateProfile` (proposed) | `user: FK`, `segment: enum(student, professional)`, `headline`, `skills`, `experience_band: enum(0_5, 5_plus)`, `availability` | One-to-one with user, exists iff user holds `candidate` role | Experience band is stored independently of segment. |
| `EducationAffiliation` (proposed) | `candidate: FK`, `institution: FK Organization(type=career_center)`, `status: enum(current_student, alumni, not_enrolled)`, `graduation_year: int`, `major: str`, `verification_status: enum(unverified, verified, rejected)` | Many per candidate | Multiple affiliations allowed (e.g., current program + prior alumni). |
| `CareerCenterEntitlement` (proposed) | `candidate: FK`, `institution: FK Organization`, `source: enum(student_verification, alumni, invitation, manual)`, `status: enum(active, revoked, expired)` | Many per candidate | This — not `role` — gates career-centre services. |
| `Organization` (proposed; may move to `organizations` domain) | `name`, `type: enum(employer, career_center)`, `website_url`, `company_approved: bool=False`, `company_verified: bool=False` | Has many memberships | Replaces `company_name`/`university` on profiles. |
| `OrganizationMembership` (proposed) | `user: FK`, `organization: FK`, `role: enum(recruiter, hiring_manager, counsellor, org_admin)`, `is_active: bool` | Many per user; many per org | Required for `employer_member` / `school_admin_member` role holders. |

## RBAC Roles

**Account roles** are additive capabilities. A user's effective permissions are the intersection of:

1. the roles they hold (`AccountRole` rows),
2. the **active role** for the current session,
3. resource-level checks (organization membership, entitlement, ownership).

Candidate segments (`student`, `professional`) are **not** RBAC roles. They affect onboarding, default filters, and which surfaces are shown, but must not be used as authorization checks. Career-centre access is authorized by `CareerCenterEntitlement`, never by segment alone.

**Active role selection.** At login, if a user holds exactly one role, that role becomes active automatically. If they hold multiple, they must choose an active role before reaching any dashboard (a role picker), or the client supplies it via `?role=` on redirect. The active role is stored **in session** and can be switched without re-authenticating. Authorization MUST reject any action performed under a role the user does not hold, even if the resource would otherwise permit it.

Role-dashboard route map (proposed):

| Active role | Landing | Notes |
| --- | --- | --- |
| `candidate` | Candidate dashboard (student vs professional landing by segment) | Requires `CandidateProfile` |
| `employer_member` | Employer dashboard for the selected organization | Requires ≥1 active `OrganizationMembership` |
| `school_admin_member` | Career-center dashboard for the selected institution | Requires ≥1 active `OrganizationMembership` |
| `platform_admin` | Admin console | — |

Exact routes are an open decision (see `login.md`).

## Password Policy

Unchanged from previous version.

- Minimum length 8; at least one letter and one digit (Django `MinimumLengthValidator(8)` + custom check; see `ARCHITECTURE.md` §5 allauth `ACCOUNT_SIGNUP_FIELDS=[email*, password1*, password2*]`).
- `password1` must equal `password2`; mismatch is a field error, no record created.
- Email must parse as a valid address and be unique (case-insensitive); duplicates return an account-conflict error without revealing which field matched beyond the email itself.

## Session Management

Unchanged mechanics; added active-role lifecycle.

- Browser UI uses allauth session cookie; API clients use DRF `Token` via `POST /api/auth-token/` (see `ARCHITECTURE.md` §5).
- Session stores `active_role` (and, for staff roles, `active_organization_id`). These are not exposed as mutable API fields without authorization.
- `logout.md` confirmation modal is required; cancel leaves the session untouched.
- Scoped to current browser session only; multi-device revocation is out of scope.

## Email Verification

Unchanged mechanics; added rules for affiliation and entitlement verification.

- `User.is_verified=False` at creation; single-use token emailed via Mailpit locally (`:8025`).
- Unverified login attempt: blocked or flagged with an account-status message, no dashboard redirect.
- Suspended login attempt: blocked with a generic account-status message (no existence leak beyond the attempting account).
- Registration email/token failure surfaces a server-timeout error with no half-created authenticated session (see `register.md` timeout scenario).
- Education affiliation and career-centre entitlement verification are **separate** from email verification and may be pending while the account is otherwise active.

## State machine

Account state (unchanged; now account-level rather than role-level):

| State | Meaning | Allowed next states |
| --- | --- | --- |
| `unverified` | Registered, email not confirmed | `active`, `suspended` |
| `active` | Verified, may log in fully | `suspended` |
| `suspended` | Admin-flagged, login blocked entirely (all roles) | `active` (unsuspend) |

Candidate segment transitions (unchanged):

| Segment | Allowed next segments | Trigger |
| --- | --- | --- |
| `student` | `professional` | Affiliation changes to `alumni`/`not_enrolled`, or candidate opts out |
| `professional` | `student` | New verified `current_student` affiliation |

Segment changes never revoke account access; they may open or close career-centre entitlements.

Role lifecycle (new):

| Event | Effect |
| --- | --- |
| Role granted | New `AccountRole` row; if user had no active role, this becomes the default candidate for active selection |
| Role revoked | `AccountRole` row removed (or soft-deleted); if it was the active role, session is forced to re-pick; role-specific artifacts (profile, membership) are **not** auto-deleted — see Open decisions |
| Membership deactivated | Staff role still held but no active organization; user is redirected to org selection or blocked from staff actions |

## Invariants

- [ ] INV-01: Every `User` row has **at least one** `AccountRole`. `AccountRole` is unique per `(user, role)`. **Conditionally**, `candidate` ⇒ exactly one `CandidateProfile`; `employer_member` / `school_admin_member` ⇒ at least one **active** `OrganizationMembership`; `platform_admin` ⇒ none.
- [ ] INV-02: `User.is_verified=False` accounts never reach a role dashboard beyond onboarding, under **any** role.
- [ ] INV-03: Failed registration (validation, duplicate, timeout) creates no user row, no `AccountRole`, and no session.
- [ ] INV-04: Logout always clears local tokens/cookies even when the server is unreachable.
- [ ] INV-05: `CandidateProfile.segment=student` requires at least one `EducationAffiliation.status=current_student`; it does not require verification to display the segment, but unverified affiliations must be clearly flagged.
- [ ] INV-06: Career-centre actions require an `active` `CareerCenterEntitlement` for the acting institution. Segment alone is insufficient.
- [ ] INV-07: Segment is presentation/onboarding state only; it must not be used as the sole authorization check, and it must not delete or hide stored experience data.
- [ ] INV-08: A candidate may hold multiple `EducationAffiliation` and `CareerCenterEntitlement` rows; no uniqueness constraint on institution.
- [ ] INV-09: `Organization.type=career_center` organizations cannot post jobs; `Organization.type=employer` organizations cannot grant career-centre entitlements.
- [ ] INV-10: Every authorized request resolves an **active role** that the user actually holds. Requests carrying an active role the user does not hold are rejected with 403 before any resource check.
- [ ] INV-11: Revoking a role must not silently delete another role's data. A user transitioning from `candidate` + `employer_member` to `employer_member` alone must retain or explicitly archive candidate data; the contract for archiving is an Open decision.
- [ ] INV-12: `User.is_suspended` blocks login for **all** roles; there is no role-scoped suspension in this version (use `OrganizationMembership.is_active` for org-level removal).

## Authorization matrix

| Role / principal | Action | Rule |
| --- | --- | --- |
| Anonymous | Register (`01`) | Allow when logged out and email unused |
| Anonymous | Log in (`02`) | Allow; generic error on bad credentials |
| Any authenticated account | Log out (`03`) | Allow own current session only |
| Any authenticated account | Switch active role | Allow only to roles the user holds; no re-auth required |
| platform_admin | Suspend/unsuspend account | Allow (platform-wide; affects all roles) |
| school_admin_member | Suspend/unsuspend candidate **within own institution** | Allow only for candidates with an entitlement or affiliation to that institution (proposed) |
| employer_member | Post job | Allow only when active role is `employer_member` and the selected `Organization.company_approved` and `company_verified` |
| school_admin_member | Approve listing | Allow when active role is `school_admin_member`, approval queue is active, and listing targets their institution |
| school_admin_member | View candidates | Allow only for candidates with an active entitlement to that institution |
| candidate (segment=student) | Use career-centre services | Allow only with an active `CareerCenterEntitlement` |
| candidate (segment=professional) | Use career-centre services | Allow only with an active `CareerCenterEntitlement` (e.g., alumni) |
| Any account | Act under a role not held | **Deny** (403) regardless of resource ownership |

## Domain events & side effects

| Event | Payload (JSON-serializable) | Produced by | Consumed by |
| --- | --- | --- | --- |
| `user.registered` | `{"user_id": "int", "role": "str"}` | Registration view | Verification-email Celery task |
| `account.role_granted` | `{"user_id": "int", "role": "str", "granted_by": "int|null"}` | Admin/invitation flow | Notification; analytics |
| `account.role_revoked` | `{"user_id": "int", "role": "str", "revoked_by": "int"}` | Admin flow | Session active-role invalidation; analytics |
| `session.active_role_changed` | `{"user_id": "int", "from": "str|null", "to": "str"}` | Role switcher / login | Analytics; audit log |
| `candidate.segment_changed` | `{"user_id": "int", "from": "str", "to": "str", "reason": "str"}` | Affiliation/segment update | Analytics; career-centre entitlement recompute |
| `affiliation.verified` | `{"user_id": "int", "institution_id": "int", "status": "str"}` | Affiliation verification | Entitlement issuance; notification |
| `entitlement.granted` | `{"user_id": "int", "institution_id": "int", "source": "str"}` | Entitlement service | Career-centre surfaces; analytics |
| `verification.email_sent` | `{"user_id": "int"}` | Email task | Mailpit locally / Mailgun in prod |
| `user.logged_in` | `{"user_id": "int", "roles": ["str"], "active_role": "str"}` | Login view / OAuth callback | Analytics log (no PII beyond id/roles) |
| `user.logged_out` | `{"user_id": "int"}` | Logout view | Session invalidation |

## Error contract

| Condition | Observable outcome |
| --- | --- |
| Missing field / mismatched / weak password / bad email | 400 with inline field errors; input preserved; no record created |
| Duplicate email | Account-conflict error; no duplicate record |
| Missing Terms/Privacy checkboxes | Agreements-required error; no record created |
| Restricted domain for Student/School Admin | Domain-restriction error; no record created |
| Wrong email or password at login | Generic "Invalid email or password"; password cleared; stay on page |
| Unverified/suspended at login | Account-status message; no dashboard redirect |
| OAuth cancel/failure | OAuth error shown; no session issued |
| DB/email timeout mid-registration | Server-timeout error; no half-created session |
| Candidate attempts career-centre action without entitlement | 403 with generic "Career-centre access required"; no institution existence leak |
| Staff account without active organization membership | 403 with generic "Organization access required" |
| Segment change without qualifying affiliation | Field error; segment unchanged; no partial write |
| Multi-role user with no active role selected | Redirect to role picker; no resource access until selected |
| Request specifying an active role the user does not hold | 403; session active role unchanged; no role escalation |
| Role revoked while it is the active role | Next request forces role re-selection; no stale authorization |

## Open decisions

- **Account role storage**: `AccountRole` many-to-one (this revision) vs denormalized `User.roles` array — see `ARCHITECTURE.md` §12; record in `docs/decisions/NNNN-role-storage.md`.
- **Active role storage**: session-only (current), URL-scoped (`/employer/...`), or persisted `User.active_role` field. Session-only is simplest but breaks deep links; URL-scoped is shareable but leaks role context; persisted field risks stale state across devices.
- **Role grant policy**: which roles can self-register (`candidate`), which require invitation (`employer_member`, `school_admin_member`), which require admin action (`platform_admin`). Current contract does not pin this down beyond "users cannot self-grant roles."
- **Role revocation semantics**: when a role is revoked, are its dependent artifacts (candidate profile, education affiliations, entitlements) archived, soft-deleted, or retained indefinitely? INV-11 currently forbids silent deletion but does not define the retention model.
- **Suspension granularity**: account-level only (current). If role-scoped suspension is needed later (e.g., suspend employer posting while keeping candidate access), it will need a new `AccountRole.is_suspended` or `OrganizationMembership.is_active` semantics beyond what exists today.
- **Domain ownership**: should `Organization`, `OrganizationMembership`, `EducationAffiliation`, and `CareerCenterEntitlement` live in this domain, a new `organizations` domain, or a `candidates` domain? This contract assumes this domain owns them provisionally.
- **Career-centre entitlement issuance**: which sources auto-grant (student verification, alumni list import, invitation) and who can revoke.
- **Alumni access**: which institutions grant entitlements to alumni, and for how long after graduation.
- **"Professional" label**: confirm with user research that working adults in trades, gig work, and shift work identify with the label; alternatives include "Working adult", "Job seeker", "Community member".
- Google OAuth scope and account-matching rule (email match vs explicit link) — see `login.md` and `ARCHITECTURE.md` §12.
- Approved email-domain list owner and storage location — see `register.md`.
- Whether `platform_admin` exists as a separate role or is a Django `is_staff` flag.