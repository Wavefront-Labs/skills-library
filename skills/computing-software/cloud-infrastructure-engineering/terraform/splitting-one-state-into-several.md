---
id: computing-software.cloud-infrastructure-engineering.terraform.splitting-one-state-into-several
name: splitting-one-state-into-several
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-split-migration, monolith-split, state-mv, removed-block, import-block]
level: practitioner
status: docs-checked
description: "Split a monolithic state into several root modules without touching infrastructure, using removed plus import blocks or state mv between pulled files."
sources: ["https://developer.hashicorp.com/terraform/language/block/removed", "https://developer.hashicorp.com/terraform/language/import", "https://developer.hashicorp.com/terraform/cli/commands/state/mv", "https://developer.hashicorp.com/terraform/cli/commands/state/push"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splitting one state into several

Goal: move the resources of `module.network` out of `platform/` into a new root `network/` with its
own state. Infrastructure must not change.

## Method A: `import` + `removed` blocks (reviewable, preferred)
1. Create `network/` with the module call and backend. An `import` block needs a matching destination
   resource block at the address it declares, and its `id` is the provider's unique resource ID.
   Add one import block per resource, taking the addresses from the old state:
```bash
cd platform
terraform state list module.network
```
```hcl
import {
  to = module.network.aws_vpc.main
  id = "vpc-0abc..."   # the import ID format is per resource type; check provider docs
}
```
   Alternatively write only the import blocks and run `terraform plan -generate-config-out=...`
   to generate resource blocks (not for resources inside modules you call; review the output).
2. `cd network && terraform init && terraform plan`: expect only imports, no other changes. Apply.
3. In `platform/`, delete the resource configuration and add a `removed` block per resource:
```hcl
removed {
  from = aws_vpc.main      # the reference documents `from` as a resource address
  lifecycle { destroy = false }
}
```
   By default `removed` destroys the real resource; `destroy = false` only drops it from state.
   `destroy` is the only lifecycle argument `removed` supports. Plan, then apply.
4. Replace in-state references (`module.network.vpc_id`) with data sources or outputs read from the new stack.

## Method B: `state mv` across state files (fast, unreviewed)
`terraform state mv` accepts `-state` and `-state-out` for local state files only (legacy options), so
pull both states to local files first:
```bash
cd platform && terraform state pull > /tmp/src.tfstate
cd ../network && terraform init && terraform state pull > /tmp/dst.tfstate
terraform state mv -state=/tmp/src.tfstate -state-out=/tmp/dst.tfstate module.network module.network
cd ../network && terraform state push /tmp/dst.tfstate
cd ../platform && terraform state push /tmp/src.tfstate
```
Freeze both stacks and back up first. `state push` refuses a state with a different lineage or a
lower serial than the destination; `-force` disables both checks, so avoid it.

## Order of operations matters
Adopt in the new state **before** forgetting in the old one, and freeze applies on
both stacks in between so the short double-ownership window is harmless.

## Verify
- [ ] Both stacks plan clean (`No changes`).
- [ ] `state list` shows each resource in exactly one state.

## Checked

Method: docs-checked 2026-11-09 against the removed block reference, the import page, the `state mv` reference and the `state push` reference (downloaded, converted to text and read). Dropped unconfirmed claims: `terraform state identities` and its version, the jq import generator, the exact plan wording for removed resources, `from = module.x` (page shows resource addresses only), and the `terraform_remote_state`/SSM alternatives. Replaced the resource syntax anchor source with the removed block page.
