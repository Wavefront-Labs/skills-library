---
id: computing-software.cloud-infrastructure-engineering.terraform.import-blocks-into-modules-and-for-each-addresses
name: import-blocks-into-modules-and-for-each-addresses
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, import-block, import-into-module, import-indexed, import-for-each, generate-config-out]
level: practitioner
status: gated
description: "Import existing objects into module and for_each/count addresses with import blocks (including for_each on import), and the limits of -generate-config-out."
sources: ["https://developer.hashicorp.com/terraform/language/import", "https://developer.hashicorp.com/terraform/language/import/generating-configuration", "https://opentofu.org/docs/language/import/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing into modules and indexed addresses

## Into a module instance
Put import blocks in the **root** module; `to` may point anywhere (Terraform 1.17.0 also accepted an import block declared inside a child module, ran, but config generation only covers the root):
```hcl
# (gated: unconfirmed, source is paywalled or blocked) (AWS ids and resources below were not run; the same address forms ran against terraform_data in local modules)
import {
  to = module.network.aws_vpc.this
  id = "vpc-0abc123"
}
import {
  to = module.network.aws_subnet.private["eu-west-1a"]
  id = "subnet-0111"
}
import {
  to = module.db["primary"].aws_db_instance.this
  id = "prod-primary"
}
```
The module must already declare the resource with matching `for_each` keys.

## Bulk with `for_each` on import (Terraform 1.7+, OpenTofu 1.7+)
```hcl
locals {
  subnets = {
    "eu-west-1a" = "subnet-0111"
    "eu-west-1b" = "subnet-0222"
  }
}
import {
  for_each = local.subnets
  to       = aws_subnet.private[each.key]
  id       = each.value
}
```
Keys must match the resource's own `for_each` keys exactly. Works with module
instances too: `to = module.app[each.key].aws_instance.web`.

## Generating config
`terraform plan -generate-config-out=generated.tf` writes HCL **only for root-module
targets** that have no resource block (ran: a module target errored with `Only resources within the root module are eligible for config generation`). For module targets, generate into a scratch
root, then move the attributes into the module by hand. Clean generated code:
remove computed-only/default attributes, replace literals with references.

## Workflow
1. Write blocks; `terraform plan` → expect `N to import, 0 to add, 0 to change, 0 to destroy`.
2. Any `~ update in-place` means config differs from reality; fix config until the
   import is a no-op (or accept the deliberate change).
3. Apply. Delete import blocks afterwards (or keep: they are no-ops once imported).

## Gotchas
- `id` format is resource-specific (see each resource's Import section): some need
  composite IDs (`sg-123_ingress_tcp_443_443_0.0.0.0/0`, `cluster/service`).
- `to` cannot use `count.index` (ran: `A single static variable reference is required`); use a literal index `aws_x.y[2]`, or `import { for_each }` with `each.key`.
- Variables are allowed in `id` (1.6+), but not values unknown at plan time (ran: `id = terraform_data.a.id` gave `Invalid import id argument ... depends on resource attributes that cannot be determined until apply`).
- Importing the same object at two addresses produces two owners — later destroys hurt.

## Verify
- [ ] Plan shows only imports, no creates or destroys.
- [ ] `terraform state list module.network` lists the imported addresses after apply.

## Checked
- Terraform 1.17.0 with local modules over `terraform_data`: import `to` addresses of `module.network.x.this`, `module.network.x.sub[each.key]`, `module.db["primary"].x.this` and a `for_each` import over a local map all planned (`5 to import`) and applied, and `terraform state list module.network` listed the imported addresses; `import { for_each }` is in the 1.7 changelog; count.index and unknown id errors reproduced; config generation limited to the root module.
- Gated: AWS id formats and resources.
