---
id: computing-software.cloud-infrastructure-engineering.terraform.type-conversion-structural-and-any-types
name: type-conversion-structural-and-any-types
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, type-conversion, tolist, tomap, toset, structural-types, collection-types, any-type, type-constraints]
level: advanced
status: verified
description: "Understand structural (object/tuple) vs collection (list/map/set) types, automatic and explicit conversion (tolist/tomap/toset/tostring), and the any constraint."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/type-constraints", "https://developer.hashicorp.com/terraform/language/expressions/types#type-conversion", "https://developer.hashicorp.com/terraform/language/functions/tomap"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Types: structural vs collection, conversion, `any`

## The two families
| Collection (one element type) | Structural (per-element types) |
|---|---|
| `list(T)`, `set(T)`, `map(T)` | `tuple([T1, T2])`, `object({a=T1, b=T2})` |
Literals are structural: `["a", 1]` is a tuple, `{ a = 1, b = "x" }` an object.
They convert to collections automatically **when all elements can unify** to one type.

## Explicit conversion
```hcl
tolist(toset(var.x))             # dedupe, then back to list (sorted for strings)
toset(["b","a","b"])             # set("a","b")
tomap({ a = "1", b = 2 })        # map(string): 2 -> "2"
tostring(42); tonumber("42"); tobool("true")
```
Conversion fails when elements cannot unify: `tomap({ a = "x", b = ["y"] })` errors ("cannot convert object to map of any single type").

## Where it bites
- `for_each` needs a map or set of strings: an object literal works (converted), a
  tuple does not — wrap in `toset()`.
- Conditional branches must unify: `var.x ? [] : ["a"]` is fine; `var.x ? {} : { a = 1 }` is fine;
  `var.x ? {} : { a = { b = 1 } }` also unifies (to a map, `tomap({})` when x is true). The error appears
  only when the branches cannot unify, e.g. `var.x ? { a = 1, b = [1] } : { a = 1 }` or `var.x ? { x = 1 } : "s"`
  (see conditional-types skill).
- `merge()` of objects returns an object; downstream `map(string)` constraints convert it
  (if possible).

## any
```hcl
variable "settings" {
  type = any
}
```
- `any` means "infer the type from the value"; it is **not** dynamic per element.
  `list(any)` requires all elements to unify to one type.
- Use `any` for pass-through blobs (e.g. Helm values, JSON-ish configs) and validate
  shape with `can(var.settings.key)` or `try()`.
- Prefer precise `object({...optional...})` for module inputs: better errors, docs and defaults.

## Inspecting
`terraform console` → `type(local.x)` shows the inferred type (1.x).

## Gotchas
- Sets are unordered; converting to list sorts strings lexically — don't rely on input order.
- Numbers in maps from YAML become numbers; comparing with strings fails silently in `==` (`1 == "1"` is false).
- `tostring(null)` is null, not `"null"`.

## Verify
- [ ] `type()` in console matches the constraint you expected.
- [ ] Module inputs reject wrong shapes with a clear error (`terraform validate` with a test tfvars).
