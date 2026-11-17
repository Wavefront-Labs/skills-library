---
id: computing-software.cloud-infrastructure-engineering.terraform.flattening-nested-structures-for-for-each
name: flattening-nested-structures-for-for-each
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, flatten, flatten-nested, for-each, for-expressions, nested-maps]
level: practitioner
status: verified
description: "Turn nested maps/lists (networks with subnets, groups with members) into flat, uniquely keyed maps for for_each using flatten and for expressions."
sources: ["https://developer.hashicorp.com/terraform/language/functions/flatten", "https://developer.hashicorp.com/terraform/language/expressions/for"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flattening nested structures for `for_each`

## The input
```hcl
variable "networks" {
  type = map(object({
    cidr    = string
    subnets = map(object({ cidr = string, az = string }))
  }))
}
# networks = { app = { cidr = "10.0.0.0/16", subnets = { a = {...}, b = {...} } }, data = {...} }
```

## Flatten to a list of objects, then key it
```hcl
locals {
  subnets = flatten([
    for net_key, net in var.networks : [
      for sub_key, sub in net.subnets : {
        key     = "${net_key}.${sub_key}"
        net_key = net_key
        cidr    = sub.cidr
        az      = sub.az
      }
    ]
  ])
  subnets_by_key = { for s in local.subnets : s.key => s }
}

resource "aws_subnet" "this" {
  for_each          = local.subnets_by_key
  vpc_id            = aws_vpc.this[each.value.net_key].id
  cidr_block        = each.value.cidr
  availability_zone = each.value.az
}
```
Addresses become `aws_subnet.this["app.a"]` — stable, human-readable, unaffected by
ordering.

## One-line variant for pairs
```hcl
locals {
  memberships = {
    for pair in setproduct(keys(var.groups), var.users) :
    "${pair[0]}/${pair[1]}" => { group = pair[0], user = pair[1] }
  }
}
```
`setproduct` when every combination is wanted; nested `for` + `flatten` when the
inner collection depends on the outer item.

## Gotchas
- Keys must be unique: `Duplicate object key` means your composite key misses a
  dimension. Never key by list index.
- `flatten` only flattens lists of lists; it does not flatten maps. An inner `for` that builds a map (`{...}`) returns a list of maps with no error and no flattening, so the inner `for` must produce a list (`[...]`).
- Keys must be known at plan: build them from input strings, not resource IDs.
- Changing the key format later re-addresses everything; add `moved` blocks.

## Verify
- [ ] `terraform console` → `keys(local.subnets_by_key)` lists the expected composite keys.
- [ ] Reordering the input map produces `No changes`.
