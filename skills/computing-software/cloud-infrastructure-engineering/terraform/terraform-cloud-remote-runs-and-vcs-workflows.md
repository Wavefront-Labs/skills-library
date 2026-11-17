---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-cloud-remote-runs-and-vcs-workflows
name: terraform-cloud-remote-runs-and-vcs-workflows
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, hcp-terraform, terraform-cloud, terraform-enterprise, remote-execution, vcs-driven-workflow, cli-driven-workflow, api-driven-workflow, run-triggers, variable-sets, speculative-plans, workspace-variables, remote-backend, tfe-provider, no-code-provisioning, cost-estimation, team-permissions]
level: advanced
status: docs-checked
description: "Run HCP Terraform/Enterprise workspaces: VCS-driven vs CLI-driven vs API-driven workflow choice, variable sets, run triggers, speculative plans on PRs, remote execution."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/workspaces/run/remote-operations", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/run/modes-and-options", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/run-triggers", "https://developer.hashicorp.com/terraform/cloud-docs/variables/managing-variables", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/vcs", "https://developer.hashicorp.com/terraform/cloud-docs/dynamic-provider-credentials"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HCP Terraform / Enterprise remote runs and VCS workflows

**Goal:** pick a run workflow per workspace, share credentials and common variables
through variable sets instead of per-workspace copies, and get PR speculative plans
and run triggers working so applies happen from a logged execution environment, not a
laptop with ambient cloud credentials.

## 1. The three workflows
| Workflow | Trigger | Typical use |
|---|---|---|
| **VCS-driven** | push or PR to a connected repo | most app-team workspaces; PRs get an automatic speculative plan |
| **CLI-driven** | `terraform plan` / `apply` run locally, execution happens in HCP Terraform | platform teams iterating |
| **API-driven** | calls to the Runs API (upload a configuration version, create a run) | an existing CI/CD system orchestrating runs |

Pick one per workspace and document it; mixing triggers on one workspace makes run
history harder to follow. API-driven runs need an API token (sent as a Bearer
token); if the token cannot apply runs for the workspace, the run cannot auto-apply.

## 2. Variable sets over per-workspace variables
Variable sets are reusable collections applied to multiple workspaces and Stacks;
they can be owned by an organisation or a project, which decides who may manage
them. Variables have a category: **Terraform** (HCL `var.x`, optional HCL value) or
**environment** (provider auth such as cloud credentials). Marking a variable
sensitive makes it write-only: nobody can read it in the UI or Variables API.
Prefer **dynamic provider credentials**: HCP Terraform issues an OIDC-compliant
workload identity token and the cloud issues temporary credentials per run, which
avoids static keys even if rotated. Variables are not evaluated for workspaces in
Local execution mode.

## 3. Speculative plans and run triggers
A **speculative plan** is a plan-only run: it shows possible changes and the policies
they affect but can never be applied. For a VCS-connected workspace HCP Terraform
starts one when a pull request opens against the selected branch, and the PR links
to it. Speculative plans do not wait on other runs. Require the plan as a PR check.

**Run triggers** let a workspace queue a run automatically after a successful apply
in any of up to 20 source workspaces. Triggered runs do not auto-apply unless the
**Auto-apply run triggers** setting is on.

## 4. Policy gates and cost
Sentinel/OPA policy sets can gate runs (see
`computing-software.cloud-infrastructure-engineering.terraform.policy-as-code-with-sentinel-and-opa`).
Cost estimation can be checked in a Sentinel policy using the `tfrun` import
(`tfrun.cost_estimate.delta_monthly_cost`), but the cost estimation page states it
is only available in policy checks (the Legacy policy execution mode).

## 5. Remote execution
Runs execute on HCP Terraform's disposable virtual machines (or your Enterprise
install). A run is locked to one configuration version and set of variable values
when it starts. A locked workspace queues runs but does not start them.

## Gotchas
- A VCS workspace needs a working directory for trigger prefixes. The "any changes
  in the repository" option queues unnecessary runs in a monorepo; use trigger
  patterns (globs) or prefixes, and add shared module directories as triggers.
- Speculative plans do not wait for or block other runs, so two PRs can produce
  plans against the same state; re-plan after rebasing.
- Run triggers fire on a successful apply, so a manual approval step delays
  downstream runs.

## Verify
- [ ] Every workspace has one documented workflow type.
- [ ] PRs touching a workspace's directory show a speculative plan as a required check.
- [ ] No long-lived static cloud credentials where dynamic provider credentials exist.
- [ ] Downstream workspaces pick up upstream changes through a run trigger or equivalent.

## Checked
2026-11-09. Confirmed against the HCP Terraform docs sources in the web-unified-docs repository: remote operations (disposable VMs, run locking, speculative plans), run modes and options (plan-only, VCS PR trigger), run triggers (successful apply, 20 source workspaces, auto-apply setting), managing variables and variable sets (categories, sensitive write-only, org/project ownership, Local mode), VCS settings (working directory, trigger patterns and prefixes), dynamic provider credentials (OIDC token) and cost estimation (Sentinel `tfrun`, legacy policy checks only).
Removed as unconfirmed: the Terragrunt `dependency` equivalence, "manual approval when cost delta exceeds a threshold" as a built-in setting, `terraform state pull/push` escape-hatch advice and "Advanced options" lock guidance, the claim that API tokens are org- or user-scoped, and the "speculative plans do not take the state lock" wording (replaced with the documented "do not wait for other runs").
Method: documentation only; no commands were run.
