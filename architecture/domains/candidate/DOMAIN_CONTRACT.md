---
id: candidate
name: Candidate
type: domain-contract
status: draft
version: 1.0.0
owner: candidate
---

# Candidate Domain Contract

## 1. Purpose

The Candidate domain manages the professional identity, career profile and employment-related information of individuals participating in the BottomUp platform.

It provides a centralized representation of each candidate, enabling other domains to access reliable and structured candidate information for recruitment, job matching, applications and AI-powered career services.

The domain ensures that candidate information is maintained consistently, securely and under the candidate's control.

## 2. Scope & Responsibilities

Define the responsibilities owned by this domain.

### In Scope

- Candidate profile creation and management.
- Candidate personal and professional information.
- Professional experience and employment history.
- Education history and qualifications.
- Skills, competencies and professional expertise.
- Certifications and professional achievements.
- Resume and portfolio references.
- Career preferences and employment preferences.
- Candidate availability and job-seeking status.
- Candidate profile completeness.
- Candidate profile visibility and privacy preferences.
- Candidate profile lifecycle management.
- Candidate consent for profile information sharing.

### Out of Scope

- Human user registration and authentication.
- Credential and session management.
- Organization membership management.
- Job posting and vacancy management.
- Job application lifecycle management.
- Recruitment pipeline and hiring workflows.
- Interview scheduling and assessment management.
- Subscription and entitlement management.
- AI agent identity and lifecycle.
- AI agent execution and orchestration.
- Payment and billing management.
- Recruitment analytics and reporting.

These responsibilities belong to their respective domains.

## 3. Domain Model

Describe the conceptual model and important relationships.

### Entities

- Candidate
  - Represents an individual's professional identity within BottomUp.
  - Associated with a human user through an external User ID reference.

- CandidateProfile
  - Contains the candidate's personal, professional and career-related information.

- WorkExperience
  - Represents a candidate's previous or current employment experience.

- Education
  - Represents academic qualifications and educational history.

- Skill
  - Represents a professional skill or competency associated with a candidate.

- Certification
  - Represents a professional certification, licence or qualification.

- Achievement
  - Represents professional accomplishments, awards or recognitions.

- Resume
  - Represents a candidate's resume document and associated metadata.

- Portfolio
  - Represents a collection of professional work samples and portfolio references.

- CareerPreference
  - Represents the candidate's preferred roles, industries and career opportunities.

- EmploymentPreference
  - Represents preferred employment arrangements, such as full-time, part-time, contract or freelance work.

- CandidateAvailability
  - Represents the candidate's availability and job-seeking status.

- CandidatePrivacySetting
  - Represents the candidate's profile visibility and information-sharing preferences.

- CandidateConsent
  - Represents permissions granted by the candidate for specific uses or sharing of their information.

### Value Objects

- CandidateId
- UserId
- CandidateName
- ContactInformation
- Location
- ProfessionalTitle
- WorkPeriod
- SkillLevel
- EmploymentType
- SalaryExpectation
- AvailabilityStatus
- ProfileVisibility
- ProfileCompleteness
- ConsentScope
- DocumentReference
- WebsiteUrl

### Aggregates & Aggregate Roots

**Candidate Aggregate**

Aggregate root: `Candidate`

Responsible for maintaining the candidate's professional identity and lifecycle.

Owns or references:

- CandidateProfile
- CandidatePrivacySetting
- CandidateAvailability
- CandidateConsent

The Candidate aggregate ensures that profile ownership, lifecycle and privacy invariants are maintained.

**Work Experience Aggregate**

Aggregate root: `WorkExperience`

Responsible for maintaining individual employment records associated with a candidate.

**Education Aggregate**

Aggregate root: `Education`

Responsible for maintaining individual educational records associated with a candidate.

**Professional Credentials Aggregate**

Aggregate root: `Certification`

Responsible for maintaining professional certifications and qualifications.

**Career Preferences Aggregate**

Aggregate root: `CareerPreference`

