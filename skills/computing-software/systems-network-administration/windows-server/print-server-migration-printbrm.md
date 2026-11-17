---
id: computing-software.systems-network-administration.windows-server.print-server-migration-printbrm
name: print-server-migration-printbrm
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, workload-migration, server-migration, printbrm, print-server, print-migration, printer-drivers, print-queues]
level: practitioner
status: draft
description: "Migrate print servers with PrintBrm: back up queues, drivers and ports, restore to a new server, x64 driver issues, GPO-deployed printer updates and cutover."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate print servers with PrintBrm

## Back up the source
```
%windir%\System32\spool\tools\PrintBrm.exe -b -s \\OLDPRINT -f '<vol>:\print\oldprint.printerExport'
```
Captures queues, shares, ports, drivers, print processors, forms and security. Print
Management console > Migrate Printers wizard does the same.

## Restore on the new server
```
Install-WindowsFeature Print-Services -IncludeManagementTools
%windir%\System32\spool\tools\PrintBrm.exe -r -s \\NEWPRINT -f '<vol>:\print\oldprint.printerExport' -o force
```
- `-o force` overwrites existing objects; `-p all` publishes printers in AD (`-p keep`).
- Review the log in Event Viewer: `Microsoft-Windows-PrintBRM/Admin`.

## Driver problems
- 32-bit-only or Type 3 drivers from old servers: install current Type 4 or vendor
  universal drivers on the new server and switch queues (`Set-Printer -DriverName`).
- Package-aware drivers matter for Point and Print restrictions on clients (Windows
  requires admin for non-package drivers since the PrintNightmare fixes).
- Remove unused drivers before export to shrink the package.

## Cutover options
1. **Keep the name**: DNS CNAME/alias of the old name to the new server
   (`DisableStrictNameChecking` and `OptionalNames` registry, SPNs), or rename the new
   server after decommissioning the old one.
2. **New name**: update GPO-deployed printers and scripts (Group Policy Preferences
   printer items: replace action, item-level targeting) and remove old connections.

## Verify
- [ ] `Get-Printer -ComputerName NEWPRINT | Measure` equals source count; test print from
  a standard-user client on each driver model.
