---
id: computing-software.cloud-infrastructure-engineering.terraform.hcp-execution-modes-and-cli-driven-runs
name: hcp-execution-modes-and-cli-driven-runs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, execution-mode, cli-driven-runs, hcp-terraform, cloud-block, tfc-agent]
level: practitioner
status: docs-checked
description: "Choose HCP Terraform execution mode per workspace (remote, local, agent) and run CLI-driven workflows with the cloud block, .terraformignore and variable behaviour."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings#execution-mode", "https://developer.hashicorp.com/terraform/cloud-docs/run/cli", "https://developer.hashicorp.com/terraform/cli/cloud/settings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Execution modes and CLI-driven runs

## Execution modes
Set in the workspace's General settings (Execution Mode):

| Mode | Where Terraform runs | Notes from the docs |
|---|---|---|
| Project Default | the project's default execution mode | the default setting for a workspace |
| Remote (custom) | HCP Terraform's own disposable virtual machines | enables Sentinel policy enforcement, cost estimation, notifications, VCS integration |
| Local (custom) | your workstation, CLI-driven workflow | the workspace still stores state; HCP Terraform does **not** evaluate workspace variables or variable sets; remote execution is disabled |
| Agent (custom) | HCP Terraform agents in isolated, private or on-premises infrastructure | if policy execution mode is also Agent, the same agent instance evaluates policies and runs Terraform |

A workspace created implicitly by `terraform init` from a `cloud` block has execution
mode "Remote".

Changing the mode after a run is planned makes that run error when applied. To
minimise that: disable auto-apply, complete runs that are past the pending stage, lock
the workspace, change the mode, re-enable auto-apply if it was on, then unlock.

## CLI-driven workflow
```hcl
terraform {
  cloud {
    organization = "corp"
    workspaces { name = "payments-prod" }      # or tags = ["payments"] for several
  }
}
```
```bash
terraform login
terraform init
terraform plan        # speculative plan in HCP Terraform, logs stream back
terraform apply       # remote run, prompts for approval; only for workspaces without a VCS repo
```
- The `cloud` block needs Terraform v1.1 or later. `workspaces.name` cannot be combined
  with `workspaces.tags`; `workspaces.project` limits matching to a project.
- `terraform plan` starts a speculative plan; `terraform apply` is for workspaces
  without a linked VCS repository. `terraform plan -out <FILE>` plus
  `terraform apply <FILE>` runs a saved plan (Terraform CLI v1.6.0 or later, also only
  for workspaces without a VCS repo).
- Remote runs use: run-specific variables from the command line or local environment
  (`TF_VAR_` environment variables work as input variables), workspace variables,
  applied variable sets, and `*.auto.tfvars` files in the configuration. You must
  still set required environment variables such as provider credentials in the
  workspace.
- A `.terraformignore` file in the configuration root excludes paths from the upload.
  Rules follow `.gitignore`: `#` comments, blank lines, trailing `/` for directories,
  `!` to negate. Without the file, `.git/` and `.terraform/` (but not
  `.terraform/modules`) are still excluded.

## When to use local mode
CI already handles credentials and approvals and you only want HCP Terraform to store
state. Workspace variables and variable sets are not evaluated in this mode.

## Gotchas
- A `cloud` block pointing at a workspace that does not exist makes `terraform init`
  create it; check its settings and variables in the UI before running (no variables
  are created by default, apart from global variable sets).
- If a workspace has a working directory set, run Terraform from a complete copy of
  the configuration directory; the CLI may upload parent directories.
- `terraform plan` in remote mode prints `Running plan in HCP Terraform.` and a URL to
  the run; Ctrl-C stops streaming but does not stop the remote plan.

## Checked
Date: 2026-11-07
Read in full: Workspace settings (cloud-docs/workspaces/settings, including Execution Mode, Change the execution mode and Terraform Working Directory), CLI-driven remote run workflow (cloud-docs/run/cli), and Connect to HCP Terraform (cli/cloud/settings).
Confirmed: the four execution mode options and their descriptions; mode-change procedure; cloud block arguments and v1.1 requirement; implicit workspace creation defaults; variable sources for remote runs; .terraformignore rules and default exclusions; speculative plan, remote apply and saved plan (v1.6.0) rules; the "Running plan in HCP Terraform" output line.
Corrected: the skill said local `-var`/`*.tfvars` are not sent and `-var` errors (the page says run-specific command-line and TF_VAR_ variables are used); remote was labelled the default (the default setting is Project Default).
Removed: `tfc-agent`, `tfe_workspace_settings.execution_mode`, "run tasks", "no policies, no run history, locking" for local mode, the remote-to-local `local-exec` gotcha, the `TF_WORKSPACE` note and the Verify checklist (none on these pages).
Not opened: the Variables page and the cloud block reference page linked from these pages.
Method: documentation only; no commands were run.
