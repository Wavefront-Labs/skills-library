---
id: computing-software.cloud-infrastructure-engineering.terraform.remote-state-read-permissions-and-exposure
name: remote-state-read-permissions-and-exposure
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, remote-state-permissions, terraform-remote-state, state-security, least-privilege]
level: practitioner
status: docs-checked
description: "terraform_remote_state needs access to the whole upstream state snapshot, secrets included; limit exposure by publishing data elsewhere, tfe_outputs and sharing controls."
sources: ["https://developer.hashicorp.com/terraform/language/state/remote-state-data", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/state#remote-state-access-controls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform_remote_state` permissions and exposure

## The core issue
`terraform_remote_state` exposes only the **root-level output values** of the other configuration (resource data and nested-module outputs are not accessible unless passed through a root `output`). But its user must have access to the **entire state snapshot**, which often includes sensitive information. The docs warn that the snapshot is a single object, so anyone or any server with enough access to read the root outputs also always has access to the full snapshot by direct network requests. Do not use `terraform_remote_state` if any of the resources in your configuration work with data you consider sensitive.

## Mitigations
1. **Publish data explicitly to a separate location** and read it with an ordinary data source. This lets you apply different access controls to shared information and to state snapshots. Pairs the page lists:
   - Amazon SSM Parameter Store: `aws_ssm_parameter` resource, `aws_ssm_parameter` data source.
   - Amazon S3: `aws_s3_object` resource and data source. Google Cloud Storage: `google_storage_bucket_object`.
   - HashiCorp Consul: `consul_key_prefix` resource and data source. Kubernetes: `kubernetes_config_map`. Azure Automation: `azurerm_automation_variable_string`.
   - DNS records (Route53, Azure DNS, Cloud DNS, Alibaba Cloud DNS) for IP addresses and hostnames, read with normal DNS lookups or the `dns` provider.
   - Generic blob stores can hold structured data via `jsonencode` / `jsondecode`. A data-only module can hide how the data is fetched, so you can change strategy later.
   - Prefer a store other infrastructure (DNS resolver, Consul Template, Kubernetes Pods) can also read.
2. **HCP Terraform / Terraform Enterprise**: HashiCorp recommends the `tfe_outputs` data source from the `tfe` provider, which is more secure because it does not require full access to workspace state to fetch outputs. You must still configure the `tfe` provider with a valid token and correct permissions.
3. **Remote state sharing controls** (for `terraform_remote_state` between workspaces): options are share with all workspaces in the organization, with all workspaces in the project, or with specific workspaces. New workspaces do not allow other workspaces to access their state by default; HashiCorp recommends least privilege, enabling access only between workspaces that need each other's information.

## Cautions
- Remote state access controls do **not** apply when using `tfe_outputs`; its protection is the token and permissions on the `tfe` provider.
- In Local execution mode a token must have permission to read and write state versions for the workspace; if the configuration references outputs from another workspace, the token also needs permission to read state outputs for that workspace.
- HCP Terraform manages API credentials for `terraform_remote_state` during its own runs, so a token usually isn't needed in the data source config.
- `terraform_remote_state` takes `backend`, optional `workspace`, optional `config` (nested blocks written as object attributes, e.g. `workspaces = { ... }`) and optional `defaults`; read root outputs through `.outputs`.

## Checked
Date: 2026-11-07. Read in full: the `terraform_remote_state` data source page and the "Manage workspace state" page. Removed because neither states them: the S3 bucket-policy JSON and per-key scoping advice, the `terraform console`/debug-log claim, GCP Secret Manager / Runtime Config, Azure App Configuration, provider lookups by tag, "write-only/ephemeral arguments", the OpenTofu state-encryption note, the claim that `tfe_outputs` is governed by the remote state sharing list (the page says the opposite), and the Verify list.
Method: documentation only; no commands were run.
