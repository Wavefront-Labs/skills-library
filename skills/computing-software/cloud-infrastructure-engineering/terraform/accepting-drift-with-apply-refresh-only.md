---
id: computing-software.cloud-infrastructure-engineering.terraform.accepting-drift-with-apply-refresh-only
name: accepting-drift-with-apply-refresh-only
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, refresh-only-apply, accept-drift, terraform-refresh-command, refresh-command, drift]
level: practitioner
status: verified
description: "Accept out-of-band changes into state with apply -refresh-only, review refresh-only plans, and replace the deprecated terraform refresh command safely."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#planning-modes", "https://developer.hashicorp.com/terraform/cli/commands/refresh", "https://developer.hashicorp.com/terraform/tutorials/state/refresh"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `apply -refresh-only` and the old `terraform refresh`

## What refresh-only does
Reads every managed object from the provider and writes the observed values into
state. It **never** changes infrastructure. It also updates root outputs.

```bash
terraform plan -refresh-only            # review: "Objects have changed outside of Terraform"
terraform apply -refresh-only           # same review, then "yes" to write state
terraform apply -refresh-only -auto-approve   # CI, after a reviewed plan
```

## When to use it
- After an emergency console change you intend to keep: refresh-only records it,
  then **update the code** so the next normal plan is clean.
- Objects deleted outside Terraform: refresh-only removes them from state (the plan
  says `has been deleted`), so the next plan proposes re-creation rather than failing.
- Outputs stale because an attribute changed upstream (e.g. a new IP).

## Reviewing
Every line in the refresh-only plan is drift. Ask for each: intended (codify it) or
not (revert by running a normal apply instead). Applying refresh-only first and a
normal plan later loses that distinction — the normal plan would have shown it as a
change to revert.

## `terraform refresh` (deprecated)
`terraform refresh` == `terraform apply -refresh-only -auto-approve`: writes state
with **no review**. If credentials point at the wrong account or region, it marks
every resource deleted and removes them from state. Replace it in scripts:
```bash
sed -i 's/terraform refresh/terraform apply -refresh-only -auto-approve/' scripts/*.sh
```
…and better, drop `-auto-approve` and review.

## Gotchas
- A refresh-only plan does not show config/code differences; follow up with a normal
  `terraform plan`.
- `-refresh=false` is the opposite (skip reading); do not combine with `-refresh-only`.
- Large states: refresh-only hits every API; use `-parallelism` to manage throttling.

## Verify
- [ ] Refresh-only plan reviewed line by line; deliberate drift has a matching code change.
- [ ] Normal `terraform plan` afterwards reports `No changes`.
- [ ] `grep -rn "terraform refresh" ci/ scripts/` returns nothing.

## Checked
- Terraform 1.9.8 with the local provider: deleting a managed file then `plan -refresh-only` shows `Objects have changed outside of Terraform` and `has been deleted`, `apply -refresh-only` drops it from state and updates outputs (the next normal plan proposes creating it); a config-only change shows `No changes` under `-refresh-only`; `-refresh=false` with `-refresh-only` fails with `Incompatible refresh options`; `terraform refresh` printed no deprecation warning on the CLI but the Terraform docs say the command is deprecated in favour of `-refresh-only`. Wrong-account behaviour and `-parallelism` throttling were not exercised.
