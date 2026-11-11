## BottomUp Domain Map (Summarised)

### A. Identity and agent

| # | Domain            | Core responsibility                                                                                 |
| - | ----------------- | --------------------------------------------------------------------------------------------------- |
| 1 | `identity_access` | Human identity, authentication, organizational memberships, roles, permissions and authorization.   |
| 2 | `organization`    | Organizational identity, profiles, capabilities, settings and lifecycle.                            |
| 3 | `candidate`       | Candidate profiles, education, skills, experience, preferences and career goals.                    |
| 4 | `agent_identity`  | Agent principals, delegation grants, scoped authority, delegation chains and agent credentials.     |
| 5 | `assistant`       | Personal agents, conversations, context, memory, planning and task orchestration.                   |
| 6 | `tool_governance` | Tool registry, approved capabilities, invocation policies, approval gates and execution governance. |

### B. Career and recruitment

| #  | Domain            | Core responsibility                                                                             |
| -- | ----------------- | ----------------------------------------------------------------------------------------------- |
| 7  | `opportunity`   | Job listings, internships, graduate programmes and publication lifecycle.                       |
| 8  | `discovery`       | Search, candidate-opportunity matching, ranking and recommendations.                            |
| 9  | `application`     | Application submissions, recruitment pipelines, interviews, offers and outcomes.                |
| 10 | `career_services` | Career-centre operations, student management, advising, programmes and institutional workflows. |
| 11 | `communication`   | Conversations, messages, announcements and user interactions.                                   |

### C. Platform services

| #  | Domain         | Core responsibility                                                                      |
| -- | -------------- | ---------------------------------------------------------------------------------------- |
| 12 | `integration`  | External connectors, APIs, webhooks, credentials and third-party system synchronization. |
| 13 | `notification` | Notification generation, routing, delivery preferences and delivery lifecycle.           |
| 14 | `billing`      | Subscription plans, entitlements, usage metering, credits, invoices and payments.        |

### D. Governance and intelligence

| #  | Domain       | Core responsibility                                                                            |
| -- | ------------ | ---------------------------------------------------------------------------------------------- |
| 15 | `analytics`  | Platform analytics, institutional reporting, employer insights and business intelligence.      |
| 16 | `compliance` | Audit evidence, privacy governance, consent requirements, retention and regulatory compliance. |

---

## A. Identity and agent domains

### 1. Identity & Access

Purpose: Manage user identities, authentication, authorization and account security.

| Capability                  | Operations / use cases                                                    |
| --------------------------- | ------------------------------------------------------------------------- |
| User Registration           | Register, create account, accept terms and conditions                     |
| Authentication              | Log in, log out, authenticate, social login, SSO                          |
| Credential Management       | Set password, change password, reset password                             |
| Email Verification          | Send verification email, verify email, resend verification                |
| Account Management          | View account, update account settings, deactivate account, delete account |
| Session Management          | Create session, refresh session, revoke session, view active sessions     |
| Multi-Factor Authentication | Enable MFA, verify MFA, disable MFA, recovery codes                       |
| User Roles                  | Assign roles, revoke roles, manage platform-level roles                   |
| Permissions                 | Define permissions, evaluate permissions, enforce access policies         |
| Account Security            | Lock account, unlock account, detect suspicious login activity            |

Important distinction:

- Identity & Access owns the `User` entity.
- Candidates owns the `Candidate` entity.
- Organizations owns the `Organization` entity and its organizational structure.

A user account does not automatically make someone a candidate, employer or career-centre staff member.

### 2. Organization

Purpose: Manage organizations and their organizational capabilities.

Recall your decision: one canonical Organization entity can have multiple capabilities, such as `employer` and `career_center`.

