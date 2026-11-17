---
id: computing-software.cloud-infrastructure-engineering.google-cloud.zone-by-zone-patch-rollout-and-disruption-budgets
name: zone-by-zone-patch-rollout-and-disruption-budgets
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vm-manager, patch-rollout-zones, patch-disruption-budget, patch-deployments, rollout-mode, os-config]
level: practitioner
status: docs-checked
description: "Roll out VM Manager patches safely: zone-by-zone vs concurrent mode, disruption budget as count or percent, canary waves via label groups, and stopping a bad patch job."
sources: ["https://docs.cloud.google.com/compute/vm-manager/docs/patch/create-patch-job", "https://docs.cloud.google.com/compute/vm-manager/docs/patch/schedule-patch-jobs", "https://docs.cloud.google.com/sdk/gcloud/reference/compute/os-config/patch-jobs/cancel", "https://docs.cloud.google.com/sdk/gcloud/reference/compute/os-config/patch-deployments/pause", "https://osconfig.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zone-by-zone patch rollout and disruption budgets

## Rollout options
- `--rollout-mode=zone-by-zone` (API `ZONE_BY_ZONE`): one zone at a time; the next zone starts when the previous one has completed. The job begins in the region with the fewest targeted VMs.
- `--rollout-mode=concurrent-zones` (`CONCURRENT_ZONES`): all zones at the same time.
- Disruption budget: the maximum number or percentage of VMs **per zone** disrupted at once: `--rollout-disruption-budget=5` or `--rollout-disruption-budget-percent=20` (API `disruptionBudget.fixed` / `.percent`). A VM counts as disrupted from the moment the agent is notified until patching completes, including reboot and post-patch steps. It also keeps counting if patching fails, a pre or post step fails, or it never answers before timing out. VMs that are not running or have no active agent do not count.
- Under zone-by-zone, if the budget in a zone is exceeded by failures, the whole job stops. With a budget of 10 and 8 failed VMs, the job continues two at a time in that zone, then 10 at a time in the next.

## Waves with recurring deployments
```yaml
# canary.yaml: patch deployment, second Wednesday of the month
instanceFilter: {groupLabels: [{labels: {env: prod, patch-wave: canary}}]}
patchConfig: {rebootConfig: DEFAULT, apt: {type: DIST}, yum: {security: true}}
recurringSchedule:
  timeZone: {id: Europe/London}
  frequency: MONTHLY
  monthly: {weekDayOfMonth: {weekOrdinal: 2, dayOfWeek: WEDNESDAY}}
  timeOfDay: {hours: 2}
rollout: {mode: ZONE_BY_ZONE, disruptionBudget: {percent: 25}}
duration: 7200s
```
```bash
gcloud compute os-config patch-deployments create prod-canary --file=canary.yaml
```
`weekOrdinal` is 1 to 4, or -1 for the last week. `dayOffset` on `weekDayOfMonth` shifts the run by days before or after, so a `patch-wave: main` deployment can use the same weekday with a positive offset. If the canary fails, stop the main wave: `gcloud compute os-config patch-deployments pause prod-main` (state becomes `PAUSED`, so no patch jobs are generated).

## Stopping a bad job
```bash
gcloud compute os-config patch-jobs cancel <JOB_ID>
```
The job must currently be active.

## Gotchas
- The budget is per zone, so 25% in 3 zones with zone-by-zone means 25% of one zone at a time.
- `duration` is the maximum time for the job; it times out when it ends. No new VM patching starts after the window, though a download or reboot already running may finish later.
- A patch job targets at most 500 VMs, and instance filters resolve when the job starts.

## Verify
- [ ] Monitoring shows serving capacity never dropped below target during a prod rollout.

## Checked
2026-10-28. Confirmed against the "Create a patch job" page (rollout modes, per-zone budget, what counts as disrupted, job stops when a zone's budget is exceeded, worked example, 500-VM limit), the gcloud `patch-jobs execute`, `patch-jobs cancel` and `patch-deployments pause` references, and the OS Config v1 discovery document (`PatchRollout`, `FixedOrPercent`, `RecurringSchedule`, `WeekDayOfMonth` with `weekOrdinal` and `dayOffset`, `PatchDeployment.state` and `duration`). Removed: the claim that zone-by-zone keeps regional services up, the "in-flight VMs finish" detail, the "timed-out" marking of remaining VMs, the MIG-image note, and a wrong "Patch Tuesday" comment on the schedule.
Method: documentation only; no commands were run.
