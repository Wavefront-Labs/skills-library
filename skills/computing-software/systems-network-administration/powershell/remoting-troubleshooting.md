---
id: computing-software.systems-network-administration.powershell.remoting-troubleshooting
name: remoting-troubleshooting
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-remoting, remoting-troubleshooting, winrm, kerberos]
level: practitioner
status: docs-checked
description: "Fix PowerShell remoting errors per about_Remote_Troubleshooting: access denied, refused connections, IP and workgroup NTLM rules, TrustedHosts, firewall, quotas, timeouts."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_remote_troubleshooting
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# PowerShell remoting troubleshooting

Settings under the `WSMan:` drive (session configuration, trusted hosts, ports, listeners) need administrative rights and an elevated session ("Run as administrator").

## Error to fix (per the about page)
| Error | What the page says |
|---|---|
| Access is denied / refused connection | Remoting must be enabled: on by default on Windows Server 2012 and later; run `Enable-PSRemoting` to re-enable. Client Windows has the WinRM service disabled by default; on servers it is Automatic. |
| Access is denied (credentials) | Default endpoints require Administrators membership; use `-Credential` with `New-PSSession`, `Enter-PSSession` or `Invoke-Command`. |
| Access is denied (non-admins) | Grant Execute on the session configuration: `Set-PSSessionConfiguration Microsoft.PowerShell -ShowSecurityDescriptorUI`. |
| Access is denied (admin from another domain) | Remote connections from other domains run with standard-user tokens. `LocalAccountTokenFilterPolicy=1` (DWord under HKLM Policies\System) changes this, but disables UAC remote restrictions for all users of affected computers. |
| Default session configurations deleted | `Unregister-PSSessionConfiguration` the changed one, then `Enable-PSRemoting` recreates defaults (it does not alter existing ones). Restored ones inherit RootSDDL (`Get-Item WSMan:\localhost\Service\RootSDDL`). |
| "WinRM client cannot process the request" (IP or workgroup) | Kerberos does not support IP addresses, so NTLM is used. Requires HTTPS transport or the target in TrustedHosts, and `-Credential` on every remote command, even as the current user. A workgroup client also needs a non-empty password on the workgroup machine. |
| `Enable-PSRemoting` "Unable to check the status of the firewall" | Network is Public and `-SkipNetworkProfileCheck` was not used. |
| ListeningOn empty / "cannot connect to destination" | Group policy misconfiguration; check `Get-WSManInstance winrm/config/listener -Enumerate`. |
| Unrecognised tool in remote session | A 32-bit configuration such as `Microsoft.PowerShell32` redirects System32 to SysWOW64; check `$Env:PROCESSOR_ARCHITECTURE` remotely. |
| Import-Module blocked by execution policy | `Import-PSSession` modules are unsigned scripts; use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`. |
| I/O operation aborted | WinRM stopped or restarted mid-operation; `Start-Service WinRM` and rerun. |

## Firewall on Public networks
On servers `Enable-PSRemoting` works on all profiles, with the Public rule limited to the local subnet. On client Windows it fails on Public networks unless `-SkipNetworkProfileCheck` is used (then also local subnet). To open it up: `Set-NetFirewallRule -Name "WINRM-HTTP-In-TCP-PUBLIC" -RemoteAddress Any` (rule names vary; check with `Get-NetFirewallRule` first).

## Enterprise enablement
Group policy **Allow automatic configuration of listeners** (Computer Configuration, Administrative Templates, Windows Components, Windows Remote Management, WinRM service) with IPv4/IPv6 filters; **Windows Firewall: Allow local port exceptions** (Domain Profile); WinRM service set to Automatic.

## TrustedHosts
In `WSMan:\localhost\Client\TrustedHosts`; comma-separated names, IPs, FQDNs, wildcards allowed; affects all users of the computer and only Administrators can change it.
```powershell
Get-Item WSMan:\localhost\Client\TrustedHosts
$cur = (Get-Item WSMan:\localhost\Client\TrustedHosts).Value
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "$cur, Server01.Domain01.Fabrikam.com"
```

## Ports, proxies, quotas, timeouts
- Alternate port: `Set-Item WSMan:\localhost\listener\listener*\port -Value 8080`. The about page says remoting uses port 80 by default (the WinRM security page elsewhere lists 5985/5986).
- Proxy: `New-PSSessionOption -ProxyAccessType IEConfig -ProxyAuthentication Negotiate -ProxyCredential <cred>`, pass as `-SessionOption` or set `$PSSessionOption`.
- Quota error "total data received ... exceeded allowed maximum": raise `MaximumReceivedObjectSizeMB` (default 10 MB) on the session configuration, for example with `Set-PSSessionConfiguration -Name Microsoft.PowerShell -MaximumReceivedObjectSizeMB 11 -Force`. Related WSMan settings: MaxEnvelopeSizeKB, MaxProviderRequests, MaxConcurrentOperations, MaxConcurrentOperationsPerUser, MaxConnections.
- Timeout error "cannot complete the operation within the time specified in OperationTimeout": the shortest of local and remote timeouts wins; for example `New-PSSessionOption -OperationTimeout 240000`. WSMan settings: MaxTimeoutMs, EnumerationTimeoutMs, MaxPacketRetrievalTimeSeconds.
- Unresponsive native program in a remote host (UI or prompting console apps): press Ctrl+C.
- Linux and macOS use remoting over SSH.

## Checked
Method: 2026-11-08 docs-only read of the about_Remote_Troubleshooting page (MicrosoftDocs/PowerShell-Docs markdown). Replaced unsupported triage commands, SPN/0x80090322 advice, Remote Management Users, MaxShellsPerUser and second-hop fixes with what the page states. Unchanged: TrustedHosts and -Credential requirement for IP connections.
