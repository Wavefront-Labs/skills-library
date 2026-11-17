---
id: computing-software.it-support-helpdesk.desktop-support.printer-driver-install-and-point-and-print
name: printer-driver-install-and-point-and-print
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, printer, printing, point-and-print, printnightmare, printer-drivers, type-4-driver, universal-print-driver, pnputil, add-printer, print-management, comptia-a-plus, tcp-ip-printer-port, print-server]
level: practitioner
status: docs-checked
description: "Install printers for standard users after PrintNightmare: Point and Print restrictions, package-aware drivers, pnputil pre-staging, GPO or Intune deployment."
sources:
  - "https://support.microsoft.com/en-us/servicing/os/windows/2021/08/kb5005652-manage-new-point-and-print-default-driver-installation-behavior-cve-2021-34481"
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/pnputil-command-syntax"
  - "https://learn.microsoft.com/en-us/powershell/module/printmanagement/add-printer"
  - "https://learn.microsoft.com/en-us/powershell/module/printmanagement/add-printerdriver"
  - "https://learn.microsoft.com/en-us/powershell/module/printmanagement/add-printerport"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# printer-driver-install-and-point-and-print

Goal: users connect to shared printers without admin rights and without
reopening the PrintNightmare hole.

## The post-2021 rule
Since the updates described in KB5005652 (CVE-2021-34481), installing a
printer driver from a print server through Point and Print needs
**administrator** rights by default. `RestrictDriverInstallationToAdministrators`
set to 1, or not defined, enforces this and overrides the Point and Print
Restrictions Group Policy settings. The value lives under
`HKLM\Software\Policies\Microsoft\Windows NT\Printers\PointAndPrint`; the
policy is "Limits print driver installation to Administrators". Microsoft
states no combination of mitigations equals setting it to 1, so do not set
it to 0 fleet-wide. If it must be 0, treat it as a documented risk
exception. Instead:

## Option 1: pre-stage drivers (best)
Put the driver in the driver store before the user connects:
```cmd
pnputil /add-driver "<driver-folder>\*.inf" /subdirs /install
```
Then (as admin, or from a script running as SYSTEM):
```powershell
Add-PrinterDriver -Name "HP Universal Printing PCL 6"
Add-Printer -ConnectionName "\\print01\Finance-MFP"   # per-user connection
```
Deploy the pnputil step through your software distribution tool. Driver
names must match exactly between client and server.

## Option 2: Package Point and Print, approved servers
Group Policy: Computer Configuration, Administrative Templates, Printers,
**Package Point and Print - Approved servers** restricts clients to Point and
Print connections to the listed servers that use **package-aware** drivers.
The separate **Point and Print Restrictions** policy applies to printers using
a non-package-aware driver on the server. If drivers will not install even
with admin rights, check whether "Only use Package Point and Print" is set.

## Option 3: direct IP printers
```powershell
Add-PrinterPort -Name "IP_10.1.2.50" -PrinterHostAddress 10.1.2.50
Add-Printer -Name "Reception" -DriverName "<driver name>" -PortName "IP_10.1.2.50"
```
Run as admin or SYSTEM. No print server dependency, harder to change
centrally.

## Deploying to users
For cloud printing see the `universal-print-cloud-printing` skill.

## Verify
The driver appears in `Get-PrinterDriver`, a standard user connects to the
share with the policy set as designed, and a test page with the needed
features (duplex, tray) prints.


## Checked

Date 2026-10-27. Documentation release: Microsoft Support KB5005652 page, pnputil command syntax and PrintManagement cmdlet pages as published October 2026. Confirmed: default behaviour and registry value and path of RestrictDriverInstallationToAdministrators, the two Group Policy settings and what each covers, no equivalent mitigation, pnputil /add-driver with /subdirs and /install (Windows 10 1607+), Add-PrinterDriver, Add-Printer -ConnectionName, Add-PrinterPort -PrinterHostAddress. Removed: the 'Do you trust this printer' prompt text, GPP printer deployment, PCL/PostScript, 32-bit driver and type-4 finishing claims that no fetched page covers.

Method: documentation only; no commands were run.
