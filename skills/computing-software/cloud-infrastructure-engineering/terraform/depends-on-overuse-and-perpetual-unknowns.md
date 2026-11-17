---
id: computing-software.cloud-infrastructure-engineering.terraform.depends-on-overuse-and-perpetual-unknowns
name: depends-on-overuse-and-perpetual-unknowns
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, depends-on-overuse, depends-on, known-after-apply, data-source-depends-on, module-depends-on]
level: practitioner
status: docs-checked
description: "Diagnose plans full of known after apply and read during apply caused by depends_on on modules and data sources, and replace them with precise references."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on", "https://developer.hashicorp.com/terraform/language/data-sources#data-resource-dependencies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `depends_on` over-use

## Symptom
Plans show many values as `(known after apply)` and data sources deferred to the
apply phase even when the code did not change, so reviewers cannot tell real changes
from noise.

## Why
- `depends_on` makes Terraform complete all actions on the dependency object,
  including read operations, before it acts on the object declaring the dependency.
  HashiCorp says to use it only as a last resort, because it can make plans more
  conservative: Terraform may treat more values as unknown (`known after apply`)
  because it is uncertain what will change on the upstream object. This is especially
  likely when you use `depends_on` for modules.
- When the dependency is an entire module, `depends_on` affects the order in which
  Terraform processes all the resources and data sources associated with that module.
- Data sources are read at plan time unless an argument (or a custom condition)
  depends on a resource that is changing in the current plan, or a value is computed
  during apply; then the read is deferred and everything using it is unknown. A
  `depends_on` on a data block makes Terraform defer querying it until after the
  dependency's operations finish.

## Fix
1. **Prefer expression references.** They let Terraform see which value you derive
   from and avoid planning changes if that particular value has not changed, even when
   other parts of the upstream object have planned changes. Pass a module dependency
   as an input instead of `depends_on`:
```hcl
module "app" {
  source        = "./app"
  vpc_id        = module.network.vpc_id     # implicit dependency, precise
  # depends_on  = [module.network]           # remove
}
```
2. **Data sources**: reference the attribute you depend on rather than `depends_on`:
```hcl
data "aws_iam_role" "r" {
  name = aws_iam_role.r.name               # dependency via reference
}
```
3. Keep `depends_on` only for hidden dependencies, where a resource relies on another
   resource's behavior without reading any of its data (HashiCorp's example: an EC2
   instance that needs an IAM role policy to boot properly). It takes a static list of
   references to resources or child modules in the same calling module, not arbitrary
   expressions.
4. For data blocks, `depends_on` is recommended on Terraform 0.13 and newer; in 0.12
   and earlier it forces the read to apply time.
5. On an `output`, add a comment explaining why when you add an explicit dependency;
   outputs rarely need one.

## Checked
Date: 2026-11-07
Read in full: depends_on reference (meta-arguments/depends_on) and Query infrastructure data (language/data-sources), including Data source behavior, Requirements and Dependencies.
Confirmed: last-resort wording and "known after apply" consequence, especially for modules; module depends_on affects all resources and data sources of the module; expression references preferred; hidden-dependency use case; static reference list; data-source deferral conditions; Terraform 0.13 note; output comment recommendation.
Removed: the invented plan-output sample (`<= data ... # read during apply`), the claim that any pending change in the dependency defers a data read and that a module depends_on links every data source to every resource, the `time_sleep`/provider-retries advice, "prefer resources over data sources for ordering", the grep and `terraform show -json | jq` commands, and the Verify checklist (not stated on the pages).
Method: documentation only; no commands were run.
