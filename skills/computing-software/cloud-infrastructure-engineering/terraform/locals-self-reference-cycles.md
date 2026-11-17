---
id: computing-software.cloud-infrastructure-engineering.terraform.locals-self-reference-cycles
name: locals-self-reference-cycles
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, locals-cycle, locals, cycle-error, self-reference]
level: practitioner
status: verified
description: "Fix Cycle and Self-referencing errors involving locals: a local referring to itself, locals that mix resource attributes into for_each, and splitting locals to break loops."
sources: ["https://developer.hashicorp.com/terraform/language/values/locals", "https://developer.hashicorp.com/terraform/language/meta-arguments/for_each#limitations-on-values-used-in-for_each"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cycles through locals

## Direct self-reference
```hcl
locals {
  tags = merge(local.tags, { Team = "x" })     # Error: Self-referencing local value
}
```
Locals are not variables you can reassign. Use separate names:
```hcl
locals {
  base_tags = { Env = var.env }
  tags      = merge(local.base_tags, { Team = "x" })
}
```

## Indirect cycle via resources
```hcl
locals {
  sg_ids = [aws_security_group.app.id, aws_security_group.db.id]
}
resource "aws_security_group" "app" {
  ingress { security_groups = local.sg_ids }   # app depends on local -> local depends on app
}
```
Terraform 1.17.0 reports the cycle members one per line, for example:
```
Error: Cycle:
  terraform_data.app
  local.sg_ids (expand)
```
Locals are single graph nodes: referencing **any** part of a local depends on **all** of it.

Fix by splitting so each consumer references only what it needs:
```hcl
locals {
  db_sg_ids = [aws_security_group.db.id]
}
resource "aws_security_group" "app" {
  ingress { security_groups = local.db_sg_ids }
}
```
For SG-to-SG references, use separate rule resources
(`aws_vpc_security_group_ingress_rule`) so groups do not reference each other.

## The "one big locals map" trap
A single `local.config` map that includes both inputs and resource attributes creates
cycles as soon as one of those resources reads `local.config`. Keep input-derived
locals separate from resource-derived locals.

## Diagnose
```bash
terraform graph -type=plan -draw-cycles | grep -i 'local\.' | head
```
The error message lists the cycle members; find the local that bridges them. `-draw-cycles`
only works together with `-type=`; the cycle edges carry `[color = "red", penwidth = "2.0"]`.
Plain `terraform graph` (no `-type`) prints a resource-only summary without cycle colouring.

## Verify
- [ ] `terraform validate` and `plan` succeed without cycle errors.
- [ ] Each local is either input-derived or resource-derived, not both.

## Checked
- Terraform 1.17.0, `terraform_data` standing in for the security groups: `tags = merge(local.tags, {...})` failed `terraform validate` with `Self-referencing local value ... cannot use its own result as part of its expression`; the indirect case (local containing `terraform_data.app.id`, consumed by `terraform_data.app`) failed validate and plan with the `Error: Cycle:` block above; splitting into `db_ids` made plan and `plan -destroy` succeed; `terraform graph -type=plan -draw-cycles | grep -i 'local\.'` listed the `local.sg_ids (expand)` edges; `-draw-cycles` without `-type` printed no cycle colouring.
- AWS: `aws_security_group` `ingress` `security_groups` and `aws_vpc_security_group_ingress_rule` exist in the provider docs source (checked there, not applied).
