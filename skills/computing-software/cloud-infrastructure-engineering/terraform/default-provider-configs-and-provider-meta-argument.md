---
id: computing-software.cloud-infrastructure-engineering.terraform.default-provider-configs-and-provider-meta-argument
name: default-provider-configs-and-provider-meta-argument
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, default-provider, implicit-provider, provider-meta-argument, provider-alias, empty-provider-block]
level: practitioner
status: docs-checked
description: "Understand default (unaliased) and implicit empty provider configurations, select alternates per resource with the provider meta-argument, and avoid silent wrong-region resources."
sources: ["https://developer.hashicorp.com/terraform/language/providers/configuration", "https://developer.hashicorp.com/terraform/language/meta-arguments/provider", "https://developer.hashicorp.com/terraform/language/modules/develop/providers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default provider configs and the `provider` meta-argument

## Default configuration
A `provider "aws" { ... }` block **without** `alias` is the default configuration for
`aws_*` resources and data sources. A root-module provider configuration is implicitly
passed to child modules.

If you do not define a provider block, Terraform assumes and creates an **empty default
configuration** for that provider. If every `provider "aws"` block in the configuration
has an `alias`, Terraform also creates an implied empty default. If the provider has
required arguments, the empty default produces an error. Many providers can also read
their settings from environment variables (see the provider's own docs), so an empty
default can behave differently on a laptop and in CI.

Make it explicit:
```hcl
provider "aws" {
  region = var.region
  default_tags { tags = local.common_tags }
}
```

## Alternate configurations
```hcl
provider "aws" {
  alias  = "use1"
  region = "us-east-1"
}

resource "aws_acm_certificate" "cloudfront" {
  provider    = aws.use1          # reference: <PROVIDER>.<ALIAS>, no quotes
  domain_name = var.domain
}

data "aws_caller_identity" "use1" {
  provider = aws.use1
}
```
- The `provider` argument expects a `<PROVIDER>.<ALIAS>` reference; quotation marks
  are not required and arbitrary expressions are not permitted (Terraform resolves it
  while building the dependency graph), so it cannot be a variable or conditional.
- `provider` is accepted on `resource`, `data`, `ephemeral`, `import` and `check`
  blocks (and `list` blocks in query configuration).
- By default Terraform takes the provider local name from the first word of the
  resource type (`google_compute_instance` uses the default `google` configuration);
  `provider =` only chooses which configuration of it.

## Gotchas
- Before you remove a provider block, destroy every resource that belongs to that
  configuration. If the state tracks a resource whose provider configuration is no
  longer available, planning returns an error asking you to reintroduce it.
- Data sources use the default configuration unless `provider =` is set, a common
  cause of "not found" in multi-region code.
- Aliased configurations are never inherited by child modules; pass them with the
  module's `providers` map.

## Checked
Date: 2026-11-07
Read in full: provider block reference (providers/configuration), provider meta-argument reference (meta-arguments/provider), and the whole "Providers Within Modules" page (modules/develop/providers).
Confirmed: unaliased block is the default; empty default is assumed when no provider block exists and when every block is aliased; error when provider has required arguments; `<PROVIDER>.<ALIAS>` reference with no quotes and no arbitrary expressions; supported blocks list; local name from first word of resource type; state keeps the provider reference and removal of a still-used provider configuration errors at plan time; aliases are never inherited.
Removed or trimmed: the named environment variables `AWS_REGION`/`AWS_PROFILE` (not on the pages); the `google-beta` local-name-mismatch paragraph and the exact `Provider configuration not present` error string (neither is stated on the pages read); the `terraform providers` and `terraform state show` Verify steps (not on the pages).
Source fix: the cited `meta-arguments/resource-provider` page returns 404; replaced with `meta-arguments/provider` and added `modules/develop/providers`.
Method: documentation only; no commands were run.
