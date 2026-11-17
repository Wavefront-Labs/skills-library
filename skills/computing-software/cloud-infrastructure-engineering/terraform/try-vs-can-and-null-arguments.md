---
id: computing-software.cloud-infrastructure-engineering.terraform.try-vs-can-and-null-arguments
name: try-vs-can-and-null-arguments
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, try-vs-can, try-function, can-function, null-argument, null-attribute, error-masking]
level: practitioner
status: verified
description: "Pick try() vs can() correctly, avoid masking real errors, and use null to omit optional arguments so the provider default applies."
sources: ["https://developer.hashicorp.com/terraform/language/functions/try", "https://developer.hashicorp.com/terraform/language/functions/can", "https://developer.hashicorp.com/terraform/language/expressions/types#null"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `try` vs `can`, and `null` arguments

## try
Returns the first argument that evaluates without error:
```hcl
locals {
  port     = try(var.settings.port, 8080)                 # optional attribute in an any-typed input
  first_az = try(data.aws_availability_zones.this.names[0], null)
}
```

## can
Returns `true`/`false` for "does this evaluate without error" — for **conditions**:
```hcl
validation {
  condition     = can(cidrhost(var.cidr, 0))
  error_message = "cidr must be a valid CIDR block."
}
```

## Choosing
| Situation | Use |
|---|---|
| Need a value with a fallback | `try(expr, fallback)` |
| Need a boolean test (validation, ternary condition) | `can(expr)` |
| Attribute may be missing on a typed object | fix the type with `optional()` instead |
| Index may be out of range | `try(list[0], null)` or `one(list)` / `length(list) > 0 ? ... : ...` |

## Error masking
`try`/`can` only catch errors in **dynamic** evaluation (missing attribute, index,
conversion). They do **not** hide references to undeclared variables/resources —
those are static errors. But they do hide typos in attribute names:
`try(var.settings.prot, 8080)` silently returns 8080 forever. Keep `try` expressions
short, and prefer typed inputs with `optional(T, default)` so typos error.

`try` with unknown values: if the first expression is unknown, the result is unknown
(not the fallback): `try(terraform_data.a.id, "fb")` plans as `(known after apply)`.

## null to omit arguments
Setting an argument to `null` is the same as not setting it, so the provider default applies:
```hcl
resource "aws_db_instance" "this" {
  kms_key_id            = var.kms_key_id            # null -> argument omitted
  backup_window         = var.env == "prod" ? "03:00-04:00" : null
  max_allocated_storage = var.autoscale ? 1000 : null
}
```
Cleaner than duplicating resources or dynamic blocks for scalar arguments.

## Gotchas
- `null` in a mandatory argument errors, because Terraform treats null as if the argument were omitted (language docs).
- Nested blocks cannot be nulled this way — use a 0/1 dynamic block.
- In module calls, passing `null` to a variable with a default yields null unless the
  variable is `nullable = false`.
- `coalesce(var.a, "x")` skips both `null` and empty strings; `try(var.a, "x")` returns
  `""` or `null` unchanged because neither is an error.

## Verify
- [ ] Misspell an attribute inside a `try`: confirm you would notice (a test or validation fails) — or remove that `try`.
- [ ] Plan with `kms_key_id = null` shows the argument absent / provider default.
