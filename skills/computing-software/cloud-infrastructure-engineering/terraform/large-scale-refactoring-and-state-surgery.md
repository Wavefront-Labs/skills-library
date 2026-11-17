---
id: computing-software.cloud-infrastructure-engineering.terraform.large-scale-refactoring-and-state-surgery
name: large-scale-refactoring-and-state-surgery
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, moved-block, state-mv, state-split, monolith-split, bulk-rename, cross-state-move, refactoring, state-surgery, backend-migration, zero-downtime-refactor, terraform-state-rm, state-backup, blast-radius-reduction]
level: advanced
status: docs-checked
description: "Rename and restructure Terraform resources at scale with moved blocks and state mv, and split a monolithic state with backups, push safety checks and zero-diff plans."
sources:
  - https://developer.hashicorp.com/terraform/language/modules/develop/refactoring
  - https://developer.hashicorp.com/terraform/cli/commands/state/mv
  - https://developer.hashicorp.com/terraform/cli/commands/state/pull
  - https://developer.hashicorp.com/terraform/cli/commands/state/push
  - https://developer.hashicorp.com/terraform/cli/commands/state/rm
  - https://developer.hashicorp.com/terraform/cli/commands/init
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Large-scale Terraform refactoring and state surgery

**Goal:** rename modules/resources at scale or split one big state into several without a real create/destroy, with a backup at every step. Individual `state mv`/`rm` mechanics and lock handling are in `computing-software.cloud-infrastructure-engineering.terraform.state-management-and-locking`; `moved` basics are in `computing-software.cloud-infrastructure-engineering.terraform.remote-state-and-module-layout`.

## 1. Back up and freeze
```bash
terraform state pull > state-backup.json
```
Also rely on backend versioning where it exists. Before `state mv` for a refactor, warn coworkers: if anyone plans between your configuration change and the `state mv`, their plan will destroy the old object and create a new one at the new address.

## 2. Rename within one state: prefer `moved` blocks
A `moved` block updates an address without destroying the object; Terraform checks state for the `from` address before planning the `to` address. Uses include moving or renaming a resource or module, enabling `count`/`for_each` while keeping the original instance, renaming a module call, and splitting a module.
```hcl
moved {
  from = module.old_naming.aws_instance.web["a"]
  to   = module.new_shape.aws_instance.web["a"]
}
```
- A `moved` block covers all instances of a resource when both addresses name the resource as a whole.
- New configurations whose state never had the `from` address ignore the block and create the resource normally.
- You cannot move a `resource` into a `data` block. Moving between resource types needs provider support.
- Removing a `moved` block is a breaking change for anyone still holding old addresses; keep historical blocks (exception: private modules where everyone has applied).
- For many renames, generating blocks from `terraform state list` output with a script avoids typos (judgement). After editing, run `terraform plan` and confirm the plan shows moves and no create or destroy. If it plans a create/destroy, an address does not match: fix before applying.
- Terraform v1.1 or later is required for `moved` blocks that refactor module addresses; older versions use `terraform state mv`.

## 3. `terraform state mv` for moves `moved` cannot express
`state mv SOURCE DESTINATION` rebinds an existing remote object to a new address. Both addresses must refer to the same kind of object (instance to instance, module to module) and a resource keeps its resource type.
```bash
terraform state mv packet_device.worker module.worker.packet_device.main
terraform state mv 'packet_device.worker["a"]' 'packet_device.helper["b"]'
```
- Use `-dry-run` first; quote brackets for your shell.
- `-lock=false` is dangerous if others may run against the same workspace; `-lock-timeout` retries the lock.
- `-state`, `-state-out`, `-backup` and `-backup-out` are legacy options for local state only. With the `remote` backend you must give a local state file to use the backup options.

## 4. Splitting a state
Judgement on sequence, using the commands above:
1. Copy the resource blocks to the new root configuration.
2. Move the objects into the new state (state surgery, ideally through a local state file; push a modified state with `terraform state push`).
3. `plan` the new root: it must show no changes.
4. Remove the blocks from the old root and `plan` it: it must not plan to destroy the real objects.

`terraform state push PATH` refuses when lineage differs (the states are different) or when the destination serial is higher (the destination has data you lack). `-force` disables both checks and overwrites the destination state: avoid. The state file must be UTF-8 without a BOM. HashiCorp recommends `state push` only when you must modify remote state by hand.

## Gotchas
- `moved` blocks and `state mv` change only addresses already in state; a typo makes Terraform plan a new object (and orphan the old one).
- Backend changes need `terraform init -migrate-state` or `-reconfigure`; back up first.
- CI definitions that point at the old root need updating as part of the refactor (judgement).

## Verify
- [ ] A state backup exists before the first move.
- [ ] Plans on both source and destination show no create or destroy before old code is deleted.
- [ ] `terraform state list` on the old state no longer contains moved resources.

## Checked
2026-11-09

Method: read the Terraform refactoring (moved) page and the `state mv`, `state push` and `init` command pages (fetched as text). Removed as unsupported by those pages: the claim that `moved` blocks can reference a different state file (1.13+), the `state replace-provider` section, the `-state=... -state-out=...` split recipe for remote backends, the claim that surgical edits bump serial but not lineage, and the date-stamped backup command. Sequence and CI advice are marked as judgement.
