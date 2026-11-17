---
id: computing-software.systems-network-administration.virtualisation.vcenter-tasks-and-events-console
name: vcenter-tasks-and-events-console
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcenter-events-console, vcenter-events, get-vievent, vmware, vsphere]
level: intro
status: docs-checked
description: "Filter and export vCenter tasks and events to find who changed or deleted something, set event retention, and query events with PowerCLI."
sources:
  - https://developer.broadcom.com/powercli/latest/vmware.vimautomation.core/commands/get-vievent
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/7-0/vsphere-monitoring-and-performance/monitoring-events-and-alarms/retention-of-events.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vCenter tasks and events: filtering and export

**Goal:** answer "who did what, when" for any inventory object.

## In the vSphere Client
- Object -> **Monitor** -> *Tasks* or *Events*. Filter by type text, user, date; the Events view includes Info/Warning/Error events and their target.
- Use the column filter on *Description* (for example "Removed", "Reconfigured", "Powered off").
- **Export** (top right) saves the current filtered view to CSV.
- Event details show the user, target, related task and full message (for reconfigure events, the changed settings).

## PowerCLI queries
```powershell
# Who deleted VMs in the last 7 days
Get-VIEvent -Start (Get-Date).AddDays(-7) -MaxSamples 100000 |
  Where-Object { $_ -is [VMware.Vim.VmRemovedEvent] } |
  Select CreatedTime, UserName, FullFormattedMessage

# All events for one VM
Get-VIEvent -Entity (Get-VM app01) -MaxSamples 5000 | Select CreatedTime, UserName, FullFormattedMessage

# Recent tasks
Get-Task | Select Name, State, StartTime, @{n='User';e={$_.ExtensionData.Info.Reason.UserName}}
```
For large ranges, use the vSphere API event collector with paging; `Get-VIEvent` without `-Start` is slow.

## Retention
vCenter -> Configure -> Settings -> General -> **Database**: event cleanup is enabled by default and retains events for 30 days. Longer retention grows the database; forward events to a SIEM via vCenter syslog instead.

## Gotchas
- Actions taken directly on an ESXi host (Host Client, esxcli) are not in vCenter events; check the host's own logs.
- HA restarts appear as events by the `vpxuser`/system, not a person.

## Verify
The export or query lists the event with the user principal that did it.

## Checked
2026-10-31: Confirmed Get-VIEvent parameters (-Start, -MaxSamples, -Entity, -Types) against
the PowerCLI Get-VIEvent reference page, and the 30-day default event retention (cleanup
enabled by default since vCenter 6.5) against the "Retention of Events" page. Removed the
EventManager/CreateCollectorForEvents API names and the hostd.log/shell.log file names
(not confirmed in fetched pages).
Method: documentation only; no commands were run.
