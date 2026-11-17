---
id: computing-software.cloud-infrastructure-engineering.terraform.logical-operator-short-circuit-evaluation
name: logical-operator-short-circuit-evaluation
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, short-circuit, operators, conditionals, null-handling, try]
level: practitioner
status: verified
description: "Know when && and || short-circuit in Terraform (1.12+) and when they do not (older versions, unknown values), and write null-safe conditions that work across versions."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/operators#logical-operators", "https://github.com/hashicorp/terraform/releases/tag/v1.12.0"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Short-circuit evaluation of `&&` and `||`

## The historical behaviour
Before Terraform 1.12, both operands of `&&` and `||` were always evaluated:
```hcl
condition = var.cfg != null && var.cfg.enabled
# < 1.12 with cfg = null:  Error: Attempt to get attribute from null value
```

## Since 1.12
Logical operators short-circuit when the left operand determines the result (Terraform 1.12 changelog; confirmed on 1.16.6, while 1.9.8 still raised the null error):
`false && X` does not evaluate X; `true || X` does not evaluate X. The example above
works.

## Writing conditions that work everywhere
Modules used across versions should not rely on short-circuiting. Version-safe forms:
```hcl
condition = var.cfg == null ? false : var.cfg.enabled
condition = try(var.cfg.enabled, false)
condition = coalesce(try(var.cfg.enabled, null), false)
```
The conditional operator `? :` only evaluates the chosen branch's value for errors in
all versions (types of both branches must still be compatible).

## Unknown values
A known deciding operand wins even beside an unknown one on 1.16.6: `false && unknown` and `unknown && false` both plan as `false`, `true || unknown` as `true`; `true && unknown` and `false || unknown` stay `(known after apply)`.

## OpenTofu
Check `tofu` release notes for its short-circuit support; do not assume parity.

## Guidance
- Set `required_version = ">= 1.12"` if a module depends on short-circuiting.
- Prefer typed variables with `optional()` defaults so null-guards are unnecessary.

## Verify
- [ ] Conditions evaluate with `null` inputs under the minimum Terraform version you support (CI matrix).