Responsible for maintaining the candidate's career and employment preferences.

**Design Considerations**

- Candidate is the primary aggregate root for candidate identity and lifecycle.
- Each candidate must be associated with an existing User ID.
- Related professional records must reference their owning Candidate ID.
- Changes to candidate-owned information must respect aggregate invariants.
- Large documents and binary files should be stored through an appropriate file storage capability, with Candidate retaining authoritative metadata and references.
- Aggregate boundaries should prevent unnecessary cross-aggregate transactional coupling.

## 4. Capabilities

List the capabilities belonging to this domain.

| Capability                        | Description                                                     |
| --------------------------------- | --------------------------------------------------------------- |
| Candidate Management              | Create, retrieve, update and deactivate candidate records       |
| Profile Management                | Manage personal and professional profile information            |
| Work Experience Management        | Maintain employment and career history                          |
| Education Management              | Maintain academic qualifications and educational history        |
| Skills Management                 | Maintain candidate skills and competencies                      |
| Certification Management          | Manage professional certifications and qualifications           |
| Achievement Management            | Maintain professional accomplishments and awards                |
| Resume Management                 | Manage resume metadata and document references                  |
| Portfolio Management              | Maintain portfolio information and professional work references |
| Career Preferences Management     | Maintain career interests and preferred opportunities           |
| Employment Preferences Management | Maintain preferred employment arrangements                      |
| Availability Management           | Manage candidate availability and job-seeking status            |
| Profile Privacy Management        | Control candidate profile visibility and information sharing    |
| Consent Management                | Record and manage candidate consent                             |
| Profile Completeness              | Calculate and maintain profile completeness indicators          |

## 5. Commands (Write Operations)

Define the domain's supported write operations.

| Command                           | Description                                                                 |
| --------------------------------- | --------------------------------------------------------------------------- |
| CreateCandidate                   | Create a candidate record associated with an existing user                  |
| UpdateCandidateProfile            | Update candidate personal and professional information                      |
| UpdateCandidateContactInformation | Update candidate contact information                                        |
| AddWorkExperience                 | Add an employment record                                                    |
| UpdateWorkExperience              | Update an existing employment record                                        |
| RemoveWorkExperience              | Remove an employment record                                                 |
| AddEducation                      | Add an educational record                                                   |
| UpdateEducation                   | Update an existing educational record                                       |
| RemoveEducation                   | Remove an educational record                                                |
| AddSkill                          | Associate a skill with a candidate                                          |
| UpdateSkill                       | Update a candidate's skill information or proficiency                       |
| RemoveSkill                       | Remove an associated skill                                                  |
| AddCertification                  | Add a professional certification                                            |
| UpdateCertification               | Update certification information                                            |
| RemoveCertification               | Remove a certification                                                      |
| AddAchievement                    | Add a professional achievement                                              |
| UpdateAchievement                 | Update an achievement                                                       |
| RemoveAchievement                 | Remove an achievement                                                       |
| AddResume                         | Associate a resume document with a candidate                                |
| UpdateResume                      | Update resume metadata or designate a preferred resume                      |
| RemoveResume                      | Remove a resume association                                                 |
| UpdatePortfolio                   | Create or update portfolio information                                      |
| UpdateCareerPreferences           | Update career interests and preferred roles                                 |
| UpdateEmploymentPreferences       | Update preferred employment arrangements                                    |
| UpdateCandidateAvailability       | Update availability and job-seeking status                                  |
| UpdateProfileVisibility           | Change candidate profile visibility settings                                |
| RecordCandidateConsent            | Record candidate consent for a specified purpose                            |
| RevokeCandidateConsent            | Revoke previously granted consent                                           |
| DeactivateCandidate               | Deactivate a candidate profile                                              |
| ReactivateCandidate               | Reactivate a previously deactivated candidate profile                       |
| DeleteCandidate                   | Initiate candidate data deletion according to applicable retention policies |

Reference the relevant capability and feature specifications for detailed behaviour.

