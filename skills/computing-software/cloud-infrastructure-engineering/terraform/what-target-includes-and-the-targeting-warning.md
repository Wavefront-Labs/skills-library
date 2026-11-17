---
id: computing-software.cloud-infrastructure-engineering.terraform.what-target-includes-and-the-targeting-warning
name: what-target-includes-and-the-targeting-warning
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, targeting-warning, target-dependencies, target, targeted-apply, resource-targeting]
level: practitioner
status: verified
description: "Know exactly what -target pulls into a plan (dependencies yes, dependents no), what the resource targeting warning means, and the mandatory full plan afterwards."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#resource-targeting", "https://developer.hashicorp.com/terraform/tutorials/state/resource-targeting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# What `-target` includes

## Dependencies in, dependents out
`-target=ADDR` plans ADDR **plus everything ADDR depends on** (transitively), but
**not** things that depend on ADDR.

```hcl
resource "terraform_data" "vpc" { triggers_replace = var.v }
resource "terraform_data" "subnet" { input = terraform_data.vpc.id }
resource "terraform_data" "web" { input = terraform_data.subnet.id }
```
| Command | Planned |
|---|---|
| `-target=terraform_data.subnet` | `vpc`, `subnet` |
| `-target=terraform_data.web` | vpc, subnet, instance |
| `-target=terraform_data.vpc` | vpc only; the subnet and instance are not updated even if they should be (plan with `triggers_replace` changed: `1 to add, 0 to change, 1 to destroy`, versus `1 to add, 1 to change, 1 to destroy` with the subnet) |
(Dependencies appear in the plan only if they have changes; unchanged ones just come along silently.)

Targeting a module (`-target=module.app`) includes every resource in it and their
dependencies (both module resources showed as `will be updated in-place`; targeting one of them planned only that one). Targeting `terraform_data.web` (no index) includes all its instances;
`'terraform_data.web["a"]'` just one.

## The warning
```
Warning: Resource targeting is in effect
You are creating a plan with the -target option, which means that the result of
this plan may not represent all of the changes requested by the current configuration.
...
Warning: Applied changes may be incomplete
```
(Terraform 1.17.0 prints the first warning on `plan` and the second on `apply`.)
Meaning: state and config now disagree for non-targeted objects; outputs may be
stale; dependents may reference old values.

## Mandatory follow-up
```bash
terraform apply -target=terraform_data.vpc      # the exceptional step
terraform plan                             # always, immediately after
```
The full plan shows what the targeted apply left behind (dependents needing
updates). Apply it or explain it.

## Inspect before you apply
```bash
terraform plan -target=module.db -out=t.tfplan
terraform show -json t.tfplan | jq -r '.resource_changes[] | select(.change.actions != ["no-op"]) | .address'
```
Surprises here are dependencies you did not realise existed.

## Gotchas
- Data sources the target depends on are read; data sources depending on the target are not (tested with `local_file`: targeting
  a resource that reads the file at `data.before` printed `Reading...` for it; targeting the resource that the data source `after` reads produced no read).
- Outputs referencing non-targeted resources are not updated (only `vpc_id` appeared under `Changes to Outputs`, not the output on `subnet`).
- A resource with `depends_on = [module.app]` that is targeted pulls every resource in `module.app` into the plan
  (two pending module updates appeared alongside the target).

## Verify
- [ ] The targeted plan contains only the expected addresses.
- [ ] A full `terraform plan` follows every targeted apply.

## Checked
- Terraform 1.17.0, `terraform_data` chain vpc, subnet, web (for_each a and b) plus a child module and outputs: `-target=subnet` and `-target=web` planned vpc replacement plus subnet update (dependencies in); `-target=vpc` planned only vpc (dependents out); `-target='terraform_data.web["a"]'` and the unindexed form behaved as described; `-target=module.app` planned both module resources and `-target=module.app.terraform_data.in2` only one; the plan warning text, the `Applied changes may be incomplete` warning on apply, a saved targeted plan listed by the `show -json | jq` line (only `terraform_data.vpc`), and the full plan after the targeted apply listing the left-behind subnet and module updates.
- Source for the warning: both warning headings printed verbatim by `plan`/`apply`. Data-source and `depends_on` bullets reproduced as described.
- Not changed: the AWS names were replaced by `terraform_data` equivalents (same graph shape); `-exclude` is covered by another skill.
