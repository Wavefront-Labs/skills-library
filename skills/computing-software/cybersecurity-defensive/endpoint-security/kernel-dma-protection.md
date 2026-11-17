---
id: computing-software.cybersecurity-defensive.endpoint-security.kernel-dma-protection
name: kernel-dma-protection
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [kernel-dma-protection, dma-attacks, thunderbolt, iommu, vt-d, pre-boot-dma, disk-encryption]
level: advanced
status: docs-checked
description: "Defend against DMA attacks: verify Kernel DMA Protection (IOMMU), firmware Thunderbolt security, BitLocker PIN needs, Linux IOMMU settings and policy for external PCIe ports."
sources: ["https://learn.microsoft.com/en-us/windows/security/hardware-security/kernel-dma-protection-for-thunderbolt", "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/countermeasures", "https://thunderspy.io/", "https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel DMA protection

DMA-capable ports (Thunderbolt/USB4, PCIe, ExpressCard, FireWire) let a malicious device read and write
memory directly - extracting BitLocker keys or injecting code on locked machines (PCILeech, Thunderspy).

## Windows Kernel DMA Protection
- Uses the IOMMU (Intel VT-d / AMD-Vi) to block DMA from external devices until a user signs in and only for drivers that support DMA remapping.
- Check the Kernel DMA Protection state in System Information (`msinfo32`) as described on the Microsoft page.
- Requires firmware support (see the Microsoft page); cannot be turned on later by software if firmware lacks it - enable the IOMMU (VT-d) in UEFI.
- Policy: `DmaGuard/DeviceEnumerationPolicy` (values are on the DmaGuard Policy CSP page): external devices whose drivers do not support DMA remapping are never enumerated.

## BitLocker interplay
Microsoft guidance: on devices **with** Kernel DMA Protection, TPM-only is acceptable for typical threat
models; on devices **without** it, use TPM+PIN or disable Thunderbolt/1394 DMA via policy
("Disable new DMA devices when this computer is locked") for higher-risk users.

## Firmware
- Thunderbolt security levels vary by controller generation; check the vendor's firmware documentation.
- Disable unused ports (ExpressCard, FireWire) in UEFI, password-protect UEFI setup.

## Linux
IOMMU behaviour is set with kernel parameters such as `intel_iommu` (see the kernel parameters reference); Thunderbolt authorisation tooling and sysfs checks are distro-specific and not covered here.

## Checked
2026-10-28. Confirmed in the Kernel DMA Protection, DmaGuard Policy CSP and BitLocker countermeasures pages: IOMMU based blocking, `DmaGuard/DeviceEnumerationPolicy` exists and only applies when Kernel DMA Protection is enabled, guidance to relax BitLocker DMA countermeasures where it is present, `intel_iommu` kernel parameter. Removed: the policy value, the msinfo32 label, Thunderbolt level names, the Linux `boltctl` and sysfs check, and the Windows 10 1803 date.
Method: documentation only; no commands were run.

## Verify
- [ ] Fleet inventory: Kernel DMA Protection On for all models; devices without it have TPM+PIN.
- [ ] UEFI settings baseline includes VT-d and setup password.