| Capability                 | Operations / use cases                                                |
| -------------------------- | --------------------------------------------------------------------- |
| Organization Management    | Create organization, update organization, deactivate organization     |
| Organization Profiles      | Manage name, description, logo, website and contact information       |
| Organization Capabilities  | Enable employer capability, enable career-centre capability           |
| Organization Verification  | Submit verification, review verification, approve/reject organization |
| Membership Management      | Add member, remove member, view members                               |
| Staff Management           | Assign staff, update staff details, deactivate staff                  |
| Organizational Invitations | Invite staff, accept invitation, reject invitation, revoke invitation |
| Organizational Settings    | Configure organization settings and preferences                       |

Boundary: Organizations owns organizational membership and organizational capabilities. Identity & Access owns authentication and the underlying access-control mechanisms.

### 3. Candidate

Purpose: Manage candidate identities within the career and recruitment context.

| Capability           | Operations / use cases                                              |
| -------------------- | ------------------------------------------------------------------- |
| Candidate Profiles   | Create profile, update profile, view profile                        |
| Personal Information | Manage name, contact information, location                          |
| Education            | Add institution, add qualification, update education history        |
| Work Experience      | Add experience, update experience, delete experience                |
| Skills               | Add skills, update skills, manage skill proficiency                 |
| Career Preferences   | Set preferred roles, industries, locations and salary expectations  |
| Career Interests     | Save career interests, update career goals                          |
| Resumes              | Upload resume, create resume, update resume, manage resume versions |
| Portfolio            | Add projects, certifications, achievements and portfolio links      |
| Profile Visibility   | Configure profile visibility and information-sharing preferences    |

Candidates should not own authentication credentials or organizational membership.

### 4. Agent Identity

**Purpose:** Manage AI agent identities as distinct principals, including their authority, delegation relationships and credentials.

An agent must have an identifiable principal and explicitly scoped authority. An agent should never automatically inherit all permissions of the human user who owns it.

| Capability | Operations / use cases |
|---|---|
| Agent Principals | Register agent, create agent identity, retrieve agent identity, deactivate agent |
| Agent Ownership | Associate agent with user, associate agent with organization, transfer agent ownership where permitted |
| Agent Registration | Register personal agent, register organizational agent, manage agent metadata |
| Delegation Grants | Grant authority to agent, revoke delegation, update delegation scope, view active grants |
| Scoped Authority | Define permitted resources, restrict actions, configure access boundaries |
| Delegation Chains | Establish delegation chain, validate delegation chain, inspect delegation provenance |
| Agent Credentials | Issue agent credentials, rotate credentials, revoke credentials, validate credentials |
| Agent Lifecycle | Activate agent, suspend agent, deactivate agent, review agent status |
| Principal Verification | Verify agent identity, validate principal, verify ownership and delegation relationships |

**Important distinctions:**

- Agent Identity owns the `AgentPrincipal` entity.
- Identity & Access owns human user identities and the underlying authorization mechanisms.
- Agent Identity determines which authority has been delegated to an agent and the scope of that delegation.
- Assistant owns the personal agent's conversational and operational experience, not its identity or authority.
- Tool Governance determines whether an agent can invoke a particular tool under the applicable execution policies.

An agent's authority must be bounded by the authority of its delegating principal. Delegation must not allow privilege escalation.

### 5. Assistant

**Purpose:** Manage personal AI assistants that help users accomplish tasks through conversations, contextual understanding, planning and approved tool execution.

Each user can have a personal agent that acts on their behalf through explicitly approved tools and integrations.

| Capability | Operations / use cases |
|---|---|
| Assistant Management | Create assistant, configure assistant, activate assistant, deactivate assistant |
| Personal Agents | Provision personal agent, associate agent with user, configure agent preferences |
| Conversations | Start conversation, send message, retrieve conversation, archive conversation, delete conversation |
| Context Management | Assemble contextual information, retrieve relevant context, manage conversation context |
| Memory Management | Store memory, retrieve memory, update memory, forget memory, manage memory preferences |
| User Preferences | Configure response preferences, communication style, working preferences |
| Task Management | Create task, update task, retrieve task, cancel task, track task progress |
| Planning and Reasoning | Interpret requests, formulate plans, break down tasks, revise plans |
| Task Orchestration | Execute task steps, coordinate subtasks, manage dependencies, handle failures |
| Tool Invocation Requests | Request tool invocation, provide execution arguments, process tool results |
| Human-in-the-Loop | Request approval, present proposed actions, process approval or rejection |
| Proactive Assistance | Generate suggestions, identify pending tasks, initiate permitted proactive workflows |
| Assistant Configuration | Configure model, system instructions, agent behaviour and operating preferences |

