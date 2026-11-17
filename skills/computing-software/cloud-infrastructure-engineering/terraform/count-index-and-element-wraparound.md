---
id: computing-software.cloud-infrastructure-engineering.terraform.count-index-and-element-wraparound
name: count-index-and-element-wraparound
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, count-index, element-wraparound, count, element-function, index-shift]
level: practitioner
status: verified
description: "Use count.index correctly: naming, spreading instances across AZs with element() wraparound vs indexing, and why removing a middle item reshuffles everything."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/count", "https://developer.hashicorp.com/terraform/language/functions/element"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `count.index` and `element()`

## Basics
```hcl
resource "aws_instance" "web" {
  count         = 3
  ami           = var.ami
  instance_type = "t3.small"
  subnet_id     = element(var.subnet_ids, count.index)   # wraps around
  tags          = { Name = format("web-%02d", count.index + 1) }   # web-01, web-02, web-03
}
```

## element() vs index syntax
| Expression | 3 subnets, count = 5 |
|---|---|
| `element(var.subnet_ids, count.index)` | 0,1,2,0,1 (wraps, modulo) |
| `var.subnet_ids[count.index]` | error at index 3 (`Invalid index`, checked on 1.9.8) |
| `var.subnet_ids[count.index % length(var.subnet_ids)]` | same as element, explicit |

Use wraparound deliberately for spreading across AZs; use direct indexing when a
mismatch should be an error. `element()` also rejects a negative index (error) and wraps by modulo only for non-negative indexes.

## The index-shift problem
```hcl
variable "users" { default = ["alice", "bob", "carol"] }
resource "aws_iam_user" "u" {
  count = length(var.users)
  name  = var.users[count.index]
}
```
Removing `bob` makes `u[1]` carol (the provider then renames or replaces it, depending on the resource) and destroys `u[2]`.
Use `for_each = toset(var.users)` for anything identified by a name.

## Where count is still right
- Identical, interchangeable instances (`count = var.replicas`).
- Conditional single resource: `count = var.enabled ? 1 : 0`.

## Referencing count resources
```hcl
aws_instance.web[0].id
aws_instance.web[*].id                     # list of all
one(aws_lb.this[*].arn)                    # 0-or-1 conditional resource
```

## Migrating count -> for_each
`moved { from = aws_iam_user.u[0]  to = aws_iam_user.u["alice"] }` per instance.

## Verify
- [ ] Removing an element from the input list plans only one destroy (for_each) or is acceptable (count of identical items).
