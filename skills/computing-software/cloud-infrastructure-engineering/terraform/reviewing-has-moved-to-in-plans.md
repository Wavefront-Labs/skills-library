---
id: computing-software.cloud-infrastructure-engineering.terraform.reviewing-has-moved-to-in-plans
name: reviewing-has-moved-to-in-plans
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, has-moved-to, moved-block, plan-review, refactoring]
level: practitioner
status: docs-checked
description: "Review refactoring plans that use moved blocks: how moves work, and checking previous_address and change actions in the plan JSON to confirm no deletes."
sources: ["https://developer.hashicorp.com/terraform/language/moved", "https://developer.hashicorp.com/terraform/internals/json-format", "https://developer.hashicorp.com/terraform/language/modules/develop/refactoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reviewing moved blocks in plans

## How a move works
```hcl
moved {
  from = aws_instance.a
  to   = aws_instance.b
}
```
Before planning the resource at `to`, Terraform checks the state for an existing object at
`from`, renames it to `to`, and then creates the plan, so the resource is not destroyed
by the move. `from` and `to` can select modules, resources and resources inside child
modules. When at least one address includes an instance key (for example `["small"]`),
Terraform treats both as specific instances, so `moved` can switch between keys and add
or remove keys when changing between `count`, `for_each` or neither.

## Review through the plan JSON
```bash
terraform plan -out=tfplan
terraform show -json tfplan
```
In `resource_changes[]`, `address` is the instance's full absolute address and
`previous_address` is its address after the previous run. `previous_address` is included
only if the address has changed, for example by handling a `moved` block.
`change.actions` is one of `["no-op"]`, `["create"]`, `["read"]`, `["update"]`,
`["delete","create"]`, `["create","delete"]` or `["delete"]`. The docs advise scanning
for `"delete"` to recognise all three situations where an object will be deleted.

A pure refactor PR should therefore show, for each moved instance, a `previous_address`
and an action of `["no-op"]`, and no `"delete"` anywhere. Treat any other action on a
moved resource as a change riding along with the move, and consider splitting it into a
separate PR (our suggestion, not stated on the pages). Count the entries that carry
`previous_address` and compare with the number of instances you intended to relocate.

## Checked
Date: 2026-11-07
Read in full: the `moved` block reference. The JSON output format page: read the `resource_changes` and change representation sections, not the whole page. The refactoring page: read the moved-block resource and instance-key sections.
Confirmed: move mechanism, argument semantics, instance-key rule, `previous_address` and `actions` semantics.
Removed (not on the pages): all sample `has moved to` console output and the claim that pure moves are excluded from the plan summary line, the red-flag table (including the error string `Moved object still exists`), the jq one-liners (rewritten as a description of the fields), the "fail CI if delete count > 0" rule, and the Verify steps. The `has moved to` plan wording is not shown on the cited pages, so it is not asserted.
Method: documentation only; no commands were run.