## 6. Queries (Read Operations)

Define supported read operations.

| Query                             | Description                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------ |
| GetCandidate                      | Retrieve candidate information                                                       |
| GetCandidateProfile               | Retrieve a candidate's complete professional profile                                 |
| GetCandidateByUserId              | Retrieve the candidate associated with a User ID                                     |
| GetCandidateWorkExperience        | Retrieve employment history                                                          |
| GetCandidateEducation             | Retrieve educational history                                                         |
| GetCandidateSkills                | Retrieve candidate skills and competencies                                           |
| GetCandidateCertifications        | Retrieve professional certifications                                                 |
| GetCandidateAchievements          | Retrieve professional achievements                                                   |
| GetCandidateResumes               | Retrieve associated resumes and metadata                                             |
| GetCandidatePortfolio             | Retrieve portfolio information                                                       |
| GetCandidateCareerPreferences     | Retrieve career preferences                                                          |
| GetCandidateEmploymentPreferences | Retrieve employment preferences                                                      |
| GetCandidateAvailability          | Retrieve candidate availability and job-seeking status                               |
| GetCandidatePrivacySettings       | Retrieve profile visibility and privacy settings                                     |
| GetCandidateConsent               | Retrieve consent records                                                             |
| GetCandidateProfileCompleteness   | Retrieve profile completeness information                                            |
| CheckCandidateProfileVisibility   | Determine whether candidate information can be exposed to a requesting actor         |
| CheckCandidateConsent             | Evaluate whether a specified information-sharing purpose is covered by valid consent |

Queries must respect candidate privacy settings, authorization requirements and data-sharing restrictions.

## 7. Business Rules & Invariants

Define rules that must always hold within the domain.

### Candidate Identity

- Each Candidate must be associated with an existing User ID.
- A User may have at most one active Candidate profile, unless multiple candidate profiles are explicitly supported in the future.
- Candidate records must not duplicate authoritative user authentication or credential information.
- A candidate must have a valid domain-owned Candidate ID.

### Profile Management

- Candidate profile information must be associated with its owning Candidate.
- Only authorized actors may modify candidate-owned information.
- Changes to professional information must preserve data integrity.
- Profile completeness must be calculated using defined business rules.
- Profile completeness must not automatically imply that information is verified or accurate.

### Professional Information

- Work experience records must belong to an existing candidate.
- Education records must belong to an existing candidate.
- Professional records must maintain valid relationships with their owning candidate.
- Employment dates must follow valid chronological rules.
- Current employment records must not have an end date unless explicitly permitted by the business rules.
- Skills and competencies must use a consistent representation.
- Certification records should support expiration dates where applicable.

### Privacy & Consent

- Candidate information must not be exposed beyond the candidate's configured visibility and applicable authorization rules.
- Private candidate information must not be accessible to unauthorized actors.
- Consent must be purpose-specific and recorded with sufficient context.
- Revoked consent must no longer authorize future processing based on that consent.
- Consent revocation must not override independent legal or contractual retention obligations.
- Sensitive candidate information must be protected against unauthorized access and disclosure.

### Candidate Lifecycle

- Deactivated candidates must not participate in new candidate-facing workflows unless explicitly permitted.
- Reactivation must preserve applicable historical records.
- Candidate deletion must follow applicable legal, privacy and retention requirements.
- Historical references from other domains must be handled consistently when a candidate is deactivated or deleted.

## 8. Domain Events

Define events produced by this domain.

