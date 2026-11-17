---
id: computing-software.systems-network-administration.virtualisation.storage-drs-datastore-clusters
name: storage-drs-datastore-clusters
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [storage-drs, datastore-cluster, sdrs, storage-io-control, sioc, vmdk-affinity, datastore-maintenance-mode, vsphere-storage, vmware, vsphere]
level: practitioner
status: draft
description: "Set up datastore clusters and Storage DRS: space and I/O thresholds, automation level, VMDK affinity rules, datastore maintenance mode, and when SDRS fights the array."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management-8-0/creating-a-datastore-cluster.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Storage DRS and datastore clusters

**Goal:** balance space (and optionally latency) across a group of datastores
automatically, and empty a datastore for maintenance with one click.

## Build the cluster
- Group datastores of the same type and performance tier (do not mix VMFS and NFS or
  fast and slow arrays). All hosts in the compute cluster should see every member.
- **Automation:** Manual (recommendations only) to start, Fully Automated once trusted.
- **Space threshold:** default 80% utilised; the minimum difference (5%) stops churn.
- **I/O metric / latency threshold** (default 15 ms): enable only if the array does not
  do its own tiering/caching. With auto-tiering or dedupe arrays, I/O balancing moves
  VMs based on symptoms the array already handles and wastes Storage vMotions.

## Rules
- **Intra-VM affinity (keep VMDKs together)** is the default; turn it off for large VMs
  so disks can be placed separately.
- **VMDK anti-affinity** spreads a VM's disks; **VM anti-affinity** keeps two VMs on
  different datastores (e.g. both domain controllers).

## Datastore maintenance mode
Right-click member → Maintenance Mode: SDRS evacuates VMs and templates (templates and
ISOs need to be handled manually in older versions). Use before decommissioning a LUN or
array firmware work. The datastore must be in the datastore cluster.

## Gotchas
- Storage vMotion costs I/O and can expand thin disks during migration on some arrays;
  dedupe arrays may lose dedupe ratio when SDRS moves data.
- Replicated datastores (SRM/array replication): moving a VM to a datastore in a
  different replication group breaks protection; use SDRS with array consistency
  groups or keep automation manual.
- Backup products tracking VMs by datastore path need CBT reset after moves (most handle it).

## Verify
Datastore cluster summary shows utilisation spread within the minimum difference;
SDRS recommendations history shows few, sensible moves; maintenance mode empties a test
datastore.
