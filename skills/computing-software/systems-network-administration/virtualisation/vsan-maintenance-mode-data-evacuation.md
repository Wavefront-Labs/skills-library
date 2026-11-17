---
id: computing-software.systems-network-administration.virtualisation.vsan-maintenance-mode-data-evacuation
name: vsan-maintenance-mode-data-evacuation
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan, vsan-maintenance-mode, ensure-accessibility, full-data-migration, no-data-migration, data-migration-pre-check, host-decommission, vmware, vsphere]
level: practitioner
status: draft
description: "Put vSAN hosts into maintenance with the right evacuation mode (ensure accessibility, full data migration, no data migration), run the pre-check, and decommission safely."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSAN maintenance mode and data evacuation

**Goal:** take a vSAN host down for patching, repair or removal without making any object
inaccessible.

## Modes
| Mode | What moves | Use for |
|---|---|---|
| Ensure accessibility (default) | Only components that would leave an object inaccessible | Short maintenance (patch, reboot) |
| Full data migration | Every component on the host | Removing the host, long hardware work, or clusters with no spare FTT |
| No data migration | Nothing | Whole-cluster shutdown, or when objects are FTT=0 by design and you accept the risk |
With "ensure accessibility", FTT=1 objects run with **zero redundancy** while the host is
down; a second failure in that window means data unavailability.

## Procedure
1. Check health is green and resync is idle.
2. Run **Data Migration Pre-check** (host → vSAN → Data Migration Pre-check) for the
   chosen mode: it reports objects that would become inaccessible or non-compliant and
   whether capacity suffices.
3. Enter maintenance (DRS migrates VMs; vSAN moves data). PowerCLI:
   `Set-VMHost -VMHost <h> -State Maintenance -VsanDataMigrationMode EnsureAccessibility`
4. Do the work; exit maintenance; wait for resync to finish **before** the next host.
5. For long outages (beyond 60 minutes), components start rebuilding elsewhere when the
   repair delay expires; that is expected and needs capacity.

## Decommissioning
Full data migration, then remove disk groups (OSA) or storage pool devices (ESA) with
"Full data migration", move the host out of the cluster, remove from vCenter. Never just
power off and remove: you leave absent components that will rebuild under pressure.

## Whole-cluster shutdown
vSAN 7U3+/8 has a **Shutdown Cluster** wizard (Cluster → right-click → vSAN → Shutdown
cluster) which handles vCenter running on the cluster; use it instead of the old manual
sequence.

## Verify
After each host returns: Skyline Health green, resync summary 0 bytes, objects Healthy,
then move to the next host.
