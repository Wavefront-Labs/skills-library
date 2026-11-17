---
id: computing-software.cloud-infrastructure-engineering.terraform.set-types-ordering-and-indexing-errors
name: set-types-ordering-and-indexing-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, set-type, type-constraints, toset, for-each, collection-types]
level: practitioner
status: verified
description: "Work with set types: no indexing, unspecified order for non-strings, toset deduplication, sets in for_each, and converting sets to lists when you need an element."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/types#collection-types", "https://developer.hashicorp.com/terraform/language/functions/toset", "https://developer.hashicorp.com/terraform/language/meta-arguments/for_each"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set types

## Properties
- Unordered, unique elements of one type.
- No index access: `var.ids[0]` on a set gives
  `Error: Invalid index - Elements of a set are identified only by their value and don't have any separate index or key`.
- `toset(["b", "a", "a"])` -> `toset(["a", "b"])` (deduplicated; strings sorted lexically).

## Where sets appear unexpectedly
- Provider attributes of type set (`security_groups`, `vpc_security_group_ids`,
  many nested blocks): `aws_instance.x.vpc_security_group_ids[0]` fails.
- Results of `setproduct`, `setunion`, `setintersection`, `setsubtract`.
- `for_each` requires a set of strings or a map.

## Getting an element
```hcl
one(aws_instance.x.vpc_security_group_ids)                # exactly one expected
tolist(aws_instance.x.vpc_security_group_ids)[0]          # order: lexical for strings
sort(tolist(var.ids))[0]                                  # explicit order
```
For sets of objects, `tolist()` order is consistent but not meaningful; key them into
a map instead: `{for o in var.objs : o.name => o}`.

## for_each with sets
```hcl
resource "aws_iam_user" "u" {
  for_each = toset(var.usernames)     # each.key == each.value == the string
  name     = each.key
}
```
Sets of objects are not allowed in `for_each`; convert to a map.

## Nested blocks that are sets
Diffs on set-typed blocks show the whole element removed and re-added when any field
changes (no element identity). Expect noisy diffs; they are normal.

## Gotchas
- `length()` works on sets; `contains()` works; `element()` does not (`cannot read elements from set of string`).
- Comparing a set to a list with `==` is false even with the same elements; convert first.

## Verify
- [ ] No index operations on set-typed values (`terraform validate` passes).
