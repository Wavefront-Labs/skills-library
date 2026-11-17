---
id: computing-software.systems-network-administration.windows-server.osconfig-security-baseline-2025
name: osconfig-security-baseline-2025
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, os-hardening, windows-server-hardening, osconfig, security-baseline, drift-control, windows-server-2025, microsoft-osconfig]
level: advanced
status: docs-checked
description: "Apply the Windows Server 2025 security baseline with OSConfig: install the module, apply member server or DC scenarios, check compliance and drift control."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/osconfig/osconfig-how-to-configure-security-baselines
  - https://learn.microsoft.com/en-us/windows-server/security/osconfig/osconfig-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSConfig security baseline (Windows Server 2025)

OSConfig is a PowerShell-driven configuration stack in Windows Server 2025 that applies
Microsoft's security baseline and corrects drift through a refresh task.

## Install
```powershell
Install-Module -Name Microsoft.OSConfig -Scope AllUsers -Force
Get-Module -ListAvailable Microsoft.OSConfig
```

## Apply a baseline scenario
Pick the scenario for the server's role:
```powershell
# Member server
Set-OSConfigDesiredConfiguration -Scenario SecurityBaseline/WindowsServer/2025/MemberServer -Default
# Workgroup server
Set-OSConfigDesiredConfiguration -Scenario SecurityBaseline/WindowsServer/2025/WorkgroupMember -Default
# Domain controller
Set-OSConfigDesiredConfiguration -Scenario SecurityBaseline/WindowsServer/2025/DomainController -Default
```
Restart the device after applying or removing a baseline. Secured-core and Defender
Antivirus scenarios also exist (`SecuredCore`, `Defender/Antivirus/WindowsServer/2025`).

## Check compliance
```powershell
Get-OSConfigDesiredConfiguration -Scenario SecurityBaseline/WindowsServer/2025/MemberServer |
  ft Name, @{ Name='Status'; Expression={$_.Compliance.Status} }, @{ Name='Reason'; Expression={$_.Compliance.Reason} } -AutoSize -Wrap
```

## Customise
Change a single setting value rather than turning off the baseline (the Learn example changes `AuditDetailedFileShare` from 2 to 3):
```powershell
Set-OSConfigDesiredConfiguration -Scenario SecurityBaseline/WindowsServer/2025/MemberServer -Setting AuditDetailedFileShare -Value 3
```
Remove the scenario (restart afterwards):
`Remove-OSConfigDesiredConfiguration -Scenario SecurityBaseline/WindowsServer/2025/MemberServer`.

## Drift control
When drift control is on, OSConfig corrects deviations through a refresh task; turning
it off disables the task. Several management tools can own the same settings, so
decide which tool owns each setting (OSConfig gives each authority a precedence order).

## Gotchas
- Baseline disables SMBv1, requires SMB 3.0 or higher and SMB signing, restricts
  authentication to NTLMv2 and disables file copy and paste in RDP sessions: test
  legacy clients, Linux SAMBA and management tools.
- Azure Arc-connected servers can also get it through Azure Policy machine configuration.

## Verify
- [ ] Compliance status Compliant for all items or documented exceptions.

## Checked
2026-10-28. Confirmed against the Learn pages "Configure security baselines with OSConfig" and "OSConfig overview": module install command, scenario names (`SecurityBaseline/WindowsServer/2025/{MemberServer,WorkgroupMember,DomainController}`, `SecuredCore`, `Defender/Antivirus/WindowsServer/2025`), `-Setting` customisation example, restart after apply/remove, SMBv1/SMB 3.0/signing/NTLMv2/RDP copy behaviour, drift control through a refresh task. Fixed: scenario path (`WS2025` was wrong), `-Name` to `-Setting`. Removed: 300+ settings, 4-hour interval, `-Repository`, GPO-override claim.
Method: documentation only; no commands were run.
