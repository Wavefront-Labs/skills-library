---
id: computing-software.cloud-infrastructure-engineering.azure.update-manager-maintenance-configurations-and-schedules
name: update-manager-maintenance-configurations-and-schedules
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, update-manager, maintenance-configuration, maintenance-schedule, scheduled-patching, customer-managed-schedules, patch-classifications]
level: practitioner
status: docs-checked
description: "Create Azure Update Manager maintenance configurations: recurrence, window length, classifications, KB/package include-exclude, reboot setting, assignment to VMs and Arc."
sources: ["https://learn.microsoft.com/en-us/azure/update-manager/scheduled-patching", "https://learn.microsoft.com/en-us/azure/virtual-machines/maintenance-configurations", "https://learn.microsoft.com/en-us/cli/azure/maintenance/configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update Manager maintenance configurations and schedules

**Goal:** patching happens in agreed windows per server group, with predictable reboots and no
surprises from automatic guest patching.

## Prerequisite: patch orchestration mode
Patch orchestration of Azure machines must be set to **Customer Managed Schedules** (`patchMode: AutomaticByPlatform` +
`bypassPlatformSafetyChecksOnUserSchedule: true`). Set it in the portal or with the Azure Policy
that schedules recurring updates, which also sets this property.
```bash
az vm update -g rg -n vm1 --set osProfile.windowsConfiguration.patchSettings.patchMode=AutomaticByPlatform \
  osProfile.windowsConfiguration.patchSettings.automaticByPlatformSettings.bypassPlatformSafetyChecksOnUserSchedule=true
```

## Create the configuration
```bash
az maintenance configuration create -g rg-patching -n mc-prod-win-sat02 -l westeurope \
  --maintenance-scope InGuestPatch --maintenance-window-duration "03:55" \
  --maintenance-window-recur-every "Month Second Saturday" \
  --maintenance-window-start-date-time "2026-11-01 01:00" --maintenance-window-time-zone "W. Europe Standard Time" \
  --reboot-setting IfRequired
# Add --windows-parameters (Windows machines only) or --linux-parameters (Linux only) for classifications
# and KB/package include or exclude lists; they take shorthand or JSON, run the command with `??` to see the keys.
```
- Recurrence: hourly, daily or weekly, or the nth weekday of the month with an offset of up to 6 days either way (second Tuesday plus 4 days lands on the Saturday after Patch Tuesday). Check the `--maintenance-window-recur-every` syntax on the CLI page.
- Guest (`InGuestPatch`) window: minimum 1 hour 30 minutes, maximum 3 hours 55 minutes. If a reboot is needed, 10 minutes must remain in the window or the reboot is skipped.
- `--reboot-setting`: `IfRequired`, `Never`, `Always`. Registry settings on the machine can still cause a reboot even with Never.

## Assign machines
Static: `az maintenance assignment create --maintenance-configuration-id <id> --resource-id <vm-id> -n <name>`.
Dynamic scopes suit fleets; the scheduled patching page lists their limits.

## Operating it
- Ring the fleet: `mc-dev-*` week 1, `mc-prod-*` week 2 (offset rules), with pre/post events for snapshots and app drain.
- Exclude problem KBs per configuration, document why, remove after fix.

## Gotchas
- Time zone values are named zones such as `W. Europe Standard Time` or `Pacific Standard Time`; the window follows daylight saving of that zone.

## Verify
- [ ] `az maintenance configuration show -g rg-patching -n <name>` recurrence and window as intended.
- [ ] After the first window: Update Manager history shows each machine succeeded with the expected reboot behaviour.

## Checked
2026-10-28. Confirmed on Microsoft Learn (scheduled patching, maintenance configurations and `az maintenance configuration` pages): Customer Managed Schedules prerequisite, `InGuestPatch` scope, 1 hour 30 minute minimum and 3 hours 55 minute maximum guest window, 10-minute reboot rule, nth-weekday recurrence with offset up to 6 days, `--reboot-setting` values, time zone names with daylight saving. check_commands found no bad commands or flags. Removed: `Offset4` recurrence string, one-schedule-per-scope rule, Resource Graph table name, deallocated-VM and assessment gotchas, Arc patch-mode claim.
Method: documentation only; no commands were run.
