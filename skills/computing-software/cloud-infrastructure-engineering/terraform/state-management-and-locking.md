---
id: computing-software.cloud-infrastructure-engineering.terraform.state-management-and-locking
name: state-management-and-locking
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-state, tfstate, state-locking, force-unlock, lock-timeout, state-mv, state-rm, state-pull, state-push, terraform-import, lineage, serial, state-recovery, state-surgery, backend-migration, migrate-state, s3-versioning, state-split, state-merge]
level: advanced
status: docs-checked
description: "Operate Terraform state safely: lock behaviour and force-unlock, state rm/push safety checks, moved/removed/import blocks, backend migration."
sources:
  - https://developer.hashicorp.com/terraform/language/state
  - https://developer.hashicorp.com/terraform/language/state/locking
  - https://developer.hashicorp.com/terraform/cli/commands/state/rm
  - https://developer.hashicorp.com/terraform/cli/commands/state/push
  - https://developer.hashicorp.com/terraform/language/modules/develop/refactoring
  - https://developer.hashicorp.com/terraform/language/block/removed
  - https://developer.hashicorp.com/terraform/language/import
  - https://developer.hashicorp.com/terraform/cli/commands/init
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform state management and locking: surgery without losing infrastructure

**Goal:** inspect, repair and move state without orphaning or destroying real resources, and without two runs writing the same state. Backend setup is in `computing-software.cloud-infrastructure-engineering.terraform.remote-state-and-module-layout`.

## 1. What state is
- State holds bindings between remote objects and the resource instances in your configuration, plus metadata. It is a JSON file you must not edit directly; use `terraform state` commands. The state format may change between versions.
- Avoid keeping state in version control or any store without locking and access control: risk of data loss and of exposing secrets held in state.
- Terraform expects a one-to-one mapping between resource instances and remote objects. If you add or remove bindings by other means (`import`, `state rm`) you must keep that rule yourself.
- State carries a `lineage` and a `serial`. `state push` refuses a different lineage, or a destination serial higher than the pushed state's, unless `-force`, which overwrites the destination.

## 2. Locking
- If the backend supports it, Terraform locks state for all operations that could write state. Not all backends support locking. If locking fails Terraform does not continue.
- `-lock=false` is available for most commands and is not recommended. `-lock-timeout=<duration>` (for example `10m`) makes a command retry acquiring the lock instead of failing at once.
- `terraform force-unlock <LOCK_ID>` is only for removing your own lock when automatic unlocking failed. Unlocking while someone else holds the lock can cause multiple writers. The lock ID is printed when unlocking fails.

## 3. Prefer config blocks over CLI surgery
| Need | Block (reviewed in a plan) | CLI |
|---|---|---|
| Rename or move an address | `moved { from = ... to = ... }` (Terraform 1.1+) | `terraform state mv` |
| Stop managing, keep object | `removed { from = ... lifecycle { destroy = false } }` | `terraform state rm` |
| Adopt an existing object | `import { to = ... id = ... }` | `terraform import` |
Blocks go through the normal plan and apply review and can cover several resources at once. `terraform plan -generate-config-out=...` with an `import` block generates the resource blocks.

## 4. `state rm` consequences
It removes the binding without destroying the object. The next plan will propose creating a new object for each forgotten instance, which may fail if names conflict with the surviving object. Use `-dry-run` first and quote addresses containing `[...]` keys for your shell.

## 5. Splitting a state
Back up with `terraform state pull`, add `removed` blocks (destroy = false) in the source root and apply, then add the code and `import` blocks in the target root and confirm the plan shows only imports.

## 6. Backend migration
`terraform init -migrate-state` copies existing state to the new backend configuration; `-reconfigure` disregards the existing configuration and prevents state migration. After migrating, run `terraform plan` and expect no changes.

## Verify
- [ ] A state backup was pulled before every manual state operation.
- [ ] After surgery `terraform plan` on every affected root shows no changes.
- [ ] No scripts rely on `-lock=false`.

## Checked
2026-11-09

Method: read the Terraform docs pages State, State Locking, state rm, state push, refactoring (moved), removed block, import and init (fetched as text). Removed as unsupported by those pages: statement that lineage is a UUID, that plan always takes the lock, CI concurrency-group advice, bucket-version rollback recipes, `-replace`/taint remarks, state mv with create_before_destroy ordering, `-target` gotcha, stale plan-file rejection, and the OpenTofu/Terraform state-version caution. Not checked: backend-specific locking (DynamoDB, GCS).
