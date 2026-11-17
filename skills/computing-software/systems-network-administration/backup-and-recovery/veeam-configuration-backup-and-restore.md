---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-configuration-backup-and-restore
name: veeam-configuration-backup-and-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam-configuration-backup, veeam, configuration-restore, bco, disaster-recovery, backup-server-recovery]
level: practitioner
status: docs-checked
description: "Protect the Veeam Backup & Replication server itself with configuration backups, not VM backup jobs: encryption with hardened repositories, and the Windows restore wizard steps."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/vbr_config.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/vbr_config_restore.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam configuration backup and restore

**Goal:** recover or move the backup server's configuration after a failure.

## What it is
Configuration backup exports data from the configuration database and saves it to a backup file in a backup repository. If the backup server fails, you can re-install it and restore the configuration from that file, or apply one server's configuration to another backup server. Veeam recommends regular configuration backups for every backup server in the infrastructure.

## Rules from the documentation
- Always use the configuration backup feature for the backup server itself. Do not back it up with backup or replication jobs: the VM freezes during snapshot creation and commit, which can disconnect it from the configuration database, remote agents or network storage such as iSCSI.
- If the infrastructure has a hardened repository, enable encryption for configuration backups; otherwise configuration backups cannot be performed.
- Cloud backup appliances (AWS, Azure, Google Cloud plug-ins) can also have their configurations backed up, which requires encryption enabled; use the respective product guides for those.

## Restore on a Windows-based backup server
Useful when the configuration database is corrupted, to deploy it on a new Microsoft SQL Server or PostgreSQL, to roll back to a point in time, or to restore into a new database on the same instance (for example for testing). You can restore on the same backup server or another one. Check prerequisites, then use the Configuration Restore wizard. Its steps: launch the wizard, select a restore mode, select a configuration backup, review its parameters, specify the password, specify the target database, specify restore options, review settings, check configuration, finalize, synchronize backups and tape libraries, and finish.

Related articles listed by Veeam, not read here: Creating Configuration Backups, Migrating to Another Windows-Based Backup Server, Migrating the Configuration Database to Another SQL Server or to PostgreSQL, Automating Configuration Database Restore, and Restoring on a Linux-Based Backup Server.

## Checked
2026-11-07. Read in full: Veeam Help Center "Managing Configuration Database" (updated 2026-03-25) and "Restoring Configuration Database on Windows-Based Backup Server" (updated 2025-11-09), build 13.1.2.57; both are short overview pages. Removed because the pages do not state them: the `.bco` file extension and contents list, menu path, daily schedule and 30-point retention advice, the off-site copy advice, the restore versus migrate mode descriptions, the claim that unencrypted backups omit credentials, the version and database-engine claims, the no-backup-available recovery path, the "old server must not return" step and the invented Verify step. Pages for creating configuration backups and the wizard step details were not read.
Method: documentation only; no commands were run.
