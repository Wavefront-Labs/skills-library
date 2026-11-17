---
id: computing-software.systems-network-administration.patch-management.windows-installed-software-inventory-from-registry
name: windows-installed-software-inventory-from-registry
category: computing-software
field: systems-network-administration
product: patch-management
tags: [uninstall-registry-keys, win32-product, software-inventory, installed-software-query, powershell, windows]
level: practitioner
status: docs-checked
description: "Inventory installed Windows software from the Uninstall registry keys (64-bit and 32-bit views, per-user caveat), why Win32_Product is harmful, and name normalising."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/admin-development/windows-installer-reconfigured-all-applications
  - https://learn.microsoft.com/en-us/windows/win32/msi/configuring-add-remove-programs-with-windows-installer
  - https://learn.microsoft.com/en-us/windows/win32/winprog64/shared-registry-keys
  - https://learn.microsoft.com/en-us/powershell/module/appx/get-appxpackage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows installed software inventory

## Never use Win32_Product
`Get-WmiObject Win32_Product` / `Get-CimInstance Win32_Product` is not query optimised: WMI uses the MSI provider
to enumerate every installed product, and this also starts a consistency check of the installed packages, verifying
and repairing the install. Symptoms are slow startup or logon and one MsiInstaller event 1035 ("Windows Installer
reconfigured the product") per installed application. The fix Microsoft documents is to stop querying the class (for a
group policy WMI filter, use `Win32reg_AddRemovePrograms`, which needs the ConfigMgr client, or the `StdRegProv` class
if ConfigMgr is not installed).

## Read the Uninstall keys
Windows Installer writes DisplayName, DisplayVersion, Publisher, InstallDate and other values under
`HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Uninstall`, in a subkey identified by the product code
GUID. A 32-bit process on 64-bit Windows has `HKLM\SOFTWARE` redirected to `Wow6432Node`, so query both views:
```powershell
$paths = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
         'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*'
Get-ItemProperty $paths -ErrorAction SilentlyContinue |
  Where-Object { $_.DisplayName } |
  Select-Object DisplayName, DisplayVersion, Publisher, InstallDate, PSChildName |
  Sort-Object DisplayName
```
- `InstallDate` is the last time the product received service: it is replaced each time a patch is applied or
  removed, or the product is repaired, so it is not a pure install date.
- An installer can set `ARPSYSTEMCOMPONENT` to keep an application out of the Programs list, so a list built from
  Programs and Features can differ from the registry list.
- Per-user installs show only in the Add/Remove Programs of that user, and per-machine installs show for all users.
  The HKLM query therefore misses applications installed only in another user's context.
- Store and MSIX apps are separate: `Get-AppxPackage -AllUsers` lists app packages (.msix or .appx) for every user
  account and needs administrator permissions.

## At scale
Run the same query remotely (for example with `Invoke-Command`) and export to CSV, or use your endpoint
management tool's own software inventory.

## Normalise for patch matching
DisplayName strings vary between vendors and versions; map each to a canonical product name and compare
`DisplayVersion` with a version-aware comparison (a `[version]` cast fails on non-numeric parts, so strip suffixes
first).

## Verify
Compare the count per machine with Programs and Features, and confirm the inventory run produces no burst of
MsiInstaller event 1035.

## Checked
Date: 2026-11-07. Read in full: Uninstall Registry Key properties page (DisplayName, DisplayVersion, Publisher,
InstallDate definition, product code GUID subkey), the Win32_Product KB (event 1035, 7035/7036, consistency check,
`Win32reg_AddRemovePrograms` needing ConfigMgr, `StdRegProv`), Configuring Add/Remove Programs (per-user versus
per-machine visibility, ARPSYSTEMCOMPONENT), Registry Keys Affected by WOW (Wow6432Node redirection of
HKLM\SOFTWARE), Get-AppxPackage (`-AllUsers`, administrator, .msix/.appx). Removed as unconfirmed: "misses non-MSI
installers", "can reset app configuration", the `SystemComponent` and `ParentKeyName` value filters, the per-user
HKU hive script, ConfigMgr SMS_InstalledSoftware, Intune Discovered apps, Defender for Endpoint and osquery
inventory references.
Method: documentation only; no commands were run.
