---
id: computing-software.cloud-infrastructure-engineering.terraform.nullable-and-object-variable-defaults
name: nullable-and-object-variable-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, nullable, nullable-false, variable-defaults, default-object, module-inputs]
level: practitioner
status: verified
description: "Control null handling with nullable = false and design defaults for object/map variables so callers can pass null or partial objects without breaking modules."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#disallowing-null-input-values", "https://developer.hashicorp.com/terraform/language/expressions/type-constraints#optional-object-type-attributes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `nullable` and defaults for object variables

## nullable
```hcl
variable "retention_days" {
  type     = number
  default  = 30
  nullable = false
}
```
- Default `nullable = true`: a caller passing `retention_days = null` gets **null**,
  not the default — the default applies only when the argument is omitted (run: a
  child module's `keep` output was `null` when the wrapper forwarded a null).
- `nullable = false`: passing null is treated as "use the default" (if one exists),
  or an error if the variable is required. This makes module wrappers that forward
  `var.x` (possibly null) safe.

The wrapper pattern this fixes:
```hcl
module "bucket" {
  source         = "./bucket"
  retention_days = var.retention_days   # wrapper's var may be null
}
```

## Defaults for objects
Whole-object default (all or nothing):
```hcl
variable "logging" {
  type = object({
    enabled = bool
    bucket  = string
  })
  default = { enabled = false, bucket = "" }
}
```
A caller setting `logging_old = { enabled = true }` fails: `attribute "bucket" is required` (ran).
Per-attribute defaults with `optional()` fix that:
```hcl
variable "logging" {
  type = object({
    enabled = optional(bool, false)
    bucket  = optional(string)
    prefix  = optional(string, "logs/")
  })
  default  = {}
  nullable = false
}
```
Now `{}` , `{ enabled = true, bucket = "x" }` and `null` all work (`{}` and `null` both gave
`{bucket=null, enabled=false, prefix="logs/"}`).

## Maps of objects
`map(object({...optional...}))` applies the optional defaults to **each** element —
the standard shape for `for_each`-driven module inputs.

## Gotchas
- `default = null` with `nullable = false` is an error (`A null default value is not valid when nullable=false`).
- A variable with `sensitive = true` makes an output that uses it fail unless the output is marked sensitive (`Output refers to sensitive values`).
- Changing a default is a behaviour change for every caller relying on it — note it in the CHANGELOG.

## Verify
- [ ] `terraform console` with `-var 'logging={}'` → `var.logging.prefix` returns `"logs/"`.
- [ ] Passing `null` for a `nullable = false` variable yields the default.

## Checked
- Terraform 1.17.0: a root wrapper forwarding a null into a child module's `nullable = false` variable (got the default 30) and a default-nullable variable (got null); `optional()` object defaults with `{}`, a full object and `-var 'logging=null'`; the all-or-nothing object error (`attribute "bucket" is required`); `map(object({optional...}))` defaults applied to each element; the `nullable = false` + `default = null` error; a sensitive variable in an unmarked output error.
