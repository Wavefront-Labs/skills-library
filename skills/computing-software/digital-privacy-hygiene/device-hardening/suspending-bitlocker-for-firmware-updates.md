---
id: computing-software.digital-privacy-hygiene.device-hardening.suspending-bitlocker-for-firmware-updates
name: suspending-bitlocker-for-firmware-updates
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, bitlocker-suspend, bitlocker, firmware-updates]
level: practitioner
status: docs-checked
description: "Suspend BitLocker for a planned firmware update with Suspend-BitLocker and a reboot count, then resume protection so you are not sent to recovery."
sources:
  - "https://learn.microsoft.com/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview"
  - "https://learn.microsoft.com/powershell/module/bitlocker/suspend-bitlocker"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Suspending BitLocker for firmware updates

**Goal:** update BIOS/UEFI firmware without triggering BitLocker recovery.

## Why
BitLocker recovery can be triggered by upgrading critical early startup components such as a BIOS or UEFI firmware upgrade,
or by clearing the TPM or modifying the PCRs used by the TPM validation profile. For planned firmware upgrades Microsoft
says you can avoid recovery by temporarily suspending BitLocker: the drive stays fully encrypted, and suspend then resume
reseals the key without entering the recovery key.

## Before the update
1. Make sure you can reach your recovery password (a 48-digit number; it may be saved as a file, printed, or stored in
   Microsoft Entra ID or Active Directory). Do not start without it.
2. In an administrator PowerShell:
   ```
   Suspend-BitLocker -MountPoint "C:" -RebootCount 1
   ```
   If you omit `-RebootCount` it defaults to 1, so protection resumes after the next restart. `-RebootCount` sets how many
   restarts before suspension ends; 0 keeps it suspended until you run `Resume-BitLocker`.
3. Run the vendor's firmware update.

## After
BitLocker automatically resumes after the specified reboot count. If you used 0, or it is still suspended, run
`Resume-BitLocker -MountPoint "C:"`.

## Gotchas
- While suspended BitLocker does not validate system integrity at startup and the encryption key is available in the
  clear: don't leave it suspended or travel with it suspended.
- If you do land in recovery, enter the recovery password; Microsoft's recovery overview lists the places it may be stored.

## Checked
2026-10-28. Confirmed on Microsoft Learn (BitLocker recovery overview; Suspend-BitLocker): recovery triggers, suspend and
resume resealing, default reboot count, RebootCount 0 behaviour, key in the clear while suspended, Resume-BitLocker, 48-digit
recovery password and storage locations. Removed (not on the fetched pages): the manage-bde commands and options, aka.ms
recovery key link, OEM auto-suspend and Secure Boot change claims.
Method: documentation only; no commands were run.
