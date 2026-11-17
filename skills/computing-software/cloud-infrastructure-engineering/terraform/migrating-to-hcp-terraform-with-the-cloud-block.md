---
id: computing-software.cloud-infrastructure-engineering.terraform.migrating-to-hcp-terraform-with-the-cloud-block
name: migrating-to-hcp-terraform-with-the-cloud-block
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, hcp-terraform, cloud-block, cloud-block-config, migrate-to-hcp, cloud-migration, workspace-mapping, cloud-workspaces-tags, tf-cloud-organization]
level: practitioner
status: docs-checked
description: "Configure the cloud block (organization, project, name or tags) and migrate existing backend state and CLI workspaces into HCP Terraform workspaces."
sources: ["https://developer.hashicorp.com/terraform/cli/cloud/settings", "https://developer.hashicorp.com/terraform/cli/cloud/migrating", "https://developer.hashicorp.com/terraform/language/terraform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The `cloud` block and migrating into HCP Terraform

## The block
```hcl
terraform {
  cloud {
    organization = "acme"
    hostname     = "app.terraform.io"   # optional; defaults to app.terraform.io (set your TFE host otherwise)
    workspaces {
      project = "networking"
      name    = "network-prod"          # one workspace
      # OR
      # tags = { layer = "network" }    # many workspaces; a map of tags needs Terraform 1.10+, older versions use a list of key-only tags
    }
  }
}
```
- `name` and `tags` cannot be combined. `name` links this directory to one existing workspace. `tags` links it to existing workspaces in the organization with matching tags; if none exist, `terraform init` prompts you to create one that carries the tags.
- `project` names an existing project; Terraform associates the configuration with workspaces in that project that match the name or tags.
- A `cloud` block cannot be combined with a `backend` block, and a configuration may have only one.
- Environment variables fill omitted attributes (the configuration wins if both are set): `TF_CLOUD_ORGANIZATION`, `TF_CLOUD_HOSTNAME`, `TF_CLOUD_PROJECT`. `TF_WORKSPACE` names a single existing workspace (it is not created for you). An empty `cloud {}` block is still required.
- Credentials: `terraform login` is recommended; a user token can also be set in the configuration (`token` attribute of the cloud block, avoid committing it).
- Add a `.terraformignore` at the configuration root to exclude files from the upload to HCP Terraform; `.git/` and `.terraform/` (except `.terraform/modules`) are excluded by default.

## Migrating existing state
1. Freeze other writers; back up state first (`terraform state pull`).
2. Replace the `backend` block with `cloud {}`. From `backend "remote"`, just swap the block: Terraform keeps using the same workspaces. A `prefix` argument becomes `tags`.
3. `terraform init` detects state from a local or other backend and prompts you to migrate it. HCP Terraform workspaces need unique names, so Terraform may ask you to rename CLI workspaces with a pattern such as `<COMPONENT>-<ENVIRONMENT>-<REGION>` (for example `networking-prod-us-east`).
4. In each new workspace set the execution mode, Terraform version, variables (sensitive values re-entered) and VCS connection as needed.
5. `terraform plan` (it runs remotely in remote mode) should report no changes.

## Gotchas
- The `cloud` block does not support `prefix`; after migration refer to workspaces by their full name (`terraform workspace select my-app-prod`, not `prod`).
- Remote execution runs on HCP Terraform workers, not your machine: move provider credentials into workspace variables or, better, dynamic provider credentials.

## Verify
- [ ] `terraform workspace list` shows the mapped HCP workspaces.
- [ ] The HCP Terraform State tab shows the migrated state; the first remote plan is clean.

## Checked
2026-10-28. Confirmed against the Terraform CLI "Connect to HCP Terraform" page (cloud block settings, `hostname` default, tags as map or key-only list, name/tags exclusivity, project, `terraform login`, migration prompts, rename pattern, `backend "remote"` to `cloud`, `prefix` to `tags`, no `prefix` support, `.terraformignore` and default exclusions).
Also confirmed against the Terraform `terraform` block reference: tag map vs key-only list and the Terraform 1.10 gate, `TF_CLOUD_*` and `TF_WORKSPACE` behaviour, mutual exclusion of `cloud` and `backend`.
Removed: `credentials.tfrc.json`, the `network-*` rename example, the claim that `terraform workspace new` creates workspaces with the tags, the `*.auto.tfvars` / `-var-file` upload rules, the workspace-version-vs-state-version rule, and the `terraform.workspace` naming note (none in the fetched page).
Method: documentation only; no commands were run.
