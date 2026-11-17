---
id: computing-software.systems-network-administration.windows-server.dhcp-backup-and-migration
name: dhcp-backup-and-migration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-dhcp-server, dhcpserver-module, export-dhcpserver, import-dhcpserver, dhcp-migration, backup-dhcpserver, dhcp-database, leases, server-replacement]
level: practitioner
status: docs-checked
description: "Back up and move a Windows DHCP server: Export-DhcpServer with leases, Import-DhcpServer on the new box, authorisation swap, relay updates, and restore from backup."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/migrate-dhcp-server
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-server-events
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/dynamic-update
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/export-dhcpserver
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/import-dhcpserver
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/backup-dhcpserver
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/restore-dhcpserver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCP backup and migration

## Backups
`Backup-DhcpServer` backs up the DHCP database to a path you give (the cmdlet documentation example uses the dhcp backup folder under the system directory). Use a DHCP-specific backup, not a Windows backup of the whole OS.
On demand / to another location:
```powershell
Backup-DhcpServer -ComputerName dhcp01 -Path '<BACKUP_DIR>\dhcp'
Restore-DhcpServer -ComputerName dhcp01 -Path '<BACKUP_DIR>\dhcp' -Force
```

## Migrate to a new server (preferred method)
1. Build the new server and install the role; do not authorise it yet.
2. Export from the old server, **including leases** so clients keep their addresses:
```powershell
Export-DhcpServer -ComputerName dhcp-old -File '<BACKUP_DIR>\dhcp-export.xml' -Leases -Force
```
3. Stop DHCP on the old server and remove its authorisation (`Remove-DhcpServerInDC`; the migration article uses `netsh dhcp delete server`).
4. Import on the new server:
```powershell
Import-DhcpServer -ComputerName dhcp-new -File '<BACKUP_DIR>\dhcp-export.xml' -BackupPath '<BACKUP_DIR>\dhcp-new-pre' -Leases -Force
Add-DhcpServerInDC -DnsName dhcp-new.ad.example.com
```
   `-ScopeId` imports selected scopes only (useful to split one server into two).
5. Point relay agents at the new server (or reuse the old IP address on the new server).
6. DNS update credentials (`Set-DhcpServerDnsCredential`) are not backed up; configure them again after a restore or import.

## Verify
- [ ] `Get-DhcpServerv4ScopeStatistics -ComputerName dhcp-new` shows in-use counts similar to the old server.
- [ ] A client on each relayed VLAN gets or renews a lease (`ipconfig /renew`) from the new server.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DhcpServer module) repositories, latest commit 2026-10-23. Confirmed: Export-DhcpServer `-File`, `-Leases`, `-Force`, `-ScopeId`; Import-DhcpServer `-File`, `-BackupPath`, `-Leases`, `-Force`, `-ScopeId`; Backup-/Restore-DhcpServer `-Path` (and `-Force` on restore); migration article uses a DHCP-specific backup and `netsh dhcp delete/add server` authorisation; Dynamic Update article states DNS credentials are not backed up. Removed the 60-minute automatic backup interval, the restart-after-restore step, the claim that failover relationships are not exported, the forward-compatibility statement and the audit event number, none of which the checked pages state.

Method: documentation only; no commands were run.
