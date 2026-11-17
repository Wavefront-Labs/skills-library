---
id: computing-software.devops-ci-cd.semaphore-ui.terraform-opentofu-templates
name: terraform-opentofu-templates
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [terraform, opentofu, tofu, tf-var, destroy, semaphore-ui]
level: practitioner
status: docs-checked
description: "Create Terraform or OpenTofu templates, pass TF_VAR variables, and use the destroy and migrate-state toggles."
sources:
  - https://semaphoreui.com/docs/user-guide/apps/terraform
  - https://semaphoreui.com/docs/user-guide/apps
  - https://semaphoreui.com/docs/user-guide/apps/terragrunt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Terraform and OpenTofu templates

Goal: run infrastructure code from Semaphore.

Create: Task Templates, New Template, choose Terraform Code (or OpenTofu Code), set the repository and the subdirectory with the configuration, then create and Run. The binary must be installed on the machine that runs the task; the official Docker image contains Ansible, Terraform and OpenTofu.

To use a variable group value or secret in Terraform, prefix its name with `TF_VAR_` (`TF_VAR_hcloud_token` is read as `var.hcloud_token`). Put sensitive values on the group's Secrets tab.

The New Task dialog has `-destroy` and `-migrate-state` toggles. The Terragrunt page says that Terragrunt offers the same options as Terraform: Plan, Destroy, Auto Approve, Upgrade, Reconfigure.

Behaviour: Semaphore runs `terraform init` automatically. State comes from the backend your code configures, or from the built-in HTTP backend (Pro).

Workspaces: see the workspaces skill.

## Checked

2026-11-07. Read in full: user-guide/apps/terraform/README.md and user-guide/apps/README.md, plus the workspaces and states pages and the Terragrunt page for the option list. Confirmed: the template creation steps, TF_VAR_ and the Secrets tab, -destroy and -migrate-state toggles, automatic init, HTTP backend as Pro, image contents. Removed: the claim that the Terraform dialog itself lists Plan/Auto Approve/Upgrade/Reconfigure (only the Terragrunt page lists them, as the same options), the inventory type names terraform-workspace and tofu-workspace (not stated on the pages read), "do not commit credentials; use group secrets or JWT/Vault", the OpenTofu binary gotcha, and the invented Verify step.
Method: documentation only; no commands were run.
