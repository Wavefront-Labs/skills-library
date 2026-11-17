---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-configuration-not-present-errors
name: provider-configuration-not-present-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provider-not-present, orphaned-provider, providers-in-modules, troubleshooting, provider-alias]
level: practitioner
status: docs-checked
description: "Fix Provider configuration not present: resources in state whose provider config was removed with a module or alias, and how to restore, destroy or re-point them."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/providers", "https://developer.hashicorp.com/terraform/cli/commands/state/replace-provider", "https://developer.hashicorp.com/terraform/cli/commands/state/rm", "https://developer.hashicorp.com/terraform/language/block/removed", "https://developer.hashicorp.com/terraform/language/block/moved"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# "Provider configuration not present"

## What it means
Terraform keeps in state a reference to the provider configuration last used for each
resource. When a resource block is removed, that record is used to find the right
configuration to destroy it. If a resource instance is still tracked in state but its
provider configuration block is gone, Terraform errors during planning and asks you to
reintroduce the provider configuration.

## Causes
1. A module containing its own `provider` block was removed from the configuration while
   its resources are still in state. Terraform needs the provider to destroy them.
2. An aliased provider configuration was deleted while resources still use it.
3. A module call was renamed without a `moved` block, so the old address is treated as
   removed.

## Fixes
**Restore temporarily, destroy, then remove** (causes 1 and 2):
```hcl
provider "aws" {
  alias  = "use1"
  region = "us-east-1"
}
module "dns" {             # put the module back
  source = "./modules/dns"
  providers = { aws = aws.use1 }
}
```
Destroy the module's resources first (for example `terraform destroy -target=module.dns`,
which destroys that target and its dependencies), then delete the module and the
provider configuration. All resources of a provider configuration must be destroyed
before you remove its block.

**Forget instead of destroy**: `terraform state rm 'module.dns'` removes the record of
every instance in the module without destroying the real objects (a later plan will
propose creating them again). Preview with `-dry-run`. For individual resources a
`removed` block does the same inside the plan and apply workflow:
```hcl
removed {
  from = aws_route53_record.www
  lifecycle { destroy = false }
}
```
By default a `removed` block removes the resource from state and destroys it; `destroy =
false` keeps the real resource.

**Rename case**: add a `moved` block with `from` and `to`; Terraform renames the existing
object in state before planning, so nothing is destroyed:
```hcl
moved {
  from = module.old
  to   = module.new
}
```

**Changing the provider source of resources already in state**:
`terraform state replace-provider FROM_PROVIDER_FQN TO_PROVIDER_FQN` updates every
resource using the "from" provider. It always writes a backup of state first.

## Prevention
- A module meant to be called by other modules must not contain provider blocks; pass
  them from the root with `providers`.
- Remove resources first, apply, then remove the provider block in a second change.

## Checked
Date: 2026-11-07
Read in full: Providers Within Modules, `terraform state replace-provider`, `terraform state rm`, `removed` block reference, `moved` block reference.
Confirmed: state keeps the provider reference and errors at planning until the block is reintroduced, destroy resources before removing the provider block, no provider blocks in called modules, `state rm` semantics, `-dry-run`, `removed` default and `destroy = false`, `moved` semantics, `replace-provider` syntax and mandatory backup.
Removed: the sample error text (not on the cited pages), the "provider path" explanation for renames, the `registry.terraform.io/-/aws` legacy address, the `removed { from = module.dns }` form (the block reference documents resource addresses only), and the Verify step. `terraform destroy -target` is described only as the destroy page states it.
Method: documentation only; no commands were run.
