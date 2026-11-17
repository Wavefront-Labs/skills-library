---
id: computing-software.cybersecurity-defensive.system-hardening.smb-signing-and-smbv1-removal
name: smb-signing-and-smbv1-removal
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [windows-hardening, smb-signing, smbv1, ntlm-relay, group-policy, smb-encryption]
level: practitioner
status: docs-checked
description: "Require SMB signing on Windows clients and servers, remove SMBv1, audit legacy dependencies first and verify with PowerShell and network checks to stop NTLM relay."
sources: ["https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing", "https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3", "https://learn.microsoft.com/en-us/powershell/module/smbshare/set-smbshare"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMB signing and SMBv1 removal

**Goal:** SMB sessions are signed (relay-resistant) and SMBv1 is gone everywhere.

## SMBv1
1. Audit usage first: `Set-SmbServerConfiguration -AuditSmb1Access $true`, then check the `Microsoft-Windows-SMBServer\Audit` event log (event ID 3000) for clients still using SMBv1.
2. Remove: `Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol`, or disable the server component with `Set-SmbServerConfiguration -EnableSMB1Protocol $false`.
3. Check: `Get-SmbServerConfiguration | Select EnableSMB1Protocol`.
Old NAS, printers/scanners (scan-to-folder), and XP/2003 systems are typical blockers; upgrade firmware or isolate.

## SMB signing
GPO: Computer Configuration > Windows Settings > Security Settings > Local Policies > Security Options:
- Microsoft network server: Digitally sign communications (always) = Enabled
- Microsoft network client: Digitally sign communications (always) = Enabled
PowerShell: `Set-SmbServerConfiguration -RequireSecuritySignature $true`; `Set-SmbClientConfiguration -RequireSecuritySignature $true`.
Windows 11 24H2 Enterprise, Pro and Education require both outbound and inbound signing; Windows Server 2025 requires outbound signing only; Windows 11 24H2 Home requires neither. Requiring signing also disables guest access to shares, and third-party servers that cannot sign will fail to connect.

## Encryption
For sensitive shares use the `-EncryptData` parameter of `Set-SmbShare` (per share) or `Set-SmbServerConfiguration` (server-wide).

## Rollout
- Deploy to a pilot OU, monitor for third-party SMB devices that cannot sign (failed connections).

## Verify
- [ ] `Get-SmbClientConfiguration | FL RequireSecuritySignature` and `Get-SmbServerConfiguration | FL RequireSecuritySignature` return True.
- [ ] `Get-SmbServerConfiguration | Select EnableSMB1Protocol` returns False.
- [ ] No SMBv1 audit events for 30 days before final removal.

## Checked

2026-10-28. Confirmed against: Microsoft Learn 'Control SMB signing behavior' (defaults per OS, GPO path, PowerShell, verify commands); Microsoft Learn 'Detect, enable and disable SMBv1, SMBv2 and SMBv3' (audit, event 3000, EnableSMB1Protocol); Set-SmbShare and Set-SmbServerConfiguration reference (EncryptData).

Removed as unconfirmed: Uninstall-WindowsFeature FS-SMB1, AES-GMAC/CMAC and CPU-overhead sentences, Get-SmbConnection Signed check, nmap check, CIS benchmark source.

Method: documentation only; no commands were run.
