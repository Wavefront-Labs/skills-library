---
id: computing-software.cybersecurity-defensive.system-hardening.blacklotus-mitigation
name: blacklotus-mitigation
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [blacklotus-mitigation, uefi-bootkit, secure-boot, dbx, boot-manager-revocation, cve-2023-24932]
level: advanced
status: docs-checked
description: "Mitigate BlackLotus (CVE-2023-24932) on Windows: apply Secure Boot revocations in stages, update boot media, the 2023 CA transition, verification and recovery planning."
sources: ["https://support.microsoft.com/en-us/topic/how-to-manage-the-windows-boot-manager-revocations-for-secure-boot-changes-associated-with-cve-2023-24932-41a975df-beb2-40c1-99a3-b3ff139f832d"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BlackLotus bootkit mitigation

BlackLotus is a UEFI bootkit that bypasses Secure Boot (CVE-2023-24932); the fix requires revoking boot managers. Patching the OS is not enough: the vulnerable
signed binaries must be **revoked** in the firmware's Secure Boot forbidden database (DBX) or via SVN, which
Microsoft ships as **opt-in, staged** changes because revocation can make old boot media unbootable.

## Staged mitigations (Microsoft KB5025885)
Mitigations ship in Windows security updates from July 9, 2024 and are not enabled by default. Follow the KB's current
steps (the revision history shows its commands, including starting the Secure-Boot-Update scheduled task, have changed):
1. Add the **"Windows UEFI CA 2023"** certificate to the Secure Boot DB.
2. Update the boot manager on the device to one signed by the 2023 CA.
3. Add the "Windows Production PCA 2011" to DBX (revokes all boot managers signed by the old CA, including
   vulnerable ones).
4. Apply the SVN (secure version number) update to the firmware to block rollback to older boot managers.
The KB's event table confirms stages: 1036 (DB update), 1799 (boot manager), 1037 (DBX update) and 1042 (SVN).
Follow the current KB revision; steps and dates have changed over time.

## Before enforcing revocations
- **Update boot media**: WinPE, PXE/WDS boot images, ConfigMgr task sequence media, recovery USBs and ISOs must be
  rebuilt with 2023-signed boot managers, or devices with revocations applied will refuse to boot them.
- **Firmware compatibility**: test per hardware model; some firmware has bugs applying DB/DBX updates. Update
  OEM firmware first.
- **BitLocker**: some devices may go into BitLocker recovery; keep a copy of the recovery key before enabling the mitigations.

## Detection
The mitigations are preventive, not corrective: if a device may already be compromised, contact your security provider (the KB says the same). The malware needs administrative or physical access.

## Verify
On a mitigated device: `[System.Text.Encoding]::ASCII.GetString((Get-SecureBootUEFI db).bytes) -match 'Windows UEFI CA 2023'`
returns True, the DBX check from the KB passes, the expected events are logged, and updated boot media
boots successfully.

## Checked
2026-10-28. Confirmed against official pages: mitigation steps (DB certificate, boot manager, DBX revocation, SVN), not enabled by default, irreversible once applied, update boot media, BitLocker recovery, event IDs 1036/1799/1037/1042, preventive-not-corrective (Microsoft KB5025885).
Removed or rewritten: CVE-2022-21894, the AvailableUpdates bit-flag claims, event IDs 1035 and 1795-1798 and the TPM-WMI source, PCR7, the third-party CA and June 2026 expiry notes, ESP/HVCI detection indicators, and two blocked or stub sources (NSA PDF, techcommunity post).
Method: documentation only; no commands were run.
