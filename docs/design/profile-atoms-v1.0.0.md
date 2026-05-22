# Design: Profile-Atoms

> **Status:** v1.0.0 — ready for implementation. Part of the Olympus broker architecture.
>
> **Spec posture:** This document specifies the *logical schema* of a profile-atom — its fields, types, references, and constraints. The on-disk serialization format is an implementation choice handled by the atom builder, not part of this specification. Examples in this document are illustrative renderings; the canonical form of a profile-atom is whatever the builder constructs and validates.
>
> **Design history:**
> - draft 1 — single governance reference; hierarchical context (context owned by profile)
> - draft 2 — governance becomes composable stack; profile and situational context become parallel dimensions; Context Qualifiers unify with Intent Qualifiers under one Qualifier Class system; durable Subjects emerge as a separate primitive distinct from session-scoped situational contexts
> - **v1.0.0** (current) — compositional examples added spanning code and writing; knowledge-source visibility scope clarified (community / organizational / personal); generalized AI OS framing made explicit; logical schema separated from serialization

---

## Purpose

A Profile is the unit a user activates to establish their working identity in Olympus. It composes role-packs (which give vocabulary and capabilities), a policy stack (which gives rules), a governance stack (which gives signing and audit posture), and a set of defaults (persona, theme, budget, identities, channels, knowledge sources, workflows) that constitute "who someone is working as."

Profile-atoms sit at the composition layer between primitive atoms (persona, policy, identity, channel, etc.) and the runtime situational layer (situational contexts). A profile is durable; a situational context is session-scoped. A profile changes infrequently — when a user changes roles, joins a project, transitions to a different compliance regime, or shifts to a different *kind* of work entirely. A situational context changes constantly — every time the user switches what they're working on within their role.

**Crucially: profile and situational context are parallel inputs to the broker, not hierarchical layers.** A profile is *who I am*. A situational context is *what I'm doing*. Neither contains the other. Both are independent dimensions the broker considers when dispatching.

---

## Olympus is a generalized AI Operating System

Profile-atoms is the mechanism by which Olympus shapes itself to whoever is sitting at the keyboard, regardless of what kind of work that person is doing. The same Olympus binary, the same broker, the same dispatch model becomes:

- a developer's environment shaped for their organization's standards and language stack
- a writer's environment shaped for their genre, voice, and citation conventions
- an SRE's environment shaped for their on-call posture and blast-radius constraints
- a security researcher's environment shaped for their investigative tools and disclosure obligations
- a designer's environment shaped for their brand system and asset libraries
- a data scientist's environment shaped for their experimental conventions and reproducibility requirements
- a product manager's environment shaped for their roadmap, stakeholders, and metrics
- a teacher's environment shaped for their curriculum, students, and grading conventions

Each of these is *a different composition of the same primitive atoms*. The mechanism that produces them is identical. Profile-atoms is the atom catalog that makes "Olympus shaped for me" a mechanical claim, not a marketing one.

The architecture is domain-agnostic by construction. The broker does not know what domain it is operating in; it just composes the inputs it's given. Compliance regimes, vocabularies, capabilities, channels, knowledge sources — all are inputs the user (or their organization, or their community) supplies via signed atoms. Olympus's value is the composition, not any specific domain's content.

---

## The four dispatch dimensions

The broker, when handling any user-initiated work, considers four independent inputs:

1. **Intent** — what's being asked (with Intent Qualifiers attached)
2. **Profile** — who's working (durable, identity-shaped)
3. **Situational Context** — what they're focused on right now (session-scoped, with Context Qualifiers attached)
4. **Subject** *(optional reference)* — the external entity the situational context refers to (durable, possibly shared across users and sessions)

These four are peers. None inherits from another. The broker permits an action when all four align: the user has the right to do this (profile), this work is active for this problem (situational context), this is what's being asked (intent), with these specifics (qualifiers). Misalignment in any dimension produces a clear, actionable refusal — switch context, switch identity within context, rephrase intent, change qualifier — rather than a generic denial.

---

## Profile vs Situational Context

The cleanest way to think about the distinction is by what each *owns*:

