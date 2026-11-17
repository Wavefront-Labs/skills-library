---
id: computing-software.cloud-infrastructure-engineering.terraform.terragrunt-dry-multi-environment-configs
name: terragrunt-dry-multi-environment-configs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terragrunt, dry, multi-environment, multi-account, hcl-generation, remote-state-generation, run-all, dependency-blocks, include-block, find-in-parent-folders, terragrunt-hcl, dependency-mocking, destroy-all, apply-all, catalog]
level: advanced
status: docs-checked
description: "Use Terragrunt to keep backend/provider config and variables DRY across a multi-account, multi-region Terraform tree: generate blocks, dependency blocks, run --all."
sources: ["https://docs.terragrunt.com/reference/hcl/blocks/", "https://docs.terragrunt.com/reference/cli/commands/run/", "https://docs.terragrunt.com/reference/hcl/functions/", "https://docs.terragrunt.com/migrate/migrating-from-root-terragrunt-hcl/", "https://docs.terragrunt.com/getting-started/quick-start/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terragrunt for DRY multi-environment Terraform

**Goal:** a tree with N accounts x M regions x K components shares one backend
definition, one provider block and one set of common variables, with per-component
overrides in a handful of lines each, instead of N x M x K near-identical copies of
`backend.tf`. (For the simpler cases, a handful of envs with no account/region matrix,
plain workspaces or tfvars already cover this; see
`computing-software.cloud-infrastructure-engineering.terraform.workspace-and-environment-strategy`
before reaching for Terragrunt.)

## 1. Shape of the tree
```
live/
  root.hcl                    # root: remote_state{} generate, common config
  prod/
    us-east-1/
      account.hcl             # account_id, account_name
      vpc/terragrunt.hcl
      eks/terragrunt.hcl      # depends on vpc
  staging/
    us-east-1/...
```
The docs now recommend naming the root file `root.hcl` rather than `terragrunt.hcl` (a
recommendation, not a requirement). `find_in_parent_folders()` with no argument looks for
`terragrunt.hcl`, so with a `root.hcl` pass the name explicitly:
`find_in_parent_folders("root.hcl")`.

Each leaf `terragrunt.hcl` wraps one OpenTofu/Terraform module through the `terraform` block's
`source`, which takes local paths, Git URLs and Git URLs with `ref` parameters.
Terragrunt downloads the whole repo (the part before the `//`) so relative paths between
modules in it keep working.

## 2. DRY backend and provider via `generate` + `include`
Root `root.hcl`:
```hcl
remote_state {
  backend = "s3"
  generate = { path = "backend.tf", if_exists = "overwrite_terragrunt" }
  config = {
    bucket       = "acme-tfstate-${get_aws_account_id()}"
    key          = "${path_relative_to_include()}/tofu.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" { region = "us-east-1" }
EOF
}
```
- `remote_state` `generate` takes `path` and `if_exists`; `generate` blocks also take a label,
  `contents`, and the same `if_exists` values: `overwrite`, `overwrite_terragrunt`
  (overwrite only a file Terragrunt generated, otherwise error), `skip` and `error`.
- `get_aws_account_id()` returns the account id of the current credentials.
- The S3 `use_lockfile` option enables native S3 locking and requires OpenTofu 1.10 or later.

Every leaf does `include "root" { path = find_in_parent_folders("root.hcl") }` to inherit this.
`include` blocks need a unique label; `merge_strategy` is `shallow` by default (or `deep`,
`no_merge`).

## 3. Per-level locals and inputs
`account.hcl` at the account level and `region.hcl` at the region level each hold a
`locals {}` block; leaves read them:
```hcl
locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
}
inputs = {
  account_id = local.account_vars.locals.account_id
  region     = local.region_vars.locals.region
}
```
Common values live once per axis (account, region), and `inputs` passes them into the
wrapped module.

## 4. Cross-module data with `dependency`
```hcl
dependency "vpc" {
  config_path = "../vpc"
  mock_outputs = { vpc_id = "vpc-mock", private_subnet_ids = ["subnet-mock"] }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}
inputs = { vpc_id = dependency.vpc.outputs.vpc_id }
```
By default Terragrunt resolves a dependency by running `terragrunt output` in it, so a
never-applied dependency fails with no outputs to fetch. `mock_outputs` supplies values
only when real outputs are not available, and `mock_outputs_allowed_terraform_commands`
limits which commands may use them; if a command is not on the list and no outputs exist,
Terragrunt errors.

## 5. Running at scale
`terragrunt run --all -- plan` (the current form; older docs and this skill's earlier
version used `run-all`) runs a command across the units in the current stack in dependency
order, and `destroy` runs in the opposite order. Cautions the run reference gives:
- `run --all` with `apply` or `destroy` silently adds `-auto-approve` (shared stdin makes
  individual approvals impossible). There is no single confirmation prompt to rely on.
- `run --all destroy` destroys all dependencies of the units under the working directory as
  well as the units themselves by default; `--queue-exclude-external` or `--exclude-dir`
  prevents that.
- When it finds external dependencies (not in the current stack) it prompts to confirm
  running them; `--non-interactive` suppresses the prompt.
- `--queue-include-dir "prod/**"` narrows the run to matching directories, and
  `--working-dir` moves where discovery starts. `--parallelism N` caps concurrent unit runs;
  by default there is no limit and every unit whose dependencies have finished starts
  immediately.
- Do not set `TF_PLUGIN_CACHE_DIR` with `run --all`; use Terragrunt's Provider Cache Server.
- `run --all plan` fails for units whose dependencies were never deployed unless the
  `dependency` blocks have mock outputs.

Scope production runs to one account or region subtree; do not point `run --all apply` at the
repo root in one shot.

## Gotchas
- Units with no `dependency` between them can run in parallel. If ordering matters for a reason
  Terragrunt cannot see, express it with a `dependency` or `dependencies { paths = [...] }`
  block.
- `mock_outputs` can mask a broken upstream module during `plan`; keep the allowed command
  list narrow (`validate`, `plan`) so `apply` fails instead of using mocks.
- Generated files are not meant to be edited: with `overwrite_terragrunt` Terragrunt rewrites
  files it generated, and by default the generated file is a read-only link to a stored copy
  (`mutable = true` makes it an ordinary writable file).
- If an included config contains `dependency` blocks, only `locals` and `include` of it are
  exposed to the child's `include` and `dependency` blocks.

## Verify
- [ ] A new account/region pair needs only small `account.hcl`/`region.hcl` files plus leaf folders, with no copy-pasted backend or provider HCL.
- [ ] `terragrunt run --all -- plan` in a fresh environment succeeds via `mock_outputs` before any dependency has been applied.
- [ ] Production `run --all apply` and `destroy` are scoped to a specific subtree and the external-dependency prompt is read.

## Checked
Checked 2026-11-08 against the Terragrunt docs: HCL blocks reference (remote_state, generate, include, dependency, terraform), the `run` command reference, HCL functions, the root.hcl migration page and the quick start.
Removed: the per-repo Terraform version pinning gotcha, the Stacks comparison, the claim that moving a folder correctly relocates state, and the `terragrunt state list` check, none of which the pages state. Updated `run-all` to `run --all` and corrected the destroy confirmation claim (docs say `-auto-approve` is added).
Method: docs-only read of cited pages, 2026-11-08
