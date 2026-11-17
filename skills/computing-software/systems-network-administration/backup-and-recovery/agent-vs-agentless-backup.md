---
id: computing-software.systems-network-administration.backup-and-recovery.agent-vs-agentless-backup
name: agent-vs-agentless-backup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [agentless-backup, agent-based-backup, image-level-backup, guest-processing, application-aware]
level: practitioner
status: docs-checked
description: "Choose agentless or agent-assisted VM backup per workload, using Veeam guest processing and Azure Backup consistency levels as worked examples."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/guest_processing.html
  - https://learn.microsoft.com/en-us/azure/backup/backup-azure-vms-introduction
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Agent vs agentless backup

**Goal:** protect each workload with the least operational overhead that still meets its RPO, RTO and consistency needs.

## What the vendor docs show
**Azure Backup (VMs)**
- The backup policy offers either an agent-based application-consistent or file-consistent backup, or an agentless crash-consistent backup. Crash-consistent needs no agent in the VM.
- For application or file-system consistent backups a backup extension must be on the VM: VMSnapshot on Windows, VMSnapshotLinux on Linux, installed at the first backup if the VM is running.
- Running Windows VMs: Azure Backup coordinates with VSS for an app-consistent snapshot; if it cannot, it falls back to a file-consistent snapshot.
- Linux VMs: file-consistent by default. For app-consistent snapshots you write your own pre and post scripts (the Linux pre-script and post-script framework); if they succeed the point is marked application-consistent, but you remain responsible for the consistency. Azure Backup uses `fsfreeze` on Linux.

**Veeam Backup & Replication (guest processing)**
- Guest processing options let the product talk to the guest OS to create transactionally consistent backups and to catalog guest files and folders.
- Application-aware processing options include transaction log backup for SQL Server, Oracle and PostgreSQL, log truncation after a successful run, pre-freeze and post-thaw scripts for applications without VSS support, and guest file exclusions.
- Limits: SQL databases on a remote UNC path are backed up crash-consistent; the `master` database is excluded; SQL log backup needs the Full or Bulk-logged recovery model (Simple is not processed); Oracle log backup needs ARCHIVELOG on; transaction log backups cannot be copied to capacity tier.

## Decision rules
- Match the consistency level to the workload: crash-consistent is acceptable where the application recovers cleanly; databases need application-aware processing or log backups.
- If one product backs up database logs and another truncates them, they will conflict; designate one owner (check each product's documentation).
- Physical servers, and machines where hypervisor or cloud snapshot integration is not available, need an agent in the OS (check the product's agent documentation).

## Verify
Each workload class has a documented method with RPO and RTO achieved in restore tests.

## Checked

2026-11-09. Confirmed against the Veeam Guest Processing page (options and limitations listed) and the Azure Backup "overview of VM backup" page (agentless crash-consistent vs agent-based consistency, extensions, VSS, Linux scripts and fsfreeze). Partial read of the Azure page (snapshot sections). Removed: the comparison table (CBT/RCT efficiency, snapshot stun, performance impact), SQL log backup interval and Oracle RMAN advice, NAS and large file server advice, claim that agentless backup injects a temporary guest component, and the physical-server and laptop rules as stated (no cited page covers them).

Method: documentation only; no commands were run.
