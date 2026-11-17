---
id: computing-software.cloud-infrastructure-engineering.terraform.terragrunt-generate-and-remote-state-blocks
name: terragrunt-generate-and-remote-state-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, terragrunt-generate, terragrunt-remote-state, terragrunt, root-hcl, find-in-parent-folders, dry-backend]
level: practitioner
status: docs-checked
description: "Keep provider and backend config DRY with Terragrunt generate and remote_state blocks: root.hcl includes, path-derived state keys, if_exists modes, bootstrap behaviour."
sources:
  - https://docs.terragrunt.com/reference/hcl/blocks/
  - https://docs.terragrunt.com/features/units/state-backend/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Terragrunt generate and remote_state blocks

## root.hcl (shared by every unit)
```hcl
# live/root.hcl
locals {
  account = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
}

remote_state {
  backend = "s3"
  generate = { path = "backend.tf", if_exists = "overwrite_terragrunt" }
  config = {
    bucket       = "<STATE_BUCKET>"
    key          = "${path_relative_to_include()}/terraform.tfstate"
    region       = "<REGION>"
    encrypt      = true
    use_lockfile = true
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<-EOF
    provider "aws" {
      region = "${local.region.locals.aws_region}"
    }
  EOF
}
```
```hcl
# live/prod/<REGION>/network/terragrunt.hcl
include "root" { path = find_in_parent_folders("root.hcl") }
terraform { source = "<MODULE_SOURCE>" }
inputs = { cidr = "<CIDR>" }
```

## Details
- `find_in_parent_folders("root.hcl")` returns the absolute path of the first file with that name in the parent folders, so units need no hard-coded path. The `include` block merges the root's settings as if pasted into the unit.
- `path_relative_to_include()` returns the relative path between the unit and the included file, so every unit gets a different state key automatically.
- `if_exists` (for `generate` and for `remote_state.generate`): `overwrite`, `overwrite_terragrunt` (overwrite only a file Terragrunt generated, otherwise error), `skip` (leave the existing file) or `error`. A relative `path` is relative to the Terragrunt working directory, where the OpenTofu/Terraform code lives.
- Bootstrap: `--backend-bootstrap` defaults to false, so Terragrunt does not create backend resources unless asked; with it off and no bucket, init fails with bucket not found. `disable_init = true` stops Terragrunt creating or modifying backend resources (only `s3`, `gcs` and `azurerm` support automatic creation), but OpenTofu/Terraform still initialises the backend and needs working credentials.
- `use_lockfile = true` in the S3 `config` enables native S3 locking and, per Terragrunt's docs, requires OpenTofu 1.10 or newer; it can run alongside `dynamodb_table` during migration (both locks must be acquired).
- With `generate` set, the backend config is written to the generated `.tf` file.
- Use a separate state key per unit; do not share a key.

## Verify
- [ ] Each unit's `terraform state pull` comes from the expected bucket and key.
- [ ] Changing the provider block in root.hcl regenerates it in all units on next run.

## Checked
2026-10-31. Confirmed against the Terragrunt HCL blocks reference (remote_state: `backend`,
`disable_init`, `--backend-bootstrap` default and table, `generate` path and `if_exists`
values, `use_lockfile` requirement) and the state-backend feature page (`root.hcl`,
`find_in_parent_folders`, `path_relative_to_include`, `include`). Removed: the claim that
Terragrunt prompts to create the bucket and lock table (the docs now make bootstrap opt-in
through `--backend-bootstrap`), `skip_bucket_creation` for S3 (documented for GCS only),
the `-backend-config` fallback description, the render/debug commands, the history of
the root file name, and the AWS account, region, role and module-version sample values.
Method: documentation only; no commands were run.