| Event                              | Trigger                        | Description                                                |
| ---------------------------------- | ------------------------------ | ---------------------------------------------------------- |
| CandidateCreated                   | Candidate creation succeeds    | A candidate record was created                             |
| CandidateProfileUpdated            | Profile information changes    | Candidate profile information was updated                  |
| CandidateContactInformationUpdated | Contact information changes    | Candidate contact information was updated                  |
| WorkExperienceAdded                | Employment record added        | A work experience record was added                         |
| WorkExperienceUpdated              | Employment record updated      | A work experience record was updated                       |
| WorkExperienceRemoved              | Employment record removed      | A work experience record was removed                       |
| EducationAdded                     | Education record added         | An educational record was added                            |
| EducationUpdated                   | Education record updated       | An educational record was updated                          |
| EducationRemoved                   | Education record removed       | An educational record was removed                          |
| CandidateSkillAdded                | Skill associated               | A skill was associated with a candidate                    |
| CandidateSkillUpdated              | Skill information changed      | Candidate skill information was updated                    |
| CandidateSkillRemoved              | Skill removed                  | A skill association was removed                            |
| CertificationAdded                 | Certification added            | A certification was associated with a candidate            |
| CertificationUpdated               | Certification updated          | Certification information was updated                      |
| CertificationRemoved               | Certification removed          | A certification association was removed                    |
| ResumeAdded                        | Resume associated              | A resume was associated with a candidate                   |
| ResumeUpdated                      | Resume information changed     | Resume metadata was updated                                |
| ResumeRemoved                      | Resume association removed     | A resume association was removed                           |
| CareerPreferencesUpdated           | Career preferences changed     | Candidate career preferences were updated                  |
| EmploymentPreferencesUpdated       | Employment preferences changed | Employment preferences were updated                        |
| CandidateAvailabilityUpdated       | Availability changed           | Candidate availability was updated                         |
| CandidateProfileVisibilityChanged  | Visibility changed             | Candidate profile visibility was changed                   |
| CandidateConsentGranted            | Consent recorded               | A candidate granted consent for a specified purpose        |
| CandidateConsentRevoked            | Consent revoked                | Previously granted candidate consent was revoked           |
| CandidateProfileCompleted          | Completeness threshold reached | Candidate profile reached a defined completeness threshold |
| CandidateDeactivated               | Candidate deactivated          | Candidate profile became inactive                          |
| CandidateReactivated               | Candidate reactivated          | Candidate profile became active                            |
| CandidateDeletionRequested         | Deletion initiated             | Candidate data deletion was requested                      |
| CandidateDeleted                   | Deletion completed             | Candidate data deletion was completed                      |

Domain events should contain identifiers and relevant metadata rather than unnecessarily exposing personal or sensitive candidate information.

## 9. Authorization Requirements

Define:

- Actors and their access levels.
- Operations requiring authorization.
- Permission evaluation rules.
- Privileged operations and restrictions.
- Cross-domain authorization requirements.

### Actors

**Candidate**

- View their own candidate profile.
- Create and update their professional information.
- Manage career and employment preferences.
- Manage profile visibility.
- Grant and revoke consent.
- Request profile deactivation or deletion.

**Platform Administrator**

- Perform authorized candidate account administration.
- Handle exceptional candidate support and moderation operations.
- Access candidate information only where explicitly authorized and necessary.

**Organization Representative**

- Access candidate information according to the applicable recruitment permissions, profile visibility and consent requirements.
- Must not modify candidate-owned professional information.

**AI Agent**

- Access candidate information only through authorized capabilities and delegated permissions.
- Must respect candidate privacy, consent and data-access restrictions.
- Must not independently change candidate-owned information without appropriate authorization.

**Other Internal Domains**

- Access candidate information through approved domain interfaces.
- Must not directly modify Candidate-owned records.

### Authorization Requirements

- Candidates may modify only their own candidate records.
- Candidate ownership must be established using the authenticated User ID.
- Administrative operations require explicit privileged permissions.
- Access to candidate information must be evaluated according to the requesting actor, purpose and candidate privacy settings.
- Organization-level access must be resolved using the Organization and Identity & Access domains.
- AI agents must operate under an explicit authorization context.
- Consent requirements must be evaluated independently of general authentication and authorization.
- Sensitive operations must generate appropriate audit records.

### Cross-Domain Authorization

Reference the Cross-Domain Authorization Specification.

Candidate must rely on Identity & Access for authentication and authoritative user authorization.

