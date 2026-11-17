---
id: computing-software.systems-network-administration.dns-dhcp.windows-dhcp-server-migration
name: windows-dhcp-server-migration
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, windows-dhcp, dhcp-server-migration, export-dhcpserver, authorization]
level: practitioner
status: draft
description: "Migrate Windows DHCP to a new server: export/import, authorisation in AD, failover re-creation, relay (helper) updates and cutover/rollback steps."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/import-dhcpserver
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DHCP server migration

## Plan
- Inventory: scopes, server/scope options, policies, classes, reservations, filters, DNS update
  settings and credential, failover relationships, audit log settings.
- List all relays (`ip helper-address`) pointing at the old server.

## Steps
1. Install the role on the new server and authorise it:
```powershell
Install-WindowsFeature DHCP -IncludeManagementTools
Add-DhcpServerInDC -DnsName dhcp-new.corp.example.com -IPAddress 10.0.0.68
```
2. Remove failover on the old server (exports do not carry relationships):
   `Remove-DhcpServerv4Failover -ComputerName dhcp-old -Name dhcp-old-dhcp2`.
3. Export with leases and import:
```powershell
Export-DhcpServer -ComputerName dhcp-old -File \\share\dhcp.xml -Leases -Force
Get-Service DHCPServer -ComputerName dhcp-old | Stop-Service   # Stop-Service itself has no -ComputerName parameter
Import-DhcpServer -ComputerName dhcp-new -File \\share\dhcp.xml -BackupPath <BACKUP_DIR> -Leases
```
Export again right before cutover if the old server kept running, to get current leases.
4. Re-apply server-level items: DNS credential (`Set-DhcpServerDnsCredential`), filters, audit path.
5. Update relays to the new IP (or give the new server the old IP), recreate failover with the partner.
6. Unauthorise and disable the old server: `Remove-DhcpServerInDC -DnsName dhcp-old.corp.example.com`.

## Rollback
Keep the old server's service stopped (not removed) for a few days; restart it and revert relays if needed.

## Verify
- [ ] Clients renew against the new server (lease table shows renewals), `Get-DhcpServerInDC` lists only intended servers, and failover state is Normal.
