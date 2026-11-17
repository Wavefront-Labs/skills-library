---
id: computing-software.systems-network-administration.virtualisation.vsan-health-and-resync-monitoring
name: vsan-health-and-resync-monitoring
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan, vsan-health, vsan-resync, skyline-health, rvc, esxcli-vsan, vsan-performance-service, object-health, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Read vSAN Skyline Health and resync status, interpret object health states, use esxcli vsan and the performance service, and decide what is urgent."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsan/vsan/8-0/vsan-monitoring/monitoring-vsan-skyline-health.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsan/vsan/8-0/vsan-monitoring/monitoring-vsan-skyline-health/about-the-vsan-skyline-health.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vSAN health and resync monitoring

**Goal:** know in minutes whether vSAN data is fully protected, degraded or unavailable,
and what the cluster is rebuilding.

## Where to look
- **Cluster → Monitor → vSAN → Skyline Health**: grouped checks (network, physical disk,
  data, cluster, capacity, HCL). Retest after fixes; silence only with a documented reason.
- **Resyncing Objects**: bytes left, ETA, reason (repair, policy change, rebalance,
  decommission).
- **Virtual Objects**: per-VM object state.
- **Performance service** (enable it): front-end IOPS/latency per VM, backend, and
  resync traffic.

## Object health states
| State | Meaning | Urgency |
|---|---|---|
| Healthy | All components present | — |
| Reduced availability with no rebuild | Component absent, rebuild waiting for the repair-delay timer (absent) | Watch; fix promptly |
| Reduced availability with no rebuild - delay timer | Same, timer running | Same |
| Non-availability related reconfig / incompliance | Policy not met but data available | Plan fix |
| Inaccessible | Quorum lost, VM I/O stopped | Emergency |
Absent (host down, network partition) waits the `VSAN.ClomRepairDelay` timer before
rebuilding; Degraded (device failed) rebuilds immediately.

## CLI
```sh
esxcli vsan cluster get                  # membership, master/backup, sub-cluster count
esxcli vsan network list
esxcli vsan debug object health summary get
esxcli vsan debug resync summary get
esxcli vsan storage list                 # OSA devices;  esxcli vsan storagepool list (ESA)
```
`Sub-Cluster Member Count` lower than host count means a partition, usually vSAN vmk
network (MTU, VLAN, multicast on very old versions).

## Gotchas
- Raising the repair delay for planned long maintenance is fine; forgetting to set it
  back delays real repairs.
- Don't start another host maintenance while resync is running; you can drop to zero
  redundancy.
- Capacity checks turn red when slack is too low to rebuild a host; that is an outage
  waiting to happen, not cosmetic.

## Verify
Skyline Health all green or acknowledged; `resync summary` shows 0 bytes left before any
planned maintenance; object health summary shows only Healthy.

## Checked
2026-10-31: Confirmed the Skyline Health monitoring location and grouping, Resyncing
Objects view and the `VSAN.ClomRepairDelay` option name (esxcli vsan debug advcfg list)
against the vSAN 8.0 Skyline Health pages and the ESXCLI vsan reference. Removed the
60-minute default value for the repair delay (not stated on the fetched pages).
Method: documentation only; no commands were run.
