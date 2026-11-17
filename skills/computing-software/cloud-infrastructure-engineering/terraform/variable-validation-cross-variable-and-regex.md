---
id: computing-software.cloud-infrastructure-engineering.terraform.variable-validation-cross-variable-and-regex
name: variable-validation-cross-variable-and-regex
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, variable-validation, cross-variable-validation, validation-regex, can-regex, input-validation]
level: practitioner
status: verified
description: "Write variable validation blocks: regex with can(regex()), list/map element checks with alltrue, and validations referencing other variables (Terraform 1.9+)."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#custom-validation-rules", "https://developer.hashicorp.com/terraform/language/functions/regex", "https://developer.hashicorp.com/terraform/language/functions/can"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variable validation: regex and cross-variable rules

## Regex patterns
```hcl
variable "bucket_name" {
  type = string
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "bucket_name must be 3-63 chars of a-z, 0-9, '.', '-', starting and ending alphanumeric."
  }
}
```
- `regex()` **errors** when nothing matches; wrap in `can()` to get a bool.
- RE2 syntax: no look-ahead/back-references. Anchor with `^...$`.
- `startswith`/`endswith` (1.3+) and `strcontains` (1.5+) are clearer for simple cases.

## Collections
```hcl
variable "cidrs" {
  type = list(string)
  validation {
    condition     = alltrue([for c in var.cidrs : can(cidrhost(c, 0))])
    error_message = "Every entry in cidrs must be a valid CIDR block."
  }
}
variable "tags" {
  type = map(string)
  validation {
    condition     = contains(keys(var.tags), "owner")
    error_message = "tags must include an owner key."
  }
}
```
Multiple `validation` blocks are allowed; each reports its own message.

## Cross-variable (Terraform 1.9+, OpenTofu 1.9+)
```hcl
variable "min_size" { type = number }
variable "max_size" {
  type = number
  validation {
    condition     = var.max_size >= var.min_size
    error_message = "max_size (${var.max_size}) must be >= min_size (${var.min_size})."
  }
}
variable "env" { type = string }
variable "instance_type" {
  type = string
  validation {
    condition     = var.env != "prod" || !startswith(var.instance_type, "t3.")
    error_message = "Burstable t3 instances are not allowed in prod."
  }
}
```
Before 1.9 (OpenTofu: before 1.9.0, per its changelog) a condition could only reference its own variable; older codebases put
these checks in `precondition` blocks or a `terraform_data` with lifecycle preconditions.

## Gotchas
- Null inputs: `can(regex(..., null))` is false, but `length(null)` errors ("argument must not be null"). Guard
  with `var.x == null || length(var.x) > 2` for nullable variables: that works on 1.16.6 (`||` short-circuits since 1.12) but still errors on 1.9.8, where you need `var.x == null ? true : length(var.x) > 2`.
- Validation runs at plan; values unknown at plan (from resources, in modules) are
  skipped until known.
- Error messages should state the rule and the bad value, ending with a full stop.

## Verify
- [ ] `terraform plan -var bucket_name=Bad_Name` fails with your message (checked: `Error: Invalid value for variable` followed by the message).
- [ ] Valid inputs plan cleanly; test with `terraform test` `expect_failures = [var.bucket_name]`.
