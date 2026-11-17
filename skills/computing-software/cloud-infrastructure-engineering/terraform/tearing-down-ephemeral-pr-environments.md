---
id: computing-software.cloud-infrastructure-engineering.terraform.tearing-down-ephemeral-pr-environments
name: tearing-down-ephemeral-pr-environments
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ephemeral-destroy, pr-env-teardown, preview-environments, workspaces, ci, destroy]
level: advanced
status: docs-checked
description: "Create per-PR preview environments with Terraform and reliably destroy them on merge/close: state keying, destroy jobs, stuck-destroy handling and orphan sweeps."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/destroy", "https://developer.hashicorp.com/terraform/cli/commands/workspace/select", "https://developer.hashicorp.com/terraform/cli/commands/workspace/delete", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/deletion", "https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral PR environments: create and destroy

## Keying state per PR
```bash
terraform init -input=false
terraform workspace select -or-create "pr-${PR_NUMBER}"   # -or-create creates it if missing
terraform apply -auto-approve -var "env_name=pr-${PR_NUMBER}"
```
Alternatively use a distinct backend key per PR. Name every resource with the env name and tag it (for example `preview=pr-123`, `expires=<date>`) so sweepers can find leftovers.

## Destroy on close/merge
```yaml
on:
  pull_request:
    types: [closed]
jobs:
  destroy:
    steps:
      - run: |
          terraform init -input=false
          terraform workspace select "pr-${{ github.event.number }}" || exit 0
          terraform destroy -auto-approve -input=false -var "env_name=pr-${{ github.event.number }}"
          terraform workspace select default
          terraform workspace delete "pr-${{ github.event.number }}"
```
- A merged PR also fires `closed`; to act only on merges, add a condition on the merged value in the event payload.
- For a `closed` event, `GITHUB_REF` is the merge-target branch when the PR merged and the PR merge ref when closed unmerged, so the checked-out code differs between the two cases. Make sure the destroy config still matches what was applied.
- Give the destroy job the same variables as apply, and use workflow `concurrency` so it cannot race the create job.
- `terraform workspace delete` refuses a workspace that still tracks resources unless `-force` (after which Terraform can no longer manage that infrastructure), and refuses your current workspace; destroy first, switch away, then delete.

## Making destroy reliable
- Add a preview-only flag (for example `var.ephemeral`) that turns off deletion protection and prevent_destroy settings in preview stacks.
- Retry once for transient eventual-consistency errors.
- Short TTL: a nightly job destroys any `pr-*` workspace whose PR is closed or older than N days.

## Orphan sweep
Some resources escape (failed creates never written to state). Sweep by tag and delete anything with no matching open PR. Best: run previews in a dedicated account or project so a scoped nuke tool is safe.

## HCP Terraform
Ephemeral workspaces can auto-destroy: under Settings, Destruction and Deletion, set up auto-destroy at a specific time or after a period of inactivity; it needs workspace admin permission. Workspaces can inherit the setting from their project, and notifications can warn 12 and 24 hours before the run. After an auto-destroy run the schedule is unset, so reschedule if the workspace is reused.

## Verify
- [ ] Closing a test PR leaves no workspace and no tagged resources after the job.
- [ ] The nightly sweep reports zero orphans.

## Checked

Method: docs-checked 2026-11-09 against the `workspace select`, `workspace delete`, HCP Terraform destruction and deletion pages and the GitHub Actions events page (downloaded, converted to text and read; the `destroy` page was only skimmed). Dropped unconfirmed claims: the TF_WORKSPACE export, specific provider flags (force_destroy, skip_final_snapshot), the AWS tagging CLI and nuke tool commands, and the replaced pull_request anchor source.
