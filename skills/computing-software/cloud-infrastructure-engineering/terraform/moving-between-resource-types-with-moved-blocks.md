---
id: computing-software.cloud-infrastructure-engineering.terraform.moving-between-resource-types-with-moved-blocks
name: moving-between-resource-types-with-moved-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, move-resource-type, cross-resource-type-move, moved-block, move-state, refactoring]
level: practitioner
status: verified
description: "Refactor one resource type into another (e.g. null_resource to terraform_data, deprecated to replacement types) with moved blocks backed by provider move_state support."
sources: ["https://developer.hashicorp.com/terraform/language/moved", "https://developer.hashicorp.com/terraform/plugin/framework/resources/state-move", "https://developer.hashicorp.com/terraform/language/resources/terraform-data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `moved` across resource types

Terraform 1.8+ allows `moved` between **different resource types** when the target
provider implements the `MoveResourceState` RPC for that source type. Without
provider support the plan errors; for example `moved { from = random_id.x to =
terraform_data.xx }` fails with `Error: Unsupported source provider for move operation:
Only moving from the official hashicorp/null provider to terraform_data is supported.`

## Supported examples
```hcl
# null_resource -> terraform_data (built-in support, Terraform 1.9+)
moved {
  from = null_resource.bootstrap
  to   = terraform_data.bootstrap
}
resource "terraform_data" "bootstrap" {
  triggers_replace = { v = "1" }      # keep the same map value that null_resource.triggers had
  provisioner "local-exec" { command = "./bootstrap.sh" }
}
```
`terraform_data.triggers_replace` takes any value, but the move does not convert it: with
`null_resource` `triggers = { v = "1" }` moved to `triggers_replace = ["1"]` (a list) the plan
was `terraform_data.bootstrap must be replaced (moved from null_resource.bootstrap)`, while the
same map (`{ v = "1" }`) gave `has moved to` with no change. Cross-type moves exist only where
the destination provider declares support (the Terraform 1.8 release added the mechanism; the
built-in `terraform` provider added `null_resource` support in 1.9, per the changelogs); check
each provider's own upgrade notes for others.

## Procedure
1. Upgrade to Terraform >= 1.8 (>= 1.9 for `null_resource` to `terraform_data`) and the provider version that adds move support.
2. Rename the resource block to the new type; adapt arguments to the new schema.
3. Add the `moved` block.
4. `terraform plan`: expect `# null_resource.bootstrap has moved to terraform_data.bootstrap`
   and **no** create/destroy. Attribute changes (`~`) may appear if the schemas differ;
   review them.
5. Apply; keep the moved block until all states (every workspace/environment) have
   applied, then delete it (or keep it in published modules for callers).

## When there is no move support
Use `removed { from = old.type  lifecycle { destroy = false } }` plus an
`import { to = new.type  id = "..." }` in the same change. Plan shows forget + import,
no infrastructure change.

## Gotchas
- `null_resource` -> `terraform_data` changes `triggers` (map) to `triggers_replace`
  (any); if the new value differs from the old one the object is replaced and the
  creation-time provisioners run again (the list example above).
- Cross-provider moves only work if the destination provider explicitly supports that
  source (the error above is what an unsupported one looks like).

## Verify
- [ ] Plan shows `has moved to` and 0 to add, 0 to destroy for the moved instance.

## Checked
- Terraform 1.17.0 with null 3.3.2 and the built-in provider: `null_resource` with `triggers = { v = "1" }` applied, then (a) `moved` to `terraform_data` with `triggers_replace = ["1"]` planned `-/+ must be replaced (moved from null_resource.bootstrap)`, (b) with `triggers_replace = { v = "1" }` planned `has moved to` and `0 to add, 0 to change, 0 to destroy`; `random_id` to `terraform_data` gave the unsupported-source error quoted; `removed { lifecycle { destroy = false } }` plus `import { to = terraform_data.z id = "abc" }` planned `will no longer be managed by Terraform, but will not be destroyed` and `1 to import, 0 to destroy`.
- Changelogs: Terraform 1.8 (providers can take ownership across resource types via `moved`), 1.9 (built-in `terraform` provider: `null_resource` to `terraform_data`), 1.7 (`removed` block), 1.4 (`terraform_data`). The `aws_instance.web.id` trigger and the AWS/Google/AzureRM rename examples were dropped rather than asserted.
- The `MoveResourceState` RPC name is in Terraform's `tfplugin6.proto` (`rpc MoveResourceState`).
