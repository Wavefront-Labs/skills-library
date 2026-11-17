---
id: computing-software.digital-privacy-hygiene.device-hardening.windows-memory-integrity-and-core-isolation
name: windows-memory-integrity-and-core-isolation
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, memory-integrity, hvci, core-isolation, windows, vulnerable-driver-blocklist, lsa-protection]
level: practitioner
status: docs-checked
description: "Turn on Memory integrity (HVCI) and Local Security Authority protection from Core isolation details, and know the driver compatibility and processor notes."
sources:
  - "https://support.microsoft.com/en-us/windows/core-isolation-e30ed737-17d8-42f3-a2a9-87521df09b78"
  - "https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity"
  - "https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/configuring-additional-lsa-protection"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows Memory integrity and Core isolation

**Goal:** make it hard for malicious programs to use low-level drivers to hijack the PC.

## Where
Windows Security > Device security > **Core isolation details**.
- **Memory integrity**, also known as Hypervisor-protected Code Integrity (HVCI): uses an isolated environment created with
  hardware virtualization.
- **Local Security Authority protection**: helps prevent theft of the credentials used to sign in, by stopping untrusted
  software running inside, or reading the memory of, the Local Security Authority.

## Compatibility
- All drivers on the system must be compatible with virtualization-based protection of code integrity, otherwise the
  system may fail. Microsoft recommends testing on a group of computers first.
- Memory integrity works better on Intel Kaby Lake and later (Mode-Based Execution Control) and AMD Zen 2 and later (Guest
  Mode Execute Trap). Older processors rely on emulation (Restricted User Mode), with a bigger performance impact.
- Update or remove software whose drivers block the feature before forcing it on.

## Scripted check
Registry: `HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity`, value `Enabled`
= 1 when memory integrity is enabled by policy or registry. Microsoft documents "Enabled with UEFI lock" as a separate
option; with the lock you need the UEFI BIOS menu to turn off Secure Boot to disable it.

## Verify
- [ ] Memory integrity and Local Security Authority protection show On in Core isolation details.

## Checked
2026-10-28. Confirmed on Microsoft Support (Device security in Windows Security) and Microsoft Learn (enable
virtualization-based protection of code integrity): names, definitions, driver compatibility warning, processor note,
registry value and UEFI lock. Removed (not on the fetched pages): the Vulnerable Driver Blocklist item, the pnputil driver
removal steps and oem23.inf example, msinfo32 checks, the VT-x and SVM requirement, the "roughly 2018" processor claim,
anti-cheat notes.
Method: documentation only; no commands were run.
