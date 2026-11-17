---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-replica-seeding-and-mapping
name: veeam-replica-seeding-and-mapping
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, replica-seeding, replica-mapping, replication, wan, initial-sync]
level: advanced
status: docs-checked
description: "Seed Veeam VM replicas from a backup at the DR site or map them to existing VMs so the first replication over the WAN sends only changes."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/replica_seeding.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Replica seeding and mapping

**Problem:** the first (initial) replication session would otherwise copy the whole VM over the WAN.

## Seeding
Use when a backup of the VMs you plan to replicate already sits in a backup repository at the DR site. During replication Veeam restores the VMs from those backups, synchronises them with the latest state of the source VMs and uses them as replicas.
- Create the seed backup first (see "Creating Replica Seeds" in the Veeam guide) and point the replication job at the DR-site repository.
- The restored VM is registered on the target host and its files go to the replica destination datastore you choose. Disk format is preserved (thin source disks are restored thin).

## Mapping
Use when the DR host already holds ready-to-use copies of the source VMs: restored VMs or replicas made by other replication jobs. Veeam synchronises them with the source and uses them as replicas. Mapping is also useful when you need to reconfigure or recreate replication jobs, for example to split one job into several.

## Combining
Seeding and mapping can be used in the same job (for example seed one VM and map another). If either is enabled, **every VM in the job must be covered**: a VM with neither a seed nor a mapping is skipped.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center page "Replica Seeding and Mapping" (read in part).
Removed (not on the page read): the UI checkbox names, "target VMs must be powered off", disk-layout and digest-reading remarks, CBT note, the Verify section.
Method: documentation only; no commands were run.