Candidate must not independently implement human authentication or organization membership authorization.

Candidate remains responsible for enforcing candidate-owned privacy and consent rules when exposing candidate information through its interfaces.

## 10. Cross-Domain Dependencies

Document interactions with other domains.

| Domain                             | Dependency                                          | Purpose                                                                               |
| ---------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Identity & Access                  | User identity and authorization                     | Associate candidates with authenticated users and validate access permissions         |
| Organizations                      | Organization identity and membership                | Determine organizational context and membership-based access to candidate information |
| Jobs                               | Job and opportunity information                     | Support candidate career preferences and relevant job discovery                       |
| Applications                       | Candidate profile and professional information      | Provide candidate information required for job applications                           |
| Matching                           | Candidate attributes and preferences                | Support candidate-job matching and recommendation processes                           |
| AI Agent                           | Candidate profile context                           | Provide authorized candidate information for AI-powered career assistance             |
| Notifications                      | Candidate communication preferences and identifiers | Support candidate-related notifications                                               |
| Billing                            | Entitlement evaluation                              | Determine whether paid candidate capabilities are available                           |
| Audit & Compliance                 | Candidate-related audit events                      | Record sensitive data access, changes and lifecycle operations                        |
| File Storage / Document Management | Document storage and retrieval                      | Store and retrieve resumes and portfolio documents                                    |

### Dependency Rules

- Identity & Access is authoritative for human user identity and authentication.
- Candidate is authoritative for candidate professional information.
- Organizations is authoritative for organizational identity and membership.
- Jobs is authoritative for job and opportunity information.
- Applications is authoritative for application lifecycle information.
- Matching is responsible for matching logic and matching results.
- AI Agent is responsible for agent execution and orchestration.
- Billing is authoritative for subscription and entitlement information.
- Audit & Compliance is responsible for audit record management.

Cross-domain interactions should use published interfaces, application services or domain events rather than direct access to another domain's internal data.

## 11. External Integrations

Document external systems and integration boundaries.

| Integration                             | Purpose                                                                   | Direction          |
| --------------------------------------- | ------------------------------------------------------------------------- | ------------------ |
| File Storage Provider                   | Store and retrieve resumes and portfolio documents                        | Outbound           |
| Resume Parsing Service                  | Extract structured professional information from resumes                  | Outbound           |
| Skills Taxonomy Provider                | Normalize skills and competencies                                         | Inbound / Outbound |
| External Professional Profile Providers | Import authorized professional profile information                        | Inbound            |
| Email Provider                          | Support candidate-related communications through the Notifications domain | Indirect           |
| AI Services                             | Support authorized extraction and enrichment of candidate information     | Outbound           |

### Integration Requirements

- External integrations must not become authoritative sources of candidate identity or profile ownership.
- Imported information must be associated with the correct candidate.
- Candidates must authorize external profile imports where required.
- Resume parsing and AI enrichment results should be treated as unverified information until accepted or verified through defined business processes.
- External integration failures must not corrupt candidate-owned records.
- Integration operations must support appropriate error handling and retry mechanisms.

## 12. Data Ownership & Lifecycle

Define:

### Authoritative Data Ownership

Candidate owns:

- Candidate ID and candidate lifecycle status.
- Candidate-to-User association reference.
- Candidate personal and professional profile information.
- Work experience and employment history.
- Education and qualifications.
- Skills and competencies associated with the candidate.
- Certifications and achievements.
- Resume and portfolio metadata and references.
- Career and employment preferences.
- Candidate availability and job-seeking status.
- Candidate privacy settings.
- Candidate consent records.
- Candidate profile completeness information.

Candidate does not own:

- Authentication credentials and sessions.
- Human identity and account security records.
- Organization membership records.
- Job and vacancy records.
- Job application records.
- Subscription and payment records.
- AI agent identity and execution state.

### Data Creation & Updates

