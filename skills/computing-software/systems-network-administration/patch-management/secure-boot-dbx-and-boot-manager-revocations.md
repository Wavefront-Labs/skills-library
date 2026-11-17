---
id: computing-software.systems-network-administration.patch-management.secure-boot-dbx-and-boot-manager-revocations
name: secure-boot-dbx-and-boot-manager-revocations
category: computing-software
field: systems-network-administration
product: patch-management
tags: [secure-boot-dbx, dbx, secure-boot, blacklotus, uefi-ca-2023, firmware-patching]
level: practitioner
status: docs-checked
description: "Apply Secure Boot dbx and boot manager revocation updates safely: BlackLotus mitigations, Windows UEFI CA 2023 rollout, Linux shim/SBAT, recovery media and firmware bugs."
sources:
  - https://support.microsoft.com/en-us/topic/kb5025885-how-to-manage-the-windows-boot-manager-revocations-for-secure-boot-changes-associated-with-cve-2023-24932-41a975df-beb2-40c1-99a3-b3ff139f832d
  - https://uefi.org/revocationlistfile
  - https://github.com/rhboot/shim/blob/main/SBAT.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure Boot dbx and boot manager revocations

The UEFI **dbx** (forbidden signatures database) blocks vulnerable boot loaders. Adding entries is a patch that can make machines unbootable from old media, or at all on buggy firmware.

## Windows: CVE-2023-24932 (BlackLotus) and CA 2023
Per KB5025885 (read 2026-10-27), steps are set through the registry value `AvailableUpdates` under `HKLM\SYSTEM\CurrentControlSet\Control\Secureboot` and then triggered with the Secure-Boot-Update scheduled task:
1. Install the 2023 Secure Boot certificates to the DB (and KEK) and update to the 2023-signed boot manager: `0x5944`. Verify with the DB check below and `UEFICA2023Status` under the `Servicing` subkey (should read Updated). Devices marked High Confidence in monthly updates may already have this.
2. Enable the revocation (adds "Windows Production PCA 2011" to the DBX): `0x80`; success is event 1037.
3. Apply the optional SVN update to firmware: `0x200`; event 1042.
```powershell
reg add HKLM\SYSTEM\CurrentControlSet\Control\Secureboot /v AvailableUpdates /t REG_DWORD /d 0x5944 /f
Start-ScheduledTask -TaskName '\Microsoft\Windows\PI\Secure-Boot-Update'
# after reboot, check
[System.Text.Encoding]::ASCII.GetString((Get-SecureBootUEFI db).bytes) -match 'Windows UEFI CA 2023'
```
Success events listed by the KB: 1036 (DB updated), 1799 (2023-signed boot manager applied), 1037 (DBX update), 1042 (SVN). The enforcement phase will make the mitigations permanent; Microsoft says it will not begin before January 2026 with at least six months of notice, so check the KB's timing section for the current date. After the April 2026 updates, enabling PCA 2011 revocation applies SVN 5.0, which invalidates older external boot media.

## Before revoking (step 3)
- Update all boot media (the KB describes building recovery media with bcdboot and its `/bootex` option): WDS/PXE, ConfigMgr boot images, USB recovery, ISO libraries, VM templates, backup recovery ISOs; old media will not boot afterwards.
- BitLocker: ensure recovery keys are escrowed; PCR7 changes can trigger recovery.
- Test each hardware model; some firmware rejects db/dbx updates or bricks (vendor BIOS updates fix).

## Linux
- Revocation can use **SBAT** (generation numbers carried in boot components such as shim and GRUB, raised on each revocation event) instead of growing the dbx; see the rhboot/shim SBAT.md document.
- Apply dbx and SBAT updates through your distribution's documented mechanism and update shim before revoking older shims; the specific tool commands are in your distribution's documentation (not confirmed here).

## Gotchas
- Applying revocation cannot be undone without disabling Secure Boot or resetting keys in firmware.
- Dual-boot and older Linux media stop booting after new SBAT/dbx entries.

## Verify
db contains CA 2023, boot manager signed by CA 2023, dbx/SVN applied per plan, and boot media rebuilt and tested; events 1036, 1799, 1037 and 1042 in the System log show success.

## Checked
Date: 2026-10-27. Documentation: Microsoft KB5025885 (current revision: AvailableUpdates values 0x5944, 0x80, 0x200, success events 1036, 1799, 1037, 1042, UEFICA2023Status, SVN 5.0 note, enforcement timing, BitLocker and firmware warnings, bcdboot /bootex media step) and rhboot/shim SBAT.md. Corrected the outdated 0x40 and 0x100 steps and removed the 2026 certificate-expiry claim and the unconfirmed mokutil and fwupdmgr commands.
Method: documentation only; no commands were run.
