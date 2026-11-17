---
id: computing-software.systems-network-administration.windows-server.smb-over-quic
name: smb-over-quic
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, file-server, smb-shares, smb-over-quic, quic, udp-443, new-smbservercertificatemapping, client-access-control, tls-1-3, smb-vpn-replacement]
level: practitioner
status: docs-checked
description: "Offer file shares over the internet without VPN using SMB over QUIC: certificate mapping, UDP 443, client access control, and client/edition requirements."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-over-quic.md
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/configure-smb-over-quic-client-access-control.md
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/new-smbservercertificatemapping
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/grant-smbclientaccesstoserver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMB over QUIC

**What:** SMB 3.1.1 carried inside QUIC (TLS 1.3 over UDP 443) so remote clients reach file
shares like a web app, with SMB authentication (Kerberos via KDC proxy, or NTLM) inside the
encrypted tunnel. No VPN.

## Requirements
- Server: Windows Server 2025 (all editions) or 2022 Datacenter: Azure Edition.
- Clients: a Windows 11 device (the doc lists Windows 11 as the client requirement).
- Certificate on the server: Server Authentication EKU (1.3.6.1.5.5.7.3.1), subject/SAN = the external name
  clients use (`files.example.com`), ECDSA P-256 or greater or RSA of at least 2048 bits, SHA256RSA signature or greater, from a CA clients trust.

## Configure
```powershell
$cert = Get-ChildItem Cert:\LocalMachine\My | ? Subject -eq 'CN=files.example.com'
New-SmbServerCertificateMapping -Name files.example.com -Thumbprint $cert.Thumbprint -StoreName My
Get-SmbServerCertificateMapping
Set-SmbServerConfiguration -EnableSMBQUIC $true     # opt-in: SMB over QUIC is not on by default
```
(Windows Admin Center also has a guided SMB over QUIC configuration.)
Firewall/perimeter: allow **UDP 443** inbound to the server (TCP 445 stays blocked from the internet).
DNS: public `files.example.com` -> the server's public IP/NAT.

## Client access control
Restrict which client certificates/devices may connect (Windows Server 2025, or Windows Server 2022 Datacenter: Azure Edition with the March 2024 KB5035857 update and its feature preview enabled):
```powershell
Set-SmbServerCertificateMapping -RequireClientAuthentication $true
Grant-SmbClientAccessToServer -Name '<SERVER_HOSTNAME>' -IdentifierType ISSUER -Identifier '<CA_SUBJECT_DN>'
Grant-SmbClientAccessToServer -Name '<SERVER_HOSTNAME>' -IdentifierType SHA256 -Identifier '<CLIENT_CERT_SHA256>'
```
Allow entries use `Grant-`/`Revoke-SmbClientAccessToServer`; deny entries use `Block-`/`Unblock-SmbClientAccessToServer`, and any deny entry in a certificate chain wins over allow entries. Clients map their certificate with `New-SmbClientCertificateMapping -Namespace <server FQDN> -Thumbprint <SHA1 thumbprint> -StoreName My`.

## Client
```powershell
New-SmbMapping -LocalPath 'Z:' -RemotePath '\\files.example.com\Projects' -TransportType QUIC
net use Z: \\files.example.com\Projects /TRANSPORT:QUIC
```
Without a domain controller reachable from the client, authentication uses NTLMv2. For Kerberos from outside, use a **KDC proxy**: Windows Admin Center configures it automatically, or configure the KDCProxy service and the client GPO
`Specify KDC proxy servers for Kerberos clients` manually. Connecting by IP address always uses NTLM.

## Verify
- [ ] The mapping works with `New-SmbMapping -TransportType QUIC` (Windows clients try TCP first and use QUIC only if TCP fails or QUIC is requested explicitly).
- [ ] From the internet, only UDP 443 is reachable on the server.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23 (smb-over-quic page dated 2025-07-24).
- Not on by default: administrator must opt in; clients use TCP unless it fails or QUIC is requested with `NET USE /TRANSPORT:QUIC` or `New-SmbMapping -TransportType QUIC`. The earlier "default on in 2025" claim was wrong.
- Requirements: Windows Server 2025 (any edition) or 2022 Datacenter: Azure Edition; Windows 11 client; UDP 443 inbound and no TCP 445 inbound; certificate EKU, key and signature rules.
- Client access control: prerequisites, `Set-SmbServerCertificateMapping -RequireClientAuthentication`, `Grant-SmbClientAccessToServer -Name <server hostname> -IdentifierType ISSUER|SHA256`, deny precedence, `New-SmbClientCertificateMapping -Namespace`. The earlier use of the mapping name as -Name and the "2025+" gate were corrected.
- KDC proxy: automatic in Windows Admin Center, NTLMv2 otherwise, IP addresses force NTLM.

Method: documentation only; no commands were run.