**Important distinctions:**

- Assistant owns the `Assistant`, `Conversation`, `Message`, `Memory` and `Task` entities.
- Agent Identity owns the underlying agent principal, delegation grants and authority.
- Tool Governance owns the tool registry, invocation policies and execution approval mechanisms.
- Integration owns the external connectors and their communication with third-party services.
- Notification owns the delivery of notifications generated by the assistant or other domains.
- Assistant may request an action, but it cannot independently grant itself permission to perform that action.

**Example workflow:**

A candidate asks their personal agent to apply for an internship.

1. Assistant interprets the request and creates a task.
2. Agent Identity establishes the agent's delegated authority.
3. Tool Governance evaluates whether the requested actions are permitted and whether approval is required.
4. Integration provides the necessary external service connection.
5. Application manages the actual application workflow.
6. Assistant communicates the outcome to the candidate.

The Assistant is the orchestration and interaction layer, not the owner of every business process it coordinates.

### 6. Tool Governance

**Purpose:** Govern the registration, availability, authorization and execution of tools that AI agents and other platform components can use.

This domain establishes the controls necessary to ensure that AI agents operate within explicitly defined boundaries.

| Capability | Operations / use cases |
|---|---|
| Tool Registry | Register tool, update tool metadata, deprecate tool, retrieve available tools |
| Tool Definitions | Define tool schemas, input parameters, output schemas and execution requirements |
| Tool Approval | Submit tool for approval, approve tool, reject tool, revoke approval |
| Capability Management | Define available capabilities, associate tools with capabilities, manage capability availability |
| Invocation Policies | Define invocation policies, configure access restrictions, enforce execution rules |
| Authorization Evaluation | Evaluate invocation request, validate agent authority, validate delegation scope |
| Approval Gates | Require human approval, approve invocation, reject invocation, revoke pending approval |
| Execution Governance | Authorize execution, reject execution, enforce execution constraints |
| Execution Limits | Configure rate limits, execution limits, resource limits and usage restrictions |
| Risk Management | Classify tool risk, identify sensitive operations, enforce additional safeguards |
| Execution Records | Record invocation requests, execution decisions, results and failures |
| Tool Lifecycle | Enable tool, disable tool, suspend tool, revoke tool availability |

**Important distinctions:**

- Tool Governance owns the `Tool`, `ToolDefinition`, `ToolPolicy`, `ToolApproval` and `InvocationDecision` entities.
- Agent Identity establishes the authority of the agent requesting an action.
- Identity & Access provides the underlying authorization mechanisms for human principals.
- Integration owns the implementation of external connectors.
- Assistant initiates tool invocation requests but does not own tool execution governance.
- Compliance consumes relevant execution records as audit evidence.

**Critical architectural principle:**

Tool availability does not imply tool authorization.

An agent may have access to a registered tool but still be prohibited from performing a particular operation because of insufficient delegation, missing approval, resource restrictions or execution policies.

---

## B. Career and recruitment domains

### 7. Opportunity

**Purpose:** Manage career opportunities published by employers and other authorized organizations, including their publication lifecycle and associated information.

