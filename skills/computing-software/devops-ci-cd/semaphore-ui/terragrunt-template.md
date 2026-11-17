---
id: computing-software.devops-ci-cd.semaphore-ui.terragrunt-template
name: terragrunt-template
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [terragrunt, terraform, opentofu, workspace, iac, semaphore-ui]
level: practitioner
status: docs-checked
description: "Enable the Terragrunt application and create a template that wraps Terraform or OpenTofu."
sources:
  - https://semaphoreui.com/docs/user-guide/apps/terragrunt
  - https://semaphoreui.com/docs/user-guide/apps
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Terragrunt templates

Goal: run Terragrunt configurations.

Prerequisites:
1. Install `terragrunt` plus a `terraform` or `tofu` binary on the Semaphore server or runner.
2. Enable the Terragrunt Code application. It is disabled by default: account menu, Applications, switch it on.

Create: Task Templates, New Template, Terragrunt Code. Set the repository and the subdirectory with `terragrunt.hcl`, then choose or create a workspace in the Inventory field (inventory type `terragrunt-workspace`; see the workspaces skill). Create, then Run.

The New Task dialog offers the same options as Terraform: Plan, Destroy, Auto Approve, Upgrade, Reconfigure. Semaphore calls `terragrunt run -- <terraform arguments>` and passes the Terraform or OpenTofu binary choice (`--tf-path`).

To use a variable group value, prefix its name with `TF_VAR_`.

Gotcha: an administrator can switch applications off in the Applications page; existing templates keep working.

## Checked

2026-11-07. Read in full: user-guide/apps/terragrunt.md and apps/README.md. Confirmed: prerequisites, disabled by default, terragrunt-workspace inventory, options, the terragrunt run command with --tf-path, TF_VAR_, and the admin switch-off behaviour (apps README). Removed: "missing binaries cause immediate task failure" and the invented Verify step.
Method: documentation only; no commands were run.
