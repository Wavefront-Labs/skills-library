---
id: computing-software.systems-network-administration.virtualisation.aria-operations-dashboards-and-capacity
name: aria-operations-dashboards-and-capacity
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [aria-operations, vrops, capacity-planning, vmware, vsphere]
level: practitioner
status: draft
description: "Use Aria Operations (VCF Operations) for vSphere capacity, time remaining, reclamation, rightsizing and dashboards, with policy settings that change results."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/aria/aria-operations/8-18/vmware-aria-operations-configuration-guide-8-18.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aria Operations dashboards and capacity

**Goal:** know how long current capacity lasts, what to reclaim, and what is unhealthy, from one tool. (Product names: vRealize Operations, then Aria Operations, then VCF Operations.)

## Setup
1. Deploy the appliance (and remote collectors near large sites).
2. Data sources -> Integrations -> add a **vCenter** account with a read-only role plus *Performance* privileges.
3. Wait one collection cycle for inventory and about two weeks for usable capacity forecasts.

## Policies drive results
Configure -> Policies: the active policy sets
- **Capacity model**: *Demand* (actual use) or *Allocation* (configured vCPU/RAM with overcommit ratios). Allocation suits contracts and VDI; demand suits efficiency.
- **Buffers**: HA buffer and headroom percentages reduce reported capacity.
- **Reclaim thresholds**: what counts as idle (for example CPU under 100 MHz for 95% of the time) and how long powered-off VMs and snapshots must exist.

## Key screens
- **Capacity**: time remaining per cluster and datacenter, the constraining resource (often memory or storage).
- **Reclaim**: idle VMs, powered-off VMs, old snapshots, orphaned disks with GB/cost recoverable.
- **Rightsize**: oversized and undersized VMs with recommended vCPU/RAM.
- **What-if**: add workloads or hosts and see impact.
- **Dashboards**: build custom ones from widgets (top-N CPU ready, datastore latency heatmaps) and share them per team.

## Alerts
Symptoms combine into alerts with recommendations; tune noise by disabling unwanted alert definitions in the policy, not by ignoring them.

## Gotchas
- Forecasts after a large migration are wrong until history catches up; exclude the period.
- Orphaned disk reports can include disks used by replicas or other vCenters; verify before deleting.

## Verify
The cluster time-remaining figure matches a manual check of usable capacity minus HA reserve and current demand trend.
