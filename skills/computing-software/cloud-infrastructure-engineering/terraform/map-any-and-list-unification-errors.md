---
id: computing-software.cloud-infrastructure-engineering.terraform.map-any-and-list-unification-errors
name: map-any-and-list-unification-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, map-any, type-unification, any-type, type-constraints, complex-types]
level: practitioner
status: verified
description: "Fix unification failures with map(any) and list(any): why mixed-shape values break, what Terraform converts silently, and when to use object types or plain any."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/type-constraints#dynamic-types-the-any-constraint", "https://developer.hashicorp.com/terraform/language/expressions/type-constraints#conversion-of-complex-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `map(any)` / `list(any)` unification

`any` inside a collection does **not** mean "anything per element". Terraform picks
**one** concrete element type that all elements can convert to.

## Failure
```hcl
variable "services" { type = map(any) }
# services = {
#   api    = { port = 80, public = true }
#   worker = { port = 0 }
# }
```
```
Error: Invalid value for input variable
The given value is not suitable for var.services: all map elements must have the same type.
```
(For a default value the same check reports `Invalid default value for variable ... all map elements must have the same type`.)
`api` and `worker` are objects with different attributes; no single object type fits.

## Silent conversions (the other surprise)
```hcl
variable "tags" { type = map(any) }
# tags = { a = "x", b = 1, c = true }   -> map(string): b = "1", c = "true"
```
Primitive mixes convert to string without error, which can break later `== 1` checks.

## Fixes
1. **Exact object type with optionals** (best for module inputs):
```hcl
variable "services" {
  type = map(object({
    port   = number
    public = optional(bool, false)
  }))
}
```
2. **Plain `any`** (no collection wrapper) keeps heterogeneous structure as an
   object/tuple; you lose validation and need `try()` everywhere.
3. Normalise inputs so all elements have the same attributes (explicit `null`s).

## Conditionals and lists hit it too
```hcl
local.x = var.flag ? [1, 2] : ["a"]       # unified to list(string): ["1", "2"]
local.y = var.flag ? { a = 1 } : {}       # unifies to map(number); no error on 1.9.8 or 1.16.6
```
The conditional errors only when the branches cannot unify (for example `{ a = 1, b = [1] }` vs
`{ a = 1 }`, or an object vs a string): return the same shape in both branches or
build the optional part with `merge()`. Plain `list(any)` with `[1, "a"]` becomes `list(string)`.

## Verify
- [ ] `type(var.services)` in console shows the intended type for every tfvars file.
- [ ] No module input uses `map(any)` for structured objects.
