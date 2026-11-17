---
id: computing-software.cloud-infrastructure-engineering.terraform.lifecycle-static-values-and-module-callers
name: lifecycle-static-values-and-module-callers
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, lifecycle-literal, lifecycle-module-caller, lifecycle, prevent-destroy, module-design]
level: practitioner
status: gated
description: "Work within lifecycle's static-value rule: why prevent_destroy cannot take a variable, and patterns that let module callers choose protection or ignore_changes anyway."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle", "https://github.com/hashicorp/terraform/issues/22544"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lifecycle needs literals

## The rule
`lifecycle` arguments are processed before variables are evaluated, so they must
be static:
```hcl
lifecycle {
  prevent_destroy = var.protect      # Error: Variables not allowed
  ignore_changes  = var.ignored      # Error: A static list expression is required
}
```
Ran on Terraform 1.17.0: `prevent_destroy = var.protect` gives `Variables not allowed` and `ignore_changes = var.ignored` gives `A static list expression is required`; on OpenTofu 1.13.2 the `ignore_changes` error is the same but `prevent_destroy = var.protect` validated and enforced the variable's value (a destroy was blocked with the default `true` and allowed with `-var protect=false`), so the literal rule is Terraform's, not OpenTofu's.

`ignore_changes` takes attribute names (not strings, not expressions);
`create_before_destroy` and `prevent_destroy` take `true`/`false` literals;
`replace_triggered_by` takes references to resources/attributes.

## Letting callers choose: patterns
**1. Two resource variants, select with count** (common for `prevent_destroy`):
```hcl
resource "aws_s3_bucket" "protected" {
  count  = var.protect ? 1 : 0
  bucket = var.name
  lifecycle { prevent_destroy = true }
}
resource "aws_s3_bucket" "unprotected" {
  count  = var.protect ? 0 : 1
  bucket = var.name
}
locals { bucket = one(concat(aws_s3_bucket.protected, aws_s3_bucket.unprotected)) }
```
Switching `protect` moves the address; add `moved` blocks between `protected[0]` and
`unprotected[0]` (ran: `has moved to`, 0 to destroy) or document `state mv`. Without it the plan fails (`Instance cannot be destroyed` on the protected one). Heavy; use only for critical resources.

**2. Use provider-side protection instead**, which is a normal argument:
`deletion_protection = var.protect` (RDS, DynamoDB, Google SQL, azurerm locks via
`azurerm_management_lock`) (gated: unconfirmed, source is paywalled or blocked). Often the better answer than `prevent_destroy`.

**3. ignore_changes broadly in the module** and document it, when the attribute is
commonly managed elsewhere (`desired_count` with autoscaling, `tags` managed by
policy).

**4. Callers wrap with their own guardrails**: policy-as-code rejecting destroys of
tagged resources, or a `removed { lifecycle { destroy = false } }` workflow.

## Gotchas
- `prevent_destroy` does not stop removal of the whole resource block from config
  (ran on 1.17.0: the plan simply destroyed it); it only blocks planned destroys
  of configured resources.
- OpenTofu 1.13.2 accepts a static variable in `prevent_destroy` (see above) but still needs a static list for `ignore_changes`.

## Verify
- [ ] No variable references inside any `lifecycle` block (`terraform validate` passes).
- [ ] Callers have a documented way to get protection for critical resources.

## Checked
- Terraform 1.17.0 and OpenTofu 1.13.2 with `terraform_data`: variable in `prevent_destroy` and `ignore_changes` rejected (Terraform) / partly accepted (OpenTofu); the `protected`/`unprotected` count pair with `one(concat(...))` applied; toggling failed on `prevent_destroy`; the `moved` block between them worked; removing the resource block destroyed it despite `prevent_destroy`.
- Gated: provider-side `deletion_protection` arguments (no cloud provider here).
