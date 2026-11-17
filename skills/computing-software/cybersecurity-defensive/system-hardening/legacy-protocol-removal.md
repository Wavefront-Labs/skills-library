---
id: computing-software.cybersecurity-defensive.system-hardening.legacy-protocol-removal
name: legacy-protocol-removal
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [legacy-protocol-removal, telnet, ftp, smbv1, tls-1-0-disable, ntlmv1, snmpv1, attack-surface-reduction]
level: practitioner
status: docs-checked
description: "Find and retire legacy insecure protocols (Telnet, FTP, SMBv1, TLS 1.0/1.1, NTLMv1, SNMPv1/2c, LM, rsh) with discovery, dependency mapping, staged removal and verification."
sources: ["https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3", "https://datatracker.ietf.org/doc/html/rfc8996", "https://www.cisecurity.org/controls/cis-controls-list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legacy protocol removal

Old protocols send credentials in clear text or use broken cryptography, and they linger because some device
or application still needs them. Removal is a discovery and dependency project more than a configuration one.

## Targets and replacements
| Legacy | Problem | Replacement |
|---|---|---|
| Telnet, rlogin/rsh/rexec | Cleartext credentials | SSH |
| FTP, TFTP (for data) | Cleartext | SFTP, FTPS, HTTPS |
| SMBv1 | Legacy protocol, superseded by SMBv2/3 | SMBv2/3 with signing |
| TLS 1.0/1.1 | Deprecated by RFC 8996 | TLS 1.2/1.3 |
| NTLMv1, LM hashes | Crackable | NTLMv2 then Kerberos |
| SNMPv1/v2c | Cleartext community strings | SNMPv3 authPriv |
| LDAP simple bind without TLS | Cleartext | LDAPS / StartTLS, signing and channel binding |
| HTTP for admin interfaces | Cleartext | HTTPS |
| POP3/IMAP/SMTP auth without TLS | Cleartext | TLS-only ports, modern auth |
| WPA/WEP, WPA2-TKIP | Broken | WPA2-AES / WPA3 |

## Process
1. **Discover use**: network flow data and IDS logs, scanner
   service detection, Windows auditing (SMB1 access auditing `Set-SmbServerConfiguration
   -AuditSmb1Access $true` then event 3000 in Microsoft-Windows-SMBServer/Audit; NTLM auditing policies),
   TLS version logging on load balancers.
2. **Map dependencies**: who/what is still using it (old printers, scanners, NAS, OT devices, legacy apps).
3. **Plan per dependency**: upgrade firmware, replace device, isolate on a segment with a protocol-converting
   gateway, or accept risk with an expiry.
4. **Disable in rings**: server side first in audit/warn modes where available; then deny.
   - SMBv1: `Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol`.
   - NTLMv1: "Network security: LAN Manager authentication level" = Send NTLMv2 response only. Refuse LM &
     NTLM.
   - Telnet/FTP servers: remove packages and close ports.
5. **Prevent return**: baselines and scanners flag the protocol; firewall rules block legacy ports between zones.

## Gotchas
- Multifunction printers scanning to SMB shares are the classic SMBv1 and NTLMv1 holdouts.
- Disabling TLS 1.0 on a server can break old monitoring agents and Java 7 clients; inventory first.
- OT environments may not be able to change; isolate instead.

## Verify
Network monitoring shows zero Telnet/FTP/SMBv1/TLS 1.0 sessions over an agreed period; scanners report no services
offering legacy protocols; exceptions list is empty or dated.

## Checked
2026-10-28. Confirmed against official pages: SMB1 audit with Set-SmbServerConfiguration -AuditSmb1Access and event ID 3000, disabling SMB1Protocol (Microsoft Learn SMB guide); TLS 1.0/1.1 deprecated (RFC 8996); LAN Manager authentication level setting name.
Removed or rewritten: WannaCry/NotPetya and signing statements, SSLv3 attribution to RFC 8996, Zeek log and nmap specifics, the 30-day figure and the blocked CISA source.
Method: documentation only; no commands were run.
