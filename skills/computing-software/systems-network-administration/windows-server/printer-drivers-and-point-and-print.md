---
id: computing-software.systems-network-administration.windows-server.printer-drivers-and-point-and-print
name: printer-drivers-and-point-and-print
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, print-server, print-services, point-and-print, printer-drivers, printnightmare, package-point-and-print, restrictdriverinstallationtoadministrators]
level: advanced
status: docs-checked
description: "Manage print server drivers and Point and Print after PrintNightmare: Type 3 vs Type 4 and package-aware drivers, RestrictDriverInstallationToAdministrators and approved servers."
sources:
  - https://support.microsoft.com/en-us/topic/kb5005652-manage-new-point-and-print-default-driver-installation-behavior-cve-2021-34481-873642bf-2634-49c5-a23b-6d8e9a302872
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/print/v4-printer-driver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Printer drivers and Point and Print restrictions

## The 2021 change
Per KB5005652, Windows updates released August 10, 2021 and later require administrative privilege to install drivers
by default (the `RestrictDriverInstallationToAdministrators` value under
`HKLM\Software\Policies\Microsoft\Windows NT\Printers\PointAndPrint`; read the KB for the exact default and its
interaction with the other Point and Print policies).

## Options (in order of preference)
1. **Package Point and Print - Approved servers**: the KB's policy that limits clients to Point and Print connections
   to the Package Point and Print servers you trust.
2. Pre-install drivers on clients with your deployment tool, so connecting only needs the queue.
3. Last resort: relax `RestrictDriverInstallationToAdministrators`; the KB lists this as reducing protection against
   CVE-2021-34481. Avoid.

GPO locations: Computer Configuration > Administrative Templates > Printers:
- Point and Print Restrictions.
- Package Point and Print - Approved servers.
- Only use Package Point and Print (the KB notes disabling it if drivers cannot install even with admin rights).

## Driver hygiene on the server
```powershell
Get-PrinterDriver -ComputerName PRINT01 | Format-List *
Get-Printer -ComputerName PRINT01 | Group DriverName | Select Count,Name
Remove-PrinterDriver -ComputerName PRINT01 -Name 'Old Driver'
```
- Prefer vendor universal drivers (few drivers for many models), x64 only.
- Driver isolation: see the printer-driver-isolation skill.
- Type 4 (v4) drivers: see Microsoft's v4 printer driver page before choosing.

## Verify
- [ ] Standard user connects to a queue on an approved server without an elevation prompt.
- [ ] The Point and Print policies match your design on every client and server.

## Checked
2026-10-28. Confirmed on KB5005652 and the v4 printer driver page: August 10, 2021 change requiring admin privilege by default,
the RestrictDriverInstallationToAdministrators registry value and path, Package Point and Print - Approved servers,
Only use Package Point and Print. Removed as unconfirmed: default value 1 phrasing, Type 3/4 package-aware
recommendations, pnputil/Add-PrinterDriver install path, IsPackageAware column, PrintNightmare naming, class-driver
description, driver isolation advice.
Method: documentation only; no commands were run.
