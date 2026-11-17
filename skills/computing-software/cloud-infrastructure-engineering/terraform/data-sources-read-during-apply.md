---
id: computing-software.cloud-infrastructure-engineering.terraform.data-sources-read-during-apply
name: data-sources-read-during-apply
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, data-read-during-apply, data-sources, known-after-apply, deferred-data-read, perpetual-diff]
level: practitioner
status: verified
description: "Explain and fix data sources shown as read during apply: unknown arguments, depends_on, changed dependencies, and the downstream known after apply cascade."
sources: ["https://developer.hashicorp.com/terraform/language/data-sources#data-resource-behavior", "https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data sources "read during apply"

```
 # data.aws_iam_policy_document.assume will be read during apply
 # (config refers to values not yet known)
 <= data "aws_iam_policy_document" "assume" {
```
Terraform normally reads data sources at **plan** time. It defers to apply when:

| Reason line in plan | Cause |
|---|---|
| `config refers to values not yet known` | an argument is unknown at plan time (a computed attribute of a new resource, or `terraform_data.t.output` of one being updated) |
| `depends on a resource or a module with changes pending` | `depends_on` (directly or via module `depends_on`) on something with changes, **or** any reference to a resource that has a pending change, even when the attribute used is known (ran: a data source reading `local_file.src.filename` and one reading a ternary over `terraform_data.t.input` were both deferred with this reason) |

Effect: every expression using the data source becomes `(known after apply)`, so
downstream resources show diffs even if the final value is identical.

## Fixes
1. **Reference stable inputs, not computed attributes**: `role_name = var.role_name`
   instead of `aws_iam_role.r.name`. Referencing the resource is not enough to stay at plan time: while that resource has any pending change the read is deferred, so only variables, locals and objects without changes keep it immediate.
2. **Remove `depends_on`** on data sources and on module blocks that contain data
   sources; use references for ordering (see the depends_on over-use skill).
3. **Replace pure-computation data sources with expressions**, for example `jsonencode({...})` (ran: a `jsonencode` over an unknown attribute made the consumer `known after apply` but produced no `will be read during apply` entry, because a function call is not a deferred read).
4. **Split stacks** when a data source must read something created in the same apply
   (e.g. an AMI built earlier in the pipeline).

## When it is expected
First apply of a new environment; a resource genuinely being replaced. The second
plan after apply should be clean.

## Detect in CI
```bash
terraform show -json tfplan | jq -r '.resource_changes[] | select(.mode=="data" and (.change.actions|index("read"))) | .address'
```
On unchanged code this list should be empty (ran: `No changes` after apply; two entries after editing the resource).

## Verify
- [ ] Plan on unchanged code: no `<= data` lines and `No changes`.

## Checked
- Terraform 1.17.0, `hashicorp/local` data sources over `local_file` and `terraform_data`: first plan listed both data sources as `will be read during apply` with `(depends on a resource or a module with changes pending)`; after apply `No changes`; after editing the resource both were deferred again; an argument unknown at plan time gave `(config refers to values not yet known)`; the `terraform show -json` jq returned the two addresses. The advice to swap `aws_iam_policy_document` for `jsonencode` and `template_file` for `templatefile()` is design advice, not a measured claim.
