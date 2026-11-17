---
id: computing-software.cloud-infrastructure-engineering.terraform.chaining-for-each-between-resources
name: chaining-for-each-between-resources
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, resource-chaining, chaining-for-each, for-each, each-value]
level: practitioner
status: verified
description: "Chain for_each from one resource to another (for_each = aws_vpc.this), keep keys aligned between related resources, and avoid unknown-key errors when chaining."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/for_each#chaining-for_each-between-resources", "https://developer.hashicorp.com/terraform/language/meta-arguments/for_each#limitations-on-values-used-in-for_each"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chaining `for_each` between resources

A resource with `for_each` is a **map of objects** keyed like its input, so it can
itself be a `for_each` source:
```hcl
variable "vpcs" {
  type = map(object({ cidr = string }))
}
resource "aws_vpc" "this" {
  for_each   = var.vpcs
  cidr_block = each.value.cidr
}
resource "aws_internet_gateway" "this" {
  for_each = aws_vpc.this          # same keys; each.value is the VPC object
  vpc_id   = each.value.id
}
```
Keys stay aligned: `aws_internet_gateway.this["prod"]` belongs to `aws_vpc.this["prod"]`.

## Why it works with unknowns
The **keys** come from `var.vpcs` (known at plan time); only the values (`id`) are
unknown. for_each requires known keys, not known values.

## Joining two resource maps by key
```hcl
resource "aws_route_table" "public" {
  for_each = aws_vpc.this
  vpc_id   = each.value.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this[each.key].id
  }
}
```

## Filtering while chaining
```hcl
resource "aws_flow_log" "this" {
  for_each = { for k, v in aws_vpc.this : k => v if var.vpcs[k].flow_logs }
  vpc_id   = each.value.id
  # ...
}
```
Filter on **input** values (`var.vpcs[k]`), not on computed attributes; filtering
on attributes that are unknown at plan time (a first apply, or a replaced object)
makes keys unknown -> `Invalid for_each argument` ("map includes keys derived from
resource attributes that cannot be determined until apply"). Once the object is in
state its attribute is known again, so the error can appear only on a fresh
environment: test against an empty state.

## Gotchas
- `for_each = aws_instance.this` where `aws_instance.this` uses `count` gives a list
  (tuple), not a map; for_each needs a map or set (error: `... is tuple with 2
  elements ... must be a map, or set of strings`). Convert:
  `{ for i, x in aws_instance.this : i => x }`.
- Chained resources inherit key renames: renaming a key in the input replaces the
  whole chain (4 to add, 4 to destroy for a four-resource chain). One `moved` block per
  resource in the chain (`from = x.vpc["prod"]`, `to = x.vpc["prodx"]`, and the same for
  each chained resource) turns it into `0 to add, 0 to destroy`.

## Verify
- [ ] `terraform state list` shows matching keys across chained resources.

## Checked
- Terraform 1.17.0 (local run, `terraform_data` standing in for the AWS resources): a four-resource chain (`vpc` -> `igw` -> `rt`, plus a filtered `flow`) applied with matching keys; `for_each` over a `count` resource failed with the tuple error quoted above; a filter on a computed `output` failed with `Invalid for_each argument` only against an empty state; renaming a key planned 4 add / 4 destroy and `moved` blocks for each chained resource made it `0 to add, 0 to destroy`.
- AWS argument names used in the examples (`aws_vpc.cidr_block`, `aws_internet_gateway.vpc_id`, `aws_route_table` `route` / `gateway_id`, `aws_flow_log.vpc_id`) were checked against the provider docs source in hashicorp/terraform-provider-aws; no AWS account was used.
