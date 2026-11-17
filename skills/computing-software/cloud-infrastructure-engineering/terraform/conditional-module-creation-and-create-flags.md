---
id: computing-software.cloud-infrastructure-engineering.terraform.conditional-module-creation-and-create-flags
name: conditional-module-creation-and-create-flags
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, conditional-module, create-flag, module-count, module-design, one-function]
level: practitioner
status: verified
description: "Turn modules or resources inside them on and off: count or for_each on module blocks vs internal create flags, referencing optional outputs, and moving between the two."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/count", "https://developer.hashicorp.com/terraform/language/modules/develop/composition#conditional-creation-of-objects", "https://developer.hashicorp.com/terraform/language/functions/one"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional module creation

## Option A: `count` on the module block (TF 0.13+)
```hcl
module "bastion" {
  source = "./modules/bastion"
  count  = var.enable_bastion ? 1 : 0
  vpc_id = module.vpc.vpc_id
}
output "bastion_ip" {
  value = one(module.bastion[*].public_ip)      # null when disabled
}
```
Addresses become `module.bastion[0].*`. Adding `count` to an existing module moves
everything: add `moved { from = module.bastion  to = module.bastion[0] }`.

## Option B: `create` flag inside the module
A common pattern (`create = true`, or one flag per optional feature):
```hcl
variable "create" {
  type    = bool
  default = true
}
resource "terraform_data" "this" {
  count = var.create ? 1 : 0
  # ...
}
output "public_ip" {
  value = try(terraform_data.this[0].output, null)
}
```

## Which to use
| Need | Choose |
|---|---|
| Caller decides whether the whole module exists | A (simpler module, no flag plumbing) |
| Module has optional sub-features (`create_iam_role`, `enable_logging`) | B, per feature |
| Module contains provider blocks (legacy) | B (ran: a child module with a non-empty `provider "tls"` block makes `count` fail with `Module is incompatible with count, for_each, and depends_on`) |
| Several instances | `for_each` on the module |

## Gotchas
- `count` must be known at plan time; derive from variables, not resource attributes.
- Every output of a conditional module must handle the disabled case (`one()`, `try()`).
- Toggling off destroys everything inside; protect stateful resources.
- Option B leaves the module's addresses stable; toggling a feature does not move other resources.
- An empty `provider "x" {}` block in a module is a deprecated proxy configuration (`Redundant empty provider block` warning) and does not trigger the count restriction; only a block with real settings does.

## Verify
- [ ] Plans succeed with the flag both true and false; outputs are null, not errors, when disabled.

## Checked
- Terraform 1.17.0 with a local module over `terraform_data`: `count = var.enable ? 1 : 0` on the module block, `one(module.bastion[*].public_ip)` gave the value when enabled and null (no error) when disabled; adding `count` to an existing module without `moved` planned 1 destroy + 1 add, and `moved { from = module.bastion to = module.bastion[0] }` gave `has moved to` and `0 to add, 0 to change, 0 to destroy`; disabling destroyed the contents. A module containing `provider "tls" { proxy { from_env = true } }` produced the incompatibility error on both plan and apply; an empty `provider "random" {}` block only produced the deprecation warning.
- The Option B resource snippet ran as `terraform_data` with `count` and `try(...[0].output, null)`: the output was the value when `create = true` and null (no error) after setting `create = false`, which destroyed the object.
