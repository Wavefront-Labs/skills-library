---
id: computing-software.systems-network-administration.powershell.remove-windows-powershell-2-0
name: remove-windows-powershell-2-0
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell-v2-removal, powershell-security, windows-features, downgrade-attack, hardening]
level: practitioner
status: draft
description: "Find and remove the Windows PowerShell 2.0 optional feature on clients and servers, detect remaining v2 use first, and verify downgrade attacks are blocked."
sources: ["https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/starting-windows-powershell"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remove PowerShell 2.0

**Why:** v2 lacks AMSI, script block logging and constrained language enforcement, so launching `powershell -Version 2` sidesteps protections. Microsoft deprecated it and newer Windows releases no longer include it by default.

## Detect
```powershell
Get-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2Root, MicrosoftWindowsPowerShellV2
# Server:
Get-WindowsFeature PowerShell-V2
```
Find real users first: events in the **Windows PowerShell** log with EngineVersion 2.0 (event 400 shows `EngineVersion=2.0`), and audit command lines containing `-Version 2`. Legacy tools (old installers, scripts requiring v2) are the typical dependencies; fix or retire them.

## Remove
```powershell
Disable-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2Root -NoRestart
Disable-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2 -NoRestart
# Server:
Uninstall-WindowsFeature PowerShell-V2
```
Deploy with Intune/Configuration Manager/DSC at scale; a restart completes the change.

## .NET note
Starting v2 needs .NET Framework 3.5. Not enabling 3.5 is a second barrier, but the optional feature should still be removed.

## Verify
`powershell.exe -Version 2 -Command "$PSVersionTable"` fails with an error that the version is not installed; compliance scan or `Get-WindowsOptionalFeature` shows Disabled.
