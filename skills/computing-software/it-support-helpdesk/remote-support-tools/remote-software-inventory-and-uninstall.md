---
id: computing-software.it-support-helpdesk.remote-support-tools.remote-software-inventory-and-uninstall
name: remote-software-inventory-and-uninstall
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, remote-software-inventory, uninstall, msiexec, registry-uninstall-keys, winget, appx]
level: practitioner
status: draft
description: "Inventory installed software on remote Windows PCs from the uninstall registry keys (not Win32_Product) and remove MSI, EXE and Appx packages silently with logging."
sources:
  - "https://learn.microsoft.com/en-us/windows/win32/msi/uninstall-registry-key"
  - "https://learn.microsoft.com/en-us/windows/win32/msi/command-line-options"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/admin-development/windows-installer-reconfigured-all-applications"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# remote-software-inventory-and-uninstall

## Inventory
```powershell
$paths = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
         'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*'
Invoke-Command -ComputerName PC01 -ScriptBlock {
  Get-ItemProperty $using:paths | Where-Object DisplayName |
    Select-Object DisplayName, DisplayVersion, Publisher, PSChildName, QuietUninstallString, UninstallString
} | Sort-Object DisplayName
```
- Per-user installs (Teams classic, Zoom, Chrome user installs) live under each user's
  `HKCU\...\Uninstall`; load their hive or run in user context.
- Do **not** use `Win32_Product` / `Get-WmiObject Win32_Product`: enumerating it triggers a
  consistency check that can repair or reconfigure every MSI on the box, and it is slow.
- Alternatives: `winget list` (user context), Intune Discovered apps, RMM inventory.

## Uninstall
| Type | Command |
|---|---|
| MSI | `msiexec /x {PRODUCT-GUID} /qn /norestart /l*v "%TEMP%\uninst.log"` |
| EXE | Use `QuietUninstallString` if present; otherwise vendor silent switch (`/S`, `/silent`, `/uninstall /quiet`) checked in vendor docs |
| Appx | `Get-AppxPackage -AllUsers *name* \| Remove-AppxPackage -AllUsers`; also `Remove-AppxProvisionedPackage -Online` to stop it returning for new users |
| winget | `winget uninstall --id <Id> --silent` |

## Exit codes
0 success; 3010 success, reboot required; 1641 reboot started; 1605 product not installed
(already gone); 1618 another install in progress, retry later.

## Gotchas
- The `PSChildName` of an MSI entry is the product code; EXE entries have arbitrary keys.
- Uninstalling security or management agents usually needs a tamper/uninstall token.
- Check for a running process first; some uninstallers wait forever for a closed app.

## Verify
The entry is gone from both uninstall keys, files/services removed, and the inventory
source (RMM/Intune) shows it absent after the next scan.
