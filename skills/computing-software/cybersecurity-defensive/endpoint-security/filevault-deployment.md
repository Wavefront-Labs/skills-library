---
id: computing-software.cybersecurity-defensive.endpoint-security.filevault-deployment
name: filevault-deployment
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [full-disk-encryption, filevault, macos, personal-recovery-key, mdm-escrow, bootstrap-token, secure-token, apple-silicon]
level: practitioner
status: draft
description: "Enable FileVault on managed Macs via MDM with escrowed personal recovery keys, secure token and bootstrap token handling, key rotation and reporting."
sources: ["Apple Platform Deployment guide - Manage FileVault with MDM", "Apple Platform Security Guide (Volume encryption with FileVault)", "CIS Apple macOS Benchmark"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FileVault deployment

**Goal:** every managed Mac has FileVault on, with a recovery key the organisation can retrieve
and rotate.

## Configuration profile (FileVault payload, via Jamf/Intune/Kandji)
- Enforce enable at next login (or during Setup Assistant with ADE).
- Personal recovery key (PRK), **escrowed to MDM** (FDERecoveryKeyEscrow payload encrypts the key to an MDM certificate).
- Do not show the recovery key to the user (or show briefly, per policy).
- Disable the option to defer more than once.

## Tokens on modern macOS
- **Secure token**: required for an account to unlock FileVault. The first user created at setup gets one; others get it from an existing secure token holder.
- **Bootstrap token**: escrowed to MDM (requires supervised/ADE), lets MDM grant secure tokens and authorise software updates and kernel extensions on Apple silicon. Check: `sudo profiles status -type bootstraptoken`.
- On Apple silicon and T2 Macs, storage is always hardware-encrypted; FileVault adds the requirement for the user password to unlock the key.

## Commands
```
fdesetup status
sudo fdesetup list                    # users able to unlock
sudo profiles status -type bootstraptoken
```

## Recovery and rotation
- Retrieve the PRK from MDM after identity verification.
- Rotate after use: MDM command or `fdesetup changerecovery -personal` (Jamf policies automate this and re-escrow).
- Institutional recovery keys (certificate-based) are deprecated on Apple silicon; use PRK escrow.

## Gotchas
- Macs encrypted before enrolment have keys MDM does not know; reissue a new PRK and escrow it.
- Missing escrow profile at enable time means no key in MDM; check escrow status in reports, not just FileVault on/off.
- Local accounts without secure token (created by scripts) cannot unlock the disk.

## Verify
- [ ] Report: FileVault on and a valid escrowed key for every Mac.
- [ ] Test recovery on a lab Mac with the escrowed key.
