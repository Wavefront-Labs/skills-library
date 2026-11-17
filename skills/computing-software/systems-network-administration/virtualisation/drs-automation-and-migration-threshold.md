---
id: computing-software.systems-network-administration.virtualisation.drs-automation-and-migration-threshold
name: drs-automation-and-migration-threshold
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [drs, drs-automation-level, migration-threshold, vm-drs-score, predictive-drs, scalable-shares, vm-overrides, resource-management, vmware, vsphere, drs-score, drs-recommendations, drs-vm-overrides]
level: practitioner
status: draft
description: "Tune DRS: manual/partial/fully automated, migration threshold 1-5, the VM DRS score model in 7/8, per-VM overrides, predictive DRS and reading DRS recommendations."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management-8-0/creating-a-drs-cluster.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DRS automation level and migration threshold

**Goal:** DRS places and balances VMs so they get the resources they demand, without
endless vMotions or surprises for VMs that must not move.

## Automation levels
| Level | Initial placement | Load balancing |
|---|---|---|
| Manual | recommendation | recommendation |
| Partially automated | automatic | recommendation |
| Fully automated (default for most) | automatic | automatic |
Maintenance mode evacuation only happens automatically in Fully automated (otherwise you
apply each recommendation).

## Migration threshold (1 conservative ... 5 aggressive)
vSphere 7+ DRS balances by **VM DRS score** (how well each VM's demand is met on its
current host, 0-100%), checked every minute, not by host load deviation. Level 3
(default) is right for most clusters. Raise to 4 for bursty workloads where contention
matters more than vMotion overhead; level 1 only applies mandatory moves (rules,
maintenance).

## Per-VM overrides
Cluster → Configure → VM Overrides: set DRS automation per VM, e.g. Manual or Disabled
for licensing-bound VMs, VMs with passthrough devices, or appliances that dislike vMotion.
Prefer VM-Host rules to pin VMs; disabling DRS per VM also disables its participation in
evacuation.

## Other settings
- **Scalable shares** (7.0+): resource pool shares scale with the number of VMs in the
  pool, fixing the classic "high-share pool with many VMs gets less per VM" problem.
- **Predictive DRS** with Aria Operations: moves VMs ahead of forecast peaks.
- **CPU over-commitment / memory metric for load balancing**: additional options to cap
  overcommit per host (advanced).

## Reading the cluster
- Cluster → Monitor → vSphere DRS → VM DRS Score histogram: many VMs below 80% means
  contention; look at CPU ready and memory ballooning, not just host utilisation.
- Recommendations tab (Manual/Partial): each shows reason and expected benefit.
- Faults tab: why a move could not happen (rules, incompatible hosts, network missing).

## Verify
Most VMs in the 80-100% score bucket; vMotion count per day is stable and explainable;
a host entering maintenance mode evacuates without manual intervention.
