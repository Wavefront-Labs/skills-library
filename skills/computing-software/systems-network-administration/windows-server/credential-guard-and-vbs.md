---
id: computing-software.systems-network-administration.windows-server.credential-guard-and-vbs
name: credential-guard-and-vbs
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, os-hardening, windows-server-hardening, credential-guard, virtualization-based-security, vbs, lsaiso, hvci, memory-integrity, device-guard, hypervisor-protected-code-integrity]
level: advanced
status: docs-checked
description: "Enable Credential Guard and VBS on Windows Server: hardware prerequisites, GPO or registry, UEFI lock, verification with msinfo32 and Win32_DeviceGuard, and app breakage."
sources:
  - https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/configure
  - https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Credential Guard and virtualization-based security

Credential Guard isolates NTLM hashes and Kerberos TGTs in LSAIso, a VBS-protected
process, defeating Mimikatz-style credential theft from LSASS.

## Prerequisites
- Check the hardware and firmware requirements on Microsoft's Credential Guard configure page (Secure Boot and
  virtualization support are the usual gates); on VMs confirm the hypervisor exposes them.
- Decide per server role (member servers, RDS hosts, jump servers) and check the page's domain-controller guidance.

## Enable
GPO: Computer Configuration > Administrative Templates > System > Device Guard >
**Turn On Virtualization Based Security**: Enabled, platform security level Secure Boot
(and DMA Protection if supported), Credential Guard Configuration **Enabled with UEFI
lock** (harder to turn off) or **Enabled without lock** (easier rollback).
Memory integrity (HVCI): "Virtualization Based Protection of Code Integrity" in the same
policy; test drivers first.

Registry equivalent:
```powershell
$dg='HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard'
Set-ItemProperty $dg EnableVirtualizationBasedSecurity 1 -Type DWord
Set-ItemProperty $dg RequirePlatformSecurityFeatures 1 -Type DWord   # 1 Secure Boot, 3 Secure Boot and DMA protection
Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' LsaCfgFlags 2 -Type DWord  # 1 with UEFI lock, 2 without
```
Reboot.

## Verify
```powershell
Get-CimInstance -Namespace root\Microsoft\Windows\DeviceGuard -ClassName Win32_DeviceGuard |
  Select VirtualizationBasedSecurityStatus,SecurityServicesRunning
```
`SecurityServicesRunning` reports which services run (Learn's table maps the values to Credential Guard and memory
integrity). Do not use the presence of `LsaIso.exe` in Task Manager to decide: Learn says that is not a recommended check.

## What breaks
- Apps that depend on credential types Credential Guard blocks lose single sign-on; test them on a pilot server (see the
  page's considerations section).
- Removing a UEFI lock is a documented multi-step procedure; read it before choosing the locked option.

## Checklist
- [ ] Win32_DeviceGuard shows Credential Guard running.
- [ ] The Credential Guard service shows as running in `SecurityServicesRunning` after reboot.

## Checked
2026-10-28. Confirmed on the Learn Credential Guard configure and memory-integrity pages: GPO/registry names
(EnableVirtualizationBasedSecurity, RequirePlatformSecurityFeatures 1/3, LsaCfgFlags 1 with lock / 2 without),
Win32_DeviceGuard SecurityServicesRunning and the warning against checking LsaIso.exe. Removed as unconfirmed: CPU/TPM
prerequisites, VM cmdlets, DC and Server 2025 default statements, VBS status value, msinfo32, the blocked-protocol
list, readiness-tool statement, Wininit event numbers.
Method: documentation only; no commands were run.
