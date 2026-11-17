---
id: computing-software.cloud-infrastructure-engineering.terraform.depends-on-for-modules-and-data-sources
name: depends-on-for-modules-and-data-sources
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, depends-on, module-depends-on, data-source-depends-on, deferred-data-read, known-after-apply]
level: advanced
status: gated
description: "Use depends_on on module blocks and data sources correctly: what it serialises, why it defers data reads to apply and causes perpetual diffs, and the reference-based alternatives."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on", "https://developer.hashicorp.com/terraform/language/data-sources#data-resource-dependencies"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# `depends_on` on modules and data sources

## On a module block
```hcl
module "app" {
  source     = "./modules/app"
  depends_on = [aws_iam_role_policy.app]   # policy must exist before anything in the module
}
```
Effect: **every** resource and data source in the module waits for the dependency,
and every data source inside the module is **deferred to apply time** whenever the
dependency has pending changes. Plans then show `(known after apply)` across the
module and outputs, and downstream resources diff on every run.

Prefer passing a reference in:
```hcl
module "app" {
  source        = "./modules/app"
  role_arn      = aws_iam_role.app.arn
  policy_ready  = aws_iam_role_policy.app.id   # module uses it, e.g. in a depends_on internally or a tag
}
```
Then only the resources that use the input wait.

## On a data source
```hcl
# (gated: unconfirmed, source is paywalled or blocked) (the EKS, helm and kubernetes examples below were not run)
data "aws_eks_cluster_auth" "this" {
  name       = aws_eks_cluster.main.name     # reference: read waits only if name is unknown
}

data "kubernetes_config_map" "aws_auth" {
  metadata {
    name = "aws-auth"
    namespace = "kube-system"
  }
  depends_on = [helm_release.bootstrap]       # forces read during apply when helm_release changes
}
```
A data source with `depends_on` is read during **apply** whenever any dependency has
a planned change → `known after apply` and cascade. Use it only when the data
genuinely appears as a side effect the graph cannot see.

## Diagnosing a perpetual diff
Plan says `# data.x.y will be read during apply  # (depends on a resource or a module with changes pending)`.
Find the `depends_on` that makes it so (the 1.2 changelog reworded this reason note; a plain reference to a resource with pending changes gives the same note), then
replace it with a reference to something unchanged or remove it.

## Gotchas
- `depends_on` takes whole objects (`aws_x.y`, `module.m`), never attributes.
- Module-level `depends_on` disables per-resource parallelism across the boundary —
  slower applies (gated: unconfirmed, source is paywalled or blocked) (not timed).
- Modules containing provider blocks cannot have `depends_on` (legacy restriction; ran: `Module is incompatible with count, for_each, and depends_on`). `depends_on = [aws_x.y.id]` is rejected with `References in depends_on must be to a whole object`.

## Verify
- [ ] With no real changes, `terraform plan` shows `No changes` (no data reads deferred).
- [ ] `grep -rn depends_on` justified with a comment for each occurrence.

## Checked
- Terraform 1.17.0: a child module with a data source and `depends_on = [terraform_data.t]` on the module block: after changing `t`, the plan showed `module.app.data.local_file.f will be read during apply` with `(depends on a resource or a module with changes pending)`; attribute-level `depends_on` rejected; the provider-block restriction reproduced. The 1.2 changelog line about the reworded note was read in the changelog.
- Gated: AWS/EKS/helm examples, parallelism cost.
