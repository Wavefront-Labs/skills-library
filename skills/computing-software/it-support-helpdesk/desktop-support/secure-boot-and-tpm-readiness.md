---
id: computing-software.it-support-helpdesk.desktop-support.secure-boot-and-tpm-readiness
name: secure-boot-and-tpm-readiness
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, secure-boot-tpm, tpm-2-0, secure-boot, ptt, ftpm, tpm-clear, windows-11-requirements, pc-health-check, bitlocker, windows-installation]
level: practitioner
status: docs-checked
description: "Check and enable TPM 2.0 and Secure Boot for Windows 11, BitLocker and compliance: tpm.msc, Confirm-SecureBootUEFI, firmware settings, and when clearing the TPM is safe."
sources:
  - "https://learn.microsoft.com/en-us/windows/whats-new/windows-11-requirements"
  - "https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/initialize-and-configure-ownership-of-the-tpm"
  - "https://learn.microsoft.com/en-us/powershell/module/secureboot/confirm-securebootuefi"
  - "https://learn.microsoft.com/en-us/powershell/module/trustedplatformmodule/get-tpm"
  - "https://support.microsoft.com/en-us/servicing/os/secure-boot/2025/06/windows-secure-boot-certificate-expiration-and-ca-updates"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# secure-boot-and-tpm-readiness

Goal: make a PC pass Windows 11 and BitLocker hardware checks without wiping
the BitLocker keys in the process.

## Check
```powershell
Get-Tpm                      # TpmPresent, TpmReady, ManufacturerVersion
tpm.msc                      # TPM management console
Confirm-SecureBootUEFI       # True / False; error on a BIOS (non-UEFI) computer
```
Windows 11 requires UEFI firmware that is Secure Boot capable and TPM
version 2.0. Windows Security, Device security, Security processor details
also shows TPM information.

## Enable
- Turn the TPM on in firmware (the setting name varies by vendor), save,
  reboot.
- `Confirm-SecureBootUEFI` is only meaningful on UEFI. If the disk is MBR,
  convert first (see
  `computing-software.it-support-helpdesk.desktop-support.gpt-uefi-partitioning-and-mbr2gpt`)
  and switch the firmware to UEFI mode.

## Clearing the TPM: only deliberately
**Back up first.** Clearing resets the TPM to an unowned state and Windows
reinitialises it. You lose all keys created with the TPM and the data they
protect, such as a virtual smart card or a sign-in PIN. Microsoft warns that
clearing can cause data loss.
1. Confirm the BitLocker recovery key is escrowed and readable (see the
   `bitlocker-recovery-key-retrieval` skill).
2. Suspend BitLocker: `manage-bde -protectors -disable C:`.
3. Clear in `tpm.msc` (Clear TPM) or Windows Security. The PC restarts and you
   may be asked to press a key to confirm.
4. Resume: `manage-bde -protectors -enable C:`; re-enrol the sign-in PIN.

## Gotchas
- Changing TPM settings or firmware boot configuration can trigger a BitLocker
  recovery prompt; Microsoft lists TPM clearing and early-startup component
  upgrades among the causes. Suspend BitLocker before planned changes.
- Windows 11 "unsupported CPU" is a separate requirement from TPM.
- On systems with two TPMs, pick one and do not toggle it; switching TPMs
  can put BitLocker into recovery.
- **Secure Boot certificate expiry:** the 2011 certificates are expiring
  during 2026: Microsoft Corporation KEK CA 2011 on 24 June 2026, Microsoft
  UEFI CA 2011 on 27 June 2026, and Microsoft Windows Production PCA 2011 on
  19 October 2026. Devices that have not received the 2023 certificates keep
  starting and installing normal Windows updates, but cannot receive new
  early-boot protections (Boot Manager, DB and DBX updates). Most devices get
  the new certificates automatically; some need an OEM firmware update.
  Check Microsoft's certificate-expiration guidance and your OEM's notes.

## Verify
`Get-Tpm` shows TpmReady True; `Confirm-SecureBootUEFI` returns True;
`manage-bde -status` shows protection on.


## Checked

Date 2026-10-27. Documentation release: Windows 11 requirements, TPM ownership/clear page, Confirm-SecureBootUEFI, Get-TPM, BitLocker recovery overview and Microsoft Support Secure Boot certificate page, as published October 2026. Confirmed: UEFI Secure Boot capable and TPM 2.0 requirements, tpm.msc and Windows Security path, clear-TPM precautions and restart prompt, Confirm-SecureBootUEFI return values, Get-Tpm properties, TPM-switch recovery warning, the three 2011 certificate expiry dates, and the effect of not updating. Removed: PTT/fTPM names, vendor mode-switch tools, PC Health Check, msinfo32 and Intune compliance details.

Method: documentation only; no commands were run.
