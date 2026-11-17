---
id: computing-software.cybersecurity-defensive.endpoint-security.bitlocker-deployment
name: bitlocker-deployment
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [full-disk-encryption, bitlocker, tpm, xts-aes-256, pre-boot-authentication, intune-disk-encryption, bitlocker-recovery]
level: practitioner
status: docs-checked
description: "Deploy BitLocker across Windows fleets: TPM protectors, XTS-AES 256, silent enablement via Intune/GPO, recovery key escrow to Entra/AD, and reporting."
sources: ["https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/configure", "https://learn.microsoft.com/en-us/powershell/module/bitlocker/get-bitlockervolume", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/manage-bde-protectors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BitLocker deployment

**Goal:** every Windows laptop and desktop has its OS and data drives encrypted with recovery
keys escrowed, so a lost device is not a data breach.

## Policy (Intune Endpoint security > Disk encryption, or GPO)
- Encryption method: Microsoft recommends the XTS-AES algorithm for all drives; choose 128 or 256 bit by device performance.
- Require device encryption; allow **silent** enablement for standard users (Entra joined, TPM 2.0).
- Startup authentication: TPM-only is common; **TPM + PIN** for high-risk users or where DMA/cold-boot attacks are in scope (Microsoft guidance notes modern devices with Kernel DMA Protection reduce the need).
- Recovery: escrow to Entra ID (Intune) or AD DS **before** enabling ("Do not enable BitLocker until recovery information is stored").
- Used-space-only encryption for new devices (fast); full for reused devices.
- Fixed data drives: auto-unlock; removable: see device control (BitLocker To Go policies).

## Commands
```
manage-bde -status
manage-bde -protectors -get C:
Get-BitLockerVolume | Select MountPoint, VolumeStatus, EncryptionMethod, ProtectionStatus
Backup-BitLockerKeyProtector -MountPoint "C:" -KeyProtectorId <id>   # saves to AD DS
```

## Recovery
- Users retrieve keys via the self-service portal (Entra) after MFA, or helpdesk via Intune/AD with identity verification.
- Rotate the recovery password after use (using `manage-bde -protectors` add and delete, or your MDM's key rotation action).

## Reporting
Intune encryption report / Defender vulnerability management; alert on devices without
escrowed keys or with protection suspended.

## Gotchas
- Firmware/BIOS updates and Secure Boot changes trigger recovery mode unless BitLocker is suspended for one reboot (`Suspend-BitLocker -RebootCount 1`).
- Devices without TPM 2.0 or with legacy BIOS cannot do silent enablement.
- Protection "Suspended" counts as encrypted but offers no protection; report it separately.

## Checked
2026-10-28. Confirmed in the BitLocker configure page and cmdlet references: XTS-AES recommended for all drives, "Do not enable BitLocker until recovery information is stored" policy, `Suspend-BitLocker -RebootCount`, `Get-BitLockerVolume`, `Backup-BitLockerKeyProtector` (saves to AD DS), `manage-bde -protectors`. Removed: AES-CBC for removable drives, `BackupToAAD-BitLockerKeyProtector`, the 99% figure.
Method: documentation only; no commands were run.

## Verify
- [ ] Encryption report: all targeted devices encrypted with keys escrowed; suspended count near zero.
- [ ] Recovery key retrieval tested for a sample device.
