---
id: computing-software.cloud-infrastructure-engineering.terraform.collection-functions-merge-zipmap-setproduct
name: collection-functions-merge-zipmap-setproduct
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, collection-functions, setproduct, zipmap, merge, lookup, distinct, transpose]
level: practitioner
status: verified
description: "Reshape lists and maps with merge, zipmap, setproduct, distinct, compact, concat, keys/values, lookup, contains, transpose and chunklist, with for-expression equivalents."
sources: ["https://developer.hashicorp.com/terraform/language/functions/zipmap", "https://developer.hashicorp.com/terraform/language/functions/setproduct", "https://developer.hashicorp.com/terraform/language/functions/merge"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collection functions

| Need | Function | Example |
|---|---|---|
| Combine maps (later wins) | `merge` | `merge(local.default_tags, var.tags)` |
| Two lists → map | `zipmap` | `zipmap(var.names, aws_instance.x[*].id)` |
| Every combination | `setproduct` | `setproduct(var.envs, var.regions)` |
| Join lists | `concat` | `concat(var.a, var.b)` |
| Drop duplicates / empties | `distinct`, `compact` | `compact([var.a, ""])` → `[a]` |
| Membership | `contains` | `contains(["dev","prod"], var.env)` |
| Map lookup with default | `lookup` | `lookup(var.sizes, var.env, "small")` |
| Keys / values | `keys`, `values` | sorted lexically by key |
| Invert map of lists | `transpose` | `{a=["x","y"]}` → `{x=["a"],y=["a"]}` |
| Batches | `chunklist` | `chunklist(var.ids, 10)` |
| Index of value | `index` | `index(var.azs, "eu-west-1b")` |
| Slice | `slice` | `slice(var.azs, 0, 2)` |
| Sum / max | `sum`, `max(...)` | `max(var.sizes...)` (expand with `...`) |
| Intersections | `setintersection`, `setunion`, `setsubtract` | |
| Any / all true | `anytrue`, `alltrue` | in validations |

## Patterns
```hcl
# all env x region combos as a for_each map
locals {
  deployments = {
    for p in setproduct(var.envs, var.regions) : "${p[0]}-${p[1]}" => { env = p[0], region = p[1] }
  }
}

# merge a list of maps
locals {
  all_tags = merge(var.tag_sets...)        # expansion symbol spreads the list as args
}

# deep merge is NOT built in: merge is shallow
locals {
  cfg = merge(local.base, { db = merge(local.base.db, var.db_overrides) })
}
```

## for-expression equivalents
Many functions are clearer as `for`: filtering (`[for x in l : x if x != ""]`),
mapping (`{ for k, v in m : k => upper(v) }`), grouping (`{ for o in l : o.team => o.name... }`
— the `...` groups values into lists).

## Gotchas
- `merge` of objects with different attribute types produces an object type; mixing
  maps and objects can surprise `for_each` (needs map/set) — wrap with `tomap()` when needed.
- `zipmap` requires equal lengths; unknown list lengths make the result unknown.
- `lookup` with a default hides typos — index directly when absence is an error.
- `setproduct` with an empty input returns empty — check for empty envs/regions.

## Verify
- [ ] Try each expression in `terraform console` with sample inputs.
- [ ] `for_each` maps built from these have unique, static keys.

## Checked
- Terraform 1.9.8 `terraform console`, one expression per run: `merge` (later wins, shallow: the nested `db` map was replaced), expansion `merge(list...)`, `zipmap` (and its length-mismatch error), `setproduct` including the empty-input result, `concat`, `distinct`, `compact`, `contains`, `lookup` with and without a default (error without), `keys`/`values` in key order, `transpose`, `chunklist`, `index` (error when absent), `slice`, `sum`, `max` needing `...` expansion, set functions, `anytrue`/`alltrue([])`, grouping `...` in a `for`, filtering and mapping `for` forms, `tomap`, and mixed-type `merge`.
