---
id: computing-software.cloud-infrastructure-engineering.terraform.object-typed-module-inputs
name: object-typed-module-inputs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, module-input-objects, module-inputs-objects, module-design, type-constraints, optional-attributes]
level: advanced
status: gated
description: "Decide between many scalar variables and grouped object inputs for a module, design object shapes with optional defaults and validation, and keep them evolvable."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/composition", "https://developer.hashicorp.com/terraform/language/expressions/type-constraints#optional-object-type-attributes", "https://developer.hashicorp.com/terraform/language/values/variables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object-typed module inputs

## Scalars vs objects
| Many scalar variables | Grouped objects |
|---|---|
| `db_engine`, `db_version`, `db_size`, `db_backup_days`... | `database = object({...})` |
| Easy to document individually | Groups related settings; one place to pass through wrappers |
| Callers can't pass the whole thing from a map | Callers can build it from a `for_each` map |
Rule of thumb: an object when the attributes only make sense together or vary per
instance (`for_each` over a map of objects); scalars for top-level, independent knobs
(`name`, `tags`, `vpc_id`).

## Shape
```hcl
variable "database" {
  description = "Database settings. Omit to use defaults."
  type = object({
    engine         = optional(string, "postgres")
    engine_version = optional(string, "16")
    instance_class = optional(string, "db.t4g.medium")
    backup_days    = optional(number, 7)
    multi_az       = optional(bool, false)
  })
  default  = {}
  nullable = false

  validation {
    condition     = contains(["postgres", "mysql"], var.database.engine)
    error_message = "database.engine must be postgres or mysql."
  }
}
```
- Every attribute `optional()` with a sensible default unless truly required.
- Validate attributes (one `validation` per rule; messages name the full path).
- Document each attribute in `description` (terraform-docs renders it as one blob — keep it tidy) (gated: unconfirmed, source is paywalled or blocked).

## Evolving
- Adding an `optional` attribute is backward compatible.
- Adding a **required** attribute, renaming or retyping is breaking → major version.
- Don't use `any` for structured inputs; it disables type errors and defaults.

## Maps of objects for collections
```hcl
variable "buckets" {
  type = map(object({
    versioning = optional(bool, true)
    lifecycle  = optional(list(object({ prefix = string, days = number })), [])
  }))
}
```
Keys become `for_each` keys — stable addresses.

## Gotchas
- Large objects make error messages long; keep nesting ≤ 2 levels.
- Callers passing an object literal with an extra attribute: no error. Terraform 1.17.0 silently drops the extra key (ran with a module call, a `-var` value and a default), so a misspelled optional attribute falls back to its default; a missing required attribute fails (`Invalid value for input variable`). Add a `validation` over `keys(var.database)` if you need strictness.
- Default `{}` plus `nullable = false` makes the whole block optional (ran: omitting it, or passing `null`, gave the defaults).

## Verify
- [ ] An example tfvars with a typo'd *required* attribute fails at plan; for optional ones add the `keys()` validation, otherwise the typo is silent.
- [ ] README (terraform-docs) shows the object type and defaults (gated: unconfirmed, source is paywalled or blocked).

## Checked
- Terraform 1.17.0: the `database` object (optional defaults, `default = {}`, `nullable = false`, `contains` validation rejecting `oracle`), explicit nulls (defaults applied), extra keys (dropped), map-of-objects defaults; `optional()` without a default came out `null`. The 1.3 `optional` feature timing was not re-read.
- Gated: terraform-docs rendering (tool not installed).
