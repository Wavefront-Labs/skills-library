---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.terraform-module-interface-design-and-root-module-composition
name: terraform-module-interface-design-and-root-module-composition
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, module-versioning, module-interface, variable-validation, root-module, module-composition, terraform]
level: advanced
status: docs-checked
description: "Lay out Terraform modules per the standard structure and compose small modules in a flat root module using dependency inversion."
sources:
  - https://developer.hashicorp.com/terraform/language/values/variables
  - https://developer.hashicorp.com/terraform/language/modules/develop/composition
  - https://developer.hashicorp.com/terraform/language/modules/develop/structure
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Module interface design and root module composition

## Standard module structure
- The root module is the only required element; Terraform files sit in the repository root and are the primary, opinionated entrypoint.
- Recommended minimum: `README.md`, `main.tf`, `variables.tf`, `outputs.tf`, even if empty. `main.tf` is the entrypoint; any nested module calls belong in the main file. `variables.tf` and `outputs.tf` hold the declarations.
- All variables and outputs should have one- or two-sentence descriptions, which feed generated documentation. The README need not document inputs and outputs because tooling generates them.
- Include a LICENSE file; many organisations will not adopt a public module without a clear licence.
- Nested modules live under `modules/`. One with a `README.md` is considered usable by external callers; without one it is internal. This is advisory only; Terraform does not block use of internal modules.
- Use relative paths such as `./modules/consul-cluster` for nested module calls so they are treated as part of the same package.
- Examples live under `examples/` at the repository root (examples for submodules too). Because they get copied, their `module` blocks should use the source address an external caller would use, not a relative path.

## Interface
- Variables take a `type`, a `description`, and may carry a `validation` block to check the value a consumer supplies. Mark secrets with `sensitive = true`; the sensitive value is still stored in state, and `ephemeral` omits it from state and plan files with restrictions on assignment.
- Accept only what the module needs. For an object input, declare just the subset of attributes the module uses; Terraform accepts any object with at least those attributes, so a caller can pass a resource or a data source directly:
```hcl
variable "ami" {
  type = object({
    id           = string
    architecture = string
  })
}
```
- Assumptions and guarantees: validate them so maintainers see design intent and consumers get errors early and in context. The docs example puts a `precondition` in an `output` block to check that an instance's root volume is encrypted.

## Composition
Keep the module tree flat, ideally one level of child modules, and wire modules together with expressions in the root module:
```hcl
module "network" {
  source          = "./modules/aws-network"
  base_cidr_block = "10.0.0.0/8"
}
module "consul_cluster" {
  source     = "./modules/aws-consul-cluster"
  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.subnet_ids
}
```
- Dependency inversion: a module receives its dependencies (network ids, an existing image) instead of creating them, so the same module can coexist with other infrastructure and the root can connect it differently per environment. A later refactor can supply the same values from data sources without changing the module.
- Conditional creation: do not make a module detect whether an object exists. Take the object as an input; the caller passes either a managed resource or a data source.
- Multiple nested modules in one package should be composable by the caller, not call each other and form a deep tree.
- Lightweight multi-cloud abstractions are possible by giving implementations the same object-typed input (for example a list of DNS recordset objects) or the same output (for example a cluster hostname).
- Data-only modules (data sources, no resources) are worth it when they raise the level of abstraction, for example a `join-network-aws` module that hides whether the shared network data comes from the API, Consul or remote state.

## Checked
Method: docs-checked 2026-11-09 against the Terraform "Module composition", "Standard module structure" and "Input variables" pages (composition and structure read in full; the variables page covers validation and sensitivity only in passing, linking to a separate validation page not read).
Removed: sample regex and min/max validation blocks, `optional()` defaults advice, "defaults only where safe" rule, `can`/`contains` validation tips, lifecycle precondition/postcondition advice, "never configure providers in modules", output naming and breaking-change versioning, registry source/version example, state-per-blast-radius split advice, Terraform 1.9 cross-variable validation gotcha, `moved {}` and max-two-levels gotchas, and terraform-docs checklist (none confirmed on pages read).
