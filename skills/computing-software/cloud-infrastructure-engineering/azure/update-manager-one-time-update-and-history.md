---
id: computing-software.cloud-infrastructure-engineering.azure.update-manager-one-time-update-and-history
name: update-manager-one-time-update-and-history
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, update-manager, one-time-update, update-now, update-history, install-patches, emergency-patching]
level: practitioner
status: docs-checked
description: "Push an emergency patch with Update Manager one-time update (portal, az vm install-patches, Arc), then audit results and update history across the fleet with ARG."
sources: ["https://learn.microsoft.com/azure/update-manager/deploy-updates", "https://learn.microsoft.com/azure/update-manager/manage-multiple-machines", "https://learn.microsoft.com/azure/update-manager/query-logs", "https://learn.microsoft.com/cli/azure/vm#az-vm-install-patches"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# One-time update and update history

**Goal:** a zero-day patch is on every affected machine within hours, and you can prove it.

## Assess first
```bash
az vm assess-patches -g rg -n vm1          # assessment of one VM, returns available patches
```
Fleet: Update Manager → Machines → select → **Check for updates**.

## Install now
Portal: Update Manager → Machines → select → **One-time update** → choose
classifications or specific KB/package → maintenance window (minutes, max 235) → reboot option.

CLI per VM:
```bash
az vm install-patches -g rg -n vm1 --maximum-duration PT2H --reboot-setting IfRequired \
  --classifications-to-include-win Critical Security --kb-numbers-to-include KB5044284
az vm install-patches -g rg -n lx1 --maximum-duration PT1H --reboot-setting IfRequired \
  --classifications-to-include-linux Security --package-name-masks-to-include "openssl*"
```
For Arc-enabled servers use the portal one-time update; loop the CLI per VM for many Azure VMs.

## History and audit
```kusto
patchinstallationresources
| where type has "softwarepatches" and properties.lastModifiedDateTime > ago(1d)
| where properties.patchName has "KB5044284"
| project machine = tostring(split(id, "/")[8]), state = tostring(properties.installationState), when = properties.lastModifiedDateTime
```
```kusto
patchinstallationresources
| where type !has "softwarepatches"
| extend status = tostring(properties.status), start = todatetime(properties.startDateTime)
| where start > ago(1d)
| summarize count() by status
```
Portal: Update Manager → **History**. Update Manager results are kept in Azure Resource Graph for 30 days, so export evidence within that window.
Per-machine: VM → Updates → History.

## Gotchas
- A reboot may still be needed after install; track `rebootStatus` (NotNeeded, Required, Started and so on) in the installation results.
- Run `status` values: NotStarted, InProgress, Failed, Succeeded, CompletedWithWarnings; per-patch `installationState`: Installed, Failed, Pending, NotSelected, Excluded.
- The longest supported maximum duration for an installation is 235 minutes.

## Verify
- [ ] ARG shows the target KB/package installed on all in-scope machines (count = fleet count).
- [ ] Machines needing reboot listed and scheduled.
- [ ] Exported history attached to the change/incident record.

## Checked
2026-10-27. Confirmed against Learn: Update Manager deploy-updates (235-minute maximum), manage-multiple-machines, query-logs (patchinstallationresources and patchassessmentresources properties, status and installationState values, 30-day retention) and the az vm install-patches CLI reference (all flags above matched).
Removed (unconfirmed): `az connectedmachine install-patches` with `--windows-parameters`, the "hundreds of machines" figure, the one-time-update/schedule interaction, the Linux package-mask matching note and the CompletedWithWarnings cause.
Method: documentation only; no commands were run.
