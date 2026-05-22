# profile-atoms — Goals

> User/agent profile compositions — durable working-identity declarations for the Olympus broker. Each profile composes role-packs, policies, governance, defaults, identities, channels, knowledge, and workflows into a coherent posture.

## What this catalog makes civilization-grade

Every AI agent / runtime reinvents "what is this user authorized to do." The mapping of (user → role → vocabulary → tools → constraints → governance) lives buried in code, scattered across config files, or hardcoded into product surfaces. Switching roles means rebuilding the surface. Onboarding a new hire means re-deriving the configuration. Compliance regimes can't be applied compositionally — they're baked in.

`profile-atoms` extracts this configuration into named, versioned, signed compositions. Activating a profile is the operational change. A new role = a new profile. A compliance regime = a governance binding in the profile's stack. Cross-organization portability = standardized atom catalog references.

This makes "Olympus shaped for me" a mechanical claim rather than a marketing one. See [`docs/design.md`](./docs/design.md) for the full architectural specification.

## What it catalogs

This catalog is composition-only. There are no primitive atoms — every entry under `profiles/` is a composition that references atoms in OTHER catalogs.

### Composition: `profile`

A profile composes:

- **role_packs** (ordered, ≥1) — vocabulary and capability scopes
- **policy_stack** (ordered, may be empty) — gating rules (intersection: all must approve)
- **governance_stack** (ordered, may be empty) — signing, audit, evidence, retention requirements (union of strictest)
- **default_persona** (required) — the lens applied to outputs
- **default_theme** (required) — TUI styling
- **default_budget** (required) — drachma caps per action/session/day
- **available_identities** (set, ≥1) — bindings situational contexts can pick from
- **available_channels** (set, may be empty) — channels situational contexts can activate
- **knowledge_sources** (set, may be empty) — grounding inputs (community / organizational / personal scopes)
- **default_workflows** (set, may be empty) — surfaced runbooks
- **update_policy** (required) — how new versions of referenced atoms are picked up
- **trust_requirements** (required) — what signing is required for referenced atoms
- **extends** (optional) — inheritance from another profile

See `schemas/profile-atom-v1.json` for the full schema.

### Profile vs situational context

Profile and situational context are **parallel inputs** to the broker, not hierarchical layers. A profile is *who I am* (durable). A situational context is *what I'm doing* (session-scoped). Neither contains the other. The broker reads both at dispatch.

See [`docs/design.md`](./docs/design.md) §"Profile vs Situational Context" for the full ownership table.

### What's NOT in a profile

- Secrets engine state (lives in the engine; profiles only reference identity-atom slot identifiers)
- Cache state (separate substrate)
- Transcript history (separate substrate)
- Active model (per-fulfillment broker decision)
- LLM provider credentials (live in identity-atoms, values in the secrets engine)
- Active identity / active channels (live on situational context; profile declares available)
- Session state (runtime, not declarative)

## Runtime consumers

- **olympus** — Profile activation establishes the broker's posture. Profile composition is read on every dispatch.

## Status & priority

**Current status:** `v0.1 — schema + 2 illustrative profiles + Astro web app + deploy`

**Priority tier:** Tier 2 — broker requires profile semantics before it can be opinionated for real users.

## Roadmap

### v0.1 — Schema + illustrative profiles + deploy

**Goal:** Schema accepted. 2 illustrative profiles (corporate developer with SOX, non-fiction author with personal substrate) demonstrate the mechanism. Site deployed at profile-atoms.com.

**Success criterion:** Olympus broker scaffold reads `profiles/<id>.json`, validates against `schemas/profile-atom-v1.json`, and produces a single composed posture object.

**Kill criterion:** Schema can't capture meaningful diversity across the design's two illustrative examples without per-domain extensions — pivot to per-domain sub-schemas.

**Work:**

- [x] Logical schema accepted (v1.0.0)
- [x] `schemas/profile-atom-v1.json` published
- [x] 2 seed profiles (jmfamily-developer, non-fiction-author)
- [x] `exports/catalog.json` building
- [x] Site live at profile-atoms.com

### v0.2 — Subject types + qualifier classes

**Goal:** Subject types and qualifier classes added as separate schema-atoms (consumed by profiles).

**Work:**

- [ ] `schema-atoms/subject-types` catalog (PagerDuty incident, GitHub PR, document URI, book chapter, etc.)
- [ ] `schema-atoms/qualifier-classes` catalog (Ordering, TimeWindow, Location, Target, Mode, Urgency, etc.)
- [ ] Profile schema extended to reference these
- [ ] Olympus broker dispatch implementation

### v1.0 — Operational

**Goal:** Profile marketplace pattern. Organizations publish profiles for internal roles; community publishes patterns. Olympus runtime consumes.

## Civilization-grade property checklist

| Property | Mechanism in this catalog |
|---|---|
| Typed | JSON Schema in `schemas/profile-atom-v1.json` validates every profile |
| Versioned | Every profile has a semver `version` field; references to other atoms are version-pinned |
| Machine-readable | `exports/catalog.json` published on every release |
| Composable | References to other catalogs' atoms; resolver verifies they exist (when the referenced catalogs are deployed) |
| Open | Apache-2.0 licensed |
| Durable | No external dependencies in the hot path |

## Related

- **Design spec:** [`docs/design.md`](./docs/design.md) — full v1.0.0 architectural specification
- **Spec:** [atoms-spec](https://github.com/convergent-systems-co/atoms-spec) — canonical structure every catalog conforms to
- **Federation:** [xdao](https://github.com/convergent-systems-co/xdao)
- **Umbrella:** [atoms](https://github.com/convergent-systems-co/atoms)
- **Manifest:** [`ATOMS.yml`](./ATOMS.yml)
