---
id: computing-software.cloud-infrastructure-engineering.terraform.module-design-and-reuse
name: module-design-and-reuse
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-modules, module-design, module-composition, module-interface, input-variables, optional-attributes, variable-validation, preconditions, postconditions, outputs, configuration-aliases, provider-aliases, semver, module-registry, private-registry, reusable-infrastructure, hcl]
level: advanced
status: docs-checked
description: "Design Terraform/OpenTofu modules with a stable interface: typed inputs with optional(), validation, conditions, composition over nesting, provider aliases."
sources:
  - https://developer.hashicorp.com/terraform/language/modules/develop/structure
  - https://developer.hashicorp.com/terraform/language/modules/develop/composition
  - https://developer.hashicorp.com/terraform/language/modules/develop/providers
  - https://developer.hashicorp.com/terraform/language/modules/develop/refactoring
  - https://developer.hashicorp.com/terraform/language/modules/develop/publish
  - https://developer.hashicorp.com/terraform/language/block/variable
  - https://developer.hashicorp.com/terraform/language/expressions/type-constraints
  - https://developer.hashicorp.com/terraform/language/expressions/custom-conditions
  - https://developer.hashicorp.com/terraform/cloud-docs/registry/publish-modules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform module design and reuse: an interface consumers can trust

**Goal:** modules that many root configurations can call without reading the source, that fail at plan time on bad input, and that can evolve without breaking callers. State layout and basic versioning live in `computing-software.cloud-infrastructure-engineering.terraform.remote-state-and-module-layout`; this skill is about the module's interface and internals.

## 1. Decide whether it should be a module
Make a module when the same concept (a service with its IAM, alarms and DNS; a tenant's network) is instantiated more than once, or when it encodes a policy you want enforced (encryption on, public access off). HashiCorp's composition guidance prefers relatively small modules that receive their dependencies. Do not wrap a single resource just to rename its arguments: it adds a version to bump and hides provider docs.

## 2. File layout (standard module structure)
```
modules/service/
  main.tf  variables.tf  outputs.tf  versions.tf
  README.md
  modules/        # optional nested modules; a README.md marks one as usable externally
  examples/basic/ # runnable example; set module source to the address a caller would use
  LICENSE
```
- The root module is the only required element; `main.tf`, `variables.tf`, `outputs.tf` are the recommended minimum filenames. Any nested module calls belong in `main.tf`.
- All variables and outputs should have one or two sentence descriptions; tooling generates input/output docs from them, so the README need not repeat them.
- Calls to nested modules use relative paths like `./modules/consul-cluster` so Terraform treats them as part of the same package.
- Nested modules should be composable by the caller, not call each other in a deep tree.
- A module intended for the registry follows `terraform-<PROVIDER>-<NAME>` naming and semantic-version tags (`v1.4.0` or `1.4.0`; other tags are ignored by the registry).

## 3. Shape the inputs
- Group related settings into one typed object; `optional(type, default)` supplies defaults:
  ```hcl
  variable "scaling" {
    type = object({
      min     = optional(number, 1)
      max     = optional(number, 4)
      cpu_pct = optional(number, 60)
    })
    default = {}
    validation {
      condition     = var.scaling.min <= var.scaling.max
      error_message = "scaling.min must be <= scaling.max."
    }
  }
  ```
- An optional attribute with a non-null default is never null inside the module: the default is substituted when the caller omits it or sets it to `null`. With no default it becomes `null`.
- A variable with no `default` is required. A `default` must be a literal and cannot reference other objects.
- Mark secrets `sensitive = true` (redacted in CLI output, still recorded in state). Set `nullable = false` when the variable must not be null; when nullable is true and a default exists, a caller can pass `null` to override the default.
- A module can accept an object type listing only the attributes it needs (for example `id` and `architecture`); Terraform accepts any object with at least those attributes, so a caller can pass a resource or a data source.

## 4. Assert, don't document
Variable `validation` is evaluated when the plan is created. `precondition` (assumptions) and `postcondition` (guarantees) live in a resource or data source `lifecycle` block; outputs can carry a `precondition`.
```hcl
output "api_base_url" {
  value = "https://${aws_instance.example.private_dns}:8433/"
  precondition {
    condition     = data.aws_ebs_volume.example.encrypted
    error_message = "The server's root volume is not encrypted."
  }
}
```
Preconditions and postconditions need Terraform v1.2.0 or later; use `check` blocks for dynamic checks against external state.

## 5. Compose, do not nest
Keep the module tree flat, with one level of child modules, and wire modules with expressions:
```hcl
module "network" { source = "./modules/aws-network" }
module "consul_cluster" {
  source     = "./modules/aws-consul-cluster"
  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.subnet_ids
}
```
This is dependency inversion: the module receives its dependencies, so the network can later move to another configuration and be read through data sources. For "create it here, exists there" cases, make the module accept the object as an input rather than detect existence inside the module.

## 6. Providers
- A module meant to be called by others must not contain `provider` blocks; provider configuration is defined in the root module and passed down (implicit inheritance or the `providers` argument).
- Each module declares its own `required_providers`. In a shared module constrain only the minimum version with `>=`.
- A module needing a second configuration declares `configuration_aliases = [aws.alternate]` inside the provider's `required_providers` entry; the caller passes it with `providers = { aws.alternate = aws.other }`.
- A module with its own provider configuration is not compatible with `for_each`, `count` or `depends_on` on the module call.

## 7. Outputs and versioning
- Outputs are the module's contract. HashiCorp's data-only module guidance: give a data-only module the same outputs as the managing module and you can swap between them.
- When you rename a resource inside a module, add a `moved` block so callers plan a move rather than destroy and create. Keep historical `moved` blocks: removing one is a breaking change.
- Treat removing or renaming inputs/outputs, and anything that forces replacement, as a major version (judgement; the sources do not define a semver policy).

## Gotchas
- A `moved` block does not stop a changed `for_each` key from replacing instances; add one `moved` block per key.
- Examples copied into other repos should use the externally usable `source`, not a relative path.

## Verify
- [ ] `terraform validate` passes in `examples/basic`.
- [ ] A deliberately bad input (min greater than max) fails at plan with your error message.
- [ ] No `provider` block anywhere under the module.
- [ ] Renaming an internal resource in a new version plans as a move with zero replaces.
- [ ] Every variable and output has a description.

## Checked
2026-11-09

Method: read the Terraform standard module structure, composition, providers-within-modules, refactoring and publishing pages, the variable and output block references, type constraints, custom conditions and the HCP Terraform publish-modules page (fetched as text). Removed as unsupported by those pages: Terraform 1.3 and 1.9 version claims for optional() and cross-variable validation, the terraform-docs workflow, `one()` and `try()` advice, the "depends_on makes data sources defer" claim, the "20 inputs" heuristic, tflint, and the CHANGELOG requirement. The semver rule for breaking changes is marked as judgement.
