---
id: computing-software.cloud-infrastructure-engineering.terraform.locals-vs-variables
name: locals-vs-variables
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, locals-vs-variables, locals, input-variables, module-design]
level: practitioner
status: verified
description: "Decide whether a value belongs in a variable, a local or hard-coded: caller-facing inputs, derived values, constants, and the over-parameterised module anti-pattern."
sources: ["https://developer.hashicorp.com/terraform/language/values/locals", "https://developer.hashicorp.com/terraform/language/values/variables", "https://developer.hashicorp.com/terraform/language/modules/develop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locals vs variables

## Rule of thumb
| Value | Put it in |
|---|---|
| Differs between callers/environments and the caller should decide | `variable` |
| Computed from variables, resources or other locals | `local` |
| Repeated constant that never varies (port 443, a naming suffix) | `local` (named constant) |
| Organisation-wide constant (approved regions, CIDR plan) | a shared data module or `local` in one place |
| Secrets | variable (sensitive/ephemeral) or a secret store lookup, never a local literal |

## Signs you have too many variables
- Variables nobody ever sets (always default): convert to locals or literals.
- A variable per resource argument (`instance_type`, `ebs_optimized`, `monitoring`, ...)
  that turns the module into a pass-through of the provider schema. Expose intent
  (`size = "small" | "large"`) and map it in locals.
- Variables used only to build names: take `name`/`env` and derive the rest in locals.

## Signs you need a variable
- Editing module code to deploy another environment.
- A local with a conditional on `terraform.workspace` growing more branches.

## Pattern: intent variable + lookup local
```hcl
variable "size" {
  type = string
  validation {
    condition     = contains(["small", "large"], var.size)
    error_message = "size must be small or large."
  }
}
locals {
  sizes = {
    small = { instance_type = "t3.small",  min = 1, max = 2 }
    large = { instance_type = "m6i.large", min = 3, max = 10 }
  }
  sz = local.sizes[var.size]
}
```

## Differences that matter
- Variables can be set from outside (tfvars, env, CLI) and validated; locals cannot be overridden.
- Locals can reference resources and data sources; variable defaults cannot.
- Variables appear in docs/registry; locals are implementation detail.

## Verify
- [ ] Every variable is set by at least one caller or documented as a tuning knob.
- [ ] No environment-specific literals inside the module.

## Checked
- Terraform 1.17.0: the intent-variable pattern (`validation` with `contains`, `local.sizes[var.size]`) planned the expected object for `size=large` and failed `size=huge` with `Invalid value for variable` plus the custom message; `default = terraform_data.r.id` on a variable failed with `Variables not allowed ... Variables may not be used here`; a local reading `terraform_data.r.id` worked; `-var` beat `TF_VAR_size`, and an `*.auto.tfvars.json` file set the variable; locals cannot be set from outside (no input mechanism).
- EC2 sizes in the example are illustrative values, not claims about current instance families.
