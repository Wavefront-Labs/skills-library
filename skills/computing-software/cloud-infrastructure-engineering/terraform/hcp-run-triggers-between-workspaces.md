---
id: computing-software.cloud-infrastructure-engineering.terraform.hcp-run-triggers-between-workspaces
name: hcp-run-triggers-between-workspaces
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, run-trigger-config, run-triggers, hcp-terraform, tfe-provider, cross-stack]
level: practitioner
status: docs-checked
description: "Chain HCP Terraform workspaces with run triggers so a successful apply in a source workspace queues a run downstream, managed with tfe_run_trigger and the auto-apply setting."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/run-triggers", "https://raw.githubusercontent.com/hashicorp/terraform-provider-tfe/main/website/docs/r/run_trigger.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run triggers between workspaces

## What they do
A run trigger connects a **source** workspace to your (destination) workspace: any run in the source that applies
successfully causes a new run to be queued in the destination. Each workspace can connect to up to 20 source
workspaces. They suit workspaces that rely on information or infrastructure produced by other workspaces, such as a
chain `network` -> `platform` -> `apps`, and make an external dependency explicit when a configuration reads values
another workspace may change.

## Configure as code
```hcl
resource "tfe_run_trigger" "platform_from_network" {
  workspace_id  = tfe_workspace.platform.id      # destination: where runs are triggered
  sourceable_id = tfe_workspace.network.id       # source: must be a workspace
}
```
Both arguments are required; the resource exports `id` and can be imported by run trigger ID.

UI: destination workspace > Settings > Run Triggers > "Source Workspaces" > "Add workspace".

## Behaviour
- Runs started by a run trigger do not auto-apply unless the **Auto-apply run triggers** setting is enabled. That
  setting is independent of the workspace's primary auto-apply setting.
- A triggered run's details link to the source workspace and the applied run that caused it; the source run's plan and
  apply details list the workspaces where HCP Terraform starts runs automatically.

## Permissions
- Adding or deleting run triggers needs admin access to the destination workspace, plus permission to read runs of
  the source workspace you connect.

## Sharing data
- Share values across workspaces with the `terraform_remote_state` data source, which needs the source workspace to
  allow access (see remote state sharing in the workspace state docs).
- HashiCorp recommends the `tfe_outputs` data source instead: it does not require full access to workspace state.

## Gotchas
- Triggered runs that need confirmation wait in the destination until someone approves; decide per workspace whether
  Auto-apply run triggers is acceptable.

## Verify
- [ ] Applying a change in the source queues a run in each destination workspace.

## Checked
Confirmed 2026-11-08 against the HCP Terraform Run triggers page and the tfe provider `tfe_run_trigger` resource doc:
20-source limit, successful-apply trigger, auto-apply independence, admin and read-runs permissions, resource
arguments and UI path. Removed: claims that speculative runs never trigger, that triggered runs use the destination's
current VCS commit, loop prevention, the Stacks suggestion, and the "read on source" wording (the page says permission
to read runs).
Method: docs-only read of cited pages, 2026-11-08
