---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-remote-state-config-and-workspace
name: terraform-remote-state-config-and-workspace
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-remote-state, remote-state-config, remote-state-backend-config, remote-state-workspace, cross-state]
level: practitioner
status: docs-checked
description: "Configure terraform_remote_state per backend type (s3, azurerm, gcs, remote) including the workspace argument, defaults, and the read-permission it implies."
sources: ["https://developer.hashicorp.com/terraform/language/state/remote-state-data", "https://developer.hashicorp.com/terraform/language/backend/s3", "https://opentofu.org/docs/language/state/remote-state-data/", "https://developer.hashicorp.com/terraform/language/backend/azurerm", "https://developer.hashicorp.com/terraform/language/backend/gcs", "https://developer.hashicorp.com/terraform/language/backend/remote"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform_remote_state`: config and workspace

`config` takes the **same arguments as the backend block** of the producing state.

## Per backend
```hcl
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "acme-tf-state"
    key    = "network/terraform.tfstate"
    region = "eu-west-1"
  }
  workspace = "prod"   # reads env:/prod/network/terraform.tfstate
}

data "terraform_remote_state" "net_az" {
  backend = "azurerm"
  config = {
    resource_group_name  = "tfstate"
    storage_account_name = "acmetfstate"
    container_name       = "tfstate"
    key                  = "network.tfstate"
    use_azuread_auth     = true
  }
}

data "terraform_remote_state" "net_gcs" {
  backend = "gcs"
  config  = { bucket = "acme-tf-state", prefix = "network" }
  workspace = terraform.workspace
}

data "terraform_remote_state" "net_hcp" {
  backend = "remote"
  config = {
    organization = "acme"
    workspaces   = { name = "network-prod" }
  }
}
```
Use: `data.terraform_remote_state.network.outputs.vpc_id`. Only **root-level outputs**
are exposed; resource data and nested-module outputs are not (re-export a nested module output with a root `output`
block).

Arguments: `backend` (required), `workspace` (optional, if the backend supports workspaces), `config` (optional object;
any argument valid in the equivalent `backend "<TYPE>"` block) and `defaults` (optional object). If the backend needs a
nested block, give it as an object attribute (`workspaces = { ... }`, not `workspaces { ... }`). No provider
configuration is needed: the data source comes from the built-in provider `terraform.io/builtin/terraform`.

## The `workspace` argument
- Optional; used if the backend supports workspaces. With S3, the default workspace is stored at `<key>`;
  other workspaces at `<workspace_key_prefix>/<workspace_name>/<key>`, and `workspace_key_prefix` defaults to
  `env:`, so `workspace = "prod"` reads `env:/prod/<key>`.
- With GCS, named workspace states are stored in an object `<prefix>/<name>.tfstate`.
- `workspace = terraform.workspace` couples consumer and producer workspace names: convenient, but breaks if naming
  diverges.
- With the `remote` backend, use `workspaces = { name = ... }` when reading. The docs state the `name` key is required
  for `terraform_remote_state` reading another HCP Terraform workspace; `prefix` is only for configuring the `remote`
  backend itself.

## `defaults`
```hcl
defaults = { vpc_id = null }
```
Default values for outputs in case the state file is empty or lacks a required output (for example before the producer
has been applied).

## Gotchas
- Anyone who can read the root outputs through the backend can also read the full state snapshot, which often holds
  sensitive data. The docs advise against `terraform_remote_state` if resources work with data you consider sensitive,
  and recommend publishing shared data to a separate store (for example SSM Parameter Store with the
  `aws_ssm_parameter` resource and data source) or, for HCP Terraform/Enterprise, the `tfe_outputs` data source, which
  does not need full access to workspace state.
- Authentication-related settings belong in `config` because it takes the backend's own arguments (S3 has `profile`
  and `assume_role = { role_arn = ... }`).
- Renaming a producer's output breaks consumers that reference it.

## Verify
- [ ] `terraform console` → `data.terraform_remote_state.network.outputs` prints the expected map.
- [ ] Workspace mapping verified for each environment (consumer `workspace` value vs the producer's workspace name).

## Checked

Checked 2026-11-08 against the Terraform pages for the terraform_remote_state data source and the S3, azurerm, gcs and
remote backends: argument list, `config` semantics and nested-block rule, built-in provider, root-outputs-only rule,
`defaults`, full-state-access warning, `tfe_outputs`, S3 `workspace_key_prefix` default `env:` and key layout,
`assume_role`/`profile`, azurerm argument names (`resource_group_name` is only required with `lookup_blob_endpoint`),
GCS `prefix` layout, and the remote backend `name` versus `prefix` note. Removed: the claim the data source is read at
plan time, the claim that credentials never come from a provider block, and the `terraform workspace show` check.

Method: documentation only; no commands were run.
