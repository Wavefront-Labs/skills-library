---
id: computing-software.systems-network-administration.virtualisation.vmotion-stun-time-large-memory-vms
name: vmotion-stun-time-large-memory-vms
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmotion-stun, stun-during-page-send, vmotion, multi-nic-vmotion, monster-vm, vmware, vsphere]
level: advanced
status: draft
description: "Keep vMotion of large, write-heavy VMs within the switchover window: pre-copy convergence, Stun During Page Send, bandwidth, multi-NIC and vMotion streams."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management-8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vMotion of large-memory VMs and stun time

## How vMotion converges
1. Pre-copy: memory copied while the VM runs; dirty pages tracked and re-sent in
   iterations.
2. When the remaining dirty set can be sent within ~500 ms, the VM is **stunned**,
   last pages and device state sent, VM resumes on the target. Default switchover
   timeout `vmotion.maxSwitchoverSeconds` = 100 s.
3. If the guest dirties memory faster than the network sends it, ESXi applies
   **Stun During Page Send (SDPS)**: injects microsecond vCPU delays to slow the page
   dirty rate. You see this as a performance dip during migration, not an outage.

## Symptoms
- Migration stuck at e.g. 70–90 % for minutes, then fails "timed out waiting for
  migration data" or "The migration exceeded the maximum switchover time".
- App-level timeouts (clustered DB heartbeats, trading feeds) during the final stun.

## Fixes in order
1. **Bandwidth**: 25 GbE+ for VMs ≥ 512 GB; dedicated vMotion network; jumbo frames.
2. **Multi-NIC vMotion**: two vmks, each on a port group with a different active uplink
   (standby on the other), same subnet. Doubles throughput on vSS/vDS.
3. **More streams (7.0U1+/8.0)**: vMotion auto-scales streams with link speed; on 100 GbE,
   check `Migrate.VMotionStreamHelpers` (0 = auto) and use multiple vmks.
4. **Encrypted vMotion** costs CPU; on very large VMs set Opportunistic not Required if
   policy allows.
5. Migrate during low write activity (batch jobs paused), or use **cluster-level
   maintenance windows** for monster VMs.
6. Raise `vmotion.maxSwitchoverSeconds` only with app owner agreement.

## Clustered apps
For WSFC/SQL AG, Oracle RAC, Exchange DAG: increase cluster heartbeat thresholds
(e.g. WSFC `SameSubnetThreshold` 10–20) so a sub-second stun does not trigger failover.

## Diagnose
`vmware.log` of the VM: lines `Migrate: ...precopy`, `SDPS`, `Stun time`.
```sh
grep -E "precopy|SDPS|switchover|Stun" /vmfs/volumes/<ds>/<vm>/vmware.log
```

## Verify
Stun time in `vmware.log` under 1 s; migration completes within the window; no app
failover events.
