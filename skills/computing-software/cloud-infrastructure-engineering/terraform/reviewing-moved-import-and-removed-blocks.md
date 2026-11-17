---
id: computing-software.cloud-infrastructure-engineering.terraform.reviewing-moved-import-and-removed-blocks
name: reviewing-moved-import-and-removed-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, review-refactors, moved-block, import-block, removed-block, state-refactoring, code-review]
level: practitioner
status: docs-checked
description: "Review Terraform refactor PRs that use moved, import and removed blocks: what each block does, red flags, the removed destroy default, and when moved blocks can be deleted."
sources:
  - https://developer.hashicorp.com/terraform/language/modules/develop/refactoring
  - https://developer.hashicorp.com/terraform/language/import
  - https://developer.hashicorp.com/terraform/language/block/import
  - https://developer.hashicorp.com/terraform/language/block/removed
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reviewing moved, import and removed blocks

Config-driven refactoring puts the state change in the PR, so review it like a migration.

## What each block does
| Block | Effect | Review focus |
|---|---|---|
| `moved { from = aws_instance.a  to = aws_instance.b }` | Before planning, Terraform checks state for an object at `from` and renames it to `to`; the plan is as if it had been created at `to`, so nothing is destroyed. | Is every old address covered? A missed address plans a destroy and create. |
| `import { to = ...  id = "..." }` plus a matching `resource` block | Imports existing infrastructure. `to` must match an existing resource block address; `id` is the provider's ID string and must be known at plan time. | Right ID format (see the provider docs); the resource block must match reality. |
| `removed { from = ...  lifecycle { destroy = false } }` | Removes a resource from state without changing the infrastructure. | `destroy` setting (below). |

## Checklist
- [ ] Plan output is attached and the counts match the PR description.
- [ ] Each `moved` covers every instance. A whole-resource address (`aws_instance.a`) moves all instances; once either address has an instance key, both are treated as specific instances. Count to for_each and similar changes need one `moved` per instance (`aws_instance.c[0]` to `aws_instance.c["small"]`).
- [ ] Adding `count` to a resource with none: Terraform automatically proposes moving the original object to instance 0 unless a `moved` mentions that resource; HashiCorp still recommends writing the block explicitly.
- [ ] Cross-type moves: you can always rename with `moved`, but changing resource type works only where the provider supports it; check the provider docs. A managed resource cannot become a data resource.
- [ ] Module renames and splits: `moved` blocks may only describe the module's own objects and its child modules'. Addresses for a module called with `count` or `for_each` need a specific instance key, for example `module.new[2].aws_instance.example`.
- [ ] Imports: `id` and `identity` are mutually exclusive. `for_each` (a map or set of strings) lets one `import` block cover several resources, with `to = aws_s3_bucket.this[each.key]` and `id = each.value`; the destination resource also uses `for_each`.
- [ ] Imports without a hand-written resource block: `terraform plan -generate-config-out=PATH` (experimental) writes HCL for imported resources not already in config; the file must not already exist. Review and clean the generated file.
- [ ] `removed` destroys by default. HashiCorp: "By default, Terraform removes the resource from state and destroys the actual resource." Set `lifecycle { destroy = false }` to hand off management without destroying. The `lifecycle` block is required, and `destroy` is its only supported argument.
- [ ] The change is applied in every workspace/environment that holds the old addresses.

## Red flags
- A replacement (`-/+`) or destroy on a stateful resource in a pure refactor PR.
- A `moved` block deleted in a shared module: configurations still using the old address then plan to delete the object instead of moving it.
- A large generated config file committed unreviewed.
- A `removed` block that omits the `destroy = false` the author intended.

## When to delete the blocks
- Published or shared modules: HashiCorp "strongly" recommends keeping all historical `moved` blocks to preserve the upgrade path. Removing one is a breaking change.
- Private modules: safe to remove only when you are certain all users have applied the new version.
- Chain moves to record history (`a` to `b`, then `b` to `c`) so configurations at either old address upgrade correctly.
- Moved blocks require Terraform v1.1 or later.

## Checked
Date: 2026-11-07. Read in full: the refactoring page, the import overview, and the `import` and `removed` block reference pages (the old `resources/syntax#removing-resources` source redirected to the resource block page, which has no `removed` content, so it was replaced by the two reference pages). Removed because the pages do not state them: the exact plan wording (`has moved to`, `will be imported`, `will no longer be managed by Terraform`), the "Terraform 1.7+" and "1.8+" version claims, the `aws_lb` / `aws_alb` example, the deletion-timing rule for `import` and root-module blocks, the state-timestamp Verify step and the state-surgery red flag.
Method: documentation only; no commands were run.
