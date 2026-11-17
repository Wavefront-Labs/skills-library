---
id: computing-software.cybersecurity-defensive.system-hardening.windows-optional-features
name: windows-optional-features
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [windows-optional-features, windows-features, powershell-v2-removal, attack-surface-reduction, windows-hardening, dism]
level: practitioner
status: docs-checked
description: "Remove unneeded Windows optional features, server roles and capabilities: PowerShell 2.0, SMB1, IIS, Telnet, TFTP, WSL and others, using PowerShell, DISM and baselines."
sources: ["https://learn.microsoft.com/en-us/powershell/module/dism/disable-windowsoptionalfeature", "https://learn.microsoft.com/en-us/powershell/module/servermanager/uninstall-windowsfeature"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows optional features and roles removal

## Discover what is installed
```powershell
# client and server: optional features
Get-WindowsOptionalFeature -Online | Where-Object State -eq Enabled | Select-Object FeatureName
# server roles and features
Get-WindowsFeature | Where-Object Installed
```

## Common removals
| Feature | Why | Command |
|---|---|---|
| SMB 1.0/CIFS (`SMB1Protocol`) | Legacy protocol | `Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol` |
| Telnet and TFTP clients | Cleartext tools | `Disable-WindowsOptionalFeature -Online -FeatureName <name from Get-WindowsOptionalFeature>` |
| Internet Information Services on non-web hosts | Unneeded service | `Uninstall-WindowsFeature -Name Web-Server` (server) |
| Other legacy or unused components | Unused attack surface | per role; find the exact name with `Get-WindowsOptionalFeature` |

Server: `Uninstall-WindowsFeature -Name <feature> -Remove` also deletes the payload from the component store
(features on demand), preventing easy reinstall (but requires a source to reinstall later).

## At scale
- Use your configuration-management tooling to enforce the same removals.
- Build removal into the golden image so new machines start clean.
- Report via inventory so drift is visible.

## Gotchas
- Some removals need a reboot.
- Legacy apps may depend on a removed component; enable only where documented.
- Re-run compliance checks after upgrades.

## Verify
`Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol` shows Disabled; a baseline scan reports the feature rules as passing.

## Checked
2026-10-28. Confirmed against official pages: Disable-WindowsOptionalFeature use with names from Get-WindowsOptionalFeature, SMB1Protocol, Uninstall-WindowsFeature with Web-Server and -Remove (Microsoft Learn cmdlet pages).
Removed or rewritten: PowerShell 2.0, SimpleTCP, WSL, IE11, Work Folders and NetFx3 feature names, Get-WindowsCapability, STIG/CIS rule claims, DSC/PowerSTIG/Intune/Defender mentions, the RestartNeeded property and the blocked STIG source.
Method: documentation only; no commands were run.
