---
id: computing-software.cloud-infrastructure-engineering.google-cloud.windows-patching-with-vm-manager
name: windows-patching-with-vm-manager
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vm-manager, os-patch, windows-patching, windows-update-classification, patch-deployment, kb-exclusions]
level: practitioner
status: docs-checked
description: "Patch Windows Server fleets with VM Manager: update classifications, KB include and exclude lists, pre/post scripts, reboot control, maintenance windows and failure triage."
sources: ["https://cloud.google.com/compute/vm-manager/docs/patch/create-patch-job", "https://cloud.google.com/compute/vm-manager/docs/patch/schedule-patch-jobs", "https://cloud.google.com/sdk/gcloud/reference/compute/os-config/patch-jobs/execute"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows patching with VM Manager

## 1. Classifications
API values: `CRITICAL`, `SECURITY`, `DEFINITION`, `DRIVER`, `FEATURE_PACK`, `SERVICE_PACK`, `TOOL`,
`UPDATE_ROLLUP`, `UPDATE`. On the gcloud command line use lowercase with hyphens (`critical`, `feature-pack`, `update-rollup`).
If no classifications are given, a default Windows update is performed. A cautious monthly set is `critical,security,definition,update-rollup`; take drivers and feature packs in planned changes.

## 2. Ad-hoc job on a canary group
```bash
gcloud compute os-config patch-jobs execute --project=<P> \
  --instance-filter-group-labels=env=prod,os=windows --instance-filter-zones=europe-west2-a \
  --windows-classifications=critical,security,definition,update-rollup \
  --windows-excludes=KB5034441 \
  --pre-patch-windows-executable=gs://<B>/scripts/drain.ps1#<GENERATION> \
  --post-patch-windows-executable=gs://<B>/scripts/undrain.ps1#<GENERATION> \
  --reboot-config=default --rollout-mode=zone-by-zone --rollout-disruption-budget-percent=20 \
  --display-name="2026-10 canary"
```
- `--windows-exclusive-patches=KB...` installs only the listed KBs and cannot be combined with classifications or excludes.
- `--reboot-config`: `default` (the agent decides from signals such as registry keys), `always`, `never` (you schedule reboots).
- Cloud Storage scripts are referenced as `gs://<bucket>/<object>#<generation>`; a `.ps1` file runs with `-NonInteractive -NoProfile -ExecutionPolicy Bypass`.
- `--dry-run` contacts the instances without patching; `--duration` is the time after which the job times out.

## 3. Recurring deployment
```bash
gcloud compute os-config patch-deployments create win-monthly --file=win-monthly.yaml
```
```yaml
instanceFilter: {groupLabels: [{labels: {os: windows, env: prod}}]}
patchConfig:
  rebootConfig: DEFAULT
  windowsUpdate: {classifications: [CRITICAL, SECURITY, DEFINITION, UPDATE_ROLLUP]}
recurringSchedule:
  timeZone: {id: Europe/London}
  timeOfDay: {hours: 2}
  frequency: MONTHLY
  monthly: {weekDayOfMonth: {weekOrdinal: 2, dayOfWeek: SATURDAY}}   # weekOrdinal 1-4, or -1 for the last week
rollout: {mode: ZONE_BY_ZONE, disruptionBudget: {percent: 25}}
duration: 10800s
```

## 4. Triage
```bash
gcloud compute os-config patch-jobs list-instance-details <JOB_ID> --format='table(name,state,failureReason)'
```
`state` values include `NO_AGENT_DETECTED` (the service could not detect the agent), `TIMED_OUT` (no success notification before the timeout), `FAILED`, `SKIPPED` and `SUCCEEDED_REBOOT_REQUIRED`. For NO_AGENT_DETECTED or TIMED_OUT the service asked the agent to patch but never heard back; see the patch-job troubleshooting steps.

## Gotchas
- Windows patching uses the Windows Update Agent.
- VMs without external access can use Cloud NAT or another proxy to reach external update sources.
- For zone-by-zone rollouts the patch job stops when the disruption budget in a zone is exceeded (failures in apply, pre/post steps or timeouts count; VMs not running or without an active agent do not). Watch the canary results before the fleet run.

## Verify
- [ ] Canary job shows all instances `SUCCEEDED` / `SUCCEEDED_REBOOT_REQUIRED`.
- [ ] Patch compliance data (taken from the Windows Update Agent API) shows no missing critical or security updates on prod Windows VMs.

## Checked
2026-10-27. Confirmed against the gcloud patch-jobs execute reference (flag names, lowercase classification values, reboot-config values, rollout flags, dry-run, duration, script path format and PowerShell flags, exclusive patches), the OS Config discovery document (WindowsUpdateSettings classifications, PatchJobInstanceDetails states, PatchRollout modes, PatchDeployment schedule fields, WeekDayOfMonth weekOrdinal range) and the VM Manager create-patch-job and OS patch management pages (disruption budget rules, Windows Update Agent, Cloud NAT, NO_AGENT_DETECTED and TIMED_OUT). Removed: Patch Tuesday comment (the second Saturday can fall before Patch Tuesday), WSUS/GPO override claim, 'common failure reason' list. Corrected: gcloud classification values are lowercase with hyphens; NO_AGENT_DETECTED and TIMED_OUT are instance states, not failure reasons.
Method: documentation only; no commands were run.
