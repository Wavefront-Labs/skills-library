---
id: computing-software.cloud-infrastructure-engineering.terraform.deposed-objects-after-failed-replacement
name: deposed-objects-after-failed-replacement
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, deposed-object, deposed, create-before-destroy, failed-apply, state-recovery]
level: advanced
status: verified
description: "Understand and clean up deposed objects left when a create_before_destroy replacement fails part-way, reading them in state and plans and removing them safely."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#create_before_destroy", "https://developer.hashicorp.com/terraform/internals/json-format#state-representation", "https://github.com/hashicorp/terraform/blob/main/docs/destroying.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deposed objects

## What they are
During a `create_before_destroy` replacement, the old object is moved aside as
**deposed** while the new one is created. If the apply fails before the old object
is destroyed (destroy error, timeout, Ctrl-C), state keeps both: the current
object and one or more deposed ones, each with a random key (`deposed_key`, e.g.
`9f7c1b2a`).

## Seeing them
```
  # terraform_data.w (deposed object 2971ac94) will be destroyed
  # (left over from a partially-failed replacement of this instance)
```
```bash
terraform show                      # "# terraform_data.w: (deposed object 2971ac94)" next to the tainted current object
terraform state pull | jq '.resources[] | select(.instances[].deposed?) | .type'
terraform show -json | jq '.values.root_module.resources[] | select(.deposed_key)'
```

## Cleaning up
1. Normal case: just run `terraform plan`/`apply`. Terraform plans to destroy the
   deposed object (and, if the current object is tainted, to replace it); fix whatever made the destroy fail (dependency still attached,
   permissions, deletion protection), then apply.
2. Old object already gone (deleted by hand): the next plan refreshes it and normally drops it;
   if the provider errors instead, run `terraform apply -refresh-only` first and read the error.
3. You want to **keep** the old object (rollback): there is no CLI to undepose.
   Options: import it at a new address, or edit state (`state pull`, remove the
   deposed instance entry, bump `serial`, `state push`) — last resort.

## Why destroys fail here
The destroy of the deposed object is an ordinary provider destroy, so the cause is in the
provider error. Typical causes: the old object is still referenced or in use by something not yet
updated, a provider-side deletion protection flag, or missing permissions. Fix the cause, then run apply.

## Gotchas
- `terraform state rm <address>` removes current **and** deposed objects of that
  instance — the real objects then become unmanaged (verified: afterwards state had no resources).
- Multiple failed attempts can accumulate several deposed objects; each is destroyed separately.

## Verify
- [ ] `terraform show -json | jq '[.. | .deposed_key? // empty] | length'` is 0 (printed 1 while one deposed object existed, 0 after the cleaning apply).
- [ ] No orphaned old objects remain in the provider console.

## Checked
- Terraform 1.17.0, `terraform_data` with `create_before_destroy`, a creation-time `local-exec` that fails for the new value: state ended with the new object tainted and the old one deposed. `terraform show` printed `# terraform_data.w: (tainted)` and `# terraform_data.w: (deposed object 2971ac94)` (the old `Deposed ID 1 = ...` format in this skill was wrong); `plan` printed `is tainted, so must be replaced` plus `(deposed object ...) will be destroyed` and `(left over from a partially-failed replacement of this instance)`.
- `state pull | jq` `select(.instances[].deposed?)` returned the type; `show -json` listed a second resource entry with `deposed_key` set and `tainted` null; `[.. | .deposed_key? // empty] | length` was 1, then 0 after the next apply destroyed the deposed object.
- Hand removal (jq drop of the deposed instance, `serial` + 1, `state push`) succeeded and the deposed object disappeared from `show`; `state rm` removed the resource including both objects.
- The cloud-specific causes of destroy failures were removed from the skill because no cloud provider was run; the section now defers to the provider error.
