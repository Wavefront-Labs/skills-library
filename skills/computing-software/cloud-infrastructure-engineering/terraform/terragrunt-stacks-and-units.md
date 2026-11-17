---
id: computing-software.cloud-infrastructure-engineering.terraform.terragrunt-stacks-and-units
name: terragrunt-stacks-and-units
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, terragrunt-stacks, terragrunt-units, terragrunt-stack-hcl, terragrunt-stack-generate, run-all, dependency-blocks]
level: practitioner
status: docs-checked
description: "Use Terragrunt Stacks: terragrunt.stack.hcl with unit and stack blocks, generating units, passing values, dependencies between units, and mock outputs."
sources:
  - https://docs.terragrunt.com/features/stacks/
  - https://docs.terragrunt.com/reference/hcl/blocks/
  - https://docs.terragrunt.com/features/units/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Terragrunt stacks and units

- A **unit** is a directory with a `terragrunt.hcl`: one deployable piece of infrastructure.
- A **stack** is a collection of related units managed together: one command for many components, automatic dependency handling, and a controlled blast radius.
- Two approaches. **Implicit** stacks are units arranged in a directory tree; **explicit** stacks are defined in a `terragrunt.stack.hcl` file.
- Docs guidance: implicit suits few, unique units and getting started; explicit suits several environments, reusable patterns, many similar units that differ only in values, versioned collections and catalogs. Start implicit, then introduce explicit stacks as you grow.

## terragrunt.stack.hcl
```hcl
locals { env = "prod" }

unit "vpc" {
  source = "<CATALOG_UNIT_SOURCE>"
  path   = "vpc"
  values = { env = local.env }
}

unit "eks" {
  source = "<CATALOG_UNIT_SOURCE>"
  path   = "eks"
  values = { vpc_path = "../vpc" }
}

stack "observability" {
  source = "<CATALOG_STACK_SOURCE>"
  path   = "observability"
  values = { env = local.env }
}
```
The `unit` block takes a label (name) and:
- `source`: where the unit's Terragrunt configuration lives, same syntax as `terraform.source`.
- `path`: relative path inside the generated `.terragrunt-stack` directory.
- `values` (optional): a map passed to the unit as inputs; the unit's `terragrunt.hcl` reads it as `values.<key>`.
- `no_dot_terragrunt_stack = true`: generate in the directory holding `terragrunt.stack.hcl` instead of `.terragrunt-stack`; the docs describe it as soft adoption without changing directories or migrating state.
- `no_validation` and `enabled` (default true; false skips the unit at generation and in `terragrunt stack output`).
A `unit` generates a single `terragrunt.hcl` at its path. A stack file can also `include` another file that declares only `unit` and `stack` blocks.

## Dependencies and mocks
In a catalog unit, `dependency "vpc" { config_path = values.vpc_path }` reads another unit's outputs. `mock_outputs` supplies values only when real outputs are not available, and `mock_outputs_allowed_terraform_commands` limits which commands may use them; elsewhere, with no outputs, Terragrunt errors. A `config_path` can also point at a directory holding a `terragrunt.stack.hcl`, which reads the outputs of every unit that stack generates (same addresses as `terragrunt stack output`).

## Commands
```bash
terragrunt stack generate   # materialise units into .terragrunt-stack
terragrunt stack output     # one entry per unit
terragrunt run --all plan   # run a command across the units in a tree
```

## Practices
- Pin the source version of catalog units and stacks so environments upgrade deliberately.
- Generated paths feed `path_relative_to_include()`: changing `path` moves state keys, so migrate state when renaming.
- Use `mock_outputs` only for plan/validate on a first deploy; never let mocks reach apply.

## Verify
- [ ] `terragrunt stack generate` is deterministic (no diff on rerun).
- [ ] State keys of generated units match the intended layout.

## Checked
2026-10-31. Confirmed against the Terragrunt stacks page (implicit vs explicit guidance), the
HCL blocks reference (`unit` arguments, `enabled`, stack `include` rules, dependency
`config_path`, `mock_outputs`, `mock_outputs_allowed_terraform_commands`, stack dependency
and `stack output`) and `run --all`. Removed: "GA in 2025", `stack run plan/apply`, `dag graph`,
the queue include/exclude flags, parallelism advice, pinned versions, CIDR and Kubernetes
version samples, and the claim that an older `run-all` form was renamed.
Method: documentation only; no commands were run.
