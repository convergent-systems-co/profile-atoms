# 0001. Use Cloudflare R2 as Terraform Remote Backend

- Status: accepted
- Date: 2026-05-26

## Context

Terraform state must be stored remotely so that CI/CD pipelines and multiple
contributors share a single source of truth. Local state is not acceptable for
a production system.

## Decision

Use Cloudflare R2 (S3-compatible) via the `s3` backend provider with the
`cs-tfstate` bucket. Each environment (dev/stg/prod) gets its own state key
under `state-bucket/convergent-systems-co/profile-atoms/<env>/terraform.tfstate`.

R2 is chosen because:
- The project already runs on Cloudflare (Pages, Workers, DNS).
- R2 has no egress fees, unlike AWS S3.
- The `s3` backend is stable and well-tested against R2.
- `use_lockfile = true` gives state-locking without a DynamoDB table.

## Consequences

- All `terraform init` calls must supply `AWS_ACCESS_KEY_ID` and
  `AWS_SECRET_ACCESS_KEY` (mapped to an R2 API token) via CI secrets.
- The bucket `cs-tfstate` must exist and be configured before first init.
- State is shared — plan/apply must be serialized per env in CI.

## Alternatives considered

- HCP Terraform (Terraform Cloud). Rejected — adds a SaaS dependency and cost
  when R2 is already available.
- AWS S3 + DynamoDB locking. Rejected — unnecessary cross-cloud dependency;
  R2 native locking via `use_lockfile` is sufficient.
- Local state. Rejected — not shareable; lost on CI runner teardown.