- Candidate records are created following an authorized candidate registration or onboarding workflow.
- The Candidate domain associates the record with an existing User ID.
- Candidate-owned information is updated through authorized commands.
- External information imports must be validated before being incorporated into authoritative candidate records.
- Candidate profile changes should be timestamped and traceable.
- Important profile changes should produce domain events.

### Data Retention & Deletion

- Candidate data must be retained according to applicable privacy, legal and business requirements.
- Candidates must have a supported process to request deletion of their personal information.
- Deletion must consider references held by other domains.
- Personal information should be anonymized or removed where retention is no longer justified.
- Audit records must follow their own retention policies.
- Binary documents must be deleted or retained according to their associated data lifecycle and applicable legal requirements.

### Data Exposure

- Other domains must access candidate information through approved interfaces.
- Candidate information should be exposed according to the requesting actor's permissions and the candidate's privacy settings.
- Sensitive personal information should be excluded from general-purpose candidate data responses unless explicitly required and authorized.
- Data transfer should follow defined domain contracts and event schemas.

### Data Consistency

- Candidate-owned records must maintain referential integrity.
- Cross-domain data consistency should generally use eventual consistency through domain events.
- Candidate profile updates must not require synchronous transactions across unrelated domains.
- Consumers must handle duplicate and out-of-order events where applicable.
- Event publishing must reliably reflect committed domain changes.

## 13. Non-Functional Requirements

Define relevant requirements for:

### Security

- Candidate personal information must be protected against unauthorized access.
- Sensitive candidate data must be encrypted in transit and at rest.
- Access to candidate information must follow least-privilege principles.
- Candidate ownership must be validated for all self-service operations.
- Sensitive data access and modification must be auditable.
- AI services and external integrations must operate within approved data-access boundaries.

### Performance

- Candidate profile retrieval should support responsive user experiences.
- Candidate profile updates should complete within acceptable application response times.
- Queries should support efficient retrieval of individual candidate information.
- Profile completeness calculations should not unnecessarily impact normal profile updates.

### Availability

- Candidate profile services should meet the platform's defined availability objectives.
- Temporary failures in external integrations should not prevent access to existing candidate information.
- Critical candidate profile operations should remain reliable during partial dependency outages.

### Scalability

- Candidate records should support growth in the number of registered candidates.
- Professional records should support increasing amounts of structured information.
- Candidate profile queries should support future matching and recruitment workloads.
- Document storage should scale independently from candidate profile data.

### Reliability

- Candidate updates must preserve data integrity.
- Domain event publication must be reliable.
- External integration failures must be recoverable.
- Critical lifecycle operations must be idempotent where appropriate.

### Privacy

- Candidate information must be processed for legitimate and defined purposes.
- Candidate consent and privacy preferences must be respected.
- Data collection should follow data minimization principles.
- Retention and deletion must comply with applicable requirements.
- Candidate information must not be exposed through unauthorized cross-domain access.

## 14. Testing Requirements

Define:

### Domain Invariant Tests

- Candidate must reference a valid User ID.
- A User cannot have multiple active candidate profiles under the default one-to-one association rule.
- Candidate-owned records must reference an existing Candidate ID.
- Work experience dates must follow valid chronological rules.
- Candidate privacy settings must be respected.
- Revoked consent must no longer authorize future consent-based processing.
- Deactivated candidates must follow defined lifecycle restrictions.

### Unit Tests

- Candidate creation and lifecycle operations.
- Candidate profile management.
- Work experience management.
- Education management.
- Skills and certification management.
- Career and employment preference management.
- Profile completeness calculations.
- Privacy and consent evaluation.

### Integration Tests

- Identity & Access integration.
- Organization authorization integration.
- File storage integration.
- Resume parsing integration.
- Candidate data retrieval by other domains.
- Domain event publication and consumption.
- Candidate deletion and cross-domain data lifecycle coordination.

### Contract Tests

- Candidate domain API contracts.
- Candidate domain event schemas.
- Cross-domain data exposure contracts.
- Authorization and privacy enforcement contracts.
- External integration contracts.

