---
id: computing-software.systems-network-administration.windows-server.lsa-protection-and-ntlm-restriction
name: lsa-protection-and-ntlm-restriction
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, os-hardening, windows-server-hardening, lsa-protection, runasppl, ntlm-restriction, ntlm-auditing, lsass, protected-process-light]
level: advanced
status: docs-checked
description: "Enable LSA protection (RunAsPPL) on servers with audit of incompatible plug-ins, and audit then restrict NTLM with the Network security NTLM policies."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/configuring-additional-lsa-protection
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-ntlm-authentication-in-this-domain
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LSA protection (RunAsPPL) and NTLM restrictions

## LSA protection
Added protection for the LSA prevents nonprotected processes from reading its memory and injecting code.

1. Audit plug-in compatibility first:
```powershell
$ifeo = 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\LSASS.exe'
New-Item $ifeo -Force | Out-Null
New-ItemProperty $ifeo -Name AuditLevel -Value 8 -PropertyType DWord -Force
```
Look for events 3065 and 3066 in Event Viewer (the page gives the log location); they identify plug-ins that would fail to load.
2. Enable:
```powershell
New-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name RunAsPPL -Value 1 -PropertyType DWord -Force
# a value of 1 configures the feature with a UEFI variable; see the page for other values
```
3. Reboot.

## NTLM restrictions
The policy **Network security: Restrict NTLM: NTLM authentication in this domain** has its own reference page (see sources).
Audit NTLM use before restricting it.

## Verify
- [ ] After the reboot, `RunAsPPL` is set and LSASS runs as a protected process.
- [ ] NTLM usage was audited before any restriction was enforced.

## Checked

2026-10-28. Confirmed against: Configuring additional LSA protection page (RunAsPPL under the Lsa key, UEFI variable option, AuditLevel 8 under Image File Execution Options LSASS.exe, events 3065 and 3066). Removed (not confirmable from the cited pages): Protected Process Light wording, RunAsPPL value 2, GPO path, event 12 text, NTLM policy table and event IDs 8001-8004, LAN Manager level advice, 30-day review period.

Method: documentation only; no commands were run.
