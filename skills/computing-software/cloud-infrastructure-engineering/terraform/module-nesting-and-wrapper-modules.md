---
id: computing-software.cloud-infrastructure-engineering.terraform.module-nesting-and-wrapper-modules
name: module-nesting-and-wrapper-modules
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, module-nesting, nested-modules, wrapper-module, thin-wrapper, module-composition, module-design]
level: advanced
status: docs-checked
description: "Keep module trees flat with composition in the root, use nested modules under modules/ for advanced pick-and-choose, and avoid modules that only wrap a single resource type."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/composition", "https://developer.hashicorp.com/terraform/language/modules/develop#when-to-write-a-module", "https://developer.hashicorp.com/terraform/language/modules/develop/structure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module nesting and wrapper modules

## Prefer flat composition
Module blocks make a configuration hierarchical, and can create a deep, complex tree.
HashiCorp strongly recommends keeping the tree flat, with only one level of child
modules, and connecting modules with expressions in the root module. This makes each
module easier to reuse in different combinations: instead of a module embedding its
dependencies, it receives them from the root, which wires the same building blocks
together differently.
```hcl
module "network" { source = "./modules/network" }
module "cluster" {
  source     = "./modules/cluster"
  subnet_ids = module.network.private_subnet_ids
}
```
(The pattern follows the composition page's example of passing outputs of one module to
inputs of another; module names are illustrative.)

## When nesting fits (standard module structure)
- Nested modules live under `modules/`. Those with a `README.md` are considered usable by
  external users; without one they are for internal use only. This is advisory;
  Terraform does not block use of internal modules.
- Use them to split complex behaviour into small modules advanced users can pick and
  choose; the docs' example splits a Consul cluster module from the IAM policy module so
  users can bring their own IAM choices. The root module stays the opinionated primary
  entrypoint.
- Call them with relative paths such as `./modules/consul-cluster` so Terraform treats
  them as part of the same repository or package instead of downloading them again.
- Several nested modules should be composable by the caller, not call each other and
  build a deeply nested tree.

## Wrapper modules that add nothing
- A good module raises the level of abstraction: it describes a new concept built from
  provider resource types (the docs' example is "HashiCorp Consul cluster running in
  AWS").
- The docs do not recommend modules that are just thin wrappers around a single other
  resource type. If the only natural name for the module is the main resource's type, it
  adds no abstraction; use the resource directly. Over-using modules makes a configuration
  harder to understand, so use moderation.

## Refactoring
Refactoring blocks in a module record renamed resources and changed module structure, so
Terraform reinterprets existing objects at their new addresses during planning, with no
manual migration step.

## Checked
Date: 2026-11-07
Read in full: Module composition (language/modules/develop/composition), Creating Modules (language/modules/develop, including when to write a module) and Standard Module Structure (language/modules/develop/structure).
Confirmed: flat tree with one level of child modules and the reason; nested modules under modules/ with README rule, relative paths and composability; thin-wrapper warning and "abstraction" test; refactoring blocks note.
Removed: the "two levels deep", "moved blocks across levels" and state-address-prefix claims, the terraform-aws-modules/s3-bucket wrapper example and "worth it when it enforces org policy" advice, the OPA/Sentinel/checkov suggestion, the alias and `count`/`for_each` multiplication gotchas, `-target` benefits, the publish-building-blocks advice, and the Verify checklist with the awk command.
Not opened: the moved block reference and Provider Requirements.
Method: documentation only; no commands were run.
