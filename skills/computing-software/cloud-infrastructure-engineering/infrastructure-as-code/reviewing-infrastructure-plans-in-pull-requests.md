---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.reviewing-infrastructure-plans-in-pull-requests
name: reviewing-infrastructure-plans-in-pull-requests
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, plan-review, plan-comment, plan-in-pr, review-checklist, destructive-changes, replace-detection, terraform, atlantis]
level: practitioner
status: docs-checked
description: "Surface Terraform plans in pull requests (HCP Terraform speculative plans, Atlantis autoplan), flag deletes and replacements from plan JSON, and review with a checklist."
sources: ["https://developer.hashicorp.com/terraform/internals/json-format", "https://www.runatlantis.io/docs/autoplanning.html", "https://developer.hashicorp.com/terraform/cloud-docs/run/ui", "https://developer.hashicorp.com/terraform/cli/commands/plan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reviewing infrastructure plans in pull requests

The plan is the change; the code diff is only the intent. Reviewers must see the plan.

## 1. Produce and post the plan
```bash
terraform init -input=false
terraform plan -input=false -lock-timeout=5m -out=tfplan
terraform show -no-color tfplan > plan.txt
terraform show -json tfplan > plan.json
```
`-out=FILE` saves the plan; `-lock-timeout=DURATION` makes Terraform retry state locking for that long. Treat saved plan files as potentially sensitive artifacts.

Ways to surface the plan on the pull request:
- **HCP Terraform**: a workspace linked to a VCS repo runs a speculative plan when a pull request is opened against the workspace's branch and posts a link to the plan in the PR; the plan is re-run when the PR is updated. Only PRs from within the same repository trigger speculative plans (not forks, on HCP Terraform). Only people with permission to read runs in the HCP organization can click through to the full plan. A speculative plan uses the head branch contents against the workspace's current state, so rebase or merge the destination branch if it has moved a lot.
- **Atlantis**: on a new PR or new commit it runs `terraform plan` in the directories it judges to hold modified Terraform projects (files matching its autoplan file list, directories containing a `modules/` path segment are handled specially). Changes only to a shared top-level module directory do not autoplan unless you configure `atlantis.yaml`, enable module autoplanning, or run `atlantis plan -d <dir>`.
- **Other CI**: post `plan.txt` as a PR comment from your own pipeline.

## 2. Detect destructive changes automatically
The JSON plan lists `resource_changes`, each with `change.actions`. Valid actions include create, update, delete, and the two replace forms `["delete","create"]` and `["create","delete"]`; scanning the list for "delete" catches all three delete-containing situations. `replace_paths` shows which attributes force replacement.
```bash
jq -r '.resource_changes[]
  | select(.change.actions | index("delete"))
  | "\(.change.actions | join("/"))  \(.address)"' plan.json
```
Fail the check or require an explicit approval when the list is non-empty for protected resource types.

## 3. Review checklist (practitioner judgement)
- The summary line "Plan: X to add, Y to change, Z to destroy" matches the PR description.
- Any delete or replace is intended and data is backed up or migrated.
- Changes outside the PR's scope suggest drift (someone changed things by hand); resolve it first.
- Permissions or network exposure widening; cost impact; tags present.
- Blast radius: number of resources and environments touched; split if large.
- Rollback: what is the revert path?

## Gotchas
- Saved plan files and plan output can contain sensitive values; restrict who can read PR comments and do not run plans from forks.
- `-refresh=false` disables synchronising state with real infrastructure, so it can hide drift; do not use it for review plans.
- A plan applied later than reviewed should be the saved plan file, otherwise a fresh plan may differ.
- The JSON representation of checks is marked experimental in the format docs; the resource_changes shape above is the stable part to rely on.

## Verify
- [ ] A test PR deleting a protected resource is blocked by the check.

## Checked
Method: docs-checked 2026-11-09 against the Terraform JSON output format page, terraform plan command page (-out, -lock-timeout, -refresh=false), the Atlantis autoplanning page, and the HCP Terraform UI and VCS-driven run workflow page.
Removed as unconfirmed: Atlantis `atlantis apply` and per-PR locking, GitHub Actions comment truncation and sticky comments, the Ansible check-mode PR comment recipe, the protected-type jq regex, and the `prevent_destroy` remark.
