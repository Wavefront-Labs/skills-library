---
id: computing-software.cloud-infrastructure-engineering.google-cloud.os-policy-rollouts-and-disruption-budgets
name: os-policy-rollouts-and-disruption-budgets
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vm-manager, os-policy, os-policy-rollout, disruption-budget, configuration-management, compliance]
level: advanced
status: docs-checked
description: "Roll out VM Manager OS policy assignments safely: instance filters, validation vs enforcement mode, disruption budgets and wait durations, revisions, reports and rollback."
sources: ["https://cloud.google.com/compute/vm-manager/docs/os-policies/create-os-policy-assignment", "https://cloud.google.com/compute/docs/os-configuration-management/working-with-os-policies", "https://cloud.google.com/sdk/gcloud/reference/compute/os-config/os-policy-assignments"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OS policy rollouts and disruption budgets

An OS policy assignment applies desired state (packages, repos, files, exec scripts) to
matching VMs **in one zone**. Every change creates a new revision that rolls out under a
disruption budget.

## 1. Assignment file
```yaml
osPolicies:
- id: ensure-auditd
  mode: ENFORCEMENT          # VALIDATION = report compliance only, change nothing
  resourceGroups:
  - inventoryFilters: [{osShortName: debian}]
    resources:
    - id: auditd-pkg
      pkg: {desiredState: INSTALLED, apt: {name: auditd}}
    - id: auditd-rules
      file:
        path: /etc/audit/rules.d/cis.rules
        state: CONTENTS_MATCH
        file: {gcs: {bucket: <B>, object: cis.rules, generation: <GEN>}}
instanceFilter:
  inclusionLabels: [{labels: {env: prod}}]
  exclusionLabels: [{labels: {os-policy: skip}}]
rollout:
  disruptionBudget: {percent: 10}
  minWaitDuration: 600s
```
`disruptionBudget` = the maximum number or percentage of VMs per zone disrupted at any given moment; `minWaitDuration` = the minimum time to wait after the configuration changes are applied by the current rollout.

## 2. Create, update, watch
```bash
gcloud compute os-config os-policy-assignments create prod-baseline --location=europe-west2-a --file=baseline.yaml --async
gcloud compute os-config os-policy-assignments describe prod-baseline --location=europe-west2-a --format='value(rolloutState,revisionId)'
gcloud compute os-config os-policy-assignments update prod-baseline --location=europe-west2-a --file=baseline.yaml
gcloud compute os-config os-policy-assignments list-revisions prod-baseline --location=europe-west2-a
gcloud compute os-config os-policy-assignment-reports list --location=europe-west2-a \
  --assignment-id=prod-baseline
```
Rollout states: `IN_PROGRESS`, `CANCELLING`, `CANCELLED`, `SUCCEEDED`. A new revision is committed whenever a rollout is triggered (create or update). Report entries carry a per-policy `complianceState`: `COMPLIANT`, `NON_COMPLIANT` or `UNKNOWN`.

## 3. Practice
1. New policy: ship in `VALIDATION` first, read reports, then flip to `ENFORCEMENT`.
2. One assignment per zone (assignments are zonal; a project can have at most 20 per zone unless the quota is raised).
3. Rollback = update with the previous file, which creates a new revision (`list-revisions` shows the history).

## Gotchas
- Exec resources must be idempotent: a `validate` script exits 100 when compliant and 101 when `enforce` should run; an `enforce` script exits 100 to report its changes were made.
- `file` resource content is limited to 32 KiB; use a Cloud Storage object (`file.gcs`) for larger files.
- `minWaitDuration` applies to each rollout step, so size it to the risk.

## Verify
- [ ] Reports show every targeted VM's policy as `COMPLIANT` after the rollout reaches `SUCCEEDED`.
- [ ] A test VM labelled `os-policy=skip` is excluded.

## Checked
2026-10-27. Confirmed against the OS Config discovery document (OSPolicyAssignment rollout states, revisionId, OSPolicyAssignmentRollout fields, instance filter labels, inventoryFilters osShortName, file resource state values, content limit of 32 KiB, GCS file generation, compliance state enum), the gcloud os-policy-assignments and os-policy-assignment-reports reference pages (--location with a zone, --assignment-id) and the working-with-OS-policies page (modes, exit codes 100 and 101, zonal assignments, 20 per zone). The view-reports page returned 404 and the source was replaced. Removed: Terraform resource name, halt-on-budget claim, 10-minute apply cycle, the complianceState filter on the reports list, the claim that there is no revert command.
Method: documentation only; no commands were run.
