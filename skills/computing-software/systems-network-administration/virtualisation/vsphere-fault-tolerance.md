---
id: computing-software.systems-network-administration.virtualisation.vsphere-fault-tolerance
name: vsphere-fault-tolerance
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [fault-tolerance, vsphere-ft, ft-logging, smp-ft, secondary-vm, zero-downtime, vsphere-ha, vmware, vsphere]
level: advanced
status: docs-checked
description: "Use vSphere Fault Tolerance: when it fits, vCPU/size limits, dedicated FT logging network, secondary VM placement, latency cost, and testing failover."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-availability/providing-fault-tolerance-for-virtual-machines/fault-tolerance-requirements-limits-and-licensing.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vSphere Fault Tolerance (FT)

**Goal:** zero-downtime, zero-data-loss protection for a small VM against a host failure,
where application-level clustering is not available.

## How it works
A **secondary VM** on another host runs in lockstep via fast checkpointing over the FT
logging network. If the primary's host fails, the secondary takes over in seconds with
the same memory state; HA then creates a new secondary.

## Limits (vSphere 8, check the current maxima)
- Up to 8 vCPUs per FT VM with VVF/Enterprise Plus licensing (2 vCPUs on Standard and
  Enterprise); host defaults of 4 FT VMs and 8 FT vCPUs per host, both adjustable with no
  hard maximum.
- Not supported with: snapshots (backup tools using VADP are supported via special
  handling), Storage vMotion of a running FT VM in older versions, linked clones,
  physical RDMs, vVols in some versions, devices like USB and serial passthrough.
- Secondary has its **own copy of the disks** (on a different datastore preferably), so
  storage doubles.

## Network
- Dedicated **FT logging vmk** on each host; bandwidth roughly follows the VM's disk
  writes plus network receive rate.
- Low latency between hosts; FT adds latency to every write/receive acknowledgement.

## Turning it on
VM → Fault Tolerance → Turn On: choose datastore and host for the secondary. Requires HA
enabled and hosts with FT-capable, compatible CPUs (EVC helps).

## Operations
- **Test Failover** and **Test Restart Secondary** from the VM menu (in a window).
- Turn off FT before maintenance that needs snapshots or reconfiguration; suspend FT to
  keep config but stop protection.
- Monitor "FT latency" and "secondary VM lag" in performance charts.

## When not to use
FT protects only against host hardware failure. A guest crash, patch problem or app bug
crashes both copies. Application clustering (SQL AG, DAG) protects against more and
often costs less.

## Verify
VM summary shows Fault Tolerance Status "Protected"; Test Failover succeeds with no
client disconnect beyond a brief pause.

## Checked
2026-10-31: Confirmed the per-VM FT vCPU limits by licensing edition (8 vCPUs on
Enterprise Plus/VVF, 2 on Standard/Enterprise) and the host defaults of 4 FT VMs and 8 FT
vCPUs (adjustable, no hard maximum) against the vSphere 8.0 "Fault Tolerance Requirements,
Limits, and Licensing" page. Removed the 128 GB memory figure and the 10/25 GbE bandwidth
figures (not stated on the fetched pages).
Method: documentation only; no commands were run.
