---
id: computing-software.cloud-infrastructure-engineering.terraform.alltrue-and-anytrue-in-conditions
name: alltrue-and-anytrue-in-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, alltrue, anytrue, variable-validation, preconditions, for-expression]
level: practitioner
status: verified
description: "Validate every element of a list or map with alltrue and anytrue over for expressions, in variable validation, preconditions and check blocks, with readable error messages."
sources: ["https://developer.hashicorp.com/terraform/language/functions/alltrue", "https://developer.hashicorp.com/terraform/language/functions/anytrue", "https://developer.hashicorp.com/terraform/language/values/variables#custom-validation-rules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `alltrue` / `anytrue`

```hcl
alltrue([true, true])          # true; alltrue([]) is true
anytrue([false, true])         # true; anytrue([]) is false
```
Elements may be bools or strings `"true"`/`"false"` (`alltrue(["true", true])` is true).

## Validate each element
```hcl
variable "subnets" {
  type = list(object({ name = string, cidr = string }))
  validation {
    condition     = alltrue([for s in var.subnets : can(cidrhost(s.cidr, 0))])
    error_message = "Every subnet cidr must be a valid CIDR block."
  }
  validation {
    condition     = alltrue([for s in var.subnets : can(regex("^[a-z0-9-]{3,32}$", s.name))])
    error_message = "Subnet names must be 3-32 chars of lowercase letters, digits and hyphens."
  }
}
```
Use several validation blocks rather than one giant condition: each gets its own
message.

## anytrue examples
```hcl
# at least one public subnet
condition = anytrue([for s in var.subnets : s.public])
# a tag map contains any forbidden key
condition = !anytrue([for k in keys(var.tags) : startswith(lower(k), "aws:")])
```

## Naming the offenders in the message
Error messages can interpolate the variable being validated:
```hcl
error_message = "Invalid CIDRs: ${join(", ", [for s in var.subnets : s.cidr if !can(cidrhost(s.cidr, 0))])}."
```
(sensitive variables are redacted in messages.)

## Empty collections
`alltrue([])` is true, so an empty list passes. Add `length(var.subnets) > 0 &&`
when empty is invalid.

## Gotchas
- A null element does not raise an error on 1.9.8: `alltrue([var.n, true])` with `n = null` returned `false` (the docs do not specify null handling), so filter nulls or `coalesce(x, false)` rather than rely on it.
- Not short-circuiting over elements: every element's expression is evaluated, so
  guard against errors per element with `can()`.

## Verify
- [ ] Invalid inputs fail plan with a message naming the bad elements; empty input handled deliberately.
