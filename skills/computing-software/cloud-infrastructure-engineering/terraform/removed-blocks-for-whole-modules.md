---
id: computing-software.cloud-infrastructure-engineering.terraform.removed-blocks-for-whole-modules
name: removed-blocks-for-whole-modules
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, removed-module, removed-block, forget-without-destroy, module, refactoring]
level: practitioner
status: verified
description: "Use removed blocks with a module address to forget or destroy an entire module call, including module instances with count or for_each, and when providers must remain."
sources: ["https://developer.hashicorp.com/terraform/language/resources/syntax#removing-resources", "https://developer.hashicorp.com/terraform/language/block/removed", "https://developer.hashicorp.com/terraform/language/modules/syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `removed` blocks for modules

## Forget a whole module (keep infrastructure)
```hcl
# module "legacy_dns" { source = "./modules/dns" ... }   <- deleted from config
removed {
  from = module.legacy_dns
  lifecycle {
    destroy = false
  }
}
```
Plan (ran): every resource under `module.legacy_dns`, including those of a nested
module, shows `will no longer be managed by Terraform, but will not be destroyed` with
`Plan: 0 to add, 0 to change, 0 to destroy.`; apply removed them from state only
(`terraform state list | grep -c legacy` printed 0).

## Destroy a whole module explicitly
```hcl
removed {
  from = module.legacy_dns
  lifecycle { destroy = true }
}
```
Ran: `destroy = true` on a nested `from = module.platform.module.inner` planned `will be
destroyed`; a `removed` block with no `lifecycle` attempted the destroy as well (it hit the
provider error below), so the default is destroy. The 1.7 changelog says module authors
can tell Terraform whether the object "should be deleted or simply removed from state".
Same result as deleting the module block, but documents intent and survives in
published modules for callers.
## Address rules
- `from` takes a module call **without instance keys**: `module.app`, not
  `module.app["eu"]` (error `Module instance keys not allowed`). Both instances of a
  `for_each` module (`eu`, `us`) were affected.
- To drop one instance of a for_each module, remove its key from the map instead
  (that destroys it).
- Nested: `from = module.platform.module.dns` works.
- The module block must be absent from config; otherwise `Removed module still exists` (ran).

## Providers
Destroying (destroy = true) needs the provider configuration that managed those
resources. If the provider block lived inside the removed module, destroy fails with
`Provider configuration not present` (ran: `module.gone.provider[...hashicorp/local] is required, but it has been removed`). Keep an equivalent provider config in the root,
or forget (destroy = false) and clean up manually.

## Destroy-time provisioners
`removed` blocks for a resource may carry `provisioner ... when = destroy` (ran: the
`local-exec` output appeared on apply; changelog v1.9).

## Verify
- [ ] Plan lists every resource of the module with the intended action and nothing else.
- [ ] `terraform state list module.legacy_dns` is empty after apply.

## Checked
- Terraform 1.17.0 with `terraform_data` (for_each, count, nested modules), `hashicorp/local` and a module-local provider: `removed` with `destroy = false` on a for_each module call (plan text, apply, empty state), `destroy = true` on a nested module, no `lifecycle`, an instance-keyed `from`, a still-present module block, a provider block inside the removed module (`Provider configuration not present`), and a destroy-time provisioner on a removed resource.
- Changelogs v1.7 (introduction) and v1.9 (destroy-time provisioners). Correction: the "1.7 only supported destroy = false" claim is not supported by the 1.7 changelog and was removed; default behaviour without `lifecycle` is to destroy.
