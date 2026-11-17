---
id: computing-software.cloud-infrastructure-engineering.terraform.choosing-stable-for-each-keys
name: choosing-stable-for-each-keys
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, stable-keys, for-each, unknown-keys, moved-block, index-shift]
level: practitioner
status: verified
description: "Choose for_each keys that never change or go unknown: business names over generated IDs, avoiding list indexes and computed values, and renaming keys safely."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/for_each", "https://developer.hashicorp.com/terraform/language/moved"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing stable `for_each` keys

The key is part of the resource address in state (`aws_subnet.this["private-a"]`).
Change the key and Terraform plans destroy + create.

## Good keys
- Human/business identifiers from config: service names, environment names,
  `"${az}-${tier}"`.
- Stable natural identifiers known at plan time: CIDR, domain name, username.

## Bad keys
| Key | Problem |
|---|---|
| List index (`for i, s in var.subnets : i => s`) | accepted (keys become `"0"`, `"1"`) but reintroduces count-style index shift |
| Resource IDs/ARNs from other resources | unknown at plan time -> `Invalid for_each argument`, and change on replace |
| `uuid()`, `timestamp()` | unknown at plan time -> `Invalid for_each argument` (keys "cannot be determined until apply") |
| Display names that teams rename | renames recreate resources |
| Values containing secrets | `Invalid for_each argument`: "Sensitive values ... cannot be used as for_each arguments" |

## Building keys from lists of objects
```hcl
variable "subnets" {
  type = list(object({ name = string, cidr = string, az = string }))
}
resource "aws_subnet" "this" {
  for_each          = { for s in var.subnets : s.name => s }    # key = name
  cidr_block        = each.value.cidr
  availability_zone = each.value.az
  vpc_id            = aws_vpc.main.id
}
```
Duplicate names error (`Duplicate object key`: "Two different items produced the key
"priv-b" in this 'for' expression") - good, it catches config mistakes.
Use the grouping operator `...` only when you intend lists per key.

## Renaming a key without recreation
```hcl
moved {
  from = aws_subnet.this["priv-a"]
  to   = aws_subnet.this["private-a"]
}
```

A `moved` block makes the rename a no-op: the plan shows
`terraform_data.this["priv-a"] has moved to terraform_data.this["private-a"]` and
`0 to add, 0 to change, 0 to destroy`; without it the same rename plans `1 to add, 1 to destroy`.

## Composite keys for nested data
`"${svc.name}/${port}"` after `flatten`; keep a separator that cannot appear in parts.

## Verify
- [ ] Reordering input lists produces `No changes`.
- [ ] Keys are all known at plan time on a fresh environment.

## Checked
- Terraform 1.17.0, `terraform_data`: a list of objects keyed by `name` applied; reordering the list gave `No changes`; a duplicate name gave `Duplicate object key` with the quoted text; `uuid()` as key and a sensitive variable in `toset([...])` each gave `Invalid for_each argument` (messages as in the table); index keys `{ for i, s in ... : i => s }` were accepted; the rename planned 1 add / 1 destroy without the `moved` block and `0 to add, 0 to destroy` with it.
- The composite-key advice (`flatten` plus a separator) is a design rule, not a command.
