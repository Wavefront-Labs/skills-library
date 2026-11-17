---
id: computing-software.cloud-infrastructure-engineering.terraform.data-source-dependency-cycles
name: data-source-dependency-cycles
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, data-source-cycle, cycle-errors, depends-on, terraform-graph, data-source-deferral, cycle]
level: practitioner
status: gated
description: "Diagnose Terraform cycle errors involving data sources: reading the cycle list, depends_on on data sources deferring reads, self-referencing lookups and refactors."
sources:
  - https://developer.hashicorp.com/terraform/language/data-sources#data-resource-dependencies
  - https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on
  - https://developer.hashicorp.com/terraform/cli/commands/graph
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Data source cycles

## Reading the error
```
Error: Cycle:
  local_file.pol
  data.local_file.doc
```
(Terraform 1.17.0 prints one node per line; older versions printed a comma-separated list.) The listed nodes are the
loop. Find the edge you didn't intend. `terraform validate` reports the same error without needing a plan.
```bash
terraform graph -type=plan | grep -E 'local_file' | head
terraform graph -type=plan -draw-cycles | dot -Tsvg > cycle.svg   # cycle edges drawn in red
```
Minimal reproduction (a data source that reads a file the resource writes, whose content feeds the resource):
```hcl
data "local_file" "doc" { filename = local_file.pol.filename }
resource "local_file" "pol" {
  content  = data.local_file.doc.content
  filename = "${path.module}/pol.txt"
}
```

## Typical data source cycles
1. **Lookup of something this config creates**:
```hcl
resource "aws_security_group" "app" { ... ingress { security_groups = [data.aws_security_group.lb.id] } }
data "aws_security_group" "lb" { tags = { Name = "lb" }  depends_on = [aws_security_group.lb] }
resource "aws_security_group" "lb" { ... egress { security_groups = [aws_security_group.app.id] } }
```
If you manage it, reference the resource directly - but two SGs referencing each other in inline rules form a cycle by the same rule as the local example above: use separate `aws_vpc_security_group_ingress_rule`/`egress_rule` resources (both exist in the AWS provider docs) that depend on both SGs. (The AWS examples here were not applied; only the cycle mechanism was run, with the local provider.)

2. **Policy documents referencing the resource they attach to, which references the policy**:
```hcl
data "aws_iam_policy_document" "bucket" { statement { resources = ["${aws_s3_bucket.this.arn}/*"] ... } }
resource "aws_s3_bucket" "this" { policy = data.aws_iam_policy_document.bucket.json }   # legacy inline policy -> cycle
```
Fix (the AWS provider docs mark the `aws_s3_bucket` `policy` argument as deprecated in favour of `aws_s3_bucket_policy`): attach with a separate `aws_s3_bucket_policy` resource (bucket -> document -> policy resource, no loop), or build the ARN from known inputs (`"arn:aws:s3:::${var.bucket_name}/*"`).

3. **depends_on on a data source pulling it to apply time**: a data source is read during plan unless its configuration depends (via `depends_on` or a reference) on a resource with pending changes or unknown values; then the read is deferred to apply and its results show `known after apply`. Tested on 1.17.0 with `depends_on = [local_file.mk]`: with no pending change to `mk` the data source was read at plan time (`Read complete` during plan); when `mk` was replaced in the same run the plan said `data.local_file.dep will be read during apply`. (Terraform 0.12 and earlier deferred every `depends_on` data read, per the data-sources docs.) If something the depended-on resource needs reads the data source, a cycle forms; deferred reads also make dependants show `known after apply`. Remove `depends_on` from data sources unless truly needed; depend on specific attributes instead.

4. **Module boundaries**: module A outputs feed module B, whose outputs feed A's data source. Terraform evaluates at the resource level, so this is sometimes fine (module outputs wired a -> b -> c validated), but `depends_on` on a whole module makes every resource and data source in it depend on everything in the other module - a frequent cause of cycles and perpetual diffs (tested: `module.a` with `depends_on = [module.b]` plus `module.b` taking `module.a`'s output fails with `Error: Cycle:` listing both modules' resources, while the same wiring without the `depends_on` validates). Replace module-level `depends_on` with explicit value references.

## Destroy-time cycles
`create_before_destroy` on one resource propagates to its dependencies; mixing with dependencies that can't be created before destroy yields cycles only during replacement plans. Check `terraform plan -destroy` and replacement scenarios.

## Verify
- [ ] `terraform validate` and plan succeed; `terraform graph -draw-cycles` shows no red edges.
- [ ] Data sources without intentional `depends_on` read at plan time (values shown, not `known after apply`).

## Checked
- Terraform 1.17.0 with the local provider: a data source/resource reference loop gave `Error: Cycle:` with one node per line from both `plan` and `validate`, and `graph -type=plan -draw-cycles` produced red edges (4 red strokes through Graphviz 12.2.1 `dot -Tsvg`); module-level `depends_on` cycle reproduced; module chain a -> b -> c validated; `depends_on` on a data source read at plan time without pending changes and during apply with a replaced dependency (docs, developer.hashicorp.com/terraform/language/data-sources: 0.12 and earlier deferred all).
- Docs fetched: lifecycle page says Terraform propagates `create_before_destroy` to all resource dependencies; AWS provider docs on GitHub (main) confirm `aws_vpc_security_group_ingress_rule`/`egress_rule` and `aws_s3_bucket_policy` exist and `aws_s3_bucket` `policy` is Deprecated.
- The AWS security-group and S3/IAM examples were not applied (no AWS account) (gated: unconfirmed, source is paywalled or blocked). The reason is that no AWS access was available, not that a source was blocked.
