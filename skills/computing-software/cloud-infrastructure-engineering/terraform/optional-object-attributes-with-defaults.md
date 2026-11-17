---
id: computing-software.cloud-infrastructure-engineering.terraform.optional-object-attributes-with-defaults
name: optional-object-attributes-with-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, optional-default, nested-defaults, optional-attributes, type-constraints, module-inputs]
level: practitioner
status: verified
description: "Declare object inputs with optional(type, default), including nested objects and maps of objects, and understand how and when defaults are applied."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/type-constraints#optional-object-type-attributes", "https://opentofu.org/docs/language/expressions/type-constraints/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `optional()` attributes with defaults (Terraform 1.3+)

## Basics
```hcl
variable "bucket" {
  type = object({
    name          = string
    versioning    = optional(bool, true)
    force_destroy = optional(bool, false)
    lifecycle_days = optional(number)        # default null
  })
}
```
Caller passes `{ name = "logs" }` → `versioning = true`, `force_destroy = false`,
`lifecycle_days = null`.

## Nested defaults
Defaults apply recursively, but only to objects that are **present**:
```hcl
variable "service" {
  type = object({
    name = string
    health_check = optional(object({
      path     = optional(string, "/healthz")
      interval = optional(number, 30)
    }), {})                                 # default {} -> inner defaults then apply
  })
}
```
- `optional(object({...}), {})` → omitted `health_check` becomes `{path="/healthz", interval=30}`.
- `optional(object({...}))` (no default) → omitted `health_check` is `null`; inner
  defaults are **not** applied to null.

## Maps of objects
```hcl
variable "queues" {
  type = map(object({
    fifo       = optional(bool, false)
    visibility = optional(number, 30)
    dlq        = optional(object({ max_receive = optional(number, 5) }))
  }))
  default = {}
}
```
Each map element gets defaults independently — the standard shape for `for_each`.

## When defaults are applied
At the module boundary, when the value is converted to the variable's type. They do
not apply to `locals` or to values you construct inside the module — define a typed
variable if you need defaulting.

## Gotchas
- The default must convert to the attribute type. A string default for a number attribute such as `optional(number, "30")` is accepted and converted to `30` (tested on 1.9.8), but keep types exact so the intent is clear.
- Defaults are visible in `terraform console` via `var.x`, which is how to debug them.
- Requires Terraform ≥ 1.3, where optional attributes with defaults were introduced (1.3 changelog); set `required_version`.
- Callers passing `null` for an optional attribute get the default.

## Checked
Run with Terraform 1.9.8 on 2026-10-18 in a scratch configuration (outputs only, no provider): omitted attributes took their defaults (`versioning=true`, `force_destroy=false`, `lifecycle_days=null`); an omitted `optional(object({...}), {})` produced the inner defaults while `optional(object({...}))` without a default gave `null`; each map element got defaults independently (`dlq={}` produced `max_receive=5`); passing `a=null` gave the default; `terraform console -var ...` printed `var.service.health_check.path` as `"/healthz"`; defaults were not applied to a `locals` object. The Terraform 1.3 changelog introduces optional attributes with defaults.

## Verify
- [ ] `terraform console -var 'service={name="api"}'` → `var.service.health_check.path` = `/healthz`.
- [ ] `terraform test` covers omitted, partial and full inputs.
