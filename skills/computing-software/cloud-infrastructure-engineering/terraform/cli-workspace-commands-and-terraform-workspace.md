---
id: computing-software.cloud-infrastructure-engineering.terraform.cli-workspace-commands-and-terraform-workspace
name: cli-workspace-commands-and-terraform-workspace
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, workspace-select, workspace-delete, workspace-new, terraform-workspace-interpolation, workspace-interpolation, tf-workspace]
level: practitioner
status: gated
description: "Operate CLI workspaces (new, select -or-create, list, show, delete -force) and use terraform.workspace in config without creating fragile per-workspace logic."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/workspace", "https://developer.hashicorp.com/terraform/language/state/workspaces", "https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_workspace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CLI workspaces and `terraform.workspace`

## Commands
```bash
terraform workspace list                    # * marks current
terraform workspace show
terraform workspace new feature-x
terraform workspace select prod
terraform workspace select -or-create pr-123   # 1.4+ (changelog): idempotent for CI
terraform workspace delete feature-x        # refuses if state has resources
terraform workspace delete -force feature-x # deletes state even with resources (they become orphaned!)
export TF_WORKSPACE=prod                    # override selection for this shell/CI job
```
The selected workspace is stored in `.terraform/environment`; `TF_WORKSPACE` beats it.

## Where state goes
- local: `terraform.tfstate.d/<ws>/terraform.tfstate`
- s3: `<workspace_key_prefix>/<ws>/<key>` (default prefix `env:`, from the S3 backend docs)
- gcs: `<prefix>/<ws>.tfstate` (GCS backend docs); azurerm: `<key>env:<ws>` (gated: unconfirmed, source is paywalled or blocked)
- `default` workspace uses the plain key and cannot be deleted.

## terraform.workspace in config
```hcl
locals {
  env      = terraform.workspace
  settings = local.env_settings[local.env]      # fails loudly on unexpected names
}
resource "aws_s3_bucket" "this" {
  bucket = "acme-${terraform.workspace}-data"
}
```
Rules:
- Use it for **naming and lookup keys**, not sprawling `terraform.workspace == "prod" ? ... : ...` conditionals.
- Guard with a lookup table so `default` or a typo'd workspace errors early.
- Inside HCP Terraform remote runs it returns the HCP workspace name (`app-prod`), not the CLI short name (gated: unconfirmed, source is paywalled or blocked).

## Good uses
Ephemeral copies (feature branches, PR previews) of the same stack with identical
config. Not for prod vs dev isolation (shared backend, credentials and code version).

## Gotchas
- `workspace delete -force` loses track of real resources (it prints a `non-empty` warning); destroy first.
- Running `apply` in the wrong workspace is the classic accident; show it in the
  prompt (`PS1`) and print `terraform workspace show` at the top of CI logs.
- `terraform.workspace` is not available in backend configuration (`Error: Variables not allowed`). `workspace delete default` fails with `cannot delete default state`, and deleting the currently selected workspace is refused (`You cannot delete the currently active workspace`).

## Verify
- [ ] `terraform workspace show` in CI logs matches the intended environment.
- [ ] `terraform plan` in `default` fails fast if `default` is not an allowed environment.

## Checked
- Terraform 1.17.0, local backend: `workspace new`, `list`, `show`, `select -or-create`, `delete` (refused with `Workspace is not empty` while the workspace tracked a resource), `delete -force` (deleted with the non-empty warning); state landed in `terraform.tfstate.d/<ws>/terraform.tfstate`; `.terraform/environment` held the selected name; `TF_WORKSPACE=prod` overrode it; a lookup table `local.env_settings[terraform.workspace]` failed with `Invalid index` in a workspace missing from the table; `terraform.workspace` in a backend block gave `Variables not allowed`. `-or-create` is in the 1.4 changelog. S3 and GCS paths were confirmed against the backend docs in the hashicorp/web-unified-docs repo.
- Gated: azurerm blob naming and HCP remote-run workspace names (no account, not in the docs read).
