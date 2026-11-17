---
id: computing-software.systems-network-administration.windows-server.secured-core-server-and-secure-boot
name: secured-core-server-and-secure-boot
category: computing-software
field: systems-network-administration
product: windows-server
tags: [os-hardening, secured-core-server, secure-boot, tpm, dma-protection]
level: advanced
status: docs-checked
description: "Enable Secured-core server: UEFI Secure Boot, TPM 2.0, DRTM System Guard, VBS/HVCI and kernel DMA protection, and check each feature."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/secured-core-server
  - https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-secure-boot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secured-core server and Secure Boot

Secured-core combines hardware root of trust features so firmware and boot-time malware cannot hide below the OS.

## Components
| Feature | Requirement |
|---|---|
| UEFI Secure Boot | check with `Confirm-SecureBootUEFI` |
| TPM 2.0 | check with `Get-Tpm` |
| Boot DMA protection | IOMMU support on the device |
| System Guard Secure Launch | enabled in the OS, needs DRTM-compatible Intel and AMD hardware |
| VBS + HVCI | HVCI-compatible drivers plus VBS requirements |

## Enable
Use hardware that supports Secured-core server and follow the enablement steps on the Secured-core server page; firmware settings (Secure Boot, TPM, virtualization) must be turned on first.

## Gotchas
- HVCI requires compatible drivers; test before enforcing.
- Microsoft is updating the Secure Boot certificates originally issued in 2011; see the Secure Boot certificate page in the sources.

## Verify
- [ ] Secure Boot, TPM, VBS/HVCI and Secure Launch show as enabled.

## Checked
2026-10-28: Confirmed on Learn pages secured-core-server and oem-secure-boot: feature list, Boot DMA protection needs IOMMU, Secure Launch needs DRTM-compatible hardware, HVCI-compatible drivers, 2011 Secure Boot certificates being updated; Confirm-SecureBootUEFI and Get-Tpm reference pages exist. Removed: msinfo32 strings, Windows Admin Center and GPO steps, mbr2gpt conversion, Win32_DeviceGuard check, 2023 and 2026 certificate dates, UEFI lock recovery claim.
Method: documentation only; no commands were run.
