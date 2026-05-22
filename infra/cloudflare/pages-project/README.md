# infra/cloudflare/pages-project

Terraform module that creates the Cloudflare Pages project hosting `profile-atoms.com`.

## What this creates

A single `cloudflare_pages_project` named `profile-atoms` with production branch `main`. Deployments arrive via `wrangler pages deploy` from `.github/workflows/deploy.yml` — no Git-source binding.

## Prerequisites

- OpenTofu or Terraform `>= 1.6.0`.
- AWS-compatible credentials for the `cs-tfstate` R2 backend (from `~/.env/convergent-systems.co/.env` via `eval "$(cat …)"`).
- `CLOUDFLARE_API_TOKEN` exported with `Cloudflare Pages — Edit` scope.
- convergent-systems-co Cloudflare account ID (FIFO var `CLOUDFLARE_ACCOUNT_ID`).

## Apply

```bash
cd infra/cloudflare/pages-project
set -a
eval "$(cat ~/.env/convergent-systems.co/.env)"
set +a
export CLOUDFLARE_API_TOKEN="$CLOUDFLARE_ACCOUNT_TOKEN"
export TF_VAR_cloudflare_account_id="$CLOUDFLARE_ACCOUNT_ID"

tofu init
tofu plan
tofu apply -auto-approve
```

Custom domain `profile-atoms.com` is attached out-of-band in the CF dashboard.

## State

```
s3://cs-tfstate/state-bucket/convergent-systems-co/profile-atoms/pages-project.tfstate
```

## Destroy

Don't destroy a project that's serving traffic. Remove the custom domain attachment first.
