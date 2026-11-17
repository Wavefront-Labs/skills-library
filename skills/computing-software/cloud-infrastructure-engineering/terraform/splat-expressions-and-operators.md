---
id: computing-software.cloud-infrastructure-engineering.terraform.splat-expressions-and-operators
name: splat-expressions-and-operators
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, splat-expression, full-splat, operators, operator-precedence, interpolation, expressions]
level: practitioner
status: verified
description: "Use splat expressions ([*]) on lists and single values, convert for_each maps with values(), and apply arithmetic, comparison and logical operators with correct precedence."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/splat", "https://developer.hashicorp.com/terraform/language/expressions/operators", "https://developer.hashicorp.com/terraform/language/expressions/strings#interpolation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splat expressions and operators

## Splat
```hcl
aws_instance.web[*].id                   # count resource -> list of ids
var.users[*].name                        # list of objects -> list of names
values(aws_subnet.private)[*].id         # for_each resource is a MAP: splat needs a list
[for s in aws_subnet.private : s.id]     # equivalent, clearer
```
- `[*]` (full splat) vs legacy `.*` (attribute-only splat): `[*]` also applies to
  following index operations; prefer `[*]`.
- Splat on a **single non-list value** wraps it into a one-element list, and on
  `null` returns `[]` — handy with optional blocks: `one(var.logging[*].bucket)`.
- Splat on a map does not iterate it: `{x = {id = 1}}[*].id` fails with `Unsupported attribute` because the map is treated as one value; use `values()` or `for`.

## Operators
| Precedence (high → low) | Operators |
|---|---|
| 1 | `!`, unary `-` |
| 2 | `*`, `/`, `%` |
| 3 | `+`, `-` |
| 4 | `>`, `>=`, `<`, `<=` |
| 5 | `==`, `!=` |
| 6 | `&&` |
| 7 | `||` |
| 8 | `cond ? a : b` |
Use parentheses whenever mixing `&&` and `||`.

- `==` compares type **and** value: `1 == "1"` is false; `[] == []` true for same types,
  but `tolist([]) == []` can be false (list vs tuple) — compare `length(x) == 0` instead.
- `/` is floating point: `5 / 2` = 2.5; use `floor()`.
- `%` modulo is integer remainder.
- `&&`/`||` short-circuit since Terraform 1.12 (changelog); on 1.9.8 both sides are evaluated,
  so `var.x != null && var.x.enabled` errors on null ("Attempt to get attribute from null value"); on 1.16.6 it returns false. For older versions use `try(var.x.enabled, false)`.

## Interpolation
`"${var.a}-${var.b}"`; a string that is only one interpolation `"${var.list}"` returns
the original value type in modern Terraform, but write `var.list` directly. Escape with `$${`.

## Verify
- [ ] `terraform console`: `values(aws_subnet.private)[*].id` returns the id list (with a stand-in map, `values({x={id=1},y={id=2}})[*].id` gives `[1, 2]`).
- [ ] Conditions combining `&&`/`||` are parenthesised (`grep -nE "&&.*\|\||\|\|.*&&"` reviewed).
