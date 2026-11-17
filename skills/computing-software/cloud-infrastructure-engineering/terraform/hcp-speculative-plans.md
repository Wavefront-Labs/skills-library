---
id: computing-software.cloud-infrastructure-engineering.terraform.hcp-speculative-plans
name: hcp-speculative-plans
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, speculative-plan, hcp-terraform, plan-on-pr, vcs-driven-runs]
level: practitioner
status: docs-checked
description: "Use HCP Terraform speculative plans: automatic PR plans in VCS workspaces, CLI terraform plan against the cloud block, plan-only API runs, and what they can and cannot do."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/run/remote-operations#speculative-plans", "https://developer.hashicorp.com/terraform/cloud-docs/run/ui#speculative-plans-on-pull-requests", "https://developer.hashicorp.com/terraform/cloud-docs/run/cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Speculative plans

A speculative plan is a plan-only run: it shows possible changes, and policies affected
by those changes, but cannot apply anything. It can start without waiting for other
runs, is not blocked by a workspace lock, and does not block the run queue. Past
speculative plans are listed alongside the workspace's other runs.

## Ways to get one
| Trigger | Notes |
|---|---|
| PR or merge request opened/updated against a VCS-connected workspace's branch | HCP Terraform posts a link to the plan and a status indicator in the PR and re-runs the plan when the PR is updated |
| `terraform plan` locally with the CLI integration (`cloud` block) | uploads the local working directory (respecting `.terraformignore`), uses the workspace's variable values, streams output and a link |
| Runs API with a configuration version marked as speculative | for custom tooling; see the configuration-versions API |
| UI: **+ New run**, run type **Plan only** | can also pick a Terraform version for the run without changing workspace settings, to test upgrades |

## Rules for pull request plans
- Only PRs that originate from within the same repository trigger speculative plans.
  Fork PRs do not, to avoid executing malicious code or exposing sensitive information
  (on Terraform Enterprise, administrators can choose to allow them).
- The workspace must allow automatic speculative plans; this can be disabled in the
  workspace's VCS settings. When the VCS Trigger Type is the Git-tag-driven option
  (the page spells it "Tab-based"), speculative plans run only when a new Git tag awaits
  approval; opening or updating a PR does not trigger them.
- The PR's destination branch must be the workspace's connected branch.
- If the workspace only treats certain directories as relevant, PRs that do not touch
  them trigger no plan; HCP Terraform still posts a passing commit status.
- The status check reflects the plan only, not a later apply.
- The plan uses the head branch contents and compares against the workspace's
  *current* state, so it can mislead if the destination branch has moved on; rebase or
  merge the destination branch into the head branch for a more accurate view.
- One PR can show links to several plans, one per connected workspace. Anyone who can
  see the PR sees the status, but only members with permission to read runs on the
  workspace can open the plan output.

## Gotchas
- Speculative plans use the workspace's variables, so a plan can execute whatever
  code the configuration contains; restrict who can open PRs from the connected
  repository accordingly.
- Policies (Sentinel or OPA) are evaluated against speculative plans in workspaces that
  use them.
- A failed or canceled speculative plan can be retried in the UI with **Retry Run**
  (requires permission to queue plans); this creates a new run on the same
  configuration version.
- Remote `terraform plan` output says `Running plan in HCP Terraform.`; Ctrl-C stops
  streaming but does not stop the remote plan.

## Checked
Date: 2026-11-07
Read in full: Remote operations (cloud-docs/run/remote-operations, incl. Speculative Plans and Retry), UI and VCS-driven run workflow (cloud-docs/run/ui, incl. Speculative Plans on Pull Requests and Testing Terraform Upgrades), and CLI-driven remote run workflow (cloud-docs/run/cli, incl. Remote Speculative Plans and Policy Enforcement).
Confirmed: plan-only, cannot apply, unblocked by queue and locks; the three trigger types and the UI Plan only option; every PR rule above; contents-of-PR-plan caveat; retry behaviour; policy evaluation on speculative plans.
Removed: "on by default" for automatic speculative plans, the Settings > Version Control toggle and "Trigger runs when files in specified paths change" wording (VCS settings page not opened), the `"speculative": true` JSON key, `TFC_AWS_PLAN_ROLE_ARN`, the upload-speed and concurrency-limit gotchas, and the Verify checklist (none on the pages).
Not opened: the VCS settings and configuration-versions API pages.
Method: documentation only; no commands were run.
