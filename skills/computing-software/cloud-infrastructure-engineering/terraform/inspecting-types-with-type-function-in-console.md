---
id: computing-software.cloud-infrastructure-engineering.terraform.inspecting-types-with-type-function-in-console
name: inspecting-types-with-type-function-in-console
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, type-function, console-type, terraform-console, type-inspection, object-vs-map, tuple-vs-list, type-errors, debugging-types]
level: practitioner
status: verified
description: "Use type() in terraform console to see the type Terraform inferred (object vs map, tuple vs list) and read the notation to fix inconsistent-conditional and conversion errors."
sources: ["https://developer.hashicorp.com/terraform/language/functions/type", "https://developer.hashicorp.com/terraform/cli/commands/console", "https://developer.hashicorp.com/terraform/language/expressions/type-constraints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting types with `type()` in console

**Goal:** stop guessing why Terraform says two values have different types;
ask it.

## 1. `type()` is console-only
```bash
$ terraform console
> type(var.subnets)
map(
    object({
        az: string,
        cidr: string,
    }),
)
> type([1, "a"])
tuple([
    number,
    string,
])
> type({a = 1})
object({
    a: number,
})
> type(toset(["a"]))
set(string)
> type(terraform_data.web)        # a resource with count, before apply
dynamic
```
`type()` cannot be used in configuration (`type(1)` in a local fails validation with `Call to unknown function`) — it exists for debugging in console.
Output (multi-line for complex types) is close to the type-constraint notation of
`variable { type = ... }`, but object attributes print as `name: type`; use `name = type` when
copying it into a variable declaration.

## 2. Reading the notation
| Literal you wrote | Inferred type | Why it matters |
|---|---|---|
| `["a","b"]` | `tuple([string, string])` | not `list(string)`; it converts to a list when needed (`tolist`, a `list(string)` variable) but `type()` shows the literal's own shape |
| `{a = 1, b = "x"}` | `object({a: number, b: string})` | not a map; conversion to `map(...)` succeeds only if the values can unify (number and string become strings; number and list do not) |
| `{}` | `object({})` | empty object, not empty map — `merge(var.map, {})` fine; `{} == tomap({})` is not |
| `[]` | `tuple([])` | `length([])` works; `[for ...]` always produces tuple/list |
| `null` | `dynamic` | type unknown until assigned |

## 3. Errors this solves
- **Inconsistent conditional result types**: `cond ? { a = 1, b = [1] } : { a = 1 }` fails
  because `type()` of the two branches is `object({a: number, b: tuple([number])})` vs
  `object({a: number})`. Plain `cond ? [] : ["a"]` is fine (both unify to a list). Fix:
  same attributes in both branches, or `merge()` (see the conditional-types skill).
- **`tomap`/`map(...)` conversion fails** ("cannot convert object to map of any single type"):
  `tomap({a=1, b=[1]})` mixes number and tuple values; check `type(local.x)`, then make values
  uniform or use an object constraint. Note `tomap({a=1, b="x"})` succeeds and turns the number
  into the string `"1"`.
- **Silent unification**: `toset([1, "1"])` gives `toset(["1"])` and `tolist([1, "1"])` gives
  `["1", "1"]`; Terraform converts numbers to strings rather than rejecting the mix.
- **`for_each` on a tuple** gives `Invalid for_each argument`: it needs a set of strings or a
  map; use `toset(...)`.

## 4. Companion checks
```
> can(tomap(local.x))        # would conversion succeed?
> try(tolist(var.y), null)
> type(module.vpc.private_subnets)   # confirm module output type before consuming
```

## Gotchas
- Console reads state; a resource not yet applied shows `dynamic` or unknown
  parts (`type(terraform_data.web)` printed `dynamic` before any apply).
- `type()` of a sensitive value works but the value stays hidden.
- OpenTofu documents a `type` function too (its docs describe it as returning the type of a value); check its docs for exact output.
- Terraform's `type()` output omits `optional(...)` markers from variable types —
  it shows the *value's* type, not the declared constraint.

## Verify
- [ ] `echo 'type(local.<x>)' | terraform console` prints the type; after changing `name: type` to `name = type` it is accepted in a `variable` block by `terraform validate`.
- [ ] The conditional/merge error disappears after the conversion `type()` suggested.
