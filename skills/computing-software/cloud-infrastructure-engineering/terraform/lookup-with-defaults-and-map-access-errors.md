---
id: computing-software.cloud-infrastructure-engineering.terraform.lookup-with-defaults-and-map-access-errors
name: lookup-with-defaults-and-map-access-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, lookup-default, lookup-function, conditionals, try, map-access]
level: practitioner
status: verified
description: "Access maps safely: lookup with defaults, index syntax errors for missing keys, try() for nested objects, and when a missing key should fail instead of defaulting."
sources: ["https://developer.hashicorp.com/terraform/language/functions/lookup", "https://developer.hashicorp.com/terraform/language/functions/try", "https://developer.hashicorp.com/terraform/language/expressions/references"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `lookup` and map access

## Index syntax fails on missing keys
```hcl
var.instance_types[var.env]
# Error: Invalid index - The given key does not identify an element in this collection value.
```
Good when a missing key is a bug.

## `lookup(map, key, default)`
```hcl
instance_type = lookup(var.instance_types, var.env, "t3.small")
```
- Always pass the default: omitting it is deprecated since v0.7 (function docs) and just
  equals `map[key]`, failing on a missing key (`the given object has no attribute "x"`).
- Works on maps and objects (object attribute lookup by string).
- Against a real `map(string)` the default must convert to the element type: `lookup(tomap({a="x"}), "b", 5)` gives `"5"` and `lookup(tomap({a="x"}), "b", [1])` is an error ("the default value must have the same type as the map elements"). Against an object-typed value (most `{...}` literals and `any` variables) any default is returned as is.

## Nested access: `try()`
`lookup` is one level. For nested optional structures:
```hcl
retention = try(var.config.logging.retention_days, 30)
```
`try` catches missing attributes, missing keys, null traversal and type errors in the
expression. It returns the first argument that evaluates without error.

## Choosing
| Situation | Use |
|---|---|
| Key must exist | `var.m[k]` (fail loudly) |
| Key optional, flat map | `lookup(var.m, k, default)` |
| Deep optional path | `try(a.b.c, default)` |
| Many optional fields of an object variable | `optional(type, default)` in the type constraint |

## Validate keys up front
```hcl
variable "env" {
  type = string
  validation {
    condition     = contains(keys(local.sizes), var.env)
    error_message = "env must be one of: ${join(", ", keys(local.sizes))}."
  }
}
```
Validation cannot reference locals before Terraform 1.9 (the 1.9 release notes: rules "can refer to other objects"); use a literal list there. The example above fails correctly on 1.9.8 and 1.16.6 with `env must be one of: dev, prod.`

## Gotchas
- `lookup` on an unknown map value returns unknown (plans as `(known after apply)`); fine for plans.
- `try` hides typos: `try(var.config.loging.retention_days, 30)` silently returns 30.
  Prefer typed variables with `optional()` so typos are errors.

## Verify
- [ ] Missing keys for required settings fail with a clear message.
