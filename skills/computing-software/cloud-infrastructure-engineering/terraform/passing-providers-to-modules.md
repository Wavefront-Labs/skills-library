---
id: computing-software.cloud-infrastructure-engineering.terraform.passing-providers-to-modules
name: passing-providers-to-modules
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, providers-map, required-providers-aliases, configuration-aliases, implicit-inheritance, providers-in-modules]
level: advanced
status: docs-checked
description: "Pass provider configurations into modules: implicit inheritance of defaults, the providers map, and declaring configuration_aliases for modules that need several."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/providers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passing providers to modules

## Implicit inheritance
A child module automatically inherits the default provider configurations of its
parent. No `providers` argument needed:
```hcl
provider "aws" { region = "eu-west-1" }
module "bucket" { source = "./bucket" }    # uses the default aws
```
Aliased configurations (those with `alias` set) are **never** inherited automatically.
Only configurations are inherited, not source or version requirements: each module
must declare its own `required_providers`.

## providers map
```hcl
provider "aws" {
  alias  = "dr"
  region = "eu-central-1"
}

module "bucket_dr" {
  source = "./bucket"
  providers = {
    aws = aws.dr          # keys: names the child expects; values: names in this module
  }
}
```
Setting `providers` on a module block overrides the default inheritance for that provider.

## Module needing several configs: configuration_aliases
```hcl
# modules/replicated-bucket/versions.tf
terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = ">= 5.0"
      configuration_aliases = [aws.primary, aws.replica]
    }
  }
}
# resources inside use provider = aws.primary / aws.replica
```
```hcl
# caller
module "data" {
  source = "./modules/replicated-bucket"
  providers = {
    aws.primary = aws
    aws.replica = aws.dr
  }
}
```
The module declares *names*; the caller binds them. The module contains no provider blocks.

## Rules
- A module meant to be called by other modules must not contain `provider` blocks.
  Such a module is not compatible with `for_each`, `count` and `depends_on` on its
  module call.
- Every module declares `required_providers` with `source`, because the source
  address is the global identifier of a provider.
- In a shared module, constrain only the minimum provider version with `>=`.
- The resource-to-provider association is static: a module call using `for_each` or
  `count` cannot pass different provider configurations to different instances, so
  use a separate module block per distinct set of configurations.

## Gotchas
- A module that still has its own provider blocks fails when combined with `count`:
  `Error: Module does not support count` ("cannot be used with count because it
  contains a nested provider configuration"). Remove the provider blocks and pass
  configurations in with `providers`.
- Remove a provider configuration only after every resource that used it is
  destroyed; otherwise planning errors and asks you to reintroduce it.

## Checked
Date: 2026-11-07
Read in full: "Providers Within Modules" (developer.hashicorp.com/terraform/language/modules/develop/providers), all sections including the Legacy Shared Modules examples.
Confirmed: implicit inheritance of default configurations, aliases never inherited, providers map semantics, configuration_aliases example, no provider blocks in shared modules, static association and separate module blocks, the `Module does not support count` error text, the destroy-before-removal rule.
Removed: the invented `Missing required provider configuration` error, the `-/aws` claim, the google-beta and nested-module gotchas, the "list every provider" claim (page says the override is per provider), and the Verify steps (`terraform providers`, `terraform validate` are not on the page). Dropped the second source (404 page).
Method: documentation only; no commands were run.
