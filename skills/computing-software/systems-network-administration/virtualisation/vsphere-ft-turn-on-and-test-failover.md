---
id: computing-software.systems-network-administration.virtualisation.vsphere-ft-turn-on-and-test-failover
name: vsphere-ft-turn-on-and-test-failover
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ft-test-failover, vsphere-fault-tolerance, fault-tolerance, vmware, vsphere]
level: practitioner
status: draft
description: "Turn on vSphere Fault Tolerance for a VM, confirm the secondary is protected, and run Test Failover and Test Restart Secondary to prove it before relying on it."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1013428
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Turn on FT and test failover

**Goal:** an FT-protected VM whose secondary has been proven to take over with no downtime.

## Before turning on
- Dedicated FT logging vmkernel (10 GbE+, 25 GbE for 4+ vCPU) on every host: vmk with *Fault Tolerance logging* service.
- HA enabled on the cluster; at least 3 hosts recommended so a secondary can be re-created after failover.
- VM within limits (vSphere 8: up to 8 vCPU / 128 GB, max 4 FT VMs or 8 FT vCPUs per host by default). No snapshots, no linked clones, no USB/serial passthrough.

## Turn on
VM -> Fault Tolerance -> Turn On Fault Tolerance -> pick datastore for the secondary's files (separate datastore improves resilience) and host. Initial sync copies memory and disks. Status becomes *Protected*.

PowerCLI (API):
```powershell
$vm = Get-VM app-db01
$vm.ExtensionData.CreateSecondaryVM_Task($null)
```

## Test
- **Test Failover**: VM -> Fault Tolerance -> Test Failover. The primary is killed, the secondary becomes primary, a new secondary is created. Clients should see no disconnect; check application sessions.
- **Test Restart Secondary**: kills the secondary to verify it is recreated.
Both are safe to run in business hours if the FT network is healthy, but run the first one in a window.

## Monitor
VM -> Summary -> Fault Tolerance: *Log bandwidth*, *Secondary VM latency*. High latency means FT logging network or the secondary host is slow and the primary is being throttled.

## Gotchas
- FT doubles CPU, memory and storage use.
- Backups of FT VMs work through snapshot APIs only with vSphere 6.5+ and supported backup vendors.
- DRS does not move FT VMs freely; placement is managed by FT/HA.

## Verify
After Test Failover the status returns to *Protected* within minutes, with the new secondary on a different host.