### Security & Privacy Tests

- Unauthorized candidate profile access.
- Candidate ownership validation.
- Cross-candidate data access isolation.
- Privileged administrative access.
- Sensitive information exposure.
- Consent enforcement.
- Consent revocation.
- Candidate deletion and retention behaviour.
- AI agent access restrictions.

## 15. Domain Acceptance Criteria

Define the conditions that must be satisfied for the domain contract to be considered implemented.

- Candidate records can be created and associated with existing User IDs.
- Candidate profiles can be created, retrieved and updated.
- Candidate professional information can be maintained independently.
- Work experience, education, skills and certifications are supported.
- Resume and portfolio references can be maintained.
- Career and employment preferences can be managed.
- Candidate availability can be managed.
- Candidate profile completeness can be calculated consistently.
- Candidate privacy settings can be configured and enforced.
- Candidate consent can be recorded, retrieved and revoked.
- Candidate lifecycle operations are supported.
- Candidate-owned data remains authoritative within the domain.
- Other domains can retrieve authorized candidate information through approved interfaces.
- Candidate domain events are published for relevant business operations.
- Cross-domain authorization requirements are enforced.
- Sensitive candidate information is protected and auditable.
- Candidate data retention and deletion requirements are supported.
- Domain invariants and security requirements are covered by automated tests.

## 16. Open Questions

List unresolved architectural and business decisions.

### 1. Candidate-to-User Relationship

**Question:** Should each User be restricted to one Candidate profile, or should a User be allowed to manage multiple Candidate profiles?

**Proposed Approach:** Adopt a one-to-one relationship initially, with one active Candidate profile per User. This simplifies ownership, authorization and lifecycle management. Revisit if BottomUp introduces multi-person or representative-managed candidate accounts.

### 2. Candidate Registration Lifecycle

**Question:** Should Candidate records be created automatically during user registration, or only when a user explicitly enters the candidate onboarding process?

**Proposed Approach:** Create Candidate records when a user explicitly selects the candidate onboarding journey. This prevents every registered user from automatically becoming a candidate and keeps Identity & Access independent of candidate-specific business workflows.

### 3. Resume Storage Ownership

**Question:** Should the Candidate domain own actual resume files, or should it only manage document metadata and references?

**Proposed Approach:** Store binary documents through a centralized File Storage or Document Management capability. Candidate should own resume metadata, document associations and lifecycle references, but not the underlying storage infrastructure.

### 4. Resume Parsing and AI Enrichment

**Question:** Should resume parsing and AI-powered profile enrichment be implemented inside Candidate or delegated to the AI Agent domain?

**Proposed Approach:** Delegate AI execution and orchestration to the AI Agent domain or an appropriate AI capability. Candidate should own the resulting structured information after validation and acceptance by the candidate.

### 5. Skills Taxonomy

**Question:** Should skills be represented as free-text values, a centralized taxonomy, or a combination of both?

**Proposed Approach:** Adopt a centralized skills taxonomy with support for aliases and normalized skill identifiers. Allow controlled free-text additions where a skill is not yet available in the taxonomy. This provides flexibility while supporting consistent matching and reporting.

### 6. Candidate Profile Visibility

**Question:** Should candidate profiles be publicly visible by default, visible only to authorized organizations, or private by default?

**Proposed Approach:** Default to private or restricted visibility until the candidate explicitly chooses to make their professional profile discoverable. Support configurable visibility levels and enforce them through Candidate-owned privacy policies.

### 7. Candidate Search and Discovery

**Question:** Should candidate search and discovery functionality belong to Candidate or to a separate Matching or Search domain?

**Proposed Approach:** Candidate should expose structured profile information and provide the necessary data interfaces. Dedicated search, indexing and matching capabilities should belong to their respective domains to avoid coupling profile management with discovery algorithms.

### 8. Candidate Verification

**Question:** Should Candidate be responsible for verifying employment history, education, certifications and other professional claims?