| Capability | Operations / use cases |
|---|---|
| Opportunity Creation | Create job listing, create internship, create graduate programme |
| Opportunity Management | Update opportunity, retrieve opportunity, duplicate opportunity, archive opportunity |
| Opportunity Details | Manage job title, description, responsibilities, qualifications, requirements and benefits |
| Employment Details | Configure employment type, work arrangement, location, compensation and working hours |
| Eligibility Requirements | Define required qualifications, skills, experience and candidate eligibility |
| Opportunity Publication | Submit for review, publish opportunity, unpublish opportunity, schedule publication |
| Publication Lifecycle | Open opportunity, close opportunity, extend deadline, expire opportunity |
| Employer Ownership | Associate opportunity with organization, manage opportunity ownership |
| Opportunity Verification | Review listing, verify listing information, flag suspicious listings |
| Opportunity Templates | Create listing templates, reuse templates, manage standard descriptions |
| Opportunity Categories | Categorize opportunities by industry, occupation, employment type and seniority |

**Important distinctions:**

- Opportunity owns the `Opportunity` entity and its publication lifecycle.
- Organization owns the organization publishing the opportunity.
- Application owns candidate submissions against opportunities.
- Discovery owns search, matching, ranking and recommendation functionality.
- Identity & Access and Organization determine whether a user is authorized to create or manage an organization's opportunities.
- Opportunity does not own the recruitment pipeline or application outcomes.

An opportunity is the published career offering. An application is a candidate's submission in response to that offering.

### 8. Discovery

**Purpose:** Help candidates and organizations discover relevant career opportunities and candidates through search, matching, ranking and recommendations.

| Capability | Operations / use cases |
|---|---|
| Opportunity Search | Search opportunities, filter opportunities, sort results, browse listings |
| Candidate Search | Search candidates, filter candidate profiles, retrieve candidate results |
| Candidate Matching | Match candidates with opportunities, calculate compatibility, identify skill alignment |
| Recommendation Engine | Recommend opportunities, recommend candidates, generate personalized recommendations |
| Ranking | Rank opportunities, rank candidates, calculate relevance scores |
| Search Preferences | Save search criteria, manage search preferences, configure alerts |
| Saved Opportunities | Save opportunity, remove saved opportunity, retrieve saved opportunities |
| Matching Criteria | Configure matching criteria, define ranking factors, manage weighting |
| Recommendation Feedback | Record feedback, dismiss recommendation, indicate interest, improve recommendations |
| Search Analytics | Track search queries, measure relevance, evaluate search performance |

**Important distinctions:**

- Discovery owns the `SearchQuery`, `SearchPreference`, `MatchResult` and `Recommendation` entities.
- Candidate owns candidate profile information.
- Opportunity owns opportunity information.
- Discovery consumes candidate and opportunity data to generate search and matching results.
- Discovery does not own the underlying candidate profiles or opportunity listings.
- Application owns actual application submissions and recruitment outcomes.

Discovery answers the question: *What opportunities or candidates are relevant?*

It does not determine whether a candidate has formally applied or whether an employer has accepted a candidate.

### 9. Application

**Purpose:** Manage the recruitment process between candidates and organizations, from application submission through screening, interviews, offers and final outcomes.

| Capability | Operations / use cases |
|---|---|
| Application Submission | Create application, submit application, withdraw application |
| Application Management | Retrieve application, update permitted application details, archive application |
| Application Documents | Attach resume, attach cover letter, submit supporting documents |
| Application Status | Track application status, update status, retrieve status history |
| Recruitment Pipeline | Create pipeline, define recruitment stages, move application between stages |
| Candidate Screening | Review application, shortlist candidate, reject candidate, request additional information |
| Interview Management | Schedule interview, reschedule interview, cancel interview, record interview outcome |
| Interview Feedback | Submit feedback, retrieve feedback, manage interviewer evaluations |
| Assessments | Assign assessment, submit assessment, evaluate assessment results |
| Offer Management | Create offer, issue offer, revise offer, withdraw offer |
| Offer Response | Accept offer, reject offer, negotiate offer, record candidate response |
| Recruitment Outcomes | Record successful application, record unsuccessful application, close recruitment process |
| Application History | Retrieve application timeline, track decisions, view recruitment history |

