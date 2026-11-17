---
id: computing-software.systems-network-administration.dns-dhcp.windows-dhcp-database-backup-and-restore
name: windows-dhcp-database-backup-and-restore
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, windows-dhcp, dhcp-database-backup, backup-dhcpserver, disaster-recovery]
level: practitioner
status: docs-checked
description: "Back up and restore the Windows DHCP database with Backup-DhcpServer and Restore-DhcpServer, and keep a portable Export-DhcpServer XML copy as well."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/backup-dhcpserver
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/restore-dhcpserver
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/export-dhcpserver
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/import-dhcpserver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database backup and restore

Two kinds of copy exist; keep both and store them off the DHCP server.

## Database backup
```powershell
Backup-DhcpServer -ComputerName dhcp1 -Path <BACKUP_DIR>
Restore-DhcpServer -ComputerName dhcp1 -Path <BACKUP_DIR>
```
- `Backup-DhcpServer` backs up the DHCP database of the DHCP server service to the directory in `-Path` (mandatory).
- `Restore-DhcpServer` restores the database from the specified location.
- Both accept `-ComputerName`, `-CimSession`, `-AsJob` and `-WhatIf`.
- Schedule the backup (for example with Task Scheduler) and write to a path on another machine, so a lost server does not take its backups with it.

## Portable export
```powershell
Export-DhcpServer -ComputerName dhcp1 -File <EXPORT_FILE>.xml -Leases -Force
```
Export-DhcpServer writes configuration (all scopes, v4 and v6) and, with `-Leases`, lease data to an XML file. `Import-DhcpServer` loads it on another server; its mandatory `-BackupPath` backs up the target's database before any change is made. Use the export when moving to a different server; use the database backup to restore the same server.

## After restoring on a different server
Check what the restore did not carry over: authorisation in AD, DNS update credentials and failover relationships are separate settings, so review each rather than assuming they came across.

## Verify
- [ ] A test restore to a lab server loads all scopes and reservations, and backups exist off-server with recent timestamps.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the Backup-DhcpServer, Restore-DhcpServer, Export-DhcpServer and Import-DhcpServer Learn pages. Removed as not stated by them: file locations, the automatic 60-minute backup, Set-DhcpServerDatabase, event IDs, esentutl repair, Add-DhcpServerInDC, failover replication and reconcile cmdlets.
