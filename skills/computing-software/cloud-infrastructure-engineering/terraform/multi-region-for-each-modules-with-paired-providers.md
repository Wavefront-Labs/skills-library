---
id: computing-software.cloud-infrastructure-engineering.terraform.multi-region-for-each-modules-with-paired-providers
name: multi-region-for-each-modules-with-paired-providers
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, module-for-each-providers, paired-providers, multi-region, configuration-aliases, provider-alias]
level: practitioner
status: docs-checked
description: "Deploy one module to several regions: the static providers limit on for_each, one block per region, paired providers via configuration_aliases, OpenTofu provider for_each."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/providers#passing-providers-explicitly", "https://opentofu.org/docs/language/providers/configuration/#for_each"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-region modules and paired providers

## The constraint (Terraform)
The association between resources and provider configurations is static, so module calls
using `for_each` or `count` cannot pass different provider configurations to different
instances. If instances need different provider configurations, use a separate `module` block
for each distinct set of provider configurations.

Related rules:
- Provider configurations can be defined only in a root module. A module meant to be called by
  other modules must not contain `provider` blocks; a module with its own provider
  configurations is not compatible with `for_each`, `count` or `depends_on`.
- Additional (aliased) provider configurations are never inherited by child modules; pass
  them explicitly with the `providers` map. Default configurations are inherited implicitly.
- Each module must declare its own provider requirements; only configurations are inherited.

## Pattern 1: one module block per region
```hcl
provider "aws" {
  alias  = "usw1"
  region = "us-west-1"
}
provider "aws" {
  alias  = "usw2"
  region = "us-west-2"
}
module "bucket_w1" {
  source    = "./publish_bucket"
  providers = { aws.src = aws.usw1 }
}
module "bucket_w2" {
  source    = "./publish_bucket"
  providers = { aws.src = aws.usw2 }
}
```
The keys of the `providers` map are the configuration names the child module expects; the
values are configuration names in the calling module.

## Pattern 2: paired providers for cross-region resources
A module that connects two regions needs both a source and a destination configuration:
```hcl
module "tunnel" {
  source    = "./tunnel"
  providers = {
    aws.src = aws.usw1
    aws.dst = aws.usw2
  }
}
```
The child declares the aliases so the caller can pass them:
```hcl
# ./tunnel
terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = ">= 2.7.0"
      configuration_aliases = [ aws.src, aws.dst ]
    }
  }
}
```
Each resource then sets `provider = aws.src` or `provider = aws.dst`. For a shared module,
constrain only the minimum provider version with `>=`.

## OpenTofu: provider for_each
Any alternate provider configuration (one with `alias`) can also take `for_each`, a map, an
object or a set of strings; the instance key is the map key or the set element:
```hcl
provider "aws" {
  alias    = "by_region"
  for_each = var.aws_regions     # map(object(...)) in the OpenTofu example
  region   = each.key
}
resource "aws_vpc" "private" {
  for_each   = { for region, config in var.aws_regions : region => config if config != null }
  provider   = aws.by_region[each.key]
  cidr_block = each.value.vpc_cidr_block
}
```
- `for_each` cannot be used on the default (unaliased) configuration.
- The instance key expression is dynamic but the configuration reference is static, so all
  instances of one resource bind to instances of the same provider block.
- The resource's `for_each` must differ from its provider's `for_each`; a provider instance
  must outlive its resources by at least one plan/apply round.
- To retire a region, make the resource's `for_each` a subset of the provider's, for example
  `setsubtract(var.aws_active_regions, var.aws_disabled_regions)`. Adding the region to the
  disabled set then lets `tofu plan` and `tofu apply` remove its resources; remove the
  region from the provider set afterwards. Setting a map element to `null` works similarly in the map example.
- Removing a key from the provider collection while resources still exist gives the
  error "Provider instance not present".

## Removal rule (both tools)
Provider configurations are used to destroy remote objects, so all resources that belong
to a configuration must be destroyed before its block is removed from the configuration;
otherwise planning errors and prompts you to reintroduce the block.

## Checked
Date: 2026-11-07. Read in full: Terraform "Providers Within Modules" (passing providers explicitly, aliases, legacy shared modules) and OpenTofu "Provider Configuration" (alias, for_each, selecting and referring to provider instances, deleting a provider instance). Confirmed: static-association rule and the separate-module-block remedy, root-only provider blocks, no inheritance of aliased configurations, `configuration_aliases`, `>=` guidance, the OpenTofu provider `for_each` forms, the alias-only restriction, the superset/subset removal approach and error text. Trims: removed the "OpenTofu 1.9+" version claim and the `module ... for_each` with `providers = { aws = aws.by_region[each.key] }` example (the cited page only links to a separate module-instances page that was not read), the `toset(var.regions)` example, the Terragrunt/codegen suggestion, the S3 replication example, and the `state show` Verify step. The Terraform `for_each` meta-argument page, previously cited, was dropped from sources because nothing from it is used.
Method: documentation only; no commands were run.
