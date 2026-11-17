---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-change-approval-and-change-windows
name: terraform-change-approval-and-change-windows
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, change-approval, change-window, apply-approval, protected-environment, freeze-period, itsm]
level: practitioner
status: docs-checked
description: "Control when and by whom Terraform applies run: approvals on saved plans, CI environment protection, change windows and freezes, ticket links and emergency paths."
sources:
  - https://developer.hashicorp.com/terraform/cloud-docs/workspaces/run/states
  - https://developer.hashicorp.com/terraform/cli/commands/plan
  - https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
  - https://www.runatlantis.io/docs/command-requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Change approval and change windows

## Approve the exact plan
Approval should apply to the plan the reviewer saw, not a fresh plan computed later:
```bash
terraform plan -out=tfplan           # plan job: store tfplan as an artifact; treat it as sensitive and restrict access
terraform apply tfplan               # apply job, after approval
```
The `-out` workflow is intended for automation. A plan without `-out` is a
speculative plan, and other changes to the target system in the meantime can make the
final effect differ, so always re-check the final non-speculative plan.

HCP Terraform / Enterprise: after planning, and after cost estimation and Sentinel
checks if enabled, a run pauses in **Needs Confirmation** until a user with permission
to apply approves it; rejecting discards the run (unless the workspace auto-applies).
Atlantis: `apply_requirements` accepts `approved` (PR approved by someone other than
the author), `mergeable` and `undiverged` (project files ahead of the base branch).

## CI environment protection (GitHub example)
```yaml
jobs:
  plan:
    runs-on: ubuntu-latest
    steps: [ ... terraform plan -out=tfplan ..., { uses: actions/upload-artifact@v4, with: { name: tfplan, path: tfplan } } ]
  apply:
    needs: plan
    environment: production        # protection rules are configured on the environment
    runs-on: ubuntu-latest
    steps: [ { uses: actions/download-artifact@v4, with: { name: tfplan } }, { run: terraform apply tfplan } ]
```
GitHub environment protection rules include:
- **Required reviewers**: up to 6 people or teams, only one needs to approve;
  **Prevent self-review** stops people approving runs they triggered.
- **Wait timer**.
- **Deployment branches and tags**: restrict which refs can deploy.
- Optionally disallow administrators bypassing the rules.
- Custom deployment protection rules created with GitHub Apps.
Environments on private repositories need a plan that supports them.

## Change windows and freezes
- Encode windows as a check, not a wiki page:
```bash
# fail the apply job outside Tue-Thu 09:00-16:00 UTC unless EMERGENCY=true
dow=$(date -u +%u); hr=$(date -u +%H)
if [ "${EMERGENCY:-false}" != true ] && { [ $dow -lt 2 ] || [ $dow -gt 4 ] || [ $hr -lt 9 ] || [ $hr -ge 16 ]; }; then
  echo "Outside change window"; exit 1; fi
```
- Holiday freezes: a repository variable such as `CHANGE_FREEZE=true` checked by the
  apply job, or a custom deployment protection rule.
- Plans (read-only) run anytime; only applies are gated.

## Ticket integration
- Require a change ticket ID in the PR (template plus check) and post the plan summary
  and apply result back to the ticket.
- Pre-approved (standard) change types can be auto-approved by policy; others need
  peer or CAB approval according to your process.

## Emergency path
Document a break-glass route: an `emergency` label or input bypasses the window but
still requires one approver and creates a retrospective ticket. Keep an audit log of use.

## Verify
- [ ] The apply job cannot run without approval from someone other than the author, and only with the saved plan artifact.
- [ ] An apply outside the window fails unless the emergency path is used, which is logged.

## Checked
2026-11-09. Confirmed against HCP Terraform run states (Needs Confirmation, discard), the `terraform plan` command page (`-out`, speculative plans), the GitHub "manage environments" page (required reviewers up to 6, prevent self-review, wait timer, deployment branches and tags, admin bypass, custom protection rules, plan limits on private repos) and the Atlantis command requirements page (`approved`, `mergeable`, `undiverged`).
Removed as unconfirmed: the "Saved plan is stale" error message, claims about GitLab protected environments, Azure DevOps checks, ServiceNow DevOps and Jira Service Management integrations, and the statement that tfplan "can contain secrets" (now phrased as advice to treat it as sensitive).
Method: documentation only; no commands were run.
