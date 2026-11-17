---
id: computing-software.cloud-infrastructure-engineering.terraform.reading-known-after-apply-and-unknown-values
name: reading-known-after-apply-and-unknown-values
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, known-after-apply, unknown-values, plan-output, computed-attributes, plan-time-unknown, for-each-unknown, count-unknown, two-phase-apply]
level: practitioner
status: gated
description: "Interpret (known after apply) in plans: which unknowns are harmless, which cascade into replacements or for_each errors, and the patterns that make values known at plan time."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/references#values-not-yet-known", "https://developer.hashicorp.com/terraform/language/meta-arguments/for_each#limitations-on-values-used-in-for_each", "https://developer.hashicorp.com/terraform/cli/commands/plan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading "known after apply" and unknown values

**Goal:** read a plan full of `(known after apply)` and tell the benign cases
from the ones that will bite at apply.

## 1. What an unknown is
A value Terraform cannot compute until the provider creates or updates something:
IDs, ARNs, generated names, IPs, anything derived from them. In plan output:
```
+ arn        = (known after apply)
~ user_data  = "base64..." -> (known after apply)   # changed to an unknown
```
Unknowns propagate: any expression using an unknown is unknown.

## 2. Benign vs dangerous
| Pattern | Meaning |
|---|---|
| `+ id = (known after apply)` on a new resource | normal |
| `~ attr = "x" -> (known after apply)` on an existing resource | the input changed to something depending on another change; check *why* |
| `-/+` with `# forces replacement` on an unknown attribute | an upstream change forces replacement downstream — the cascade you must understand before applying |
| whole nested block `(known after apply)` | often a `dynamic` block fed by an unknown list |
| `(known after apply)` in `tags` | typically a name derived from an unknown ID |

Dangerous cascades: a new `random_id` → every `name = "${random_id.x.hex}"` →
replacement of everything named when the provider marks `name` as forcing replacement (ran: with `random_id` replaced, a `terraform_data` consumer of `random_id.sg.hex` was only updated in place, so the cascade depends on the resource type). Grep the plan for `forces replacement`.

## 3. Hard errors caused by unknowns
- `count`/`for_each` from an unknown:
  `The "for_each" set includes values derived from resource attributes that cannot be determined until apply`.
  Fix: key on input values (`var.names`), not on `aws_x.y.id`; or use
  `-target` for a first apply (last resort).
- `provider` configuration from an unknown (e.g. `host = aws_eks_cluster.c.endpoint`
  on first apply): providers must configure at plan time; the Kubernetes/Helm
  providers error or plan against nothing. Split into two states or two applies (gated: unconfirmed, source is paywalled or blocked).
- Conditionals on unknowns: `unknown ? a : b` is unknown in full; if `a` and `b`
  have no common type you get `Inconsistent conditional result types` at plan time (ran on 1.17.0 with `terraform_data.t.id == "z" ? { a = 1 } : "str"`), not at apply.
- `validation` blocks: an unknown input value passes validation at plan and may
  fail later.

## 4. Making values known
- Prefer attributes the provider marks "plan-known": names you set, ARNs that
  are computable from inputs (`aws_iam_role.arn` is computed; building the ARN from
  `data.aws_caller_identity` + name is known).
- `terraform_data` / `random_*` with `keepers`: known after the first apply.
- Provider-defined functions (`provider::aws::arn_build`) compute at plan time (gated: unconfirmed, source is paywalled or blocked).
- "Deferred actions" (Terraform Stacks) plan what they can and defer the rest — the designed fix for provider-config unknowns (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- `terraform show -json` exposes unknowns in `after_unknown`; `after` simply
  omits them — do not conclude an attribute was removed (ran: `after` lacked `input`, `after_unknown` had `{"id":true,"input":true,"output":true}`).
- Unknown-ness is per plan: after the first apply the same config plans clean.
- Sensitive + unknown prints as `(sensitive value)`, hiding the unknown (ran for an output; the JSON still has `after_unknown: true`).
- `moved`/`import` blocks cannot have unknown addresses or IDs (ran: `Invalid import id argument ... cannot be determined until apply`).

## Verify
- [ ] Every `-/+` in the plan has a `# forces replacement` attribute you can explain.
- [ ] Plan contains no `for_each`/`count` unknown errors on a fresh workspace (ran: `Invalid for_each argument ... known only after apply` for `toset([terraform_data.t.id])` on empty state).
- [ ] Second `plan` after apply shows `No changes` (no perpetual unknowns).

## Checked
- Terraform 1.17.0, `terraform_data` and `random_id`: unknown-attribute plan output and JSON (`after`, `after_unknown`, sensitive output), resource `for_each` from an unknown, conditional type mismatch error time, import id unknown, `random_id` replacement effect.
- Gated: Kubernetes/Helm provider configuration, `provider::aws::arn_build`, and Stacks deferred actions.