**Important distinctions:**

- Application owns the `Application`, `RecruitmentPipeline`, `Interview`, `Assessment` and `Offer` entities.
- Candidate owns candidate profile information and resumes.
- Opportunity owns the job listing and its publication lifecycle.
- Organization owns the employer identity and organizational membership.
- Communication owns messages exchanged between participants.
- Notification handles delivery of application-related notifications.
- Discovery provides matching and recommendation results but does not own application decisions.

**Critical architectural principle:**

Application submission and application processing must be separate concerns.

A candidate can submit an application, but the employer controls the recruitment workflow and associated decisions, subject to applicable platform policies.

### 10. Career Services

**Purpose:** Support career-centre operations and institutional career development workflows, including student management, advising, programmes and institutional engagement.

| Capability | Operations / use cases |
|---|---|
| Student Management | Retrieve students, manage student records, associate students with institution |
| Student Groups | Create student groups, manage cohorts, organize students by programme or graduation year |
| Career Advising | Create advising sessions, schedule consultations, record advising outcomes |
| Advising Records | Maintain advising notes, track student progress, manage follow-up actions |
| Career Programmes | Create career programmes, manage programme details, publish programmes |
| Programme Registration | Register students, withdraw students, manage programme participation |
| Career Events | Organize career fairs, workshops, networking sessions and recruitment events |
| Event Management | Manage event schedules, registrations, attendance and participation |
| Employer Engagement | Manage employer relationships, coordinate recruitment activities |
| Institutional Opportunities | Coordinate internship opportunities, graduate employment programmes and institutional initiatives |
| Student Progress | Track career readiness, monitor participation, assess career development progress |
| Career Centre Reporting | Generate student reports, programme reports and employment outcome reports |
| Institutional Workflows | Manage approvals, assignments, administrative tasks and institutional processes |

**Important distinctions:**

- Career Services owns the `CareerProgramme`, `AdvisingSession`, `CareerEvent` and associated institutional workflow entities.
- Organization owns the career centre as an organization and its organizational capabilities.
- Candidate owns the candidate's career profile and personal information.
- Application owns recruitment applications and outcomes.
- Analytics owns cross-platform analytical models and reporting infrastructure.
- Career Services may maintain operational records but should not duplicate candidate profile ownership.

**Important architectural consideration:**

A career centre is an organizational capability, not a separate organizational identity.

An organization with the `career_center` capability can access career-centre functionality according to its approved permissions and institutional configuration.

### 11. Communication

**Purpose:** Manage conversations and communication between platform participants, including direct messages, group discussions, announcements and recruitment-related communications.

| Capability | Operations / use cases |
|---|---|
| Direct Messaging | Send message, receive message, retrieve message, edit permitted message |
| Conversations | Create conversation, retrieve conversation, archive conversation |
| Group Conversations | Create group conversation, add participant, remove participant |
| Message Management | Mark as read, mark as unread, delete message where permitted |
| Attachments | Attach document, attach image, retrieve attachment |
| Announcements | Create announcement, publish announcement, update announcement, archive announcement |
| Communication Channels | Manage communication channels, configure channel access |
| Conversation Participants | Add participant, remove participant, manage participant permissions |
| Communication Preferences | Configure communication preferences, manage blocked users |
| Moderation | Report message, review reported content, moderate conversation |
| Communication History | Retrieve conversation history, maintain message history |
| Automated Communications | Support system-generated messages and assistant-mediated communications |

**Important distinctions:**

- Communication owns the `Conversation`, `Message`, `Announcement` and related communication entities.
- Notification owns notification delivery, including email, push and in-app delivery.
- Assistant owns AI conversations between a user and their personal agent.
- Communication owns human-to-human conversations and platform communication channels.
- Integration owns external messaging connectors where applicable.
- Compliance defines applicable retention and audit requirements.

**Important architectural consideration:**