| Profile owns | Situational Context owns |
|--------------|--------------------------|
| Vocabulary scope (role-packs) | The currently bound identity (one from profile's set) |
| Policy stack | The currently active channels (subset of profile's) |
| Governance stack | Subject reference (the external thing being worked on) |
| Default persona (the lens) | Session-scoped persona override, if any |
| Default theme | Remaining budget for this work |
| Default budget rules | Context Qualifiers (typed situational specifics) |
| Available identities (the set) | The transcript thread this context lives in |
| Available channels (the set) | |
| Knowledge sources for grounding | |
| Default workflows | |

A profile says: "I am [role]. I can act as any of [identity set]. I can reach [channel set]. I am subject to [policy stack]. I am governed by [governance stack]."

A situational context says: "I'm currently focused on [subject]. I'm bound to [one identity]. I have [subset of channels] active. I have qualifiers [context qualifiers] set as defaults for any intent I dispatch."

Neither contains the other. The broker reads both at dispatch.

---

## Logical Schema

The fields below constitute the logical structure of a profile-atom. The atom builder is responsible for enforcing the schema, validating references, and producing whatever serialized form the storage layer requires. The schema below is the contract; the format is not.

### Identity fields

These fields establish the profile-atom's own identity within the catalog.

**`canonical_name`** *(string, required)* — Fully-qualified atom name in `<namespace>/profiles/<slug>` form. Must be globally unique within the atom catalog. Establishes the profile's identity for references from other atoms and from user activations.

**`version`** *(semver string, required)* — Semantic version. Updates to a profile-atom create new versions; consumers reference specific versions and only pick up updates per their declared update policy.

**`authored_by`** *(signing key identifier, required)* — The signing key that authored this profile composition. May be an individual user's key, an organization's signing key, or a community-trusted key.

**`signed_by`** *(array of signing key identifiers, optional)* — Additional signatures endorsing this profile. Co-signing supports patterns like "personally authored, organizationally endorsed."

**`description`** *(string, required)* — Human-readable description of who this profile is for and what kind of work it shapes Olympus for. Surfaced in profile selection UI.

### Composition references

These fields compose the profile from other atoms. Every reference is pinned to a specific version; updates require explicit re-pin.

**`role_packs`** *(ordered array of role-pack references, required, at least one)* — One or more role-pack atoms whose vocabularies and capabilities the profile activates. Each entry pairs a reference (`<namespace>/role-packs/<name>@<version>`) with a priority (integer, lower is higher priority). When role-packs claim overlapping verbs, priority order breaks ties. If priority doesn't resolve ambiguity, the Intent Compiler asks the user for clarification.

**`policy_stack`** *(ordered array of policy-atom references, may be empty)* — Policies that gate actions under this profile. Composition is intersection: every policy in the stack must approve an action for it to proceed; any single denial blocks. Order matters only for evaluation efficiency (cheap policies first).

**`governance_stack`** *(ordered array of governance-binding references, may be empty)* — Governance bindings that establish signing, coauthorization, audit, evidence, escalation, and retention requirements. Composition unions requirements across bindings; for each requirement level, the strictest wins. Compliance-binding atoms (SOC2, HIPAA, etc.) are referenced here.

### Defaults

These fields establish defaults that apply when situational contexts and user actions don't specify otherwise.

**`default_persona`** *(persona-atom reference, required)* — The lens applied to outputs by default. Users can switch persona within a session; the default is what every new session starts with.

**`default_theme`** *(theme-atom reference, required)* — Visual styling for the TUI under this profile.

**`default_budget`** *(structured value, required)* — Drachma budget constraints. Contains:
- `per_action` (decimal, required) — drachma cap per single fulfillment
- `per_session` (decimal, required) — drachma cap per session
- `per_day` (decimal, required) — drachma cap per 24-hour period
- `on_cap_hit` (enum, required) — behavior when a cap is exceeded; one of `warn`, `require_confirm`, `deny`

### Availability sets

These fields declare what the profile *authorizes* the user to do. Situational contexts pick from these sets but cannot exceed them.

**`available_identities`** *(unordered set of identity-atom references, required, at least one)* — The identities the user is authorized to bind contexts to. Situational contexts each pick one. Users cannot bind to an identity not in this set. This is where access control lives — junior profiles don't list elevated identities; senior profiles do.

**`available_channels`** *(unordered set of channel-atom references, may be empty)* — The channels the profile authorizes. Situational contexts can activate any subset; they cannot reach channels not in this set.

### Grounding

**`knowledge_sources`** *(unordered set of knowledge-atom references, may be empty)* — Knowledge-atoms the resolver grounds responses in. Span community, organizational, and personal scopes (see "Knowledge source visibility" below) — referenced uniformly regardless of scope.

### Discovery

**`default_workflows`** *(unordered set of workflow-atom references, may be empty)* — Workflow-atoms surfaced prominently via autocomplete, command discovery, and prompt suggestions. The runbooks, scripts, and procedures the user reaches for most in this role.

### Lifecycle and trust

**`update_policy`** *(structured value, required)* — How this profile responds when referenced atoms publish new versions. Contains:
- `auto_upgrade` (boolean, required) — whether the profile picks up new versions automatically
- `notification` (boolean, required) — whether the user is notified when upgrades become available
- `diff_visualization` (enum, required) — `required`, `optional`, or `none`; whether the user must see a diff before upgrading

**`trust_requirements`** *(structured value, required)* — What signing is required for each kind of referenced atom. Activation aborts with a clear error if any referenced atom doesn't meet the trust requirement. Contains per-atom-type entries specifying `must_be_signed_by` or `must_be_signed_by_any_of` with one or more trusted signing key identifiers.

### Optional: inheritance

**`extends`** *(profile-atom reference, optional)* — Another profile-atom this one extends. Extension pins the parent at version; explicit re-pin is required to pick up parent updates. Fields override the parent by merge: arrays append (with deduplication), scalars overwrite. Trust requirements compose by union (child requirements add to parent requirements; child cannot relax).

---

## Qualifier Classes: one substrate, two scopes

**Qualifier Classes are the substrate; the scope of application is what differs.**

A Qualifier Class is a schema-atom defining a typed semantic concept (Ordering, TimeWindow, Location, Target, Filter, Expectation, Depth, Urgency, Symptom, Threshold, Mode, BlastRadius, Genre, Audience, Voice, and others contributed by role-packs).

The class is the same across scopes. The application differs:

- **Intent Qualifiers** are instances applied to an intent. They specialize what's being asked.
- **Context Qualifiers** are instances applied to a situational context. They specialize what's true about the current problem.

Both compose into the broker's dispatch input. The broker reads both scopes when matching capabilities and evaluating policies.

**Why this matters:**

- Context qualifiers are how situational rule additions get expressed. The context carries `Mode(incident)`; the governance stack has rules conditional on `Mode(incident)`; the policy stack composes them. No special-case mechanism needed.
- Cross-scope qualifier classes (a class usable at either scope) become natural. `Urgency` might be set on an intent ("this is urgent") or on a context ("this whole situation is urgent"). The class definition is the same; the scope of application is the user's choice.
- Default Context Qualifiers fill in unstated Intent Qualifiers at compile time. If the situational context has `Target(payment-validator)` set, an intent like "show me the logs" doesn't need to restate the target — the broker uses the context default.
- The Intent Compiler reads both Intent Qualifiers (from the utterance) and Context Qualifiers (from the active context) when compiling. Cache keys include both.

The Qualifier Class system is one extensible substrate. Schema-atoms host the class definitions. Role-packs may contribute role-specific classes. Applications happen at the appropriate scope.

---

## What's NOT in a profile

To be explicit about boundaries:

- **Not the secrets engine state.** Profiles reference identities; identities reference slots in the engine; the engine owns the slots. Profile activation triggers slot resolution but doesn't carry slot values.
- **Not the cache.** L1/L2/L3 cache state is separate substrate. Profiles influence cache keys but don't own cache state.
- **Not the transcript history.** Profile activation is recorded as an event in history, but history is a separate substrate that crosses profiles.
- **Not the active model.** Model selection is a runtime decision the broker makes per-fulfillment. A profile may *bias* model selection but doesn't *bind* a specific model.
- **Not LLM provider credentials.** Those live in identity-atoms, with values in slots in the secrets engine.
- **Not the active identity or active channels.** These live on the situational context (the profile declares what's *available*; the context declares what's *active*).
- **Not session state.** A profile is a durable declaration; session state is what the runtime currently holds.

---

## Knowledge source visibility

Knowledge-atoms referenced by a profile may exist at different scopes of trust and visibility:

**Community knowledge** — published broadly, often signed by a recognized authority. Examples: a published style manual, an open scientific corpus, a community-maintained best-practices guide, a public technical specification. Any user can install and reference these.

**Organizational knowledge** — published within an organization, signed by the organization, available to members. Examples: internal architecture decisions, proprietary documentation, organization-specific style guides, internal libraries. Only members with access can install and reference these.

**Personal knowledge** — authored by the user themselves, signed by their own key, never shared externally. Examples: a writer's own research corpus for their current book, a developer's notes on a system they maintain, a researcher's collection of papers relevant to their work. The user is the only one who has these.

The atom mechanics handle all three identically — they're all signed atoms with versioning, references, and trust chains. The difference is the trust scope of the signing key and the distribution mechanism. Profile-atoms reference knowledge sources without caring which scope they come from; the trust requirements field gates whether the profile will accept a given source based on who signed it.

This matters in practice because personal knowledge is often the most valuable input. A writer's voice samples, a developer's accumulated notes on a codebase, a researcher's annotated bibliography — these are what make broker outputs feel grounded in the user's actual work rather than generic. Profile-atoms surface them as first-class.

---

## Subjects: the durable thing situational contexts can reference

A subject is **a reference to an external entity that exists outside Olympus and has its own lifecycle**. Examples:

- An incident in PagerDuty (`subject: incident-4823`)
- A pull request on GitHub (`subject: PR-7891`)
- A customer support ticket (`subject: ticket-12`)
- A branch in a repository (`subject: branch/feature/auth-refactor`)
- A document being collaboratively edited (`subject: doc/quarterly-roadmap`)
- A book chapter being written (`subject: my-book/chapter-04`)
- A research project (`subject: lab-notebook/experiment-178`)

Subjects are *not authored declarative artifacts* — they don't live in atom catalogs. They're typed references to things in other systems that Olympus tracks for history-threading purposes.

A subject minimally carries:
- **subject_type** — a reference to a subject type defined in schema-atoms
- **subject_id** — the opaque external identifier
- **channel_ref** — the channel-atom that knows how to look up the subject's current state externally

### What subjects enable

**History threading across users and sessions.** Many users may work on the same subject over its lifetime. The broker's history records each dispatch with its subject reference. A query like "show me all activity related to this subject" returns a chronological thread of every situational context that referenced it, across users, sessions, and profiles.

**Continuity across profile transitions.** When a user working on a subject under one profile hands off to a colleague working under a different profile, the new context references the same subject. The history is queryable. The new user gets "here's what's been tried" without inheriting the previous user's session state.

**Subject-aware capability matching.** Capabilities can declare they handle particular subject types. The broker uses subject type as part of capability matching.

**External-system synchronization.** Because the subject carries a channel reference, the broker can periodically poll the external system to check current state. When a subject reaches a terminal state externally, the broker can surface "this subject is now resolved; do you want to close associated contexts?"

### What subjects don't do

- They don't store state. The external system stores the subject's state; Olympus only references it.
- They don't replace situational contexts. Many situational contexts can reference the same subject. The subject is the shared thing; situational contexts are user-specific working focus.
- They don't need to be signed atoms. They're typed references, not authored declarations.

---

## Composition semantics

How a profile's referenced atoms combine at activation:

### Vocabulary composition (role-packs)

- All verbs from all referenced role-packs are in scope simultaneously
- When two role-packs define a verb with the same canonical name, priority order breaks ties
- If priority doesn't resolve, the Intent Compiler asks for clarification
- Qualifier classes from all role-packs are similarly in scope (namespaced by their owning role-pack)

### Policy composition

- All policies in the stack are evaluated for every action
- Every policy must approve; any single denial blocks
- Compliance rules from the governance stack layer additional policies on top of the explicit stack
- Stack order matters only for evaluation efficiency

### Governance composition

- All governance bindings in the stack contribute requirements
- For each action type, requirements union across bindings
- For each requirement level, strictest wins
- A profile cannot relax a binding it references; only add additional bindings

### Persona application

- The default persona is the lens applied to outputs at lens-time
- Users can switch within the session (session-scoped switches)
- The profile's default is what every new session starts with
- Policies can constrain persona switching independently

### Identity availability

- The profile declares the set of identities its situational contexts can bind to
- A context binds one identity from the set
- Users cannot bind to an identity not listed in the profile

---

## Activation lifecycle

### Profile activation

1. The broker reads the profile-atom and verifies its signing chain
2. Referenced atoms are pulled from local atom cache; missing atoms trigger a fetch
3. The signing chains of all referenced atoms are verified against the profile's trust requirements
4. If any verification fails, activation aborts with a clear error
5. The compiler is bound to the profile's vocabulary scope
6. The policy stack and governance stack are loaded into the broker's gate-evaluator and audit pipeline
7. The default persona-atom is loaded; its prompt-atom is selected based on the active model
8. The default theme is applied to the TUI
9. The user's last situational context within this profile (if any) is offered for restoration
10. The activation is recorded as a signed event in history

### Situational context creation

Situational contexts are created independently of profile activation. A user activates a profile once per session, then creates situational contexts as their focus changes.

1. The user invokes context creation or references a subject
2. The broker prompts (or accepts CLI flags) for: which identity to bind from the profile's available set, which channels to activate from the profile's allowed set, an optional subject reference, any initial Context Qualifiers
3. The context is created and becomes the active context for subsequent dispatches
4. The context creation is recorded in history

### During use

- All resolver dispatches consult the active profile, active situational context, intent, and intent qualifiers
- Context switches within a profile are fluid and frequent — no reactivation
- Persona switches within a session don't trigger reactivation
- Atom updates upstream are deferred — the profile pins versions and picks them up only on explicit refresh

### Situational context end

- A context can be explicitly closed
- A context auto-suspends when the user is idle for a configurable duration
- A context auto-archives when the referenced subject reaches a terminal state externally
- Context closure does *not* affect subjects. The subject persists; future contexts may reference it again.

### Profile deactivation

1. All active situational contexts under the profile are suspended with checkpoint
2. Any uncommitted history events are flushed
3. The slot-resolution releases (credentials de-injected from any still-running processes per their slot's lifecycle)
4. The deactivation is recorded in history

### Profile update propagation

- A profile-atom can be updated (new version published)
- Active sessions running on the previous version continue until the user explicitly upgrades or until the previous version is revoked
- Auto-upgrade is opt-in per profile, declared via `update_policy`
- Upgrades show the user a semantic diff (referenced atoms changed, policies tightened, governance changes)
- Upgrades are themselves recorded events; downgrade requires the previous version to still be available and unrevoked

---

## Profile-to-profile transitions

When a user switches profiles mid-session (e.g., paged for an incident while in their developer profile), the previous profile's active situational contexts are suspended-with-checkpoint, not closed. On switchback within a configurable window (default 24h), they're restored. After the window expires, contexts are archived but recoverable from history.

Concurrent profile activation is not supported within a single session. A user working under multiple postures (e.g., a consultant with multiple clients, or someone with both a personal and professional identity) runs separate Olympus sessions for each. This is a deliberate constraint — concurrent profile activation creates ambiguity about which posture governs any given action.

### Cross-profile subject continuity

A user may switch profiles *while a subject is still in scope*. Example: a developer responds to a production incident in their SRE profile; when the incident resolves, they switch to a Postmortem Author profile to write up what happened. Both profiles can create situational contexts referencing the same subject. The history of activity on that subject threads across both profiles (and across multiple users if the work was shared).

The durable element is the subject, not the situational context.

---

## Relationship to other atoms

### To role-pack-atoms

A profile references one or more role-packs. Role-packs are the *vocabulary and capability* layer; profiles are the *composition and posture* layer. A role-pack is reusable across many profiles.

### To policy-atoms

A profile references a stack of policy-atoms. The stack defines the floor; the governance stack and Context Qualifiers can layer additional conditional policies. Compositions never relax.

### To compliance-atoms

Compliance-atoms are pre-authored governance bindings encoding regulatory regimes (SOC2, HIPAA, FedRAMP, SOX, GDPR, etc.). A profile references compliance-atoms via its governance stack.

### To governance-binding-atoms

A profile's governance stack is a composable list of governance-binding-atoms. Compositions union requirements and take strictest. Centrally authored bindings (org-wide, regulatory) layer with team-specific or profile-specific bindings.

### To persona-atoms

A profile declares a default persona. The persona is the lens; the profile is the posture. Personas are reusable across profiles.

### To identity-atoms

A profile declares a set of identities its contexts can bind to. Situational contexts each bind one. Identities are reusable across profiles.

### To channel-atoms

A profile declares a set of allowed channels. Situational contexts subset. Channels are reusable.

### To knowledge-atoms

A profile lists knowledge sources for grounding. Knowledge-atoms span community, organizational, and personal scopes; all are referenced uniformly via the same field.

### To context-atoms (situational contexts)

A situational context is a session-scoped runtime object referencing a profile but not contained by it. The profile constrains what the context can do; the context inhabits those constraints situationally.

### To subjects

A situational context may reference at most one subject. Subjects are durable references to external entities, queryable for current state via the channel-ref attached.

### To workflow-atoms

A profile lists default workflows surfaced via discovery. Workflow-atoms are signed intent sequences, reusable across profiles.

### To agent-atoms

Agents are compositions of (trigger + persona + workflow + policy floor + budget + identity + channels). A profile may declare default agents to spawn at activation — for example, a profile might spawn a background watcher agent appropriate to the work. The profile bootstraps; agents run independently.

---

## Signing and trust

A profile-atom is signed. Its signature establishes who authored it and what trust chain it descends from.

**The profile's own signature.** Who authored the composition. An individual user can sign their own profile (informal use). An organization signs profiles it endorses for its members. Profiles can be co-signed.

**The trust of referenced atoms.** The profile's `trust_requirements` field declares what signing is required for each kind of referenced atom. Mismatches abort activation.

**Revocation.** A revoked profile, or a profile referencing a revoked atom, fails activation. Active sessions continue until they end naturally; new activations are blocked.

---

## Illustrative example: Corporate developer with regulatory compliance

The rendering below is one illustration of a constructed profile-atom. The format is illustrative; the canonical form is whatever the atom builder produces and the catalog stores.

```
profile-atom: jmfamily/profiles/developer @ 1.0.0
  authored_by: jmfamily-signing-key
  description: |
    JM Family developer working on Python services with corporate
    engineering standards, SOX compliance, and TDD discipline.

  role_packs (priority-ordered):
    1. convergent-systems/role-packs/clean-code @ 2.1.0
    2. convergent-systems/role-packs/python-senior @ 3.0.0
    3. convergent-systems/role-packs/documentation @ 1.4.0
    4. convergent-systems/role-packs/tdd-test-writer @ 2.0.0

  policy_stack (intersection):
    - jmfamily/policies/code-style-floor @ 1.0.0
    - jmfamily/policies/secret-handling @ 2.0.0
    - jmfamily/policies/dependency-vetting @ 1.0.0
    - olympus/policies/no-curl-pipe-sh @ 1.0.0

  governance_stack (union of strictest):
    - jmfamily/governance/engineering-standards @ 2.0.0
    - jmfamily/governance/sox-compliance @ 1.0.0

  default_persona: convergent-systems/personas/peer-programmer @ 2.0.0
  default_theme:   jmfamily/themes/developer-light @ 1.0.0

  default_budget:
    per_action:  0.5 drachma
    per_session: 50 drachma
    per_day:     200 drachma
    on_cap_hit:  warn

  available_identities (set):
    - jmfamily/identities/developer-github @ 1.0.0
    - jmfamily/identities/developer-bitbucket @ 1.0.0
    - jmfamily/identities/personal-experiments @ 1.0.0

  available_channels (set):
    - jmfamily/channels/internal-package-registry @ 1.0.0
    - jmfamily/channels/github-enterprise @ 1.0.0
    - convergent-systems/channels/anthropic-api @ 1.0.0
    - convergent-systems/channels/openai-api @ 1.0.0
    - olympus/channels/ollama-local @ 1.0.0

  knowledge_sources (set):
    - jmfamily/knowledge/internal-libraries @ 2.0.0
    - jmfamily/knowledge/architecture-decisions @ 1.0.0
    - jmfamily/knowledge/style-guide @ 3.0.0
    - convergent-systems/knowledge/python-stdlib @ 1.0.0

  default_workflows (set):
    - jmfamily/workflows/new-service-scaffold @ 2.0.0
    - jmfamily/workflows/refactor-with-tests @ 1.0.0
    - jmfamily/workflows/dependency-upgrade @ 1.0.0

  trust_requirements:
    role_packs:  signed by any of [convergent-systems-key, olympus-official-key]
    policies:    signed by any of [jmfamily-signing-key, olympus-official-key]
    governance:  signed by jmfamily-signing-key
    identities:  signed by jmfamily-signing-key

  update_policy:
    auto_upgrade:        false
    notification:        true
    diff_visualization:  required
```

### Walkthrough of this profile in use

A developer activates this profile and starts work. They create a situational context bound to one of their available identities (developer-github), with the github-enterprise and anthropic-api channels active, referencing subject `jmfamily-github/services/payment-validator` and Context Qualifier `Mode(refactor)`.

The developer says: *"clean up the validator and add tests for the edge cases I keep finding bugs in."*

The Intent Compiler reads all four role-pack vocabularies. It atomizes the request into a chain — a refactor intent (claimed by clean-code-pack), an enumerate-bugs intent that triggers a clarification because "bugs I keep finding" is ambiguous, and a write-failing-tests intent (claimed by tdd-test-writer-pack). After clarification, the broker dispatches each atom.

The peer-programmer persona shapes outputs as proposals rather than imperatives. The policy stack constrains the refactor to match the style guide. The governance stack — including SOX compliance — requires signed evidence for changes to financial code paths (the payment-validator qualifies). Every step produces signed audit records.

The developer experiences a single coherent response that proposes refactored code, identifies relevant bugs from issue history and code analysis, and writes failing tests for them. The four role-packs collaborated invisibly. Corporate governance fired transparently.

---

## A second domain: Non-fiction author with personal substrate

The same logical schema serves a completely different kind of work. Rather than show a second rendering, here's a description of what an author's profile-atom would contain to demonstrate that the mechanism is genuinely domain-agnostic.

**Identity fields** would establish a personal profile (`independent/profiles/non-fiction-author@1.0.0`), authored by the user's own signing key, described as a non-fiction author working on long-form narrative work.

**Role-packs** would reference two: a `community/role-packs/researcher` pack contributing verbs like `research`, `source`, `verify`, `cite`, `synthesize`; and a `community/role-packs/author-nonfiction` pack contributing `draft`, `revise`, `outline`, `voice-check`, `restructure`. Priority would resolve verb ambiguity (e.g., "draft" might exist in both vocabularies).

**Policy stack** would include `independent/policies/citation-required` (every factual claim must carry its source), `independent/policies/voice-consistency` (outputs maintain the author's established voice), and `community/policies/fact-check-floor` (a minimum standard for factual verification).

**Governance stack** would be light — a single `community/governance/personal-creative-work` binding that records what happened without heavy compliance ceremony. No SOX, HIPAA, or similar; personal creative work doesn't need them.

**Default persona** would be `community/personas/thoughtful-collaborator` — a lens that frames outputs as proposals with margin notes, asking clarifying questions rather than committing to choices unilaterally.

**Available identities** would contain a single entry: `independent/identities/personal-author`. The author writes as themselves; no multi-identity ceremony needed.

**Available channels** would include `anthropic-api` and `ollama-local` for inference, `google-scholar`, `wikipedia-research`, `jstor`, and `internet-archive` for research, `zotero-local` for citation management, and `git-local` for manuscript versioning.

**Knowledge sources** would span all three visibility scopes: community knowledge (Chicago Manual of Style, non-fiction conventions), personal knowledge (`independent/knowledge/my-book-research-corpus` — the author's accumulated research, `independent/knowledge/my-style-samples` — examples of the author's own writing for voice grounding).

**Default workflows** would include `draft-section-with-citations`, `literature-review`, `voice-consistency-check`, `fact-check-pass`.

**Trust requirements** would accept community-trusted keys for role-packs and policies, the author's own key for identities and personal knowledge, with stricter requirements for any governance binding.

When this author works, the broker composes their profile identically to how it composes the corporate developer's profile. Different role-packs, different vocabulary, different policies, different governance, different channels, different knowledge sources, different persona — but the same dispatch mechanism. The author says "I need to find three good case studies about organizations that recovered from major outages, and draft a section showing the pattern across them," and the broker atomizes the request, dispatches research/synthesis/draft intents in turn, grounds the synthesis in the author's voice samples and the draft in the chapter's existing prose, and produces a coherent response: case studies found, pattern identified, draft section written — all with citations, in the author's voice, ready for revision.

The architecture handled both cases the same way. That is the point.

---

## What this enables

**Profile marketplace.** Organizations publish profiles for internal roles. The community publishes profiles for common patterns. Users adopt and customize.

**Onboarding gets concrete.** A new hire activates the org's profile and is instantly working with the right vocabulary, policies, governance, channels, and knowledge sources.

**Compliance becomes an attribute.** Activating a profile with a compliance governance binding means all subsequent actions comply by construction.

**Role transition is a profile change.** When someone is promoted or changes specialty, switching their allowed profiles is the operational change. The profile *is* the role.

**Multi-context professionals get clean switching.** People who work across roles (developer who's also on-call, researcher who also writes for the public, consultant with multiple clients) activate different profiles per session. Each profile binds different vocabulary, policies, identities, channels.

**Vocabulary scoping matches actual work.** A user in a multi-role profile speaks all referenced role-packs' vocabularies simultaneously, with the compiler asking for clarification when verbs collide.

**Governance updates propagate centrally.** When an org tightens signing policy, they update the governance-binding-atom. Every profile referencing it picks up the change.

**Subjects thread continuity across users and sessions.** Work that spans multiple shifts, multiple roles, or multiple people has continuous history queryable by subject.

**Situational rule additions become declarative.** "While in incident-mode" or "while in drafting-mode" is a Context Qualifier triggering conditional rules in the governance stack. No special-case mechanism.

**Personal substrate becomes first-class.** A user's own knowledge, voice samples, research collections, and notes participate in the broker's grounding via personal knowledge-atoms. The substrate the user has built becomes part of how Olympus serves them.

---

## Open questions

These are issues not yet settled by this design that downstream design work will need to address.

### Subject type registry

Subjects have types (pagerduty-incident, github-pr, jira-ticket, document-uri, book-chapter, lab-experiment, etc.). The registry of subject types and their lookup channels should live as a schema-atom (`schema-atoms/subject-types`). Each type declares: how the broker resolves current state externally, what subject ID format to expect, what subject-related events to record in history. The initial subject type catalog is to be drafted.

### Subject lifecycle observability

How aggressively does the broker poll external systems for subject state? Recommendation: poll-on-context-creation plus poll-on-explicit-refresh, with configurable background polling for high-priority subjects.

### Profile inheritance complexity

Inheritance is supported but creates change-propagation complexity. Recommendation: pin all ancestor versions; explicit re-pin required to update. Whether `extends` can chain multiple levels deep is a tractable but unresolved question — recommendation is to support multi-level inheritance with explicit pinning at every level.

### Profile diff visualization

When upgrading a profile, the user needs to see what changed in semantically meaningful terms — not a raw field diff. This is itself a capability the broker can compose: given two profile-atom versions, produce a narrative summary of behavioral changes (policies tightened/relaxed, governance changes, role-packs added/removed, etc.). Worth designing alongside the broker's general diff-summarization capability.

### Profile validation pre-publication

A validation capability runnable before publishing a profile-atom to a catalog: walk the profile, check all references resolve, verify all signatures, simulate activation against trust requirements, report any issues. Should exist as a built-in broker capability.

### Default vs mandatory

Default persona, theme, budget are user-overridable within a session. Policy stack and governance stack are mandatory — situational contexts and user actions can only add restrictions, never relax. This distinction is encoded by which fields the runtime allows overrides on; it should be made explicit in implementation tests.

### Permissions on profile authoring

Who can publish profiles to community or organizational catalogs? Trust-chain governance for the catalog itself. Recommendation: profile catalogs have their own admission policies, authored as governance-bindings, applied to catalog operations rather than to individual atoms.

### Profile telemetry boundary

Whether the broker emits telemetry about profile activations is privacy-sensitive depending on profile names and contents. Recommendation: telemetry opt-in per profile via the governance stack — strict-compliance profiles opt out by default; community profiles may opt in.

### Cross-organization profile portability

A consultant working with multiple organizations may want the same personal profile across them, but each organization's policies and channels are organization-specific. Resolution: personal profile lists only personal identities, policies, and channels; client work happens under client-published profiles, switched per engagement. The personal profile is the "between clients" posture, not the "while serving client" posture.

---

## Summary

A profile-atom is the named, durable composition of role-packs, policy stack, governance stack, default persona, default theme, default budget, available identities, available channels, knowledge sources, and default workflows that defines "who someone is working as" in Olympus. It is signed, versioned, references other atoms at pinned versions, and activates as a coherent posture.

Profile and situational context are parallel dimensions in broker dispatch, not hierarchical. Profile is who I am; situational context is what I'm doing. Both contribute independently to dispatch, with Qualifier Classes providing typed specifics at both scopes.

Subjects are durable references to external entities (incidents, PRs, tickets, chapters, experiments) that situational contexts can reference and history can thread by. Subjects outlive individual situational contexts; situational contexts are session-scoped and per-user.

Governance is composable. Multiple governance bindings layer with union-of-requirement, strictest-wins. Compliance regimes, organizational rules, team-specific rules — all compose cleanly.

Profile changes are meaningful and infrequent. Situational context changes are fluid and constant. Subject references thread continuity across both. The architecture is parallel and orthogonal, not stacked.

The mechanism is domain-agnostic. The same logical schema serves developers working under corporate compliance, authors writing with personal substrate, SREs responding to incidents, researchers running experiments, designers building brand systems, and any other kind of work composed from the underlying atoms. Olympus is a generalized AI operating system; profile-atoms is how it shapes itself to whoever is working.