**Proposed Approach:** Candidate should own verification status and related metadata, but verification workflows should be delegated to a dedicated verification capability or an appropriate external service. Candidate should distinguish between self-declared, externally verified and unverified information.

### 9. Candidate Availability

**Question:** Should candidate availability represent general job-seeking status, immediate availability, or both?

**Proposed Approach:** Support both concepts separately. Maintain a job-seeking status, such as actively looking, open to opportunities or not looking, alongside an optional availability date or period.

### 10. Candidate Salary Expectations

**Question:** Should salary expectations belong to Candidate, or should they be maintained within job applications?

**Proposed Approach:** Maintain general salary preferences within Candidate as career preferences. Allow applications to capture application-specific salary expectations separately when required.

### 11. Candidate Data Deletion

**Question:** Should candidate deletion be a hard deletion, soft deletion or anonymization process?

**Proposed Approach:** Implement a controlled deletion workflow. Deactivate the candidate immediately where appropriate, coordinate deletion or anonymization across dependent domains, and retain only information required by applicable legal, regulatory or contractual obligations.

### 12. Candidate Consent Granularity

**Question:** Should consent be managed as a single general agreement or as separate permissions for different purposes, organizations and data categories?

**Proposed Approach:** Adopt purpose-specific consent records. Where appropriate, record the purpose, data categories, recipient or recipient scope, timestamp, consent version and revocation status. Avoid treating general platform terms acceptance as blanket authorization for all candidate data sharing.

### 13. Candidate Contact Information Ownership

**Question:** Should candidate contact information be owned by Identity & Access or Candidate?

**Proposed Approach:** Identity & Access should remain authoritative for authentication-related identifiers, such as the login email. Candidate should own professional contact information intended for profile display and recruitment communication. Any shared information should be exposed through controlled interfaces rather than duplicated without clear ownership.

### 14. Candidate Profile Completeness

**Question:** Should profile completeness be a simple percentage or a weighted score based on the importance of individual profile sections?

**Proposed Approach:** Use a configurable weighted completeness model based on required and recommended profile sections. Keep completeness separate from profile verification and professional suitability.

### 15. Multiple Resumes

**Question:** Should candidates be allowed to maintain multiple resumes for different roles or industries?

**Proposed Approach:** Support multiple resumes per candidate, with the ability to designate a default resume and associate specific resumes with different career preferences or applications.

### 16. Candidate Profile Versioning

**Question:** Should historical versions of candidate profiles be retained?

**Proposed Approach:** Maintain an appropriate change history for important candidate profile information, particularly information used in recruitment and applications. Consider immutable snapshots or references at application submission time so that historical applications are not unintentionally altered by subsequent profile updates.

### 17. Candidate Information Exposure to AI Agents

**Question:** Should AI agents have direct access to complete candidate profiles, or should access be restricted to purpose-specific information?

**Proposed Approach:** Adopt purpose-specific, least-privilege access. AI agents should receive only the candidate information required for a particular task, subject to authorization, privacy settings and applicable consent requirements.

## 17. Related Specifications

List relevant documents.

- DOMAIN_ARCHITECTURE.md
- DOMAIN_CONTEXT_MAP.md
- Cross-Domain Authorization Specification
- Domain Event Specification
- Data Ownership Specification
- Candidate Lifecycle Specification
- Candidate Profile Management Specification
- Candidate Onboarding Specification
- Candidate Privacy & Consent Specification
- Resume & Document Management Specification
- Candidate Skills & Competencies Specification
- Candidate Career Preferences Specification
- Candidate Availability Specification
- Candidate Profile Visibility Specification
- Candidate API Specification
- Candidate Domain Data Model Specification
- Relevant capability and feature specifications

---

**Document Status:** Draft

**Version:** 1.0.0

**Owner:** Candidate Domain

**Next Step:** Validate domain boundaries, aggregate ownership, cross-domain dependencies and open questions against the overall BottomUp Domain Architecture before implementation.
