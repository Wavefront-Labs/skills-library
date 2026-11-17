---
id: computing-software.cloud-infrastructure-engineering.azure.update-manager-patch-orchestration
name: update-manager-patch-orchestration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, update-manager, azure-update-manager, patch-orchestration, maintenance-configurations, dynamic-scoping, hotpatch, automatic-vm-guest-patching, patch-assessment, patch-mode, azure-orchestrated, pre-post-events, event-grid, wsus, azure-arc, patch-compliance, reboot-setting, windows-update, linux-updates]
level: practitioner
status: docs-checked
description: "Patch Azure and Arc machines with Update Manager: periodic assessment, maintenance configurations, dynamic scopes, patch modes, hotpatch, pre/post events, reboot control."
sources: ["https://learn.microsoft.com/en-us/azure/update-manager/overview", "https://learn.microsoft.com/en-us/azure/update-manager/scheduled-patching", "https://learn.microsoft.com/en-us/azure/update-manager/dynamic-scope-overview", "https://learn.microsoft.com/en-us/azure/update-manager/pre-post-scripts-overview", "https://learn.microsoft.com/en-us/azure/update-manager/manage-pre-post-events", "https://learn.microsoft.com/en-us/azure/automanage/automanage-hotpatch", "https://learn.microsoft.com/en-us/cli/azure/maintenance/configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update Manager — patch windows you can defend to change control

**Goal:** every VM and Arc server assessed daily, patched in a known window in waves,
with a compliance view that satisfies the auditor and a reboot you planned.

## 1. Prerequisites
- Azure VMs: the VM agent only (no extra agent). Arc servers: the Connected Machine
  agent. Check the supported-OS list in the prerequisites page before onboarding.
- Scheduled patching uses the **Customer Managed Schedules** orchestration: it sets the
  VM properties patch mode `AutomaticByPlatform` and `BypassPlatformSafetyChecksOnUserSchedule`
  = true, which Update Manager does for you after you consent in the portal. Patch mode values
  are `AutomaticByOS`, `AutomaticByPlatform`, `ImageDefault` and `Manual` (Windows allows
  `AutomaticByOS`, `AutomaticByPlatform`, `Manual`; Linux allows `AutomaticByPlatform`, `ImageDefault`).
- Periodic assessment checks for updates every 24 hours; enable it per machine or at scale with Azure Policy.
- Windows VMs pull from Windows Update/Microsoft Update or WSUS (set by GPO/registry);
  Linux from the distro repos — Update Manager is the orchestrator, not the source.
  Private subnets need outbound access to the update sources.

## 2. Maintenance configuration
```bash
az maintenance configuration create -g rg-ops -n mc-prod-wave1 -l uksouth --maintenance-scope InGuestPatch \
  --maintenance-window-start-date-time "2026-11-01 02:00" --maintenance-window-duration "03:55" \
  --maintenance-window-recur-every "Month Second Tuesday" --maintenance-window-time-zone "UTC" \
  --reboot-setting IfRequired \
  --install-patches-windows-parameters '{"classificationsToInclude":["Critical","Security"],"kbNumbersToExclude":[]}' \
  --install-patches-linux-parameters '{"classificationsToInclude":["Critical","Security"]}'
az maintenance assignment create ... --maintenance-configuration-id <mc-id> --resource-id <vm-id>   # static
```
- Recurrence can be the nth weekday of the month with an offset of up to +/-6 days (the docs example: second Tuesday with +4 days gives the following Saturday). Use offsets to stagger waves; see the `az maintenance configuration create` reference for the exact `--maintenance-window-recur-every` syntax.
- The longest supported maintenance window duration is 235 minutes (3 h 55 min).
- **Dynamic scoping** groups machines by subscription, resource group, location, resource type, OS type and tags, so new VMs join a schedule without per-VM assignments (`az maintenance assignment create` has `--filter-tags` and `--filter-os-types`).
- `--reboot-setting` accepts `IfRequired`, `Never`, `Always`.

## 3. Pre/post events
Maintenance configuration → *Events* → Event Grid system topic → subscriptions for
the pre-maintenance and post-maintenance events (the pre-event is delivered about 30 minutes
before the schedule start; handlers such as an Automation runbook or Function can start
deallocated VMs, take a snapshot, or silence alerts, and the post-event can deallocate
again or run smoke tests). Event Grid delivery is at-least-once, so handlers must be idempotent.
Cancelling is your job: the cancellation API must be called from the pre-event at least 10 minutes
before the start time, otherwise the run proceeds in the window. A pre-event schedule needs at least
40 minutes lead time when you create or edit it, or the current run is auto-cancelled.

## 4. On-demand and hotpatch
- `az vm assess-patches` / `az vm install-patches --maximum-duration PT2H --reboot-setting IfRequired --classifications-to-include-win Critical Security`
  for a single machine now (also from the portal *One-time update* over many).
- **Hotpatch**: supported Windows Server 2022 and 2025 images (see the Hotpatch page for the exact publisher/offer/SKU list). A baseline is refreshed every three months and you receive hotpatch releases for the next two months; baselines need a restart, as do updates outside the Hotpatch program. `az vm` has `--enable-hotpatching`, which requires `--patch-mode AutomaticByPlatform` and `--enable-agent`. Hotpatch does not support automatic rollback.
- Automatic VM guest patching without your own schedule (Azure Managed - Safe Deployment): patch mode `AutomaticByPlatform`, with Azure applying patches on availability-first principles.
- Linux on-demand: `--classifications-to-include-linux Critical Security Other`; `az vm install-patches` also has `--package-name-masks-to-exclude` and `--exclude-kbs-requiring-reboot`.

## 5. Compliance and reporting
Update Manager portal -> *Machines* / *History*, and Azure Resource Graph (`patchassessmentresources`; the Update Manager query-logs page documents the properties):
```kusto
patchassessmentresources
| where type =~ "microsoft.compute/virtualmachines/patchassessmentresults"
| extend crit = toint(properties.availablePatchCountByClassification.critical), sec = toint(properties.availablePatchCountByClassification.security)
| where crit + sec > 0 | project id, crit, sec, lastAssessed = properties.lastModifiedDateTime
```

## Gotchas
- Scheduled patching requires patch mode `AutomaticByPlatform` with the bypass property; machines left on another patch mode are not on the Customer Managed Schedules orchestration.
- Other patch orchestrators on the same machine (for example Windows Update for Business or Intune policies) compete with Update Manager; pick one.
- Pre-event handlers that start deallocated VMs must also decide whether to cancel: a failed pre-event does not cancel the run by itself.
- Pre-event cancellation applies to one schedule run, not the entire schedule.

## Verify
- [ ] Every production VM shows *Assessment: compliant/non-compliant* with a timestamp < 24 h in Update Manager (none *No data*).
- [ ] Maintenance run history: `Succeeded` for all machines in the wave; failures triaged within the next business day.
- [ ] Pre/post event test: a deallocated VM is started, patched, and deallocated again in one run; a deliberate pre-event failure cancels the run.
- [ ] Resource Graph query above returns 0 rows a week after each Patch Tuesday wave.

## Checked
2026-10-27. Confirmed against Learn: Update Manager overview, scheduled patching, dynamic scope, pre/post events (timings, cancellation), manage multiple machines (patch orchestration modes), query-logs (Resource Graph tables and properties), Hotpatch, and the az maintenance configuration/assignment and az vm install-patches CLI references (every flag used above matched).
Corrected: recurrence offsets (+/-6 days, not Offset7/Offset10), pre-event timing and cancellation rules, window maximum stated as 235 minutes.
Removed (unconfirmed): ESU note, FQDN tag, built-in policy names, `--extension-properties InGuestPatchMode=User`, the az vm update --set property paths, event type names, default patch-mode claims, Windows Update/proxy details, the 20-minute rule and the alerts preview note.
Method: documentation only; no commands were run.
