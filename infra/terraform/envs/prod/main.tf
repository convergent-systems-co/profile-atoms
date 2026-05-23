terraform {
  required_version = ">= 1.7.0"
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.0"
    }
  }
}

# CLOUDFLARE_API_TOKEN from env, never in code. See ~/.ai/Common.md §4.
# Required token scopes:
#   - Account → Cloudflare Pages → Edit
#   - Zone → DNS → Edit (for the profile-atoms.com zone) — NOT YET GRANTED
provider "cloudflare" {}

# NOTE: the profile-atoms Cloudflare Pages project was created out-of-band
# (before terraform was wired). Apex domain attachment + DNS were added
# via direct API call on 2026-05-23 for the .com domain attachment;
# the matching CNAME record is BLOCKED until the env-file token gains
# Zone → DNS → Edit scope on the profile-atoms.com zone. See parent
# atoms repo summary for the morning fix-up checklist.
module "pages_project" {
  source = "git::https://github.com/convergent-systems-co/core-infra.git//terraform/cloudflare/pages-project?ref=v0.1.0"

  cloudflare_account_id = var.cloudflare_account_id
  project_name          = "profile-atoms"
  production_branch     = "main"
  custom_domain         = "profile-atoms.com"
  zone_id               = var.zone_id
}

variable "cloudflare_account_id" {
  description = "Cloudflare account ID that owns the Pages project."
  type        = string
}

variable "zone_id" {
  description = "Cloudflare zone ID for profile-atoms.com."
  type        = string
}

output "project_name" {
  value = module.pages_project.project_name
}

output "subdomain" {
  value       = module.pages_project.subdomain
  description = "Default *.pages.dev hostname for the project."
}

output "custom_domain" {
  value       = module.pages_project.custom_domain
  description = "Custom hostname attached to the Pages project."
}
