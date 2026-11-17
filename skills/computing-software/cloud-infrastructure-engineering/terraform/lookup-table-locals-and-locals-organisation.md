---
id: computing-software.cloud-infrastructure-engineering.terraform.lookup-table-locals-and-locals-organisation
name: lookup-table-locals-and-locals-organisation
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, locals, lookup-table, lookup-tables, locals-naming, locals-file, environment-config]
level: practitioner
status: gated
description: "Drive per-environment settings from lookup-table locals keyed by env or workspace, fail loudly on unknown keys, and organise and name locals so they stay readable."
sources: ["https://developer.hashicorp.com/terraform/language/values/locals", "https://developer.hashicorp.com/terraform/language/functions/lookup", "https://developer.hashicorp.com/terraform/language/style"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lookup-table locals and organising locals

## Lookup table keyed by environment
```hcl
locals {
  env_settings = {
    dev  = { instance_type = "t3.small",  min = 1, max = 2,  multi_az = false }
    stg  = { instance_type = "m6i.large", min = 2, max = 4,  multi_az = true }
    prod = { instance_type = "m6i.large", min = 3, max = 12, multi_az = true }
  }
  env = local.env_settings[var.env]       # errors on unknown env: good
}

resource "aws_autoscaling_group" "web" {   # (gated: unconfirmed, source is paywalled or blocked) (AWS resource not run; the lookup pattern ran with terraform_data)
  min_size = local.env.min
  max_size = local.env.max
}
```
- Index with `[]`, not `lookup(map, key, default)`: a typo'd env should fail, not
  silently get defaults. Add a validation on `var.env` with `contains(keys(local.env_settings), var.env)`: Terraform 1.17.0 accepts locals in variable validations (ran; the plan rejected `prd` with `Invalid value for variable` and the custom message), so older advice that validations cannot reference locals no longer holds; listing the allowed values explicitly is still the portable choice.
- Keyed by `terraform.workspace` works too, but an explicit `var.env` is clearer and
  testable.
- Partial overrides: `merge(local.defaults, lookup(local.overrides, var.env, {}))`.

## Organising locals
- Put locals near their use: a `locals` block at the top of the file whose resources
  use them. Cross-cutting ones (`common_tags`, `name_prefix`) in `locals.tf` / `main.tf`.
- Names describe the value, not how it is computed: `private_subnet_ids`, not
  `subnets_flattened_list`.
- Snake_case; booleans read as predicates (`create_dns_record`, `is_prod`).
- One expression per local; split long `for` expressions into named intermediate locals.
- Do not wrap a single variable in a local (`local.region = var.region`) — noise.

## Common tags pattern
```hcl
locals {
  name_prefix = "${var.project}-${var.env}"
  common_tags = {
    project = var.project
    env     = var.env
    managed = "terraform"
  }
}
```
Prefer provider `default_tags` for tags when available (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Locals cannot be overridden by callers; if a value needs per-env tweaking by users,
  it should be a variable with a default from the table.
- Lookup tables whose entries have different object shapes validated and planned in 1.17.0 (ran), but converting them with `tomap()` silently turned numbers into strings (`a = 1` became `"1"`); keep all entries the same shape (use `null` for unused fields) so the types stay predictable.

## Verify
- [ ] `terraform plan -var env=prd` (typo) fails with an invalid-key / validation error.
- [ ] `terraform console` → `local.env` shows the expected object per env.

## Checked
- Terraform 1.17.0, local-only config: `local.env_settings[var.env]` with `env=prd` failed with `Invalid index` (no validation) and with `Invalid value for variable` plus the custom message (with a local-based validation); `merge(local.defaults, lookup(local.overrides, var.env, {}))` returned the override (`b = 9`); `terraform console` printed `local.env`; mixed-shape entries and `tomap()` coercion measured.
- Gated: the AWS autoscaling group and `default_tags`.
