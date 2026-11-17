---
id: computing-software.cloud-infrastructure-engineering.terraform.plan-action-symbols-in-place-vs-replace
name: plan-action-symbols-in-place-vs-replace
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, plan-symbols, action-symbols, plan-output, update-in-place]
level: practitioner
status: verified
description: "Read every plan action symbol (+, -, ~, -/+, +/-, <=) and the summary line, and know which ones risk downtime or data loss before approving."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan", "https://developer.hashicorp.com/terraform/tutorials/cli/plan", "https://developer.hashicorp.com/terraform/internals/json-format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plan action symbols

## The legend
| Symbol | Wording in plan | JSON `actions` | Risk |
|---|---|---|---|
| `+` | will be created | `["create"]` | low |
| `-` | will be destroyed | `["delete"]` | high: data loss |
| `~` | will be updated in-place | `["update"]` | usually low; some providers apply in-place updates with side effects such as a restart (see the provider docs for that argument) |
| `-/+` | must be replaced (destroy then create) | `["delete","create"]` | high: downtime + new ID |
| `+/-` | must be replaced (create then destroy) | `["create","delete"]` | medium: `create_before_destroy` in effect |
| `<=` | will be read during apply | `["read"]` | data source deferred; shows unknowns downstream |
| (none) `# ... has moved to ...` | moved | `["no-op"]` + `previous_address` | none if no other change |
| `# ... will no longer be managed by Terraform, but will not be destroyed` | forget (`removed` block with `destroy = false`) | `["forget"]` (`removed` blocks need 1.7+) | object stays, state entry removed |

Inside a resource block, attribute lines use the same symbols: `~ instance_type = "t3.small" -> "t3.large"`, `+ tag`, `- tag`, and `# forces replacement` marks the attribute causing a replace when the provider marks one (`~ content = "one" -> "two" # forces replacement` on `local_file`). Replacement caused by `replace_triggered_by`, `-replace` or a tainted object is explained in a comment line instead (`will be replaced due to changes in replace_triggered_by`, `will be replaced, as requested`, `is tainted, so must be replaced`).

## Summary line
`Plan: 3 to add, 1 to change, 2 to destroy.` A replace counts once in **add** and
once in **destroy**. So `1 to add, 1 to destroy` may be a single replacement, not two
unrelated changes; search the plan for `must be replaced`.

## Fast triage
```bash
terraform plan -no-color -out=tfplan > plan.txt
grep -E "must be replaced|will be destroyed" plan.txt
terraform show -json tfplan | jq -r '.resource_changes[]
  | select(.change.actions | index("delete")) | "\(.change.actions|join(",")) \(.address)"'
```

## What to stop on
- Any `-` or `-/+` on stateful resources (databases, buckets, disks, DNS zones, KMS keys).
- `-/+` where you expected `~`: find the `# forces replacement` attribute.
- `~` on resources whose provider docs say the change causes a reboot.
- Large counts of `<=` after adding `depends_on` to a module or data source.

## Verify
- [ ] Every destroy and replace in the plan is intended and named in the PR description.
- [ ] Summary counts reconcile with the grep of destroys/replaces.

## Checked
- Terraform 1.17.0, one plan built from `terraform_data` resources plus a `local_file` data source: it printed the legend `+`, `~`, `-`, `-/+`, `+/-`, `<=` and produced `+` (new), `~` (input change), `-` (resource removed), `-/+` (`triggers_replace` change), `+/-` (same with `create_before_destroy`), `<=` (data source depending on a changing resource, comment `will be read during apply`), `has moved to`, and `will no longer be managed by Terraform, but will not be destroyed`; `Plan: 3 to add, 2 to change, 3 to destroy` reconciled (one new plus two replacements to add; one removed plus two replacements to destroy); `terraform show -json` gave actions `create`, `delete`, `update`, `["delete","create"]`, `["create","delete"]`, `read`, `forget`, and `no-op` with `previous_address`; both triage commands (grep and the jq filter) ran; `# forces replacement` appeared on `local_file.content` but not on `terraform_data.triggers_replace`.
