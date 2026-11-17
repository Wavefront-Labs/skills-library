---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-application-aware-processing
name: veeam-application-aware-processing
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-backup-job, application-aware-processing, log-truncation, vss, guest-processing, sql-server, guest-interaction-proxy, application-consistent]
level: practitioner
status: docs-checked
description: "Veeam application-aware processing: crash-consistent default, supported applications, VSS and Linux agent, log backup and truncation, requirements and limits."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/application_aware_processing.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/guest_processing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam application-aware processing

**Goal:** transactionally consistent backups and replicas of VMs running transaction-log applications.

## Behaviour
- By default Veeam does not process application logs and creates a **crash-consistent** backup of VMs with applications that use transaction logs.
- Enable application-aware processing in job settings for Microsoft Active Directory, SQL Server, SharePoint, Exchange, Oracle and PostgreSQL. Veeam prepares the application, then triggers the VM snapshot and copies data.
- Windows VMs: Microsoft VSS ensures no unfinished transactions or incomplete application files. Linux VMs: an agent connects to the guest OS and prepares databases and instances.
- Guest processing deploys non-persistent runtime components (run only during processing) or, if needed, persistent agent components in the guest.

## Job settings
- Transaction log backup: SQL Server Log Backup, Oracle Log Backup, PostgreSQL WAL Files Backup.
- Transaction log truncation on the guest after the VM is processed successfully.
- Pre-freeze and post-thaw scripts for applications that do not support VSS.
- VM guest OS file exclusion.

## Requirements and limits
- Supported for Linux VMs, Windows client from Vista and Windows Server from 2012 R2 SP1 (see the Workloads page for guest versions).
- VMware Tools and the latest updates must be installed in the guest.
- A group Managed Service Account (gMSA) cannot be used for VMs running SharePoint or PostgreSQL.
- Applications with no VSS writer (MySQL is the example given) cannot use VSS-based processing; use VMware Tools quiescence with pre-freeze and post-thaw scripts.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center pages "Application-Aware Processing" and "Guest Processing".
Removed (not on those pages): credential and `sysadmin` requirements, guest interaction proxy and VIX details, the three-option SQL log table and "one owner of the log chain" advice, freeze duration claim, the error/fix table (RPC, `vssadmin`, snapshot stun), Verify section.
Method: documentation only; no commands were run.
