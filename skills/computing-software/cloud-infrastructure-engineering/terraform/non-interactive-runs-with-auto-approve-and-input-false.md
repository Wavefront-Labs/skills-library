---
id: computing-software.cloud-infrastructure-engineering.terraform.non-interactive-runs-with-auto-approve-and-input-false
name: non-interactive-runs-with-auto-approve-and-input-false
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, auto-approve, input-false, non-interactive, tf-in-automation, tf-input, automation, ci, terraform-apply]
level: intro
status: docs-checked
description: "Run plan and apply without prompts in CI: -input=false, -auto-approve, saved plan files, TF_INPUT and TF_IN_AUTOMATION, and when each is appropriate."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/apply#apply-options", "https://developer.hashicorp.com/terraform/cli/config/environment-variables", "https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-interactive runs: `-auto-approve` and `-input=false`

**Goal:** a pipeline that never waits on a prompt, and never auto-approves
something a human should have seen.

## 1. The two flags do different things
- `-input=false` disables all of Terraform's interactive prompts, including the
  prompt for unset root-module variables. It also removes the interactive approval
  of a plan, so `terraform apply -input=false` without `-auto-approve` or a saved
  plan conservatively assumes you do not want to apply and the operation fails.
- `-auto-approve` (on `apply`) skips interactive approval of the plan before
  applying. This includes destructive operations such as deleting resources.
  Terraform ignores it when you pass a saved plan file, because passing the plan
  file is treated as the approval.

## 2. Command shapes (from the automation tutorial)
```bash
terraform init  -input=false
terraform plan  -out=tfplan -input=false
terraform apply -input=false tfplan          # saved plan: applies without a prompt
```
Auto-approve variant, for pre-production or development:
```bash
terraform init  -input=false
terraform apply -input=false -auto-approve   # implicitly plans, then applies
```
Because `-input=false` stops variable prompts, supply values with `-var` and
`-var-file` on `plan` (or `apply` without a saved plan). A saved plan accepts no
extra planning modes or options: the plan file already holds those decisions.

## 3. Environment equivalents
- `TF_INPUT` set to `false` or `0` behaves as if `-input=false` was given.
- `TF_IN_AUTOMATION` set to any non-empty value makes Terraform avoid suggesting
  specific commands to run next. It is a purely cosmetic change to
  human-readable output.
- `TF_CLI_ARGS` adds arguments to every command, directly after the subcommand;
  `TF_CLI_ARGS_name` (for example `TF_CLI_ARGS_plan="-refresh=false"`) affects only
  that command. Flags typed on the command line take precedence.
- `TF_VAR_name` sets an input variable.

## 4. Choose the shape
- Manual review is strongly recommended for production. Plan, have a human review,
  then apply the saved plan.
- Use automatic approval only with non-critical infrastructure; the tutorial says
  manual review is always recommended when Terraform may make destructive changes.
- The apply page recommends that anyone using `-auto-approve` makes sure nobody can
  change the infrastructure outside the Terraform workflow, to limit drift, and to
  run and review a plan first.
- Allow only one plan outstanding at a time: applying a plan invalidates other plans
  produced against the same state.

## Gotchas
- Plan and apply on different machines: archive the whole working directory
  (including `.terraform`) after plan and extract it at the same absolute path
  before apply. A plan assumes the same operating system and CPU architecture and
  identical Terraform and provider versions; an upgrade between plan and apply
  produces an error.
- The plan file holds the full configuration, state and variables passed to plan;
  protect it as sensitive. Prefer environment variables for provider credentials,
  which are not stored in the plan.
- HCP Terraform remote execution (CLI-driven runs): you cannot apply a saved plan to
  remote operations, and speculative plans are not applyable.
- Use a backend that supports remote state and locking for pipelines.

## Checked
Date: 2026-11-07
Read in full: the terraform apply command page (Usage, Automatic and Saved Plan
Mode, Apply Options), the CLI environment variables page (TF_INPUT, TF_CLI_ARGS,
TF_VAR_name, TF_IN_AUTOMATION and the rest of the list), and the Running Terraform
in automation tutorial.
Removed because no cited page states them: the table of exact error strings, the
claim that a missing variable hangs until timeout, `terraform destroy` flags,
`-force` history, `init` backend-migration prompts, HCP "auto apply" behaviour,
the `CONFIRM_DESTROY` pattern and the Verify checklist. `TF_CLI_ARGS_apply` was
replaced by the documented `TF_CLI_ARGS_plan` example.
Method: documentation only; no commands were run.
