---
id: computing-software.cybersecurity-defensive.endpoint-security.credential-guard-deployment
name: credential-guard-deployment
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [windows-security-features, credential-guard, virtualization-based-security, vbs, lsaiso, ntlm-hashes, kerberos-tgt-protection, hvci]
level: advanced
status: docs-checked
description: "Enable Windows Credential Guard (and VBS/HVCI) to isolate NTLM hashes and Kerberos tickets from LSASS, with prerequisites, compatibility impacts and verification."
sources: ["https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/configure", "https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/how-it-works"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credential Guard

**Goal:** credential theft tools that read LSASS memory cannot obtain reusable NTLM hashes or
Kerberos TGTs from protected machines.

## What it does
Virtualization-based security (VBS) runs an isolated LSA (`LsaIso.exe`) in a separate virtual
trust level; LSASS holds only protected blobs. Protects NTLM hashes and Kerberos TGTs/keys
derived from passwords. Does not protect: credentials typed into a compromised session
(keyloggers), local accounts in the SAM, Kerberos service tickets in use, or a kernel already compromised before boot.

## Prerequisites
64-bit CPU with virtualisation extensions (VT-x/AMD-V) and SLAT, UEFI with Secure Boot, TPM
2.0 recommended. Windows Enterprise/Education (and Server 2016+).
**Enabled by default** on eligible Windows 11 22H2+ Enterprise/Education devices and on
Windows Server 2025 (domain-joined, non-DC), but verify rather than assume.

## Enable
Intune Settings catalog: Device Guard > Credential Guard "Enabled with UEFI lock" (lock
prevents remote disablement; removal then needs physical presence) or "Enabled without lock"
during pilot. GPO: Computer Configuration > Administrative Templates > System > Device Guard >
Turn On Virtualization Based Security. Also enable memory integrity (HVCI) where drivers allow.

## Verify on a device
```powershell
(Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard).SecurityServicesRunning
# 1 = Credential Guard running, 2 = HVCI running
```
or `msinfo32` > "Virtualization-based security Services Running".

## Compatibility
- Check the Credential Guard requirements and known-issues pages for unsupported authentication (for example NTLMv1 and MS-CHAPv2); plan EAP-TLS before enabling on laptops using PEAP.
- Not supported on domain controllers.
- Some third-party hypervisors and old drivers conflict with VBS/HVCI.

## Gotchas
- UEFI lock makes rollback painful; pilot without lock first.
- Credential Guard does not stop attackers using a logged-on session's access (token theft); it removes hash reuse.

## Checked
2026-10-28. Confirmed in the Credential Guard configure and how-it-works pages: Intune Settings catalog Device Guard > Credential Guard with UEFI lock or without lock, default enablement from Windows 11 22H2 and Windows Server 2025, the `Win32_DeviceGuard` `SecurityServicesRunning` check. Removed: the specific list of broken protocols.
Method: documentation only; no commands were run.

## Verify
- [ ] Fleet report (Defender/Intune) shows Credential Guard running on eligible devices.
- [ ] Purple-team test: LSASS dump on a protected machine yields no reusable NT hash for domain accounts.
