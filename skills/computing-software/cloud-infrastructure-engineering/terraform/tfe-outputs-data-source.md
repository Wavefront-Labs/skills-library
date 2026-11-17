---
id: computing-software.cloud-infrastructure-engineering.terraform.tfe-outputs-data-source
name: tfe-outputs-data-source
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, tfe-outputs, hcp-terraform, remote-state-sharing, cross-state, tfe-provider]
level: practitioner
status: docs-checked
description: "Read another HCP Terraform/TFE workspace's outputs with the tfe_outputs data source, using values, nonsensitive_values and the workspace state access settings."
sources: ["https://raw.githubusercontent.com/hashicorp/terraform-provider-tfe/main/website/docs/d/outputs.html.markdown", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/state#accessing-state-from-other-workspaces"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `tfe_outputs`

Gets the state outputs of a workspace so output values in one configuration can be used in another. It reads outputs,
not the whole state, so it is the more secure option than `terraform_remote_state`, which needs full access to
workspace state (HCP Terraform run-triggers docs recommend `tfe_outputs`).

```hcl
data "tfe_outputs" "network" {
  organization = "acme"
  workspace    = "network-prod"
}

locals {
  vpc_id = data.tfe_outputs.network.nonsensitive_values.vpc_id
}
```

Schema (provider docs): `workspace` is required; `organization` is optional; read-only `id`,
`nonsensitive_values` (a subset of the outputs) and `values` (sensitive).

The state-management page also shows a different form that wraps the settings in a `config` argument
(`organization` plus `workspaces = { name = "..." }`) and reads `data.tfe_outputs.vpc.outputs.subnet_id`. The two
pages differ; check the provider version you use against its registry documentation before copying either form.

## Sensitive handling
- `values` is preemptively marked **sensitive** and is only populated after a run completes in the source workspace.
- `nonsensitive_values` holds the subset of outputs known to be non-sensitive; use it to reach those outputs without
  `nonsensitive()`.

## Authentication and access
- Configure the `tfe` provider with a valid authentication token and correct permissions to HCP Terraform.
- For workspaces executing in Local mode, the token must be able to read state outputs of the other workspace.
- Remote state access controls (Settings > remote state sharing) govern `terraform_remote_state`; the docs state they
  do not apply when using the `tfe_outputs` data source.
- New workspaces do not allow other workspaces to access their state by default. HashiCorp recommends least privilege.

## Gotchas
- `values` is empty until a run has completed on the source workspace.
- Prefer provider-specific data sources where available; the docs call them usually the most resilient way to share
  information between separate configurations.

## Verify
- [ ] `terraform console`: `data.tfe_outputs.network.nonsensitive_values` shows the expected keys.

## Checked
Confirmed 2026-11-08 against the tfe provider `tfe_outputs` data source doc and the HCP Terraform workspace state page
(access controls, configuration form, tfe_outputs note). Removed: `nonsensitive()` advice details, the "team read
state outputs" permission wording, TFE_TOKEN workspace-variable advice, last-applied-state, unknown-type and
cross-organisation claims, and the sharing-list verify step (the docs say sharing controls do not apply to tfe_outputs).
Method: docs-only read of cited pages, 2026-11-08
