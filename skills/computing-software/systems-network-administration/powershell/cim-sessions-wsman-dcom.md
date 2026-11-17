---
id: computing-software.systems-network-administration.powershell.cim-sessions-wsman-dcom
name: cim-sessions-wsman-dcom
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, cim, cimcmdlets, new-cimsession, new-cimsessionoption, wsman, dcom, remote-management, cimsession]
level: practitioner
status: docs-checked
description: "Create CIM sessions over WSMan or DCOM with New-CimSession and New-CimSessionOption: credentials, ports, HTTPS options, DCOM packet settings, WMI firewall and UAC."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/new-cimsession
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/new-cimsessionoption
  - https://learn.microsoft.com/en-us/windows/win32/wmisdk/connecting-to-wmi-remotely-starting-with-vista
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CIM sessions over WSMan and DCOM

A CIM session is a client-side object representing a connection to a local or remote computer. It holds connection details such as ComputerName and the protocol, and any CIM cmdlet can use it. Both cmdlets are Windows-only.

## Create sessions
```powershell
New-CimSession                                              # local computer, DCOM
New-CimSession -ComputerName Server01                       # WSMan by default when ComputerName is given
New-CimSession -ComputerName Server01, Server02 -Name FileServers
Get-CimSession -Name File*
New-CimSession -ComputerName Server01 -Credential $cred -Authentication Negotiate
```
- Without `-ComputerName`, the session goes to the local computer and is a DCOM session.
- `-Name` is a friendly name for later lookup; it need not be unique.
- `-Credential` accepts a user name, `Domain\User`, a UPN or a PSCredential. With no credential, the current user is used.
- `-ComputerName` takes NetBIOS names, IP addresses or FQDNs. If the target is in a different domain than the user, use the FQDN.
- `-Authentication` values: Default, Digest, Negotiate, Basic, Kerberos, NtlmDomain, CredSsp. NtlmDomain cannot be used for the local computer. CredSSP is flagged as raising security risk, because credentials passed to a compromised remote computer can be used to control the network session.
- `-CertificateThumbprint` (separate parameter set) gives client-certificate authentication; per the page it maps only to local user accounts, not domain accounts.
- `-OperationTimeoutSec`: 0 (the default) means the server default. A value below the 3-minute robust-connection retry timeout makes network failures longer than that unrecoverable.
- By default the cmdlet contacts the remote WS-Management endpoint to check the port and the credentials. `-SkipTestConnection` skips that, for endpoints that cannot use WS-Identify or to save time.
- `-Port`: default ports are 5985 (HTTP) and 5986 (HTTPS). An alternate port needs a matching WinRM listener on the target and applies to every computer in that command, so avoid it unless needed.

## DCOM instead of WSMan
```powershell
$so = New-CimSessionOption -Protocol Dcom
New-CimSession -ComputerName Server01 -SessionOption $so
```
`-Protocol` accepts Dcom, Default or Wsman.

DCOM option parameters:
- `-Impersonation`: Default, None, Identify, Impersonate, Delegate. If omitted, New-CimSession uses Impersonate.
- `-PacketIntegrity` and `-PacketPrivacy`: DCOM CIM sessions have both set to true by default.

## WSMan option parameters
```powershell
$option = @{ ProxyAuthentication='Kerberos'; ProxyCredential=$cred; SkipCACheck=$true; SkipCNCheck=$true; UseSsl=$true }
New-CimSessionOption @option
```
- `-UseSsl` adds HTTPS protection; WSMan already encrypts all content over HTTP. If SSL is not available on the port, the command fails. The page recommends using it only when PacketPrivacy is not specified.
- `-SkipCACheck`, `-SkipCNCheck`, `-SkipRevocationCheck` relax HTTPS certificate validation. Use them only for trusted computers (isolated network, or listed as a WinRM trusted host).
- `-NoEncryption` turns data encryption off. Other options: `-Encoding` (Default, Utf8, Utf16), `-MaxEnvelopeSizeKB`, `-HttpPrefix` (default /wsman), `-ProxyType` (default InternetExplorer; None, WinHttp, Auto), `-Culture`, `-UICulture`.

## Prerequisites for remote WMI over DCOM (win32 page)
- Firewall: allow WMI on the target. Enable the group with `netsh advfirewall firewall set rule group="windows management instrumentation (wmi)" new enable=yes`. The page also gives separate rules for DCOM (TCP 135 via the rpcss service), the WMI service (winmgmt), the callback sink (unsecapp.exe) and outgoing winmgmt traffic.
- UAC access-token filtering can change which operations are allowed or what data comes back. When not connecting as the built-in Administrator, the effect differs between domain and workgroup. Connecting with a nondomain account in the target's local Administrators group requires granting that account remote DCOM access, activation and launch rights.
- CIMOM: only for connections between computers without a trust relationship, set the `AllowAnonymousCallback` DWORD (0 blocks, 1 allows anonymous callbacks) under `HKLM\SOFTWARE\Microsoft\WBEM\CIMOM`. Do not change it for same or trusted domains.

## Checked
Method: 2026-11-08 docs-only read of the New-CimSession and New-CimSessionOption reference pages (MicrosoftDocs/PowerShell-Docs markdown) and the win32 remote WMI page (MicrosoftDocs/win32 markdown). Rewritten to what they state; dropped unsupported claims (CDXML module list, dynamic RPC port range, Test-WSMan fallback, TrustedHosts, WMF requirement, error-message table, KB5004442 hardening). Unchanged: the WSMan default and DCOM example.