Assistant conversations and platform communication should remain separate bounded contexts.

A personal agent may interact with users through its own conversation interface and may also request permission to send messages through Communication. These are different operations with different authorization requirements.

---

## C. Platform services

### 12. Integration

**Purpose:** Manage connections between LevelUp and external systems, including third-party APIs, institutional systems, external services and synchronization workflows.

| Capability | Operations / use cases |
|---|---|
| Connector Registry | Register connector, update connector, disable connector, deprecate connector |
| External Connections | Establish connection, disconnect service, retrieve connection status |
| OAuth Management | Initiate OAuth authorization, exchange authorization code, refresh tokens, revoke access |
| API Credentials | Store credentials securely, rotate credentials, revoke credentials |
| API Management | Manage API endpoints, configure API requests, handle API responses |
| Webhook Management | Register webhook, receive webhook, validate webhook, retry webhook |
| Data Synchronization | Synchronize records, retrieve external updates, reconcile data |
| Import and Export | Import records, export records, validate imported data |
| External Mapping | Map external identifiers, map data fields, transform external data |
| Integration Monitoring | Monitor connector health, track failures, manage connection errors |
| Retry Management | Retry failed operations, configure retry policies, handle synchronization failures |
| Integration Logs | Record requests, responses, synchronization events and errors |

**Important distinctions:**

- Integration owns the `Connector`, `ExternalConnection`, `ExternalCredentialReference`, `WebhookSubscription` and synchronization-related entities.
- Tool Governance determines whether an AI agent can invoke an integration capability.
- Agent Identity establishes the agent's delegated authority.
- Assistant requests actions through approved tools and integrations.
- Individual business domains own the internal business records created or updated through integrations.
- Compliance governs relevant data handling and retention requirements.

**Critical architectural principle:**

Integration is the technical connectivity layer, not the owner of external business processes.

For example, importing a job listing from an external recruitment system should result in an Opportunity-owned record rather than an Integration-owned opportunity.

### 13. Notification

**Purpose:** Manage notification generation, routing, delivery, preferences and delivery lifecycle across the platform.

| Capability | Operations / use cases |
|---|---|
| Notification Generation | Generate notification, create notification event, process notification request |
| Notification Templates | Create template, update template, manage reusable notification content |
| Notification Preferences | Configure preferences, enable notifications, disable notifications |
| Notification Channels | Configure in-app, email and push notification channels |
| Notification Routing | Determine recipients, route notifications, prioritize notifications |
| Notification Delivery | Send notification, queue notification, process delivery result |
| Delivery Tracking | Track delivery status, record failures, retrieve delivery history |
| Notification Management | Mark as read, mark as unread, dismiss notification |
| Notification Scheduling | Schedule notification, cancel scheduled notification |
| Notification Rules | Define notification rules, configure triggers, manage delivery conditions |
| Notification Batching | Group notifications, consolidate notifications, prevent excessive delivery |
| Retry Management | Retry failed delivery, manage delivery attempts |

**Important distinctions:**

- Notification owns the `Notification`, `NotificationTemplate`, `NotificationPreference` and `NotificationDelivery` entities.
- Other domains generate business events that may trigger notifications.
- Communication owns the underlying message and conversation entities.
- Integration provides external delivery connectors where applicable.
- Assistant may request notifications but does not own their delivery lifecycle.

**Example:**

When an employer schedules an interview:

1. Application creates the interview record.
2. Application generates an interview-related business event.
3. Notification consumes the event and creates relevant notifications.
4. Notification routes and delivers the notifications through configured channels.

Notification should not need to understand the complete business logic of every domain generating its events.

### 14. Billing

**Purpose:** Manage platform monetization, subscriptions, entitlements, usage metering, credits, invoicing and payment processing.

