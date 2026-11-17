---
id: computing-software.cloud-infrastructure-engineering.terraform.create-before-destroy-naming-propagation-and-cycles
name: create-before-destroy-naming-propagation-and-cycles
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, create-before-destroy, cbd-naming, cbd-propagation, cbd-cycle, create-before-destroy-cycle, lifecycle, name-prefix]
level: advanced
status: gated
description: "Use create_before_destroy without name collisions, understand how it propagates to dependencies, and untangle the cycles it causes."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#create_before_destroy", "https://github.com/hashicorp/terraform/blob/main/docs/destroying.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `create_before_destroy`: naming, propagation, cycles

## Naming collisions
Creating the replacement before destroying the old one means both exist at once.
Unique-name resources then fail: `InvalidGroup.Duplicate`, `BucketAlreadyExists`,
`name already in use`.
```hcl
# (gated: unconfirmed, source is paywalled or blocked) (the AWS name collisions and name_prefix below were not run; no AWS provider here)
resource "aws_launch_template" "web" {
  name_prefix = "web-"                 # provider appends a unique suffix
  lifecycle { create_before_destroy = true }
}

resource "random_id" "sg" {
  byte_length = 3
  keepers     = { vpc = var.vpc_id }   # new suffix whenever the replacement trigger changes
}
resource "aws_security_group" "web" {
  name = "web-${random_id.sg.hex}"
  lifecycle { create_before_destroy = true }
}
```
Prefer `name_prefix` where the provider offers it.

## Propagation
If resource **A** is CBD and **B** depends on A, then when A is replaced B must be
updated to point at new-A before old-A goes away. Terraform therefore forces CBD
ordering onto the **dependencies** of a CBD resource (things A depends on) — you
cannot have A create-before-destroy while something it depends on is
destroy-before-create. In the plan the legend line `+/- create replacement and then destroy` marks the dependency (ran: with `a` CBD and `dep` not, replacing `dep` showed `+/-` for `dep`), versus `-/+ destroy and then create replacement` for ordinary replaces. `(destroy deposed <key>)` nodes appear in the apply graph of a saved plan (`terraform graph -plan=tfplan`), not in `-type=plan`.
Practical rule: when you set CBD on a resource, set it on the resources it depends
on that may also be replaced (e.g. launch template + its security group).

## Cycles
Typical error:
```
Error: Cycle: aws_security_group.web (destroy deposed), aws_instance.web, aws_security_group.web
```
Causes and fixes:
- A CBD resource depends on a non-CBD resource that is being replaced → add CBD to
  the dependency, or stop replacing it (fix the attribute forcing replacement). On plain `terraform_data` objects Terraform propagated CBD itself and planned without a cycle (also with an explicit `create_before_destroy = false` dependent), so the cycle shown above is provider-specific (gated: unconfirmed, source is paywalled or blocked).
- A resource references *itself* indirectly through a provisioner or `depends_on`
  → remove the unnecessary `depends_on`.
- Security group rules inline in two groups referencing each other → split into
  `aws_vpc_security_group_ingress_rule` resources.
`terraform graph -type=plan -draw-cycles` needs an explicit `-type`. In Terraform 1.17.0 and OpenTofu 1.13.2 the cycle error went to stderr and the DOT output contained no `red` edges, so rely on the error's node list; the red-edge claim did not reproduce.

## Gotchas
- Not settable from variables (`Variables not allowed`); a module's resources cannot be made CBD by the caller. In a CBD replace the old object is destroyed without running destroy-time provisioners (Terraform provisioners doc; ran: the log line was not written).
- CBD + `prevent_destroy` on the old object blocks the replacement completely (ran: `Error: Instance cannot be destroyed`).
- If the destroy of the old object fails, it becomes **deposed** (see deposed skill).

## Verify
- [ ] Plan shows `+/-` (create then destroy) for the resource.
- [ ] No `Cycle:` error in `terraform plan`; replacement apply completes without duplicate-name errors.

## Checked
- Terraform 1.17.0 / OpenTofu 1.13.2, `terraform_data`, `random_id`: CBD propagation to a dependency shown as `+/-`; `random_id` with `keepers` replaced (`forces replacement`) while the CBD consumer updated in place; `(destroy deposed ...)` found only via `graph -plan`; `-draw-cycles` produced no red edges on a two-module cycle (Terraform printed a multi-line `Error: Cycle:` list, OpenTofu a single-line one); variables rejected in `lifecycle`; `prevent_destroy` + CBD blocked the replace; destroy provisioner skipped under CBD, as the provisioners doc says.
- Gated: AWS duplicate-name errors, `name_prefix` and the `aws_security_group` cycle recipes.
