---
id: computing-software.cloud-infrastructure-engineering.terraform.objects-changed-outside-of-terraform-plan-section
name: objects-changed-outside-of-terraform-plan-section
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, outside-changes, changed-outside, resource-drift, plan-output, refresh, drift, plan-noise]
level: practitioner
status: docs-checked
description: "Handle changes made outside Terraform: refresh-only mode, resource_drift and relevant_attributes in plan JSON, ignore_changes, and the risks of -refresh=false."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#planning-modes", "https://developer.hashicorp.com/terraform/internals/json-format#resource-drift", "https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#ignore_changes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Objects changed outside of Terraform

**Goal:** tell "Terraform noticed the real object differs from state" apart from
"Terraform is about to change it", and pick the right response to drift.

## 1. Where drift comes from
By default a plan first reads the current state of existing remote objects so the
state is up to date, then compares configuration to that prior state and proposes
changes so the remote objects match the configuration. Differences between the
refreshed objects and the earlier state are changes made outside Terraform. The
plan page does not describe the exact wording of the plan block that reports them;
read the actions section for what will actually change.

## 2. Refresh-only mode
`-refresh-only` (Terraform v0.15.4 and later) creates a plan whose goal is only to
update the Terraform state and root module output values to match changes made to
remote objects outside Terraform, for example while responding to an incident. It is
a planning mode, so it is mutually exclusive with `-destroy`, and it is available
on both `terraform plan` and `terraform apply`:
```bash
terraform plan  -refresh-only      # review the drift
terraform apply -refresh-only      # accept it into state and outputs
```
`-refresh=false` disables the refresh that synchronises state with remote objects.
It can make planning faster, but Terraform then ignores external changes, so the
plan may be incomplete or incorrect. It cannot be combined with refresh-only mode.

## 3. In machine-readable output
`terraform show -json <PLANFILE>` prints the plan as JSON. Two fields cover drift:
- `resource_drift`: the changes Terraform detected when it compared the most recent
  state to the prior saved state. It uses the same object structure as
  `resource_changes`.
- `relevant_attributes`: the sources of all values contributing to changes in the
  plan; use it to filter `resource_drift` and decide which external changes may have
  affected the plan result.

Each change has `change.actions` with values such as `["update"]`, `["delete"]`,
`["create"]` and `["no-op"]`, and `before` and `after` values. `terraform plan
-detailed-exitcode` returns 0 for an empty diff, 1 for an error and 2 for a non-empty
diff, which is the documented way to turn plan results into an exit code.

## 4. Responding to legitimate outside changes
Choose per attribute:
- Make the configuration match the new real value, then plan again.
- Let Terraform revert the change on apply.
- Tell Terraform to ignore it with `lifecycle { ignore_changes = [...] }`:
```hcl
resource "aws_instance" "example" {
  # ...
  lifecycle {
    ignore_changes = [tags]
  }
}
```
Rules from the lifecycle reference:
- The listed attributes are considered when planning a create but ignored when
  planning an update. Use index notation for map and list elements, such as
  `tags["Name"]` and `list[0]`.
- `ignore_changes = all` makes Terraform create and destroy the object but never
  propose updates to it.
- Only attributes defined by the resource type can be listed; you cannot apply
  `ignore_changes` to itself or other meta-arguments.
- The HashiCorp use case is letting Terraform share management of one object with a
  separate process, and the docs call such outside modification "rare".

## Checked
Date: 2026-11-07
Read in full: the terraform plan command page (Planning Modes, Planning Options
including -refresh=false, Other Options including -detailed-exitcode), the JSON output
format page (plan representation, change representation, values and configuration
representations) and the lifecycle reference page (ignore_changes plus the other rules).
Removed because none of the cited pages state them: the sample "Note: Objects have
changed outside of Terraform" block and its wording, the claim that the block is
filtered to plan-affecting drift since version 1.4, the classification table
(including "has been deleted", provider-normalised values and `state rm` advice), the
`jq` command, the nightly refresh-only plus detailed-exitcode alarm (the pages do not
show those two flags combined), the `ignore_changes = all` reporting claim and the
Verify checklist. The plan page has no section named for drift, so its anchor in
`sources` now points at Planning Modes.
Method: documentation only; no commands were run.