| Capability | Operations / use cases |
|---|---|
| Subscription Plans | Create plan, update plan, publish plan, retire plan |
| Subscription Management | Subscribe, upgrade, downgrade, cancel subscription |
| Plan Entitlements | Define entitlements, assign entitlements, evaluate entitlement availability |
| Usage Metering | Record usage, calculate consumption, retrieve usage history |
| Usage Limits | Define usage limits, enforce limits, monitor consumption |
| Credits Management | Allocate credits, consume credits, refund credits, expire credits |
| Pricing Management | Configure pricing, manage billing intervals, define usage-based pricing |
| Invoicing | Generate invoice, retrieve invoice, issue credit note |
| Payment Processing | Initiate payment, process payment result, handle payment failure |
| Refund Management | Request refund, process refund, record refund outcome |
| Billing History | Retrieve billing history, retrieve payment history |
| Billing Notifications | Generate billing events, communicate payment failures and subscription changes |

**Important distinctions:**

- Billing owns the `Subscription`, `SubscriptionPlan`, `Entitlement`, `UsageRecord`, `CreditBalance`, `Invoice` and payment-related entities.
- Identity & Access determines which authenticated users are accessing the platform.
- Organization owns organizational identity and membership.
- Billing determines the subscription and commercial entitlements associated with a user or organization.
- Individual domains enforce their own business rules while consulting Billing for applicable entitlements.
- Integration may provide payment gateway connectivity.

**Important architectural consideration:**

Authorization and entitlement evaluation are related but separate concerns.

A user may have permission to access a feature but lack the subscription entitlement to use it. Conversely, having a subscription entitlement does not automatically grant permission to access another user's data.

---

## D. Governance and intelligence domains

### 15. Analytics

**Purpose:** Provide analytical capabilities across the platform, supporting operational monitoring, institutional reporting, employer insights and business intelligence.

| Capability | Operations / use cases |
|---|---|
| Event Collection | Collect platform events, ingest business events, track user interactions |
| Data Processing | Transform data, aggregate records, process analytical datasets |
| Platform Analytics | Measure registrations, active users, engagement and platform adoption |
| Candidate Analytics | Analyse candidate activity, career readiness, skills and employment outcomes |
| Employer Analytics | Analyse opportunity performance, recruitment activity and candidate engagement |
| Career Centre Analytics | Generate institutional reports, monitor student outcomes, evaluate programmes |
| Recruitment Analytics | Analyse application volumes, recruitment pipelines, conversion rates and hiring outcomes |
| Opportunity Analytics | Analyse listing views, engagement, application conversion and listing performance |
| Assistant Analytics | Measure assistant usage, task completion, tool invocation and task success rates |
| Business Intelligence | Generate dashboards, reports, trends and performance indicators |
| Reporting | Generate reports, export datasets, schedule recurring reports |
| Data Exploration | Query analytical datasets, explore trends, compare performance |
| Metrics Management | Define metrics, manage metric definitions, track key performance indicators |

**Important distinctions:**

- Analytics owns analytical datasets, metric definitions, aggregation models and reporting outputs.
- Other domains own the underlying transactional business records.
- Analytics consumes events and data from other domains.
- Analytics should not become the primary source of truth for operational business entities.
- Compliance governs access to sensitive analytical data and applicable privacy requirements.

**Important architectural consideration:**

Operational data and analytical data should be treated separately.

For example, Application owns the authoritative application status, while Analytics may maintain aggregated application conversion statistics for reporting.

Analytics must also respect data access boundaries. An employer should not gain access to candidate information simply because that information exists in an analytical dataset.

### 16. Compliance

**Purpose:** Manage platform-wide privacy, regulatory compliance, consent, audit evidence, data governance and retention requirements.

