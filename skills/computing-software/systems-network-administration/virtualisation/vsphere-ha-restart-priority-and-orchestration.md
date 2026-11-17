---
id: computing-software.systems-network-administration.virtualisation.vsphere-ha-restart-priority-and-orchestration
name: vsphere-ha-restart-priority-and-orchestration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsphere-ha, restart-priority, vm-restart-orchestration, vm-dependencies, ha-overrides, startup-order, vmware, vsphere]
level: practitioner
status: draft
description: "Order vSphere HA restarts: five restart priorities, start-next conditions (heartbeats, guest ready, delay), VM-to-VM dependency rules, and tiering infrastructure VMs first."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere HA restart priority and orchestration

**Goal:** after a host failure, DNS, directory and databases come back before the
application servers that need them.

## Restart priority
Six levels: Highest, High, Medium (default), Low, Lowest, Disabled. Set per VM in
Cluster → Configure → VM Overrides. Suggested tiers:
| Tier | VMs |
|---|---|
| Highest | Domain controllers, DNS, vCenter (if on this cluster), NSX managers |
| High | Database servers, message brokers |
| Medium | Application servers |
| Low | Web/front ends |
| Lowest/Disabled | Test, dev, VDI pools that rebuild themselves |

## "Start next priority VMs when"
Cluster-wide condition before HA moves to the next tier:
- **Resources allocated** (default): placed and powered on, fastest.
- **Powered on**.
- **Guest heartbeats detected** (VMware Tools running).
- **App heartbeats detected**.
Plus **additional delay** (seconds) and a **timeout** (default 600 s) after which HA
continues anyway, so one broken VM cannot block the rest.

## VM-to-VM dependency rules
Configure → VM/Host Rules → "Virtual Machines to Virtual Machines" rule: VMs in group B
restart only after group A is started. Use sparingly; they are hard dependencies and HA
waits up to the timeout. Priorities are usually enough.

## PowerCLI
```powershell
Get-VM dc01,dc02 | Set-VM -HARestartPriority Highest -Confirm:$false
Get-Cluster Prod | Get-VM | Select Name, HARestartPriority | Sort HARestartPriority
```
(Newer priority levels may need the vSphere API `ClusterDasVmSettings` via `Get-View`.)

## Gotchas
- Priority affects HA restarts only, not DRS or a manual cluster power-on; for whole-site
  power-up you still need a documented startup order.
- Admission control decides whether there is room at all; priorities only order
  restarts within the capacity you have.
- Disabled restart priority leaves VMs off after a failure; flag them on a report so it
  is a choice, not an accident.

## Verify
Export VM overrides and compare to the tier list; in a test failure the event log shows
Highest-tier VMs started first.
