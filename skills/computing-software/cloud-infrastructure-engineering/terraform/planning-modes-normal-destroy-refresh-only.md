---
id: computing-software.cloud-infrastructure-engineering.terraform.planning-modes-normal-destroy-refresh-only
name: planning-modes-normal-destroy-refresh-only
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, planning-modes, plan-mode, refresh-only, plan-destroy, terraform-plan, planning-options, replace, target]
level: intro
status: verified
description: "Choose the right planning mode (normal, -destroy, -refresh-only) and combine it with planning options (-replace, -target, -var) without hitting the mutually-exclusive flag errors."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#planning-modes", "https://developer.hashicorp.com/terraform/cli/commands/plan#planning-options"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Planning modes: normal, destroy, refresh-only

**Goal:** know the three mutually-exclusive modes of `terraform plan` and which
options are valid in each.

## 1. The modes
| Mode | Flag | Compares | Writes on apply |
|---|---|---|---|
| Normal | (none) | config vs refreshed state | infrastructure + state |
| Destroy | `-destroy` | empty config vs refreshed state | deletes everything (or `-target` subset) |
| Refresh-only | `-refresh-only` | real infrastructure vs state | **state only** — never touches infrastructure |

`terraform apply` accepts the same mode flags (`apply -destroy`, `apply -refresh-only`)
and `terraform destroy` == `apply -destroy`. Exactly one mode per run.

## 2. Refresh-only in practice
```bash
terraform plan -refresh-only
# "Note: Objects have changed outside of Terraform" ... "This is a refresh-only plan, so Terraform will not take any actions to undo these."
terraform apply -refresh-only          # prompts; updates state to match reality
```
Use it to accept drift (someone changed a tag by hand and you want state to reflect
it) or to confirm that a `plan` diff is config-driven, not drift-driven. It replaced
the standalone `terraform refresh` command, which applied the state change with no
review.

## 3. Planning options (any mode)
- `-refresh=false` — skip the refresh step (not valid with `-refresh-only`).
- `-replace=ADDR` — force replacement; normal mode only.
- `-target=ADDR` - limit scope; valid in normal, destroy and refresh-only modes (all three
  ran). `-exclude=ADDR` is an OpenTofu 1.9+ option; Terraform 1.17.0 rejects it
  (`flag provided but not defined: -exclude`).
- `-var`, `-var-file` — input values.
- `-out=FILE`, `-detailed-exitcode`, `-json`, `-lock`, `-lock-timeout`,
  `-parallelism`, `-input`, `-no-color`, `-compact-warnings` — any mode.

## 4. Errors you will see
- `-refresh=false` with `-refresh-only`: `Error: Incompatible refresh options` ("It doesn't
  make sense to use -refresh-only at the same time as -refresh=false, because Terraform
  would have nothing to do").
- `-destroy` with `-refresh-only`: `Error: Incompatible plan mode options` ("The -destroy and
  -refresh-only options are mutually-exclusive").
- `-replace` with `-destroy` or `-refresh-only`: `Error: Unsupported plan mode` ("Forcing
  resource instance replacement (with -replace=...) is allowed only in normal planning
  mode"). `-target` is allowed in both (it limits what is refreshed or destroyed).
- `apply -refresh-only tfplan` (or `apply -destroy tfplan`) where `tfplan` was a normal
  plan is **not** an error: Terraform prints `Warning: Can't change plan mode when applying
  a saved plan` ("This flag will be ignored") and applies the saved normal plan, so check
  the plan's mode before applying.

## Gotchas
- Refresh-only still reads data sources and can fail if they error.
- A refresh-only apply bumps the state serial (3 to 4 in the test); concurrent normal
  applies will see a stale plan - coordinate.
- In destroy mode `prevent_destroy` resources make the plan fail outright; there
  is no "skip" — see
  `computing-software.cloud-infrastructure-engineering.terraform.plan-destroy-and-reviewing-destroy-plans`.
- Modes are stored in the saved plan. `terraform show tfplan` of a refresh-only plan prints
  "This is a refresh-only plan, so Terraform will not take any actions to undo these";
  a destroy plan shows only the `- destroy` legend and `Plan: 0 to add, 0 to change, N to
  destroy` (no separate "destroy plan" header) - read it before applying someone else's plan
  file.

## Verify
- [ ] `terraform plan -refresh-only` after a manual change shows the drift under `Objects have changed outside of Terraform` followed by the "refresh-only plan" note (there is no `Plan:` line; with no drift it prints `No changes. Your infrastructure still matches the configuration.`).
- [ ] After `apply -refresh-only`, a normal `plan` shows the config-vs-state diff (it will now want to revert the manual change unless config is updated).

## Checked
- Terraform 1.17.0 with local_file and terraform_data: deleting/changing the managed file then `plan -refresh-only` printed the drift note (local_file reports a changed file as `has been deleted`) and no `Plan:` line; `apply -refresh-only` bumped the state serial 3 -> 4 and the following normal plan wanted to create the file again; every error and warning quoted above was produced by the flag combination named; `-target` ran in refresh-only and destroy modes; `-refresh-only` still failed with a data-source read error (`Read local file data source error`); `-destroy` with `prevent_destroy` failed with `Instance cannot be destroyed`; `terraform show` of the saved plans was compared as described.
- `terraform refresh -help` prints no deprecation text; the Terraform docs page for `terraform refresh` says the command is deprecated in favour of `-refresh-only` on plan and apply. `-exclude` is not in Terraform 1.17.0 and is in OpenTofu 1.9 (see the exclude skill).