| Capability | Operations / use cases |
|---|---|
| Audit Management | Record audit evidence, retrieve audit records, investigate activities |
| Audit Trails | Track sensitive operations, record actor identity, preserve action provenance |
| Privacy Management | Define privacy requirements, manage privacy policies, monitor compliance |
| Consent Management | Record consent, retrieve consent status, withdraw consent, manage consent history |
| Data Retention | Define retention policies, configure retention periods, enforce retention rules |
| Data Deletion | Process deletion requests, manage data erasure workflows, record deletion evidence |
| Data Export | Process data access requests, generate personal data exports |
| Regulatory Management | Maintain regulatory requirements, map controls, track compliance obligations |
| Data Governance | Classify data, define data handling requirements, manage sensitive data policies |
| Access Auditing | Review access records, investigate unauthorized access, monitor privileged operations |
| Incident Management | Record privacy incidents, investigate incidents, track remediation |
| Compliance Reporting | Generate compliance reports, maintain evidence, track outstanding obligations |
| Policy Management | Define policies, update policies, manage policy versions |
| Risk Management | Identify compliance risks, assess impact, track mitigation measures |

**Important distinctions:**

- Compliance owns compliance policies, consent records, audit evidence, retention policies and compliance workflows.
- Identity & Access owns authentication and authorization enforcement.
- Agent Identity owns agent delegation records and principal relationships.
- Tool Governance owns tool invocation policies and execution decisions.
- Individual domains remain responsible for enforcing their own business rules and data lifecycle operations.
- Compliance establishes cross-domain governance requirements and verifies that applicable controls are followed.

**Critical architectural principle:**

Compliance should not become the owner of all sensitive data merely because that data is subject to regulatory requirements.

For example, Candidate owns candidate profile information, while Compliance governs the requirements for collecting, processing, retaining and deleting that information.

---

## E. Cross-Domain Ownership Principles

The following principles should guide domain implementation and prevent overlapping responsibilities.

### 1. Single ownership of business entities

Each authoritative business entity must have one owning domain.

| Entity | Owning domain |
|---|---|
| User | Identity & Access |
| Organization | Organization |
| Organization Membership | Organization |
| Candidate | Candidate |
| Agent Principal | Agent Identity |
| Delegation Grant | Agent Identity |
| Assistant | Assistant |
| Conversation / Message (AI assistant) | Assistant |
| Conversation / Message (platform communication) | Communication |
| Memory | Assistant |
| Task (assistant task) | Assistant |
| Tool Definition | Tool Governance |
| Tool Invocation Decision | Tool Governance |
| Opportunity | Opportunity |
| Search Query | Discovery |
| Match Result | Discovery |
| Application | Application |
| Interview | Application |
| Offer | Application |
| Career Programme | Career Services |
| Advising Session | Career Services |
| Notification | Notification |
| Connector | Integration |
| Subscription | Billing |
| Entitlement | Billing |
| Usage Record | Billing |
| Analytical Dataset | Analytics |
| Audit Evidence | Compliance |
| Consent Record | Compliance |

### 2. Domain ownership versus access control

A domain owning an entity does not mean it independently determines every access decision.

For example:

- Organization owns organizational memberships.
- Identity & Access owns the underlying roles, permissions and authorization mechanisms.
- Identity & Access evaluates whether a principal can perform an action on an organizational resource.
- Organization provides the relevant membership and capability context.

### 3. Agent authority versus tool execution

AI agent execution involves three distinct responsibilities:

| Concern | Owning domain | Responsibility |
|---|---|---|
| Agent identity and delegation | Agent Identity | Establish who the agent is and what authority has been delegated |
| Tool authorization and governance | Tool Governance | Determine whether a tool invocation is permitted |
| External connectivity | Integration | Provide the technical means to interact with external systems |
| Business operation | Relevant business domain | Execute the actual business operation |

Assistant coordinates these responsibilities but does not replace them.

### 4. Transactional versus analytical ownership

Transactional domains own authoritative business records. Analytics consumes relevant data to produce reports, metrics and insights.

Analytical outputs must not silently become authoritative transactional records.

### 5. Business events versus notifications

Business domains publish events when relevant business activities occur.

Notification consumes relevant events and manages notification delivery.

Communication manages conversations and messages between platform participants.

These responsibilities should remain distinct.