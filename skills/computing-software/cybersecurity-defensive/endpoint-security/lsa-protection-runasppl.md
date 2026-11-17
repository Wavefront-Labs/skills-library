---
id: computing-software.cybersecurity-defensive.endpoint-security.lsa-protection-runasppl
name: lsa-protection-runasppl
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [windows-security-features, lsa-protection, runasppl, lsass-protection, credential-theft, audit-mode, event-3065, event-3066]
level: practitioner
status: docs-checked
description: "Enable LSA protection (RunAsPPL) to block credential dumping from LSASS: audit mode for incompatible plugins, Intune/GPO settings, UEFI lock, verification and known bypass limits."
sources: ["https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/configuring-additional-lsa-protection", "https://www.microsoft.com/en-us/security/blog/2022/10/05/detecting-and-preventing-lsass-credential-dumping-attacks/", "https://attack.mitre.org/techniques/T1003/001/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LSA protection (RunAsPPL)

Runs LSASS as a Protected Process Light: non-protected processes, even with admin/SeDebugPrivilege,
cannot open it to read memory or inject code. Stops most Mimikatz-style dumping. Complements
Credential Guard (which isolates secrets in VBS).

## Audit first
Third-party LSA plugins (smart card, password filters, some SSO/AV DLLs) must be signed appropriately
or they fail to load.
- Audit mode: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\LSASS.exe`
  value `AuditLevel` (DWORD) = 8, as documented by Microsoft.
- Review CodeIntegrity Operational events 3065 (unsigned/insufficiently signed DLL would be blocked) and
  3066 (plugin does not meet Microsoft signing level) for weeks; contact vendors for signed versions.

## Enable
- Registry: `HKLM\SYSTEM\CurrentControlSet\Control\Lsa` `RunAsPPL` DWORD:
  `1` = enabled with UEFI variable lock (cannot be disabled by registry alone on UEFI/Secure Boot devices),
  a second value enables it without the UEFI lock; see the Microsoft page for the exact data.
- Intune: Settings catalog > Local Security Authority > "Configure LSASS to run as a protected process"
  (Enabled with UEFI lock / without).
- GPO: System > Local Security Authority > Configure LSASS to run as a protected process (Win11 22H2 ADMX).
- Audit mode for LSA protection is enabled by default on Windows 11 22H2 and later.
Reboot required.

## Verify it is on
- Event 12 in System log from Wininit: "LSASS.exe was started as a protected process with level: 4".

## Limits
- Attackers with kernel access (vulnerable signed drivers, BYOVD) can remove PPL; pair with the
  vulnerable driver blocklist and HVCI.
- Does not protect credentials already copied elsewhere (SAM, NTDS, cached creds) or tokens.
- Removing UEFI-locked RunAsPPL needs the Microsoft opt-out tool and physical presence.

## Gotchas
- Old smart card middleware and password filter DLLs are the usual breakers; audit catches them.
- Some EDRs rely on their own protected access; check vendor compatibility (most are fine).

## Checked
2026-10-28. Confirmed in Configuring additional LSA protection: `AuditLevel` = 8 under Image File Execution Options for LSASS.exe, events 3065 and 3066, WinInit event 12 with protection level 4, audit mode default on Windows 11 22H2+. Removed: the Process Explorer protection string, the Mimikatz lab check and the 22H2 gate on the non-locked RunAsPPL value.
Method: documentation only; no commands were run.

## Verify
Fleet compliance report (Intune or hunting query for Wininit event 12) shows protection level 4 on
target devices, with zero 3065/3066 blocks for business plugins.
