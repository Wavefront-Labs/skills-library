---
id: computing-software.cloud-infrastructure-engineering.terraform.ignore-changes-for-expected-drift
name: ignore-changes-for-expected-drift
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ignore-changes, expected-drift, ignore-drift, ignore-changes-all, ignore-changes-list, lifecycle]
level: practitioner
status: gated
description: "Silence drift that is expected (autoscaling counts, tags added by other systems) with lifecycle ignore_changes: list vs all, map-key and nested paths, and the traps."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#ignore_changes", "https://opentofu.org/docs/language/meta-arguments/lifecycle/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `ignore_changes` for expected drift

## Typical expected drift
- ASG/ECS `desired_count` changed by autoscaling.
- Tags stamped by other tools (`LastScanned`, cost tools, AWS Backup).
- Image tag updated by a deploy pipeline (`container_definitions`, `image`).
- Kubernetes annotations added by controllers.

## Attribute list (preferred)
```hcl
resource "aws_ecs_service" "api" {
  desired_count = 2
  lifecycle {
    ignore_changes = [desired_count]
  }
}

resource "aws_instance" "web" {
  tags = { Name = "web" }
  lifecycle {
    ignore_changes = [
      tags["LastScanned"],          # one map key
      metadata_options[0].http_tokens,
    ]
  }
}
```
Paths are static references: map keys in `["..."]`, list/block index `[0]`. No
variables, no expressions — `ignore_changes = var.list` is invalid (ran in Terraform 1.17.0 and OpenTofu 1.13.2: `A static list expression is required`). The `metadata_options[0].http_tokens` and ECS/ASG examples were not run (gated: unconfirmed, source is paywalled or blocked). A map-key path ran on `terraform_data` (`input["LastScanned"]`): changing that key produced no diff; note that the dynamically typed `input` also hid a change to the sibling `Name` key there, so confirm per-key behaviour on your provider's typed map attribute.

## `all`
```hcl
lifecycle { ignore_changes = all }
```
Terraform creates the object then never updates it (ran: changing the config produced `No changes`). Valid for "create once, owned
by someone else afterwards" (e.g. a bootstrap secret). Dangerous everywhere else:
config edits silently do nothing, which looks like a bug months later.

## Better alternatives first
- Tags from other systems: `aws` provider `ignore_tags { keys = [...] key_prefixes = [...] }`
  — provider-wide, no per-resource lifecycle (gated: unconfirmed, source is paywalled or blocked).
- Image tag changes: let the deploy tool own the task definition entirely, or pass
  the tag in as a variable.

## Gotchas
- Ignoring an attribute also ignores **your** changes to it; to change desired_count
  deliberately you must remove the ignore, apply, re-add — or use `-replace`.
- `ignore_changes` cannot prevent replacement caused by *other* attributes (ran: a changed `triggers_replace` still planned `must be replaced` while `input` was ignored).
- It applies to arguments in config, not to computed-only attributes.
- Inside modules it is not configurable by callers; expose a boolean and duplicate
  the resource with `count` if you need both behaviours.

## Verify
- [ ] After the external system changes the value, `terraform plan` shows `No changes`.
- [ ] Changing an un-ignored attribute still produces a diff.

## Checked
- Terraform 1.17.0 with `terraform_data`: map-key ignore, `ignore_changes = all`, replacement through another attribute, and the variable-in-`ignore_changes` error (also on OpenTofu 1.13.2).
- Gated: AWS ECS/ASG/EC2 examples and the provider-level `ignore_tags`.
