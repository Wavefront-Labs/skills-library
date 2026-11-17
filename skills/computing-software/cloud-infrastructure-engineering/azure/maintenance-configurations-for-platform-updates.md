---
id: computing-software.cloud-infrastructure-engineering.azure.maintenance-configurations-for-platform-updates
name: maintenance-configurations-for-platform-updates
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, virtual-machines, maintenance-control, platform-maintenance, dedicated-hosts, isolated-vms, maintenance-configuration]
level: advanced
status: docs-checked
description: "Control when Azure applies host platform updates with maintenance configurations (scope Host) for dedicated hosts and isolated VMs, and apply pending updates on demand."
sources: ["https://learn.microsoft.com/azure/virtual-machines/maintenance-configurations", "https://learn.microsoft.com/azure/virtual-machines/maintenance-configurations-cli", "https://learn.microsoft.com/azure/virtual-machines/maintenance-and-updates"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maintenance configurations for platform updates

**Goal:** for workloads that can't tolerate surprise host maintenance pauses, choose the window in which Azure
updates the host - for up to 35 days.

## Scopes (don't mix them up)
| maintenanceScope | Controls |
|---|---|
| **Host** | Platform updates that don't require a restart, for **dedicated hosts**, **isolated VMs** and isolated scale sets |
| OSImage | OS image upgrades for scale sets with automatic OS upgrades enabled |
| InGuestPatch | Guest patching via Azure Update Manager (VMs and Arc-enabled servers) |
This skill covers **Host**.

## Create and assign
```bash
az maintenance configuration create -g rg-maint --resource-name mc-hosts-sat --location westeurope \
  --maintenance-scope Host --maintenance-window-start-date-time "2026-11-01 02:00" \
  --maintenance-window-duration "05:00" --maintenance-window-recur-every "Week Saturday" \
  --maintenance-window-time-zone "W. Europe Standard Time"
# dedicated host
az maintenance assignment create -g rg-hosts --location westeurope --resource-name host01 \
  --resource-type hosts --provider-name Microsoft.Compute --resource-parent-name hostgroup01 \
  --resource-parent-type hostGroups --configuration-assignment-name mc-hosts-sat \
  --maintenance-configuration-id $(az maintenance configuration show -g rg-maint --resource-name mc-hosts-sat --query id -o tsv)
# isolated VM: --resource-type virtualMachines --resource-name vm01
```
The Host scope requires a window of at least two hours.

## Check and apply pending updates
```bash
az maintenance update list -g rg-hosts --resource-name host01 --resource-type hosts --provider-name Microsoft.Compute \
  --resource-parent-name hostgroup01 --resource-parent-type hostGroups
az maintenance applyupdate create -g rg-hosts --resource-name host01 --resource-type hosts --provider-name Microsoft.Compute \
  --resource-parent-name hostgroup01 --resource-parent-type hostGroups
```
Updates not applied within 35 days are applied by Azure anyway.

## Gotchas
- Host scope supports only isolated VMs and scale sets and dedicated hosts; rack-level maintenance isn't supported.
- Combine with Scheduled Events in the guest to drain gracefully even within your window.

## Verify
- [ ] Assignment listed for each host/isolated VM; `az maintenance update list` shows pending updates landing in the window.

## Checked

Date: 2026-10-28.

Confirmed against Learn (maintenance-configurations, maintenance-configurations-cli, maintenance-and-updates): three scopes (host, OS image, guest), host scope resources, 35-day schedule limit with automatic application afterwards, two-hour minimum window, `--resource-parent-name`/`--resource-parent-type hostGroups` for dedicated hosts, Scheduled Events. The CLI checker flagged the resource-parent flags as missing; the Learn CLI guide uses them as shown.
Removed: a fourth Resource scope row, the 5-hour recommendation, security-update bypass and the memory-preserving maintenance note.

Method: documentation only; no commands were run.
