---
id: computing-software.cloud-infrastructure-engineering.terraform.inconsistent-conditional-result-types
name: inconsistent-conditional-result-types
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, conditional-types, type-mismatch, conditional-expression, inconsistent-conditional-result-types]
level: advanced
status: verified
description: "Fix 'Inconsistent conditional result types' when ternary branches are objects/tuples of different shapes, using tomap/tolist, typed locals, null, or merge."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/conditionals", "https://developer.hashicorp.com/terraform/language/expressions/type-constraints#conversion-of-complex-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inconsistent conditional result types

## The error
```
Error: Inconsistent conditional result types
  The true and false result expressions must have consistent types. The 'true'
  value includes object attribute "b", which is absent in the 'false' value.
```
Both branches of `cond ? a : b` must convert to a single type. Literal objects and
tuples have per-element types. Terraform first tries to unify the two branch types
(for example two objects whose attribute values share one type become a `map`), so many
mismatched literals are accepted. The error appears only when no common type exists
(checked on Terraform 1.9.8 and 1.16.6, same behaviour):
```hcl
var.f ? { a = 1 } : { b = 2 }                 # OK: result is tomap({ a = 1 }) when true
var.f ? { a = 1, b = [1] } : { a = 1 }        # error: 'true' value includes attribute "b"
var.f ? { a = { b = 1 } } : { a = { c = [1] } }  # error: type mismatch for attribute "a"
var.f ? [{ a = 1 }] : [{ b = [2] }]           # error: type mismatch for tuple element 0
var.f ? [1] : { a = 1 }                       # error: 'true' value is tuple, 'false' is object
var.f ? [{ a = 1 }] : []                      # OK: tolist([...])
var.f ? { a = 1 } : null                      # OK
var.f ? [1, 2] : ["a"]                        # OK: unified to list(string), so ["1", "2"]
```
A side effect of unification: the result may be a map or list rather than the object or
tuple you wrote, with numbers turned into strings when the other branch holds strings.

## Fixes by case
**Objects with different attributes of different types: give both branches the same attributes**
```hcl
# error: 'true' includes "b", absent in 'false'
cfg = var.prod ? { a = 1, b = [1] } : { a = 1 }
# good: same attributes, null or empty for the unused one
cfg = var.prod ? { a = 1, b = [1] } : { a = 1, b = null }
# good: add the optional part with merge()
cfg = merge({ a = 1 }, var.prod ? { b = [1] } : {})
```
`var.prod ? { a = 1, b = [1] } : {}` still errors (the empty object lacks `a`), so use the
`merge` form instead.

**Tags: all-string values unify on their own, so no `tomap` is needed**
```hcl
tags = var.prod ? { env = "prod", tier = "1" } : { env = "dev" }   # OK, map(string)
tags = merge({ env = var.prod ? "prod" : "dev" }, var.prod ? { tier = "1" } : {})
```

**List of objects vs empty list**
```hcl
rules = var.enabled ? [{ port = 443, cidr = "0.0.0.0/0" }] : []   # OK, becomes list(object)
rules = var.enabled ? tolist([{ port = 443 }]) : tolist([])        # explicit form
```
Objects inside a list that differ in attributes or attribute types still error (see above).

**Nested objects: give both branches the same attributes**
```hcl
config = {
  logging = var.prod ? { level = "warn", sink = "s3" } : { level = "debug", sink = null }
}
```
This form is accepted; unused attributes carry `null`.

**Use a typed local or variable**
Declare the shape once:
```hcl
variable "overrides" {
  type    = object({ size = optional(string), replicas = optional(number) })
  default = {}
}
```
Then branches are converted to that type.

**Avoid the conditional**: a lookup table keyed by environment
(`local.settings[var.env]`) with uniformly shaped entries.

## Diagnosing
`terraform console` → `type(<true branch>)` and `type(<false branch>)` show the mismatch.

## Verify
- [ ] `terraform validate` passes for both values of the condition (test both via tfvars).
- [ ] `type()` of the result is the collection/object type you intended.
