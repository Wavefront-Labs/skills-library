---
id: computing-software.cloud-infrastructure-engineering.terraform.moved-blocks-vs-state-mv
name: moved-blocks-vs-state-mv
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, moved-vs-state-mv, moved-block, state-mv, refactoring, decision-guide]
level: practitioner
status: verified
description: "Choose between moved blocks and terraform state mv for a refactor: reviewability, multi-environment rollout, modules, cross-state moves and emergencies."
sources: ["https://developer.hashicorp.com/terraform/language/moved", "https://developer.hashicorp.com/terraform/cli/commands/state/mv", "https://developer.hashicorp.com/terraform/language/modules/develop/refactoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `moved` block or `state mv`?

## Default: `moved` blocks
| Property | `moved` block | `terraform state mv` |
|---|---|---|
| Reviewed in a PR | yes, appears in plan (`# terraform_data.a has moved to terraform_data.c`) | no, runs immediately (`-dry-run` prints `Would move ...`) |
| Applies with other changes atomically | yes (ran: one apply moved `a` to `c` and updated its input in place) | no, separate step |
| Rolls out to every workspace/env automatically | yes, each apply moves | must be run per state |
| Works for module consumers | yes, ship it in the module | consumers must run commands |
| Needs state access on a laptop | no | yes (it also wrote `terraform.tfstate.backup` and a timestamped `.backup` file next to the local state) |
| Undo | revert the PR before it is applied; after apply, replace the block with the reverse move (both together are a cycle error) | another `state mv` |

## When `state mv` is the right tool
- **Between two different states** (`-state`/`-state-out`: ran `terraform state mv
  -state=terraform.tfstate -state-out=other.tfstate terraform_data.d terraform_data.d`, which
  created `other.tfstate`). `moved` only rewrites addresses inside the state being applied.
- **Emergency** fix where a PR cycle is not possible; follow up with config.
- **Very old Terraform** (< 1.1): `moved` blocks arrived in the v1.1 changelog.

## Rules for `moved`
- Keep blocks until every state that uses the config has applied. For shared modules,
  keep them for at least one major version.
- Chains are fine (`a -> b`, `b -> c` planned `terraform_data.a has moved to terraform_data.c`); a cycle
  (`a -> b`, `b -> a`) fails with `Cyclic dependency in move statements`.
- Put them in a `moved.tf` file with a comment and date for later clean-up.

## Rules for `state mv`
- Freeze applies, `state pull` backup, `-dry-run`, then run, then no-op plan (ran:
  after `state mv c d` plus the matching config rename the plan said `No changes`).
- Record the commands in the PR that changes the config.

## Verify
- [ ] Refactor PR either contains moved blocks or links a recorded state-surgery runbook.
- [ ] All environments show clean plans after rollout.

## Checked
- Terraform 1.17.0 with `terraform_data` and local state files: `moved` chain a to b to c, a cycle, a moved block combined with an in-place update (plan text `moved from`), `state mv -dry-run`, `state mv` (backup files created, no-op plan after), and `state mv -state/-state-out` across two state files; v1.1 changelog for the introduction of `moved`.
- Removed the unchecked claims about resource-type changes and the removed+import alternative; the "undo" row is design guidance rather than a measured result.
