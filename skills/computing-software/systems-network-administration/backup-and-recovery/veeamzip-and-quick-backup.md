---
id: computing-software.systems-network-administration.backup-and-recovery.veeamzip-and-quick-backup
name: veeamzip-and-quick-backup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeamzip, quick-backup, ad-hoc-backup, pre-change-backup]
level: practitioner
status: docs-checked
description: "Take ad-hoc Veeam backups: VeeamZIP for a standalone full backup file without a job, and Quick Backup for an on-demand incremental restore point in an existing job chain."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/veeamzip.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/quick_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VeeamZIP and Quick Backup

## VeeamZIP
Quickly back up one or several VMs without configuring or scheduling a backup job.
- A VeeamZIP job always produces a full backup file (VBK) that acts as an independent restore point.
- Destination: a backup repository, a local folder on the backup server, or a network share. A Veeam Cloud Connect repository cannot be a target, and an object storage repository cannot be a target for Cloud Director VeeamZIP jobs.
- Veeam does not enforce backup repository throttling rules during VeeamZIP jobs.
- Minimal settings: destination, compression level, and optionally encryption and application-aware processing.
- Files appear in the Home view under Backups > Disk (Exported). Progress and results are in the History view.
- Restore: right-click the backup in the Home view and choose a restore option, or double-click the backup file on the machine where Veeam Backup & Replication is installed.

## Quick Backup
An on-demand incremental backup that adds a restore point for VMs already in a backup job, without configuring a new job or changing the existing one.
- Works for incremental chains and for reverse incremental chains (deprecated).
- Only for VMs that have been successfully backed up at least once and have a full restore point; otherwise it cannot run.
- It triggers an existing backup job that processes the VM; if none exists, the quick backup is terminated.
- For several VMs in different jobs, a set of jobs is triggered and each stores its restore point in the right chain. If a VM is in several jobs, the job that made its most recent restore point is started.
- If a quick backup overlaps the scheduled job, the job waits for the quick backup to finish.
- Not possible for VMware Cloud Director VMs processed by Cloud Director jobs; if a regular job processes the VM, start it from the Computer view.
- Retention for quick backups has its own article (Retention Policy for Quick Backups), not read here.

## Choosing
Need a standalone full file with no job: VeeamZIP. Need a fresh incremental restore point inside an existing job chain: Quick Backup.

## Checked
2026-11-07. Read in full: Veeam Help Center "VeeamZIP" (updated 2025-05-14) and "Quick Backup" (updated 2025-09-17), build 13.1.2.57. Both are short overview pages; the linked "Creating VeeamZIP Backups", "Managing and Restoring VeeamZIP Backups", "Performing Quick Backup" and "Retention Policy for Quick Backups" were not read. Removed because the pages do not state them: VeeamZIP "never expires" and "delete after N days", the menu paths for starting each, "disable guest quiescence", import on another Veeam server, "quick backups count against retention points", the hypervisor snapshot row (72 hours), the monitoring/retention and immutable-repository gotchas and the invented Verify step.
Method: documentation only; no commands were run.
