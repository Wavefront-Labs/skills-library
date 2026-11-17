---
id: computing-software.cloud-infrastructure-engineering.terraform.reading-inconsistent-type-error-messages
name: reading-inconsistent-type-error-messages
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, type-error-messages, type-constraints, troubleshooting, conditional-types]
level: practitioner
status: verified
description: "Decode Terraform type errors: Inconsistent conditional result types, Incorrect attribute value type, Invalid function argument and Unsuitable value type, and fix them fast."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/type-constraints", "https://developer.hashicorp.com/terraform/language/expressions/conditionals#result-types", "https://developer.hashicorp.com/terraform/language/functions/type"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading type error messages

## `Inconsistent conditional result types`
```
The true and false result expressions must have consistent types. The 'true'
value includes object attribute "name", which is absent in the 'false' value.
```
Other variants seen on Terraform 1.17.0: `The 'true' value is tuple, but the 'false' value is object.`
(`cond ? ["a"] : {a=1}`) and `Type mismatch for object attribute "name": The 'true' value is string, but the 'false' value is tuple.`
Both branches must unify. Objects whose attributes are all convertible to one type do unify to a map
(`cond ? {name="x"} : {}` has type `map(string)`; `cond ? {a=1} : {b=2}` is `map(number)`), so the error appears only when the
attribute types cannot unify, e.g. `{name=["x"]}` against `{n="y"}`. Fix: same shape in both (`{ name = null }`), or wrap with
`tomap()`/`tolist()`, or move the condition inside attributes.

## `Incorrect attribute value type`
```
Inappropriate value for attribute "content": string required, but have tuple.
```
(`local_file.content = [{id="a"},{id="b"}]` on the local provider.) The message names the attribute and the
type needed versus the type you passed. Passing a string where a collection is needed, or a list of objects
instead of IDs: use `[x]`, `x[*].id`, `toset(...)`.

## `Invalid function argument`
```
Invalid value for "inputMap" parameter: argument must not be null.      # keys(null), lookup(null, "a")
Invalid value for "lists" parameter: element 0: string required, but have object.   # join(",", [{id="a"}])
```
The parameter name tells you which argument; "element N" points to the element. (`merge(null)` is accepted and returns `{}`.)

## `Invalid value for input variable` / `Invalid default value for variable`
For a declared type `map(object({ port = number }))` and the value `{ api = { port = "x" } }`:
- a bad `default` prints a path: `["api"].port: a number is required.`
- a bad `-var` prints `Unsuitable value for var.svc set using -var="svc=...": a number is required.` (no path)
- a bad `.tfvars` value prints `The given value is not suitable for var.svc declared at main.tf:5,1-15: a number is required.`
- a scalar given to `set(string)` prints `set of string required, but have string.`
Find the failing element by comparing the value to the type constraint (older versions printed
`element "api": attribute "port": ...`; the Terraform 1.17.0 output above does not).

## `Invalid template interpolation value`
```
Cannot include the given value in a string template: string required, but have tuple.
```
Interpolating a list/map into text (`"a${local.objs}"`): use `join(",", list)` or `jsonencode(obj)`. A string that is only
`"${x}"` (nothing else) returns `x` unchanged and raises no error.

## `Unsupported attribute` on a list
```
Can't access attributes on a list of objects. Did you mean to access attribute "id" for a specific element of the list, or across all elements of the list?
```
(Printed for a `list(object)` value such as `tolist(local.objs).id`; a tuple, such as a literal `[{id="a"}]`, prints `This value does not have any attributes.`)
Use `x[0].id`, `x[*].id` (returns `["a","b"]`), or for_each map `x["key"].id`.

## Debug technique
```bash
echo 'type(local.subnet_map)' | terraform console
echo 'type(var.flag ? local.a : local.b)' | terraform console   # map(string) for {name="x"} vs {}
```
`type()` shows the exact inferred type, revealing tuple vs list and object vs map.

## Verify
- [ ] `terraform validate`/`plan` pass, and `type()` of the fixed expression matches the expected constraint.

## Checked
- Terraform 1.17.0 with the local provider and `terraform console`: every error message above was reproduced and quoted from real output: the three `Inconsistent conditional result types` variants and the unification to `map(string)`/`map(number)`/`tomap({...})`; `Incorrect attribute value type` for `local_file.content = tuple`; `Invalid function argument` for `keys(null)`/`lookup(null,"a")` (`inputMap`) and `join` (`lists`, not `list`); `merge(null)` returned `{}`; `Invalid template interpolation value` only for `"a${...}"` with the single-`"${x}"` form unwrapping silently; both `Unsupported attribute` messages (list vs tuple); `[*].id` returned `["a","b"]`; `Invalid default value for variable` path form, `-var` form, `.tfvars` form and `set of string required, but have string`.
- `type()` in console printed `list(string)`, `tuple([string, number])`, `object({a: number, b: string})`, `map(number)`, matching the Debug section.
- The old `element "api": attribute "port"` path format did not appear on 1.17.0 and was replaced.
