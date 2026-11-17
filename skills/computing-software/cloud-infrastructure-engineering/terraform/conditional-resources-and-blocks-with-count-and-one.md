---
id: computing-software.cloud-infrastructure-engineering.terraform.conditional-resources-and-blocks-with-count-and-one
name: conditional-resources-and-blocks-with-count-and-one
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, conditional-count, count-ternary, one-function, optional-block, conditional-block, dynamic-block, feature-flags]
level: practitioner
status: verified
description: "Toggle resources with count = cond ? 1 : 0, reference them safely with one() and splats, and make single nested blocks optional with 0/1-element dynamic blocks."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/count", "https://developer.hashicorp.com/terraform/language/functions/one", "https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional resources and optional blocks

## Toggle a resource
```hcl
resource "aws_eip" "nat" {
  count  = var.enable_nat ? 1 : 0
  domain = "vpc"
}
```
Condition must be known at plan (from variables/locals, not created resources); a
condition on an apply-time attribute fails with `Invalid count argument` ("depends on
resource attributes that cannot be determined until apply").

## Reference it safely
```hcl
locals {
  nat_ip = one(aws_eip.nat[*].public_ip)     # value or null
}
output "nat_ip" { value = local.nat_ip }
```
- `one(list)` returns the single element, `null` for empty, errors on >1 — exactly
  the semantics of a 0/1 resource. (Terraform 0.15+.)
- Avoid `aws_eip.nat[0].public_ip` outside a guarding conditional: it errors when count
  is 0 (`Invalid index ... random_id.nat is empty tuple` in the local test).
- Older idiom: `try(aws_eip.nat[0].public_ip, null)` — works but hides typos.

## Optional nested block
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    id     = "expire"
    status = "Enabled"
    dynamic "noncurrent_version_expiration" {
      for_each = var.noncurrent_days == null ? [] : [var.noncurrent_days]
      content {
        noncurrent_days = noncurrent_version_expiration.value
      }
    }
  }
}
```
`[] / [x]` gives zero or one block. Using an object variable:
`for_each = var.logging != null ? [var.logging] : []` then `logging.value.bucket`.

## count vs for_each for toggles
`count` reads well for a single boolean toggle. For "toggle plus a name", use
`for_each = var.enabled ? toset(["main"]) : toset([])` so the address
(`["main"]`) does not change if you later add more.

## Gotchas
- Flipping the toggle destroys the resource — expected, but make sure reviewers see it.
- `count` and `for_each` cannot both be set; toggling a `for_each` resource uses a
  filtered map: `{ for k, v in var.x : k => v if v.enabled }`.
- Adding count to an existing resource: address `x` becomes `x[0]` automatically (plan
  shows `x has moved to x[0]`, no moved block needed). This does **not** hold for module
  calls: adding `count = 1` to `module "db"` plans destroy of `module.db...` and create of
  `module.db[0]...` until you add `moved { from = module.db  to = module.db[0] }`.

## Verify
- [ ] Plan with the flag off shows no resource and no error; a `null` output is simply absent
  from `terraform output` (`Warning: No outputs found`), and flipping the flag off later
  plans `nat_ip = "..." -> null`.
- [ ] Plan with the optional block value null omits the block entirely.

## Checked
- Terraform 1.17.0 with random, tls and `terraform_data`: `count = var.enable_nat ? 1 : 0` plus `one(random_id.nat[*].hex)` returned `null` with the flag off and the value with it on; `one([1,2])` failed with `must be a list, set, or tuple value with either zero or one elements` and `one([])` gave `null`; `try(x[0].y, null)` also gave `null`; `random_id.nat[0].hex` with count 0 failed with `Invalid index`; a count depending on an apply-time attribute failed with `Invalid count argument`; `dynamic "subject"` on `tls_cert_request` with `[]` / `[var.subj]` produced no block / one block (`subject { # forces replacement` appeared on the flip); `for_each = var.enabled ? toset(["main"]) : toset([])` created `terraform_data.tog["main"]`; `count` plus `for_each` failed with `Invalid combination of "count" and "for_each"`; adding `count` to a resource gave `has moved to x[0]` automatically and to a module call did not (moved block fixed it).
- AWS names (`aws_eip.domain`, `public_ip`, `aws_s3_bucket_lifecycle_configuration` `rule` `id`/`status`/`noncurrent_version_expiration`/`noncurrent_days`) were checked in the provider docs source; `one` arrived in Terraform 0.15 (0.15 changelog).
