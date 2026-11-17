---
id: computing-software.cloud-infrastructure-engineering.terraform.unknown-for-each-keys-errors
name: unknown-for-each-keys-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, each-key, unknown-keys, for-each, invalid-for-each-argument, known-after-apply]
level: advanced
status: verified
description: "Fix 'Invalid for_each argument ... keys cannot be determined until apply' by keying on static inputs, separating keys from values, and avoiding -target workarounds."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/for_each#limitations-on-values-used-in-for_each", "https://developer.hashicorp.com/terraform/language/meta-arguments/count#when-to-use-for_each-instead-of-count"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unknown `for_each` keys

## The error
```
Error: Invalid for_each argument
  The "for_each" map includes keys derived from resource attributes that cannot be
  determined until apply, and so Terraform cannot determine the full set of keys
  that will identify the instances of this resource.
```
With a set (`toset([...])`) the wording is `The "for_each" set includes values derived from resource attributes that cannot be determined until apply ...`; both seen on 1.9.8.
`count` has the twin: `The "count" value depends on resource attributes that cannot
be determined until apply, so Terraform cannot predict how many instances will be created.`

## Why
Instance addresses (`aws_x.y["key"]`) must be known at plan. **Values** may be
unknown; **keys** may not.

## Fixes
1. Key on configuration, not on generated IDs:
```hcl
# bad: keys are subnet IDs created in this run
for_each = toset(aws_subnet.private[*].id)

# good: keys are AZ names from input; values may be unknown
for_each = aws_subnet.private          # map keyed by AZ already
subnet_id = each.value.id
```
2. Build maps with static keys and unknown values:
```hcl
for_each = { for az, s in aws_subnet.private : az => s.id }
```
3. Conditional inclusion based on unknowns → base the condition on inputs:
```hcl
# bad: count = aws_instance.x.id != "" ? 1 : 0           (id is known only after create)
# good:
count = var.multi_az ? 1 : 0
```
4. Lists whose **length** is unknown (`data` source result with deferred read): pass
   the expected names in as a variable.
5. Values that come from another stack: read them from an already-applied state
   (`terraform_remote_state`) — known at plan.

## The -target workaround
`terraform apply -target=aws_subnet.private` then full apply works but makes
greenfield deploys two-step forever. Fix the keying instead. (Terraform's
experimental *deferred actions* and Stacks handle some of these cases.)

## Gotchas
- `toset(list_with_unknown_elements)` makes the whole set's keys unknown.
- `keys()` of a map from a resource with `for_each` is known; `values()` may not be.
- Sensitive keys are a different error with a similar fix (`toset(var.s)` with a sensitive `var.s` also gives `Invalid for_each argument`).

## Verify
- [ ] `terraform plan` from an empty state (fresh workspace) succeeds with no `-target`.
- [ ] Planned addresses show readable static keys.
