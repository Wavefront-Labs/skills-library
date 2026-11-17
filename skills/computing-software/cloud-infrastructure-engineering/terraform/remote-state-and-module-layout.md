---
id: computing-software.cloud-infrastructure-engineering.terraform.remote-state-and-module-layout
name: remote-state-and-module-layout
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, hcl, remote-state, s3-backend, use-lockfile, dynamodb-locking, state-locking, workspaces, modules, module-versioning, moved-block, import-block, removed-block, terraform-plan, terraform-apply, lock-file, hcp-terraform, blast-radius]
level: practitioner
status: docs-checked
description: "Run Terraform/OpenTofu safely at team scale: locked remote state split per environment and component, thin versioned modules, and moved/import/removed blocks for refactors."
sources:
  - https://developer.hashicorp.com/terraform/language/backend
  - https://developer.hashicorp.com/terraform/language/backend/s3
  - https://developer.hashicorp.com/terraform/language/state
  - https://developer.hashicorp.com/terraform/language/state/locking
  - https://developer.hashicorp.com/terraform/language/state/remote-state-data
  - https://developer.hashicorp.com/terraform/language/modules/develop/refactoring
  - https://developer.hashicorp.com/terraform/language/import
  - https://developer.hashicorp.com/terraform/language/block/removed
  - https://developer.hashicorp.com/terraform/cli/commands/init
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Terraform remote state and module layout: small states, safe refactors

**Goal:** every root module has its own locked remote state, environments cannot clobber each other, modules are reusable and versioned, and refactors never destroy real infrastructure.

## 1. Remote state with locking
S3 example with native lockfile locking:
```hcl
terraform {
  backend "s3" {
    bucket       = "example-tfstate-<ACCOUNT_ID>"
    key          = "network/prod/terraform.tfstate"
    region       = "eu-west-1"
    encrypt      = true
    use_lockfile = true
  }
}
```
- `use_lockfile` defaults to `false`. DynamoDB-based locking (`dynamodb_table`) is deprecated and will be removed in a future minor version; both can be set at once to migrate.
- With `use_lockfile`, the credentials also need `s3:GetObject`/`s3:PutObject` on the `<key>.tflock` object.
- The S3 docs strongly recommend Bucket Versioning for state recovery. `encrypt` enables server-side encryption of state and lock files; `kms_key_id` selects a KMS key.
- Other workspaces are stored under `<workspace_key_prefix>/<workspace_name>/<key>` (default prefix `env:`).
- State can contain sensitive values, so restrict who can read it. Locking happens automatically on operations that can write state; `-lock=false` is not recommended.
- Backend blocks cannot reference variables, locals or data sources.

## 2. Split state by blast radius
One state per component per environment, for example:
```
live/prod/{network,data,app}   live/stage/{network,data,app}   modules/{vpc,rds,service}
```
- Judgement, not from the docs: keep a plan small enough to review and owned by one team.
- `terraform_remote_state` reads root module outputs from another state, but its user needs access to the entire state snapshot, which may hold sensitive data. HashiCorp recommends `tfe_outputs` in HCP Terraform/Enterprise because it does not need full state access.
- Directories per environment keep backends, credentials and code separate; CLI workspaces share one backend configuration.

## 3. Module design
- A module is a reusable concept, not a single-resource wrapper; see `computing-software.cloud-infrastructure-engineering.terraform.module-design-and-reuse`.
- Reusable modules must not contain `provider` blocks; they declare `required_providers` and constrain a minimum with `>=`.
- Pin module versions by registry version or an immutable Git ref in the source address rather than a branch.

## 4. Refactor without destroying
```hcl
moved {
  from = aws_instance.web
  to   = module.web.aws_instance.this
}
import {
  to = aws_s3_bucket.logs
  id = "example-logs-bucket"
}
removed {
  from = aws_s3_bucket.legacy
  lifecycle { destroy = false }
}
```
- `moved` updates an address instead of destroying and recreating; removing a `moved` block is a breaking change for callers still on old addresses. Moved blocks for module addresses need Terraform v1.1 or later.
- `import` needs a matching `resource` block. Write only the `import` block and run `terraform plan -generate-config-out=...` to generate the resource block.
- `removed` with `destroy = false` removes the object from state without destroying it.

## 5. Plan and apply discipline
- Judgement: save a plan in CI, review it, and apply that saved plan so apply matches the reviewed plan.
- A saved plan embeds the backend settings from `.terraform/terraform.tfstate`; do not put credentials in `-backend-config`.
- Use `force-unlock` only for your own lock when automatic unlocking failed; it requires the lock ID Terraform printed.

## Gotchas
- Two roots with the same `key` share one state object; derive keys from the directory.
- Changing backend settings needs `terraform init -migrate-state` (copy state) or `-reconfigure` (ignore the old configuration). Back up state first.

## Verify
- [ ] Every root has a unique backend key, versioning, and locking enabled.
- [ ] Two concurrent plans on one root: the second waits or fails on the lock.
- [ ] Modules are referenced by an immutable version.
- [ ] A rename via `moved` plans as moved, with zero destroys.

## Checked
2026-11-09

Method: read the Terraform backend, S3 backend, state, locking, remote state data, refactoring, import, removed and init pages (fetched as text). Removed as unsupported by those pages: GCS and Azure backend settings, OpenTofu state encryption, the Terraform 1.10, 1.5 and 1.7 version claims, `.terraform.lock.hcl` platform advice, tflint, and the plan-duration rule of thumb (kept as judgement). Related: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.plan-review-and-environment-promotion
