---
id: computing-software.cloud-infrastructure-engineering.terraform.prevent-destroy-and-intentional-destroy-workflow
name: prevent-destroy-and-intentional-destroy-workflow
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, prevent-destroy, prevent-destroy-override, prevent-destroy-workflow, lifecycle, deletion-protection]
level: practitioner
status: docs-checked
description: "Protect stateful resources with lifecycle prevent_destroy, know its limits (literal only, bypassed by removing the block), and run a reviewed two-step intentional destroy."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#prevent_destroy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `prevent_destroy` and the intentional-destroy workflow

## Protect
```hcl
resource "aws_db_instance" "main" {
  # ...
  lifecycle {
    prevent_destroy = true
  }
}
```
With `prevent_destroy = true`, Terraform rejects plans that would destroy the infrastructure object associated with the
resource and returns an error. The argument must be present in the configuration. It is meant as protection against
accidentally replacing objects that are costly to reproduce (databases, storage, other stateful resources). The docs
warn that it makes certain configuration changes impossible to apply and stops `terraform destroy` from operating once
such objects exist, so use it sparingly.

## It does not protect against removing the block
Except for `create_before_destroy`, Terraform does not record lifecycle rules in state. If you remove the resource's
configuration, an apply destroys the real infrastructure even when `prevent_destroy` was enabled. To stop managing an
object without destroying it, use the docs' "Remove a resource from state" instructions instead. Reviewers must read
the plan, not just the lifecycle setting. If your provider offers its own deletion protection setting, enable it as a
second layer (check that provider's resource documentation for the argument and its behaviour).

## Intentional destroy (two reviews)
1. Change 1: set `prevent_destroy = false` (and any provider-level protection) and apply; the plan should show only that
   protection change.
2. Change 2: remove the resource. The plan shows the destroy. Make sure a backup or final snapshot exists first
   (provider-specific). Apply.
Separate changes make the destructive step its own explicit review.

## Not configurable
All lifecycle settings affect how Terraform builds and traverses the dependency graph, so only literal values are
allowed: `prevent_destroy = var.protect` is invalid. Keep it a literal `true` and use the workflow above to lift it.

## Verify
- [ ] A test change that would destroy or replace the resource makes the plan fail.
- [ ] The destroy change is applied only after the backup or snapshot is confirmed in the provider.

## Checked

Checked 2026-11-08 against the Terraform lifecycle meta-argument page (prevent_destroy section): plan rejection, the
must-be-present rule, use sparingly guidance, the `terraform destroy` effect, the not-recorded-in-state behaviour, and
the literal-values-only rule. Removed (not stated on the readable page; the provider registry page was unreadable): the
exact error text, the AWS `deletion_protection` and snapshot arguments, `removed` block usage, `-exclude`, `-replace`
behaviour and the two-resource `count` module workaround.

Method: documentation only; no commands were run.
