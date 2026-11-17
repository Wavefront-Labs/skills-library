---
id: computing-software.cloud-infrastructure-engineering.terraform.for-expressions-with-if-filters-and-grouping
name: for-expressions-with-if-filters-and-grouping
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, for-if-filter, grouping-mode, for-expression, expressions]
level: practitioner
status: verified
description: "Write for expressions that filter with if, build maps vs lists, group values with the ... operator, and avoid duplicate key and ordering surprises."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/for"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for expressions: filters and grouping

## Shapes
```hcl
[for s in var.subnets : s.cidr]                       # list (tuple)
{for s in var.subnets : s.name => s.cidr}             # map (object)
[for k, v in var.map : "${k}=${v}"]                   # iterate map: key, value
[for i, s in var.list : "${i}:${s}"]                  # iterate list: index, value
```

## Filtering with `if`
```hcl
public_subnets = {for s in var.subnets : s.name => s if s.public}
non_empty      = [for x in var.items : x if x != null && x != ""]
prod_only      = {for k, v in var.envs : k => v if contains(["prod", "staging"], k)}
```
`if` is evaluated per element; elements failing it are dropped (not set to null).

## Grouping mode (`...`)
When several elements produce the same key, a plain map errors:
```
Error: Duplicate object key "eu-west-1a"
```
Add `...` after the value to collect them into lists:
```hcl
subnets_by_az = {for s in var.subnets : s.az => s.id...}
# { "eu-west-1a" = ["subnet-1", "subnet-3"], "eu-west-1b" = ["subnet-2"] }
```

## Ordering
- Iterating a map or object goes in lexical key order (`[for k, v in {b=1,a=2,c=3} : k]` is `[a, b, c]`).
- Iterating a set of strings goes in lexical order; for sets of other types the
  for-expression docs say the order is arbitrary and may change in future versions
  (on 1.9.8 and 1.16.6 small sets of numbers and bools came out sorted, which you should not rely on).
- Lists keep their order. If order matters for the result (block order, priority),
  iterate a list, or `sort()` keys explicitly.

## Common recipes
```hcl
# invert a map
{for k, v in var.m : v => k}
# map of lists -> flat list of pairs for for_each
flatten([for svc, ports in var.ports : [for p in ports : { svc = svc, port = p }]])
# index a list of objects by a field
{for u in var.users : u.email => u}
```

## Gotchas
- Result of `[for ...]` is a tuple; pass through `tolist()` if a module input needs `list(...)` and types differ.
- Filters on unknown values make the whole result unknown at plan time; avoid
  filtering on resource attributes when feeding `for_each`.

## Verify
- [ ] `terraform console` shows the expected shape (`type(...)`).
