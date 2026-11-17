---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-configs-from-variables-and-provider-for-each
name: provider-configs-from-variables-and-provider-for-each
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provider-for-each-limitation, provider-variables, provider-for-each, provider-configuration]
level: advanced
status: docs-checked
description: "Configure providers from variables and locals (what values are allowed), the default and empty-configuration rules, and OpenTofu's provider for_each with its constraints."
sources: ["https://developer.hashicorp.com/terraform/language/providers/configuration#provider-configuration-1", "https://opentofu.org/docs/language/providers/configuration/#for_each"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider configs from variables; provider `for_each`

## Expressions in provider blocks (Terraform)
You can use expressions to configure provider arguments, but only values Terraform knows
before it applies the configuration: input variables and arguments you set directly in
configuration. You cannot reference computed resource attributes such as `google.web.public_ip`.
```hcl
variable "aws_region" {
  type    = string
  default = "us-west-2"
}
locals {
  common_tags = { Environment = "production", Project = "web-app" }
}
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = local.common_tags
  }
}
```
OpenTofu's page words this the same way: you can safely reference input variables, but not
resource attributes unless they are defined directly in the configuration or documented as
available during planning. It also allows ephemeral values in provider configuration.

Many providers read shell environment variables or other sources for arguments, which keeps
credentials out of version control; check the provider's documentation for each argument.

## Defaults and aliases
- With no `provider` block, Terraform assumes an empty default configuration. If the provider
  has required arguments, that is an error.
- If every `provider` block for a provider has an `alias`, Terraform still creates an implied
  empty default configuration; resources without a `provider` argument use it, and error if the
  provider needs arguments.
- Refer to an alias as `<PROVIDER_NAME>.<ALIAS>` in the `provider` argument of resource,
  data and module blocks.
- `alias` and the deprecated `version` cannot both appear in one block. Declare version
  constraints in `required_providers` instead.
- Define provider blocks in the root module; Terraform strongly recommends against them in
  child modules.

## Terraform: no provider for_each
Terraform's provider block supports only provider arguments, `alias` and `version`; there is no
`for_each`. Module calls using `for_each` or `count` cannot give different instances different
provider configurations; use one module block per distinct set (see
multi-region-for-each-modules-with-paired-providers).

## OpenTofu: provider for_each
```hcl
variable "aws_regions" {
  type = map(object({ vpc_cidr_block = string }))
}
provider "aws" {
  alias    = "by_region"
  for_each = var.aws_regions
  region   = each.key
}
```
- `for_each` can only be combined with `alias`, because the default configuration must have
  exactly one instance.
- The value must be a map, an object or a set of strings; the key or element becomes the
  instance key.
- Reference an instance as `aws.by_region["eu-west-1"]`, typically with the key chosen
  per resource instance: `provider = aws.by_region[each.key]`.
- A resource's `for_each` should be a subset of the provider's, never identical: OpenTofu then
  warns "Provider configuration for_each matches resource", and removing a key later fails with
  "Provider instance not present". A `null` map element keeps the provider instance while the
  resources are destroyed, or use `setsubtract(...)` for the resource collection.
- A targeted destroy such as `tofu apply -destroy -target=<resource>` is the warning's suggestion for destroying
  objects before removing the provider configuration.

## Gotchas
- Provider `for_each` is OpenTofu syntax; this page set does not document it for Terraform.

## Checked
Date: 2026-11-07. Read in full: Terraform "provider block reference" and OpenTofu "Provider Configuration". Confirmed: allowed expression values, computed-attribute restriction, empty default configuration and error, alias rules, `alias`/`version` exclusivity, provider-block placement advice, OpenTofu provider `for_each` forms and alias-only restriction, instance-key syntax, warning and error text, `null`/`setsubtract` approach. Corrections: the draft said resource attributes are allowed in provider blocks (e.g. an EKS endpoint) and that unknown values give bad plans; the page says computed resource attributes cannot be referenced, so that example and the "split into two roots" remedy were removed. Trims: "OpenTofu 1.9+" (the cited What's New page is a stub with no content), the module `for_each` example, `-exclude`, `.tofu` files, IAM remark and the Verify steps (`tofu providers`).
Method: documentation only; no commands were run.
