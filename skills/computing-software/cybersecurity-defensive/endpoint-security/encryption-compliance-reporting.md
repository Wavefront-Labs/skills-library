---
id: computing-software.cybersecurity-defensive.endpoint-security.encryption-compliance-reporting
name: encryption-compliance-reporting
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [encryption-compliance-reporting, bitlocker-reporting, filevault-reporting, intune-encryption-report, disk-encryption, audit-evidence]
level: practitioner
status: draft
description: "Report disk encryption compliance across fleets: Intune encryption report, BitLocker/FileVault status queries, key escrow verification, exceptions and audit evidence."
sources: ["https://learn.microsoft.com/en-us/mem/intune/protect/encryption-monitor", "https://learn.microsoft.com/en-us/powershell/module/bitlocker/get-bitlockervolume", "https://support.apple.com/guide/deployment/intro-to-filevault-dep82064ec40/web"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encryption compliance reporting

Auditors and lost-device breach decisions need proof: was this specific device encrypted, with a key we
can recover?

## Sources
| Platform | Source |
|---|---|
| Windows (Intune) | Devices -> Monitor -> Encryption report (encryption readiness, status, TPM version, profile state); Device compliance "Require BitLocker" |
| Windows (local/script) | `Get-BitLockerVolume | Select MountPoint, VolumeStatus, ProtectionStatus, EncryptionMethod, KeyProtector`; `manage-bde -status` |
| Windows (ConfigMgr/MBAM) | BitLocker management compliance reports |
| macOS | MDM FileVault status and escrowed personal recovery key; `fdesetup status` |
| Linux | Custom inventory: `lsblk -o NAME,TYPE,FSTYPE` showing crypto_LUKS for root; `cryptsetup status` |
| Defender for Endpoint | Advanced hunting `DeviceTvmSecureConfigurationAssessment` (ConfigurationId for BitLocker) |

## Check key escrow, not just encryption
- Entra: device -> BitLocker keys present for each OS volume (Graph `informationProtection/bitlocker/recoveryKeys`).
- AD: `msFVE-RecoveryInformation` child objects.
- MDM FileVault escrow present.
A device encrypted without escrowed key is a data-loss risk and may be non-compliant with policy.

## Report
- Fleet % encrypted (OS volumes, fixed data volumes), encryption method (XTS-AES 128/256), protection on (not suspended), key escrowed.
- Exceptions list with reason and expiry (e.g. lab devices).
- Monthly evidence export with date stamp for auditors.

## Gotchas
- `ProtectionStatus Off` with `FullyEncrypted` = suspended BitLocker (key in clear) - counts as non-compliant.
- Devices not checked in for 30 days have stale status; report them separately.

## Verify
- [ ] Monthly report: encrypted + protected + escrowed >= target (e.g. 99%).
- [ ] Sample of 10 devices: recovery key retrievable.
