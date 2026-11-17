---
id: computing-software.cybersecurity-defensive.system-hardening.winrm-hardening
name: winrm-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [winrm-hardening, powershell-remoting, winrm, https-listener, jea, windows-hardening]
level: practitioner
status: docs-checked
description: "Harden WinRM and PowerShell remoting: HTTPS listeners, no Basic auth or unencrypted traffic, firewall scoping, JEA endpoints, TrustedHosts hygiene and logging."
sources: ["https://learn.microsoft.com/en-us/windows/win32/winrm/installation-and-configuration-for-windows-remote-management", "https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/winrm-security", "https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WinRM hardening

WinRM (WS-Management, ports 5985 HTTP / 5986 HTTPS) underpins PowerShell remoting, Ansible for Windows and many
management tools.

## Transport and authentication
The default ports are 5985 (HTTP) and 5986 (HTTPS). Review Microsoft's WinRM security article for when message-level encryption over HTTP is sufficient and when HTTPS is needed.
```powershell
# service settings (also enforce via GPO: Windows Components > Windows Remote Management)
Set-Item WSMan:\localhost\Service\AllowUnencrypted $false
Set-Item WSMan:\localhost\Service\Auth\Basic $false
Set-Item WSMan:\localhost\Service\Auth\CredSSP $false
Set-Item WSMan:\localhost\Client\AllowUnencrypted $false
Set-Item WSMan:\localhost\Client\Auth\Basic $false
```
Disable CredSSP unless there is a documented need: it delegates the user's credentials from the client to the target server.

## Network scope
- Scope the Windows Firewall rule for inbound WinRM to management subnets, PAWs and jump hosts only, not "Any".
- Disable the WinRM service on clients that are not managed remotely.

## Least privilege: JEA
Just Enough Administration endpoints restrict what a remote session can run:
```powershell
New-PSRoleCapabilityFile -Path .\HelpDesk.psrc -VisibleCmdlets 'Restart-Service','Get-Service'
New-PSSessionConfigurationFile -Path .\HelpDesk.pssc -SessionType RestrictedRemoteServer -RunAsVirtualAccount -RoleDefinitions @{ 'CORP\HelpDesk' = @{ RoleCapabilities = 'HelpDesk' } } -TranscriptDirectory '<TRANSCRIPT_DIR>'
Register-PSSessionConfiguration -Name HelpDesk -Path .\HelpDesk.pssc
```
Restrict who can connect to the default PowerShell endpoint with the session configuration permissions.

## Client side
- Keep `TrustedHosts` as short as possible: it only suppresses the error for hosts that cannot be authenticated and is not a statement that the hosts are trustworthy.

## Logging
Collect the WinRM operational log, PowerShell script block and module logging, and JEA session transcripts. Alert on WinRM connections from non-admin sources.

## Verify
`Get-Item WSMan:\localhost\Service\AllowUnencrypted` and `...\Service\Auth\Basic` return False, and a connection attempt from a workstation subnet is blocked by the firewall.

## Checked

2026-10-28. Confirmed against: Microsoft Learn WinRM installation and configuration (ports 5985/5986, AllowUnencrypted, CredSSP, TrustedHosts); WinRM security (TrustedHosts meaning); JEA overview; New-PSSessionConfigurationFile, New-PSRoleCapabilityFile and Register-PSSessionConfiguration references (parameters used in the JEA example).

Removed as unconfirmed: HTTPS listener one-liner, STIG/CIS claims, firewall rule display name, default endpoint permission claim, event ids and wsmprovhost.exe, winrm get / Test-WSMan verify commands.

Method: documentation only; no commands were run.
