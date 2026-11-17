---
id: computing-software.systems-network-administration.windows-server.smb-authentication-hardening-2025
name: smb-authentication-hardening-2025
category: computing-software
field: systems-network-administration
product: windows-server
tags: [file-server, smb-authentication-rate-limiter, smb-signing, restrict-ntlm, smb-security]
level: advanced
status: docs-checked
description: "Use Server 2025 and Windows 11 24H2 SMB hardening: authentication rate limiter, NTLM blocking on the SMB client, signing by default and alternative ports."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security-hardening.md
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/configure-smb-authentication-rate-limiter.md
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-ntlm-blocking.md
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-ports.md
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/manage-smb-dialects.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMB authentication hardening (Server 2025)

## Authentication rate limiter
The SMB server inserts a delay (default **2000 ms**) after each failed NTLM or PKU2U authentication, which slows
brute-force guessing against SMB. Enabled by default in Windows Server 2025 and Windows 11 24H2.
```powershell
Get-SmbServerConfiguration | Format-List InvalidAuthenticationDelayTimeInMs
Set-SmbServerConfiguration -InvalidAuthenticationDelayTimeInMs 2000
```
The value must be a multiple of 100 in the range 0-10000 and can only be set with PowerShell (the on/off switch is also available in Group Policy). Keep it on; it does not affect Kerberos.

## Block NTLM on the SMB client
Stop clients from ever sending NTLM to a remote SMB server (pass-the-hash and relay mitigation):
```powershell
Set-SmbClientConfiguration -BlockNTLM $true
```
Exceptions for servers that only do NTLM go in the Group Policy setting `Block NTLM Server Exception List` (IP addresses, NetBIOS names or FQDNs); there is no PowerShell parameter for it, only the `BlockNTLMServerExceptionList` registry value under `HKLM:\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation`.
Per mapping: `New-SmbMapping -RemotePath \\fs01\share -BlockNTLM $true` or `net use \\server\share /BLOCKNTLM`. GPO: Computer Configuration > Administrative Templates > Network > Lanman Workstation. Available from Windows Server 2025 and Windows 11 24H2.
Accessing shares by IP address uses NTLM, so with BlockNTLM those fail; use names that Kerberos can resolve to an SPN.

## Signing required by default
Windows Server 2025 and Windows 11 24H2 require SMB signing for all outbound and inbound connections by default (previously only SYSVOL and NETLOGON). Old NAS devices that cannot sign
break: check `Get-SmbConnection | Select ServerName,Signed` and fix the device rather than turning signing off.

## Dialect control
```powershell
Set-SmbServerConfiguration -Smb2DialectMin SMB300
Set-SmbClientConfiguration -Smb2DialectMin SMB311
```
Accepted values include None, SMB202, SMB210, SMB300, SMB302 and SMB311; dialect min/max control is available from Windows Server 2025 and Windows 11 24H2.

## Alternative ports
Clients can map shares on alternative TCP, QUIC or RDMA ports (`New-SmbMapping ... -TcpPort <port>` or `net use \\fs01\share /TCPPORT:<port>`; also `-QuicPort` and `-RdmaPort`), useful behind restrictive firewalls; the server needs a matching listener (`New-SmbServerAlternativePort`, `Get-SmbServerAlternativePort`).

## Verify
- [ ] `InvalidAuthenticationDelayTimeInMs` shows the intended delay; NTLM SMB attempts from clients blocked;
  signing required and all connections Signed = True.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- Rate limiter: default 2000 ms, multiple of 100, range 0-10000, PowerShell-only delay setting, does not affect Kerberos, enabled by default in 2025 (configure-smb-authentication-rate-limiter and smb-security-hardening pages). Removed the `EnableAuthRateLimiter` property, which is not in the Set-SmbServerConfiguration reference.
- Block NTLM: `Set-SmbClientConfiguration -BlockNTLM`, `New-SmbMapping -BlockNTLM`, `net use /BLOCKNTLM`, Lanman Workstation GPO path. Wrong claim fixed: the exception list has no PowerShell parameter (Group Policy or registry value only).
- Signing required by default on 2025/24H2; Smb2DialectMin values; alternative ports with `-TcpPort`, `-QuicPort`, `-RdmaPort`, `/TCPPORT`, and `New-SmbServerAlternativePort` (smb-ports page).

Method: documentation only; no commands were run.
