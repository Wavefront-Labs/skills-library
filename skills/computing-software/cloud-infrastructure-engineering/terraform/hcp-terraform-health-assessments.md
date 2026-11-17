---
id: computing-software.cloud-infrastructure-engineering.terraform.hcp-terraform-health-assessments
name: hcp-terraform-health-assessments
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, hcp-terraform, health-assessments, continuous-validation, drift-detection, check-blocks, notifications]
level: practitioner
status: docs-checked
description: "Turn on HCP Terraform health assessments for scheduled drift detection and continuous validation of checks/postconditions, route alerts, and act on results."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/workspaces/health", "https://developer.hashicorp.com/terraform/language/checks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HCP Terraform health assessments

When enabled, HCP Terraform periodically runs a health assessment per workspace. It
creates a speculative plan to read the current state of your infrastructure and does not
modify infrastructure. Two evaluations:
- **Drift detection**: whether real infrastructure matches your configuration
  (configuration drift). It does not detect state drift.
- **Continuous validation**: whether custom conditions in the configuration keep
  passing. It evaluates `check` blocks, preconditions and postconditions; HashiCorp
  recommends `check` blocks for post-apply monitoring.

## Enable
- Workspace: Settings > Health > Health Assessments > Enable > Save settings. Needs
  workspace admin. An organization owner can instead enforce assessments for all
  eligible workspaces in the organization settings, which overrides workspace-level
  settings.
- Requirements: HCP Terraform Standard or Premium edition; Terraform 0.15.4+ for drift
  detection only, 1.3.0+ for drift detection and continuous validation; **Remote or
  Agent** execution mode (not Local); at least one run that successfully applied; the
  latest run must be successful.

## Scheduling
- The next assessment is scheduled a fixed period after the more recent of the last
  apply or last assessment (the page's example: a 24-hour cadence, last apply 4 hours
  ago, next assessment in 20 hours). On Terraform Enterprise, admins can change the
  frequency.
- Starting a run during an assessment cancels the assessment until the next period, so
  workspaces with frequent runs may rarely be assessed.
- If the latest run ended errored, canceled or discarded, assessments pause until a run
  applies successfully. Workspace admins can start an on-demand assessment from the
  Health page in the UI ("Start health assessment").

## Make continuous validation useful
```hcl
check "health_check" {
  data "http" "terraform_io" {
    url = "https://www.terraform.io"
  }
  assert {
    condition     = data.http.terraform_io.status_code == 200
    error_message = "${data.http.terraform_io.url} returned an unhealthy status code"
  }
}
```
Results appear under Health > Continuous validation. Multiple preconditions and
postconditions on one object are shown only if one fails.

**False positives:** the assessment's speculative plan evaluates `check` blocks last,
and data sources can return new values, so a check can fail against a change that has
not been applied. Use nested data sources that query your actual resource
configuration, not a computed "latest" value.

## Alerts
HCP Terraform sends notifications about assessment results according to the workspace's
notification settings; continuous validation alerts are configured there. Workspaces with
drift or failed checks show a Health warning on the organization's Workspaces page.

## Acting on drift
Health > Drift shows the proposed changes. Either overwrite the drift (queue a plan and
apply to revert to the configuration) or update the configuration to include the changes
and push a new configuration version. State drift (external changes that do not
invalidate the configuration) is handled with refresh-only mode.

## Checked
Date: 2026-11-07
Read in full: Health (cloud-docs/workspaces/health). The second cited URL (language/checks) redirects to the Validate page, which I fetched but did not re-read for this review because every claim kept here comes from the Health page.
Confirmed: both evaluation types and their definitions; speculative plan mechanism; requirements (edition, versions, execution modes, successful runs); enabling steps and permissions; org enforcement override; scheduling rules and the 24-hour example; assessment cancelled by new runs; pause after errored/canceled/discarded runs; on-demand button; false-positive guidance; resolving drift options; where results show.
Removed: "refresh-only plan" and "roughly daily", the org "Settings > Health" path, the `tfe` provider `assessments_enabled` attribute, the `cert_expiry` example using `timecmp`/`plantimestamp`, the "warnings in normal runs" claim, named notification triggers, the credentials gotcha and `ignore_changes`/`ignore_tags` advice, and the Verify checklist (none confirmed by the page).
Method: documentation only; no commands were run.
