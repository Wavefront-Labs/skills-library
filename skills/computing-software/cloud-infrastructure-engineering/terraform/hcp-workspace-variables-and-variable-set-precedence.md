---
id: computing-software.cloud-infrastructure-engineering.terraform.hcp-workspace-variables-and-variable-set-precedence
name: hcp-workspace-variables-and-variable-set-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, hcp-terraform, workspace-variable-precedence, variable-set-precedence, variable-sets, priority-variable-sets, tfe-variable]
level: practitioner
status: docs-checked
description: "Resolve which value an HCP Terraform run uses across workspace variables, global/project/workspace variable sets, priority sets, auto.tfvars and CLI -var."
sources: ["https://raw.githubusercontent.com/hashicorp/terraform-provider-tfe/main/website/docs/r/variable_set.html.markdown", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/variables#precedence", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/variables/managing-variables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HCP Terraform variable precedence

## Order (highest first)
Per the HCP Terraform precedence page, when variables of the same type share a key the platform resolves them in this order:
1. Priority global variable sets.
2. Priority project-scoped variable sets owned by an organization.
3. Priority workspace-scoped variable sets owned by an organization.
4. Priority project-scoped variable sets owned by a project.
5. Priority workspace-scoped variable sets owned by a project.
6. Command-line `-var` / `-var-file` (CLI workflow).
7. Local environment variables prefixed `TF_VAR_` (CLI workflow).
8. Workspace-specific variables.
9. Workspace-scoped variable sets owned by a project.
10. Project-scoped variable sets owned by a project.
11. Workspace-scoped variable sets owned by an organization.
12. Project-scoped variable sets owned by an organization.
13. Global variable sets (they cannot conflict with each other: global sets may not share a key).
14. `*.auto.tfvars` files.
15. `terraform.tfvars` (Terraform Enterprise ignores this file; HCP Terraform uses it).

Within one scope and ownership, if two non-priority sets define the same key, the set whose name sorts first (Unicode code points) wins; for priority sets of the same scope and ownership the alphabetical order of names decides. Avoid overlaps instead of relying on it.

## Terraform vs environment variables
- *Terraform variables* map to `var.x` (mark HCL for lists and maps).
- *Environment variables* are exported in the run's shell on disposable Linux workers: provider credentials, `TF_LOG`, `TF_CLI_ARGS_plan`.
- Precedence applies between variables of the same type with the same key.

## Patterns
- Credentials and org-wide settings: global or project variable sets, ideally dynamic-credentials environment variables.
- Guard-rails that workspace owners must not override (for example `allowed_regions`): a **priority** variable set. It does not guarantee the configuration uses the variable, so back it with policy checks or run tasks.
- Per-environment values: workspace variables, or a `*.auto.tfvars` file committed in VCS (lower precedence than workspace variables).

## Managing as code
```hcl
resource "tfe_variable_set" "aws" {
  name         = "aws-dynamic-creds"
  organization = "acme"
  priority     = false
}
resource "tfe_variable" "role" {
  key             = "AWS_REGION"
  value           = "eu-west-2"
  category        = "env"
  variable_set_id = tfe_variable_set.aws.id
}
resource "tfe_project_variable_set" "aws" {
  variable_set_id = tfe_variable_set.aws.id
  project_id      = tfe_project.platform.id
}
```
`tfe_project_variable_set` controls which project can use a set, not who owns it; ownership is set with `parent_project_id` on `tfe_variable_set`. `tfe_variable_set` also has `global` and `priority` arguments.

## Gotchas
- Overwritten variables are marked in the UI; check the workspace variables page first when a value is unexpected.
- Stacks reference variable sets directly with a `store` block, so these precedence rules do not apply to them.

## Verify
- [ ] The workspace's effective value matches the row you expect in the order above.
- [ ] No two sets of the same scope define the same key unless that is intended.

## Checked
2026-10-28. Confirmed against the HCP Terraform variables overview and precedence page, and the `tfe_variable_set` and `tfe_project_variable_set` resource docs in the terraform-provider-tfe repository: the 15-step order, lexical tie-break, priority-set behaviour and caveat, TF_VAR_ and CLI placement, terraform.tfvars note, Stacks note, resource arguments.
Corrected: the old order put all variable sets below workspace variables and had workspace-scoped priority sets beating global ones (the docs rank priority global sets highest); the claim that an environment `TF_VAR_x` has lower precedence than a Terraform variable; `*.auto.tfvars` being above workspace variable sets.
Removed: `TFC_AWS_PROVIDER_AUTH` as a documented example and the "sensitive variables are write-only" and "remote runs ignore local files" gotchas (not in the fetched pages).
Method: documentation only; no commands were run.
