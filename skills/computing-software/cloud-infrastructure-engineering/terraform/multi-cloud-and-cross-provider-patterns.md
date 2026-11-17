---
id: computing-software.cloud-infrastructure-engineering.terraform.multi-cloud-and-cross-provider-patterns
name: multi-cloud-and-cross-provider-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, multi-cloud, provider-aliases, multi-provider, cross-cloud-dependencies, dns-delegation, vpn-peering, cloudflare, datadog, cross-account, provider-configuration-aliases, blast-radius, required-providers]
level: advanced
status: docs-checked
description: "Compose several clouds, accounts and SaaS providers in one Terraform config: provider aliases, passing providers to modules, remote state wiring, state splits."
sources:
  - https://developer.hashicorp.com/terraform/language/providers/configuration
  - https://developer.hashicorp.com/terraform/language/modules/develop/providers
  - https://developer.hashicorp.com/terraform/language/state/remote-state-data
  - https://developer.hashicorp.com/terraform/language/block/terraform
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-cloud and cross-provider patterns in Terraform

**Goal:** wire resources that span clouds or accounts (DNS in one provider pointing at a load balancer in another, networks peered across clouds) without every root needing every cloud's credentials.

## 1. Multi-cloud is usually multi-provider
Several providers in one root (for example `aws` plus `cloudflare`) is ordinary. The real risk is coupling resources that do not need to change together into one state. Judgement: default to one root per logical system, with only the providers it needs.

## 2. Aliases for several accounts or regions of one provider
```hcl
provider "aws" {
  region = "us-east-1"
}
provider "aws" {
  alias  = "euw1"
  region = "eu-west-1"
}

resource "aws_instance" "euro" {
  provider = aws.euw1
  # ...
}
```
- Refer to an alias as `<PROVIDER>.<ALIAS>` in the `provider` argument of resources, data sources and modules.
- The block without `alias` is the default; resources that do not set `provider` use it. If every block has an alias, Terraform creates an implied empty default, which errors for providers with required arguments.
- Provider configurations are defined only in the root module.

## 3. Passing providers into modules
- Child modules inherit default (non-alias) provider configurations automatically. Only configurations are inherited, not source or version requirements; each module must declare its own `required_providers`.
- Aliased configurations are never inherited; pass them with the `providers` map. Keys are the names the child expects, values are the caller's configurations.
```hcl
module "tunnel" {
  source = "./tunnel"
  providers = {
    aws.src = aws.usw1
    aws.dst = aws.usw2
  }
}
```
```hcl
# inside ./tunnel
terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = ">= 2.7.0"
      configuration_aliases = [aws.src, aws.dst]
    }
  }
}
```
- `configuration_aliases` only names the slots the module expects; the root must still define the providers and pass them in.
- A module with its own provider blocks is not compatible with `for_each`, `count` or `depends_on` on the module call.

## 4. Cross-root wiring
Expose values as root outputs and read them elsewhere with `terraform_remote_state`:
```hcl
data "terraform_remote_state" "aws_root" {
  backend = "s3"
  config = {
    bucket = "..."
    key    = "aws/alb/terraform.tfstate"
    region = "us-east-1"
  }
}
```
- It exposes only outputs, but the reader needs access to the entire state snapshot, which may contain sensitive values.
- In HCP Terraform/Enterprise HashiCorp recommends the `tfe_outputs` data source, which does not need full state access.
- Judgement: put both sides in one root only when the change must be atomic (for example both halves of a VPN or peering); otherwise separate roots keep blast radius and credentials separate.

## 5. Versions per provider
Each `required_providers` entry is versioned independently, and terraform finds a single provider version compatible with all modules. In a shared module, constrain the minimum with `>=`; the root can pin tighter.

## Gotchas
- Removing a provider configuration while resources it created are still in state errors at plan time; destroy or move those resources first.
- Judgement: scope CI credentials per root so one pipeline does not hold every cloud's credentials.

## Verify
- [ ] No root configures a provider it has no resources or data sources for.
- [ ] Aliased providers needed by a module are passed through `providers`.
- [ ] Cross-root reads go through outputs, and readers' access to state is deliberate.

## Checked
2026-11-09

Method: read the Terraform provider configuration, providers-within-modules, remote state data and terraform block pages (fetched as text). Removed as unsupported by those pages: the Dependabot/Renovate and `~>` pinning advice, the claim that provider SDKs retry and rate-limit independently, and the claim that aliases cannot be declared inside child modules beyond the documented pass-through rules. The invalid semicolon-separated provider blocks in the draft were replaced with valid HCL.
