# profile-atoms

> User/agent profile compositions — the durable "working-identity" declarations users activate in the [Olympus](https://github.com/convergent-systems-co/olympus) broker. Each profile composes role-packs, policy stack, governance stack, default persona/theme/budget, available identities/channels, knowledge sources, and default workflows into a coherent posture.

`profile-atoms` is a `*-Atoms` catalog in the [Convergent Systems](https://xdao.co) ecosystem. It defines what exists in its domain — typed, versioned, machine-readable, composable, and open — so runtimes (and humans) can stand on shared infrastructure instead of reinventing it.

## Structure

```
profile-atoms/
├── ATOMS.yml              # Catalog manifest
├── profiles/              # Profile compositions (each profile composes other catalogs' atoms)
├── schemas/               # profile-atom-v1.json
├── exports/               # CI-generated catalog.json
├── docs/                  # Design doc + how-to-author
├── scripts/               # validate.py + build-exports.py
└── web/                   # Astro site for profile-atoms.com
```

## Composition shape

This catalog is unusual: it catalogs **only compositions**, not primitive atoms. Every "atom" here IS a composition that references atoms from other catalogs (`prompt-atoms`, `agent-atoms`, `policy-atoms`, `identity-atoms`, `channel-atoms`, `theme-atoms`, `compliance-atoms`, `knowledge-atoms`, `workflow-atoms`).

A profile says: *"I am [role]. I can act as any of [identity set]. I can reach [channel set]. I am subject to [policy stack]. I am governed by [governance stack]. My default persona/theme/budget is [...]"*

The Olympus broker reads a profile and a situational context as **parallel inputs** — neither contains the other. See [`docs/design.md`](./docs/design.md) for the full architectural specification.

## How to consume

Machine-readable exports are published in [`exports/catalog.json`](./exports/catalog.json) on every release.

The deployed catalog at [profile-atoms.com](https://profile-atoms.com) serves:
- `/exports/catalog.json` — full machine-readable catalog
- `/profiles/<id>.json` — individual profile JSON
- `/schemas/profile-atom-v1.json` — the validation schema

## How to contribute

1. Read [`docs/design.md`](./docs/design.md) for the architecture.
2. Read [`schemas/profile-atom-v1.json`](./schemas/profile-atom-v1.json) for the validation schema.
3. Add a new profile under `profiles/<slug>.json`. Reference atoms in other catalogs by their canonical name + version.
4. Open a PR. CI validates the schema and rebuilds `exports/catalog.json`.
5. Larger structural changes go through the [XAIP process](https://github.com/convergent-systems-co/xaips).

## Ecosystem

- **Federation:** [xdao.co](https://xdao.co)
- **Spec:** [github.com/convergent-systems-co/atoms-spec](https://github.com/convergent-systems-co/atoms-spec)
- **Umbrella directory:** [atoms.convergent-systems.com](https://atoms.convergent-systems.com) — every catalog at a glance
- **Olympus broker:** [github.com/convergent-systems-co/olympus](https://github.com/convergent-systems-co/olympus) — the runtime consumer

## License

Apache-2.0 — see [`LICENSE`](./LICENSE).
