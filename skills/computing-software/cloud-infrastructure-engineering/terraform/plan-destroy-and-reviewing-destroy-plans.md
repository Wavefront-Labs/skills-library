---
id: computing-software.cloud-infrastructure-engineering.terraform.plan-destroy-and-reviewing-destroy-plans
name: plan-destroy-and-reviewing-destroy-plans
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, plan-destroy, destroy-plan, terraform-destroy, teardown, destroy-review, prevent-destroy, deletion-protection]
level: practitioner
status: docs-checked
description: "Produce and review a destroy plan with plan -destroy -out before tearing anything down: what blocks a destroy and the review checklist that catches data loss."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan", "https://developer.hashicorp.com/terraform/cli/commands/destroy", "https://developer.hashicorp.com/terraform/cli/commands/apply", "https://developer.hashicorp.com/terraform/cli/commands/show", "https://developer.hashicorp.com/terraform/cli/commands/state/list", "https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#prevent_destroy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `plan -destroy` and reviewing destroy plans

**Goal:** never run `terraform destroy` blind. Produce the destroy plan as a file,
review it like any other change, then apply that exact file.

## 1. Commands
```bash
terraform plan -destroy -out=destroy.tfplan     # destroy planning mode, saved
terraform show destroy.tfplan                    # review the saved plan
terraform apply destroy.tfplan                   # executes it; no confirmation prompt
```
`terraform destroy` is a convenience alias for `terraform apply -destroy`; it runs its
own plan and prompts for approval, and it does not accept a plan file argument. A saved
plan is better for anything shared or automated because the reviewed plan is what
runs. When you pass a saved plan, Terraform treats that as the approval and cannot take
further planning options. Destroy mode "creates a plan whose goal is to destroy all
remote objects that currently exist, leaving an empty Terraform state". The `-destroy`
option on `apply` exists from Terraform v0.15.2; earlier versions need `terraform
destroy`.

Name the plan file with a suffix such as `.tfplan`, not `.tf`. A saved plan holds
sensitive values in cleartext, so treat it as a sensitive artifact.

## 2. Reading a destroy plan
- The plan ends with a summary line of the form `Plan: 2 to add, 1 to change, 2 to
  destroy.` In destroy mode expect the `destroy` count to be the whole story; read any
  other entry before approving.
- Entries marked `-` are destroyed; `-/+` are destroy-then-recreate.
- For a teardown of everything, compare the destroy count with `terraform state list`
  (lists every resource in state; give an address or module such as `module.elb` to
  filter).

## 3. What blocks a destroy
| Blocker | What happens |
|---|---|
| `lifecycle { prevent_destroy = true }` | Terraform rejects plans that would destroy the object and returns an error; it also prevents the `terraform destroy` command from operating once such objects exist |
| A provider configuration removed too early | If a resource instance is still tracked in state but its provider configuration block is gone, planning errors and asks you to reintroduce the block; keep provider blocks until the last resource is destroyed |

`prevent_destroy` does not stop Terraform destroying a resource whose configuration you
removed, so check removed resource blocks too. The lifecycle page also documents a
`destroy` option: set to false it removes a resource from state without destroying the
real infrastructure object.

Provider-specific safeguards (deletion protection flags, non-empty storage, final
snapshots) are defined by each provider; read the provider's resource documentation for
the resources in the plan.

## 4. Review checklist
- [ ] Stateful resources (databases, volumes, buckets, keys, secrets) listed? Each has a backup or an explicit "data loss accepted" note.
- [ ] Other configurations that read this one's outputs, for example through `terraform_remote_state`, will break after a destroy.
- [ ] The count matches the intended scope, whole configuration or an intended subset.

## Gotchas
- `terraform destroy -target ADDRESS` destroys that resource and its dependencies; read the plan before approving it. HashiCorp recommends `-target` only for exceptional circumstances.

## Checked
Date: 2026-11-07
Read in full: `terraform plan` (all sections), `terraform destroy`, `terraform apply`, `terraform show`, `terraform state list`. Lifecycle page: read the `prevent_destroy` section and the `destroy` option text only (matched lines of the page, not the whole page).
Confirmed: destroy mode text, `-destroy` on apply from v0.15.2, destroy as alias with no plan file argument, saved plan applies without prompting, `.tf` suffix warning, cleartext plan warning, summary line format, `-/+` symbol meaning, `state list` filtering, `prevent_destroy` behaviour, `destroy -target` text, provider-removal error behaviour (Providers Within Modules page, read in full for another skill in this batch).
Removed (not on any cited page): `less` pipe, `terraform graph -type=plan-destroy`, data sources being read during destroy plans and the `-refresh=false` workaround, the `Instance cannot be destroyed` string, provider deletion-protection table row, DependencyViolation, HCP workspace protection, KMS 7-30 day claim, saved-plan checksum claim, `workspace delete` claim, the `terraform state list | wc -l` pipe, the "0 to add, 0 to change" expectation, the contradictory `-target` sentence, and the Verify steps. The block that hosts the lifecycle `destroy` option was not checked, so the skill does not name one.
Method: documentation only; no commands were run.
