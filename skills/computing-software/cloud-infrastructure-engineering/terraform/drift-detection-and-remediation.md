---
id: computing-software.cloud-infrastructure-engineering.terraform.drift-detection-and-remediation
name: drift-detection-and-remediation
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, drift, drift-detection, configuration-drift, refresh-only, detailed-exitcode, resource-drift, plan-json, show-json, jq, ignore-changes, out-of-band-changes, import-blocks, cloudtrail]
level: advanced
status: docs-checked
description: "Find and fix Terraform drift: plan -refresh-only with -detailed-exitcode, resource_drift in plan JSON, then revert, adopt via apply -refresh-only, ignore_changes or import."
sources:
  - "https://developer.hashicorp.com/terraform/cli/commands/plan"
  - "https://developer.hashicorp.com/terraform/internals/json-format"
  - "https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle"
  - "https://developer.hashicorp.com/terraform/tutorials/state/resource-drift"
  - "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events-cli.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform drift detection and remediation: know what changed, decide who wins

**Goal:** every difference between code, state and the real cloud is detected, attributed
and resolved deliberately (reverted, adopted into code, or explicitly ignored) instead of
being overwritten by the next unrelated apply. The nightly-plan pattern is introduced in
`computing-software.cloud-infrastructure-engineering.infrastructure-as-code.plan-review-and-environment-promotion`;
this skill is the triage and fix.

## 1. Detect with machine-readable output
```bash
terraform plan -refresh-only -detailed-exitcode -out=drift.tfplan -lock-timeout=5m
rc=$?            # 0 no changes, 1 error, 2 changes present
terraform show -json drift.tfplan > drift.json
jq -r '.resource_drift[]? | "\(.address)\t\(.change.actions|join(","))"' drift.json
```
- Refresh-only mode (`-refresh-only`, Terraform v0.15.4 and later) creates a plan whose goal
  is only to update state and root module outputs to match changes made to remote objects outside
  Terraform. The tutorial prefers it over the `terraform refresh` subcommand because it shows the
  changes instead of silently overwriting state.
- `-detailed-exitcode` exit codes: 0 succeeded with empty diff, 1 error, 2 succeeded with
  non-empty diff. `-out=FILE` saves the plan; `-lock-timeout=DURATION` retries a held state lock.
- In the JSON plan format, `resource_drift` describes the changes Terraform detected between the
  most recent state and the prior saved state, using the same object structure as `resource_changes`.
  `relevant_attributes` can be used to filter `resource_drift` to external changes that affected the plan.
  The `jq` filter above assumes `address` and `change.actions` fields as in `resource_changes`; test
  it against your Terraform or OpenTofu version.
- A normal `plan` (without `-refresh-only`) also reads `resource_changes`; that catches code merged
  but not yet applied, which is a pipeline gap rather than drift.

## 2. Classify each drifted item
| Kind | Usual fix |
|---|---|
| Out-of-band edit you want to undo | Revert: normal `plan` then `apply` (read the plan; without `-refresh-only` Terraform attempts to revert manual changes) |
| Out-of-band edit you want to keep | Adopt: update the configuration to match, then `terraform apply -refresh-only` to record it in state |
| Attribute owned by another process | `lifecycle { ignore_changes = [...] }` for that attribute |
| Resource exists but Terraform does not know it | Import (see below) |

The AWS CloudTrail user guide shows how to find who changed a resource:
`aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=<NAME>`.
Lookup covers management events for the last 90 days in the current Region, and only one
attribute key/value pair is allowed per command. For other clouds use their audit logs.

## 3. Remediate
- **Revert** (code is right): run `plan`, review, `apply`. The tutorial warns that a manual change
  left unreconciled means Terraform "may unintentionally destroy or recreate resources".
- **Adopt** (the change was right): edit configuration until `plan` is clean, then
  `terraform apply -refresh-only`. A refresh-only operation does not change infrastructure; it
  only records drift in state, so on its own it does not make the code agree.
- **Ignore** (another process shares management of the object):
  ```hcl
  resource "aws_autoscaling_group" "web" {
    # ...
    lifecycle { ignore_changes = [desired_capacity] }
  }
  ```
  The lifecycle page describes `ignore_changes` as the way to let Terraform share management with
  a separate process, calls such cases "rare", and says the `all` keyword makes Terraform never
  propose updates to the object. Comment why and who owns the attribute; avoid `all`.
- **Import** unmanaged resources with `import` blocks and `terraform plan -generate-config-out=PATH`
  (PATH must not already exist); see
  `computing-software.cloud-infrastructure-engineering.terraform.importing-existing-infrastructure`.

## Prevent
Make humans read-only on managed resources and apply only from CI, so that out-of-band edits
are the exception. Preventive controls are organisational and not set by these pages.

## Gotchas
- Exit code 2 means a non-empty diff; check `resource_drift` and `resource_changes` before alerting
  on it, and pin the jq filter in a test because JSON shapes can differ between Terraform and OpenTofu versions.
- Drift jobs take the state lock unless locking is disabled, so use `-lock-timeout` and schedule them
  away from deploy windows.
- `ignore_changes` hides future edits to that attribute in code as well.

## Verify
- [ ] The scheduled job runs `plan -refresh-only -detailed-exitcode` per root and reports addresses from `resource_drift`.
- [ ] A manual change in a sandbox shows up by address in the next report.
- [ ] Every `ignore_changes` has a comment naming the owning system.
- [ ] After remediation, `plan -refresh-only` and `plan` both exit 0.

## Checked
Checked 2026-11-08 against the Terraform `plan` command page, the JSON output format page, the lifecycle
meta-argument page, the "Manage resource drift" tutorial and the AWS CloudTrail "view events with the CLI" page.
Removed: the perpetual-diff and k8s/AWS-tag rows, the claim that a refresh during plan only changes in-memory
state, the exit-code-2-for-output-only claim, the `default_tags` tagging and cloud-inventory approach, the
aztfexport mention, and the claim that `tag` or `desired_capacity` are universal ignore targets.
Method: docs-only read of cited pages, 2026-11-08
