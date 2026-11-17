---
id: computing-software.cloud-infrastructure-engineering.terraform.merging-defaults-with-overrides-in-locals
name: merging-defaults-with-overrides-in-locals
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, merge-defaults, locals, merge-function, optional-attributes, configuration-layering]
level: practitioner
status: verified
description: "Layer defaults, environment settings and per-item overrides in locals with merge(), and know when optional() defaults or a deep-merge pattern work better."
sources: ["https://developer.hashicorp.com/terraform/language/functions/merge", "https://developer.hashicorp.com/terraform/language/expressions/type-constraints#optional-object-type-attributes", "https://developer.hashicorp.com/terraform/language/values/locals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Merging defaults with overrides

## Shallow layering with `merge`
```hcl
locals {
  defaults = {
    instance_type = "t3.small"
    min_size      = 1
    max_size      = 3
    monitoring    = false
  }
  env_overrides = {
    prod = { instance_type = "m6i.large", min_size = 3, max_size = 12, monitoring = true }
    dev  = {}
  }
  settings = merge(local.defaults, local.env_overrides[var.env])
}
```
`merge` is **shallow** and later arguments win. A nested map in an override replaces
the default nested map entirely (with the example above and `var.env = "prod"`, `tags = { a = 1, b = 2 }` in the defaults and `tags = { c = 3 }` in the override gives `tags = { c = 3 }`).

## Per-item overrides in collections
```hcl
variable "services" {
  type = map(object({
    cpu    = optional(number)
    memory = optional(number)
  }))
}
locals {
  svc_defaults = { cpu = 256, memory = 512 }
  services = {
    for name, s in var.services : name => merge(
      local.svc_defaults,
      { for k, v in s : k => v if v != null }    # drop unset optionals so defaults survive
    )
  }
}
```
Without the `if v != null` filter, `optional()` attributes arrive as `null` and
overwrite the defaults (`merge(local.svc_defaults, s)` gave `memory = null` for `a`, whereas the filtered form gave `{cpu = 1, memory = 512}`).

## Simpler: `optional()` defaults (TF 1.3+)
```hcl
type = map(object({
  cpu    = optional(number, 256)
  memory = optional(number, 512)
}))
```
Prefer this when the defaults are static; use `merge` layering when defaults depend on
environment or other variables.

## Deep merge
No built-in deep merge. Options: merge each nested key explicitly
(`tags = merge(local.defaults.tags, o.tags)`), or the `Invicton-Labs/deepmerge` module.
Explicit is clearer for 1-2 levels.

## Verify
- [ ] `echo 'local.settings' | terraform console -var env=prod` shows the expected merged map.
- [ ] Unset optional attributes keep their defaults.
