---
id: computing-software.it-support-helpdesk.desktop-support.bitlocker-recovery-key-retrieval
name: bitlocker-recovery-key-retrieval
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, workstation-security, bitlocker, bitlocker-recovery-key, key-id, entra-id-device, intune-recovery-keys, ad-recovery-password, manage-bde, recovery-trigger, bitlocker-recovery-loop]
level: practitioner
status: docs-checked
description: "Get a user past the BitLocker recovery screen safely: verify identity, match the key ID, find keys in Entra, Intune or AD, find the trigger, and rotate the key."
sources:
  - "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview"
  - "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-process"
  - "https://learn.microsoft.com/en-us/intune/device-configuration/endpoint-security/encrypt-bitlocker-windows"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/manage-bde-protectors"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# bitlocker-recovery-key-retrieval

Goal: unlock the user's PC in minutes, give the key only to the right
person, and stop it happening again.

## 1. Verify identity
A recovery key unlocks all data on the disk. Verify the caller to the same
standard as a password reset, and confirm both the person and that the named
device belongs to them (Microsoft's helpdesk recovery checklist starts here).

## 2. Match the Key ID
The preboot recovery screen shows a recovery key ID. Record it and the device
name; either locates the 48-digit recovery password, and a device can have
several. In the AD DS password viewer you can also search by the first eight
characters of the Password ID.

## 3. Find the key
| Where escrowed | How |
|---|---|
| **Microsoft Entra ID** (Entra-joined or hybrid) | Microsoft Entra admin center, "View or copy BitLocker keys". Admin needs a role holding `microsoft.directory/bitlockerKeys/key/read` (for example Cloud Device Administrator or Helpdesk Administrator) |
| **Entra self-service** | The user signs in at myaccount.microsoft.com, Devices tab, selects the device, View BitLocker Keys (unless your tenant restricts it) |
| **Intune** | Devices, select the device, Monitor, Recovery keys |
| **Active Directory** | Active Directory Users and Computers, computer object, BitLocker Recovery tab (needs the BitLocker Recovery Password Viewer from RSAT), or right-click the domain, Find BitLocker Recovery Password |
| Configuration Manager, other tools | follow that product's documentation |
If no key exists anywhere, the data cannot be recovered; back up what you can
from other sources and reimage.

Read the 48 digits out in groups of six; the recovery console checks each
six-digit block and lets the user correct a typo.

## 4. Why did recovery trigger?
Microsoft's list of causes includes: too many wrong PIN attempts, a BIOS or
UEFI firmware upgrade, changes to boot device order or PXE boot, TPM cleared,
disabled or failing its self-test, a new motherboard, and changes to the
measurements (PCRs) the TPM validates. Gather the cause before handing over
the key, for root-cause analysis.
- Planned firmware or hardware work: suspend BitLocker first. Suspend and
  resume reseals the key without needing the recovery key.
  `manage-bde -protectors -disable C:` suspends until the next boot (or use
  `-rebootcount`), `manage-bde -protectors -enable C:` resumes.
- Check protectors afterwards with `manage-bde -protectors -get C:`.

## 5. Rotate the disclosed key
- Intune: the **BitLocker key rotation** device action. It needs Windows 10
  1909 or later or Windows 11, and Entra-joined or hybrid devices need
  client-driven recovery password rotation enabled in the BitLocker policy.
  Your admin role needs the Remote tasks permission "Rotate BitLockerKeys".
- Manual: `manage-bde -protectors -delete C: -id <ID>` for the used protector
  (deleting the last protector turns protection off, so add the new one
  first), `manage-bde -protectors -add C: -RecoveryPassword`, then back up
  the new one with `manage-bde -protectors -aadbackup C: -id <ID>` (Entra) or
  `-adbackup` (AD DS). The PowerShell route is `BackupToAAD-BitLockerKeyProtector`.
- Policy can rotate the password automatically after it is used.

## Gotchas
- Wrong key ID means the key will not work; confirm you have the matching one.
- Backup to Entra ID or AD DS may not happen automatically; make sure policy
  enables it, or devices encrypted before enrolment may have no escrowed key.
- Entra ID stores at most 200 recovery keys per device; reaching the limit
  makes silent encryption fail.

## Verify
Device boots normally twice, protectors show TPM (plus recovery password)
healthy, and a new key is escrowed after rotation.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn BitLocker recovery overview and recovery process, Intune BitLocker encryption page, manage-bde-protectors, as published October 2026 (Windows 10/11). Confirmed: helpdesk recovery steps and key ID use, Entra role permission name, Intune Recovery keys path and rotation prerequisites (Windows 10 1909+), AD DS viewer and first-eight-character search, trigger list, suspend/resume resealing, manage-bde -disable/-enable/-delete -id/-add/-aadbackup/-adbackup, 200-key limit. Removed: aka.ms key link, BitLocker-API event advice, MBAM wording, Entra menu wording that the page does not give.

Method: documentation only; no commands were run.
