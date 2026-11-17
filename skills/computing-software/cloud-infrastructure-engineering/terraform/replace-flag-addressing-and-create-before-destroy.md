---
id: computing-software.cloud-infrastructure-engineering.terraform.replace-flag-addressing-and-create-before-destroy
name: replace-flag-addressing-and-create-before-destroy
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, replace-flag, replace-address, replace-indexed, replace-create-before-destroy, forced-replacement]
level: practitioner
status: verified
description: "Force replacement with -replace: addressing indexed and module instances per shell, multiple targets, saved plans, and how create_before_destroy changes the order."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#replace-address", "https://developer.hashicorp.com/terraform/cli/state/resource-addressing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `-replace` addressing and create-before-destroy

## Addresses
```bash
terraform plan -replace='aws_instance.web'
terraform plan -replace='aws_instance.web[2]'
terraform plan -replace='aws_instance.web["blue"]'
terraform plan -replace='module.app["eu"].aws_instance.web[0]'
terraform plan -replace='aws_instance.a' -replace='aws_instance.b'     # repeatable
terraform plan -replace='aws_instance.web' -out=tfplan && terraform apply tfplan
```
- Must be a **resource instance**: `-replace=aws_instance.web` on a resource with
  `count` does not match any instance - Terraform 1.17.0 prints `Warning: Incompletely-matched
  force-replace resource instance` ("lacks an instance key") with the `-replace="..."` options
  to use, and the plan replaces nothing. Give the index, or repeat per instance.
- Whole modules cannot be replaced with one flag (`-replace='module.app["eu"]'` fails with
  `Invalid force-replace address ... A resource instance address is required here`); list
  the instances (`terraform state list 'module.app["eu"]' | sed "s/^/-replace=/"`).
- PowerShell 5.1: `-replace='aws_instance.web[\"blue\"]'` (or `--%` then
  `-replace="aws_instance.web[\"blue\"]"`); cmd: `-replace="aws_instance.web[\"blue\"]"`.
  Without the backslashes the quotes are stripped and Terraform reports `Invalid force-replace
  address "aws_instance.web[blue]"` (`Index brackets must contain either a literal number or
  a literal string`).

## Order of operations
| Resource lifecycle | Plan symbol | Order |
|---|---|---|
| default | `-/+` | destroy old, then create new (downtime) |
| `create_before_destroy = true` | `+/-` | create new, repoint dependents, then destroy old |
For zero-downtime replacement of an instance behind a load balancer, CBD plus a
health-checked attachment is what makes `-replace` safe.

## Why `-replace` over `taint`
`taint` writes state immediately and anyone's next apply replaces it; `-replace`
is shown in a reviewable plan and does nothing if you discard the plan.

## Gotchas
- `-replace` cannot be combined with `-refresh-only` or `-destroy` (`Error: Unsupported plan
  mode ... allowed only in normal planning mode`).
- A misspelled address that matches no resource does not fail: Terraform 1.17.0 printed no
  warning and `No changes` - read the plan to confirm `will be replaced, as requested`.
- Dependents with `replace_triggered_by` on the replaced resource are replaced too (`will
  be replaced due to changes in replace_triggered_by`).
- `prevent_destroy` blocks `-replace`: `Error: Instance cannot be destroyed`.

## Verify
- [ ] Plan line reads `# <address> will be replaced, as requested`.
- [ ] Symbol is `+/-` when CBD is expected.

## Checked
- Terraform 1.17.0 with `count`, `for_each` and a `for_each` module of `terraform_data`: `-replace` with `[2]`, `["blue"]`, `module.app["eu"].terraform_data.web[0]`, two repeated flags and a `replace_triggered_by` dependent all planned `will be replaced, as requested` (and `due to changes in replace_triggered_by`); the no-index, whole-module, wrong-address, `prevent_destroy`, `-destroy` and `-refresh-only` cases gave the results quoted; quoting was run in Windows PowerShell 5.1 (`\"` form and `--%` worked, bare quotes failed) and in cmd.exe (`\"` worked, bare quotes failed). The `+/-` symbol and `create_before_destroy` ordering were confirmed by a `create_before_destroy` replacement plan (`+/-`).
- AWS-specific zero-downtime advice (load balancer health checks) is not exercised here.
