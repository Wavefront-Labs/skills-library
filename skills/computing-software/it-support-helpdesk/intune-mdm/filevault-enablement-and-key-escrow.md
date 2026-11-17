---
id: computing-software.it-support-helpdesk.intune-mdm.filevault-enablement-and-key-escrow
name: filevault-enablement-and-key-escrow
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, macos-management, filevault, filevault-escrow, personal-recovery-key, fdesetup, intune-macos]
level: practitioner
status: docs-checked
description: "Enforce FileVault on managed Macs with Intune and escrow recovery keys: policy types, Setup Assistant enforcement, key retrieval and rotation, taking over existing encryption."
sources:
  - "https://learn.microsoft.com/en-us/intune/device-configuration/endpoint-security/encrypt-filevault-macos"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# filevault-enablement-and-key-escrow

Goal: every managed Mac is encrypted, the personal recovery key (PRK) is escrowed
in Intune, and the help desk can recover a Mac without the user having
recorded the key.

FileVault is macOS whole-disk encryption using XTS-AES 128-bit, which cannot be
changed to 256-bit from Intune or macOS. It needs macOS 10.13 or later and
user-approved MDM enrollment.

## Deployment in two stages
1. Key escrow preparation: the device is set up so Intune can back up the key.
2. Disk encryption starts after the key is escrowed.
The device shows the PRK to the user once. Intune exposes only the options in
its templates and settings catalog, not every FileVault capability.

## Policy types
- **Endpoint security > Disk encryption > Create policy**, platform macOS,
  profile macOS FileVault. Simplest. Settings: Enable = On, Use Recovery Key,
  Recovery Key Rotation In Months, Location (guidance text for users), Allow
  deferral until sign out, Defer Dont Ask At User Logout, Defer Force At User
  Login Max Bypass Attempts.
- **Settings catalog** (Devices > By platform > macOS > Configuration > Create >
  New policy): under Full Disk Encryption set FileVault Enable = On and Defer =
  Enabled (the page says Defer is required for FileVault to apply), plus FileVault
  Recovery Key Escrow > Location. Optional: Show Recovery Key, the two Defer
  settings, Recovery Key Rotation In Months. The only route to Setup Assistant
  enforcement.
- The Device configuration Endpoint protection template for macOS is
  deprecated and cannot create new profiles.

Write the Location text so users know where to get the key, for example: sign in
to the Intune Company Portal website, open Devices, pick the Mac, select Get
recovery key. Add your support contact.

## Setup Assistant enforcement (macOS 14+)
Encrypts during setup with no user step, key escrowed automatically.
- Mac enrolled through Apple Business Manager or Apple School Manager; the
  enrollment profile has Await final configuration = Yes; target with a device
  filter on EnrollmentProfileName.
- Settings catalog: FileVault > Force Enable in Setup Assistant = Enabled and
  Defer = Enabled (Defer must be Enabled for macOS 14.4).
- Before macOS 14.4 the account created interactively in Setup Assistant must
  be an Administrator.

## Key escrow, viewing and rotation
- Intune escrows a key when its policy encrypts a device, or when a user
  uploads the key of a Mac they encrypted themselves.
- Admins can view a PRK only for devices marked **Corporate**, never Personal
  (BYOD). Viewing is via the device > Monitor > Recovery keys > Show Recovery Key,
  which writes an audit log entry. The admin role needs Remote tasks with the
  Rotate FileVault key right set to Yes (built-in: Help Desk Operator, Endpoint
  Security Administrator).
- Users get the key from the Company Portal website (portal.manage.microsoft.com,
  the recommended route) or the Company Portal / Intune mobile apps: Devices,
  pick the Mac, Get recovery key.
- Automatic rotation: Recovery Key Rotation In Months (1 to 12). The old key is
  invalid after rotation and the user fetches the new one in Company Portal.
- Manual rotation (Corporate devices only): Devices > All devices > device >
  Secure > Rotate FileVault recovery key. Rotate after any key has been
  disclosed, for example to unlock a locked-out user.

## Taking over a Mac the user already encrypted
Deploy the FileVault policy (endpoint security profile) first, then either:
- Method 1: the user opens the Company Portal website, picks the Mac, chooses
  Store recovery key and enters their current key; Intune validates it and
  rotates to a new escrowed key.
- Method 2 (user lacks the key): in Terminal run
  `sudo fdesetup changerecovery -personal` in /Applications/Utilities, enter the
  device password; the new key is displayed and the Mac's next check-in lets
  Intune assume management. Speed up with Sync from the admin center or Company
  Portal > Settings > Sync.
Verify in the encryption report (Devices > Monitor > Device encryption status)
that status and key availability show, and test a retrieval.

## Troubleshooting
| Symptom | Check |
|---|---|
| Enablement fails | User-approved MDM enrollment |
| Escrow fails | Device network connectivity; encryption report escrow status |
| Setup Assistant enforcement does nothing | Defer = Enabled; Await final configuration |
| User cannot get key | Device is enrolled and was encrypted through Intune; Corporate vs Personal |
| Admin cannot see key | Device marked Personal: expected |
Error -2016341107 (0x87d1138d): the user did not accept the FileVault prompt;
consider Setup Assistant enforcement. Use Intune policy conflict detection for
overlapping FileVault policies. A compliance policy with Require encryption of
data storage can block access until encrypted.

## Verify
Encryption report shows the Mac encrypted, a recovery key is available for
Corporate devices, and a test retrieval through Company Portal works.

## Checked
2026-11-08. Confirmed against the Microsoft Learn page Encrypt macOS devices
with FileVault using Intune (last updated 2026-04-15): policy types and
settings, Setup Assistant enforcement, escrow, Corporate vs Personal key access,
rotation, takeover methods, error code. Removed as unconfirmed: Jamf steps (page
unreadable), the secure token and bootstrap token section, local diagnostic
commands, institutional recovery key and Apple silicon recovery notes.
Method: documentation only; no commands were run.
