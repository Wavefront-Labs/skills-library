---
id: computing-software.systems-network-administration.patch-management.aws-ssm-patch-manager
name: aws-ssm-patch-manager
category: computing-software
field: systems-network-administration
product: patch-management
tags: [ssm-patch-manager, patch-deployment, patch-baseline, maintenance-window, aws, patch-compliance]
level: practitioner
status: docs-checked
description: "Patch EC2 and hybrid servers with AWS Systems Manager Patch Manager: patch baselines with approval delays, patch groups, maintenance windows or patch policies, and compliance."
sources:
  - https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager.html
  - https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-policies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Systems Manager Patch Manager

## Building blocks
- **Patch baseline**: OS, approval rules (classification, severity, auto-approve after N
  days), explicit approved/rejected patches, whether non-security updates are included.
  AWS-provided defaults exist (`AWS-DefaultPatchBaseline` etc.); create custom ones for
  control.
- **Patch group**: tag `Patch Group` (or `PatchGroup`) on instances → baseline mapping. Use `PatchGroup` (no space) if tags in instance metadata are allowed; patch groups are not used by patch-policy-based patching.
- **Run**: `AWS-RunPatchBaseline` document with `Operation=Scan` or `Install`,
  `RebootOption=RebootIfNeeded|NoReboot` (default `RebootIfNeeded`).
- **Scheduling**: Quick Setup **patch policies** (organisation-wide) or maintenance
  windows with targets and concurrency/error thresholds.

## Custom baseline (CLI)
```sh
aws ssm create-patch-baseline --name "rhel9-prod" --operating-system REDHAT_ENTERPRISE_LINUX \
  --approval-rules 'PatchRules=[{PatchFilterGroup={PatchFilters=[{Key=CLASSIFICATION,Values=[Security,Bugfix]},{Key=SEVERITY,Values=[Critical,Important]}]},ApproveAfterDays=7,EnableNonSecurity=false}]' \
  --rejected-patches "<package-name>" --rejected-patches-action BLOCK
aws ssm register-patch-baseline-for-patch-group --baseline-id pb-0abc... --patch-group "rhel9-prod"
```
Windows baselines approve by MSRC severity and classification; `ApproveAfterDays` gives
ring-like deferral (dev 0, prod 7); it is not supported for Debian Server or Ubuntu Server baselines.

## Maintenance window run
```sh
aws ssm send-command --document-name AWS-RunPatchBaseline \
  --targets Key=tag:PatchGroup,Values=rhel9-prod \
  --parameters Operation=Install,RebootOption=RebootIfNeeded \
  --max-concurrency 10% --max-errors 5%
```
Prefer this inside a maintenance window task so it's scheduled and logged.

## Compliance
```sh
aws ssm list-compliance-summaries --filters Key=ComplianceType,Values=Patch
aws ssm describe-instance-patch-states-for-patch-group --patch-group rhel9-prod
```
See the Patch Manager compliance documentation for org-wide reporting options.

## Gotchas
- Instances must be SSM-managed (agent, IAM role, network path to SSM endpoints).
- Linux baselines use the instance's configured repos; a broken repo looks like "no
  patches". Use repo snapshots for reproducibility.
- `ApproveAfterDays` counts from each patch's release date, evaluated in UTC.
- Stateful clusters need orchestration beyond percentage concurrency (one node per AZ, etc.).

## Verify
Compliance summary shows Compliant ≥ target per patch group; a test instance with a known
missing patch flips to Compliant after the window.

## Checked
Date: 2026-10-27. Documentation checked: AWS CLI references for `ssm create-patch-baseline` (operating system names, `ApproveAfterDays` and its Debian/Ubuntu limit, `EnableNonSecurity`, `--rejected-patches-action` ALLOW_AS_DEPENDENCY or BLOCK), `register-patch-baseline-for-patch-group`, `describe-instance-patch-states-for-patch-group` and `list-compliance-summaries` (`ComplianceType` Patch); Systems Manager pages for patch groups (tag keys `Patch Group` and `PatchGroup`, not used with patch policies), `AWS-RunPatchBaseline` parameters (`Operation` Scan or Install, `RebootOption` default RebootIfNeeded) and predefined baselines (`AWS-DefaultPatchBaseline`). Removed the Resource Data Sync, Security Hub and repository-metadata release-date claims, and the example kernel package name.

Method: documentation only; no commands were run.
