---
id: computing-software.systems-network-administration.dns-dhcp.windows-dhcp-export-import-and-reservations
name: windows-dhcp-export-import-and-reservations
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, windows-dhcp, dhcp-export-import, reservations, dhcpserver-powershell]
level: practitioner
status: docs-checked
description: "Export and import Windows DHCP scopes, leases and reservations with PowerShell, and bulk-create reservations from CSV."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/export-dhcpserver
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/import-dhcpserver
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4reservation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export/import and reservations

## Export/import whole server or scopes
```powershell
Export-DhcpServer -ComputerName dhcp1 -File <EXPORT_DIR>\dhcp1.xml -Leases -Force
Export-DhcpServer -ComputerName dhcp1 -File <EXPORT_DIR>\scopes.xml -ScopeId <SCOPE_ID> -Leases
Import-DhcpServer -ComputerName dhcp2 -File <EXPORT_DIR>\dhcp1.xml -BackupPath <BACKUP_DIR> -Leases -ScopeOverwrite
```
- With neither `-ScopeId` nor `-Prefix`, the export holds the whole server configuration, all v4 and v6 scopes, plus lease data if `-Leases` is given. With `-ScopeId` or `-Prefix`, only those scopes or prefixes and all server-level settings are exported.
- `-BackupPath` is mandatory on import: the DHCP database is backed up there before any change.
- If an imported scope already exists on the target and `-ScopeOverwrite` is absent, a warning is shown and the import moves on to the next scope. With `-ScopeOverwrite` the target scope is overwritten.
- `-Leases` on import also imports the lease data in the file. Check that server-level settings you rely on arrived (bindings, DNS credentials) rather than assuming they did.

## Reservations from CSV
```powershell
# reservations.csv columns: ScopeId,IPAddress,ClientId,Name,Description
Import-Csv .\reservations.csv | ForEach-Object {
  Add-DhcpServerv4Reservation -ComputerName dhcp1 -ScopeId $_.ScopeId -IPAddress $_.IPAddress `
    -ClientId $_.ClientId -Name $_.Name -Description $_.Description
}
```
- `Add-DhcpServerv4Reservation` reserves the IPv4 address in the scope for the client ID; the address is then leased only to that client.
- For Windows clients the MAC address is used as the client ID. The Learn examples write it as dash-separated hex, for example `F0-DE-F1-7A-00-5E`.
- `-Name` is the client host name or a label for the reservation; `-Description` is free text.
- `-Type` accepts DHCP, BootP or Both (default Both).

## Verify
- [ ] Reservation counts match between source and target, and a test client receives its reserved address.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the Export-DhcpServer, Import-DhcpServer and Add-DhcpServerv4Reservation Learn pages. Removed as not stated by them: the list of what the XML contains beyond scopes and leases, Get-DhcpServerv4Reservation CSV export, lease-to-reservation pipeline, and failover replication behaviour.
