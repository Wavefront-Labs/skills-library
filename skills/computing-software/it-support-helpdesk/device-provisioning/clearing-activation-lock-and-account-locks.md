---
id: computing-software.it-support-helpdesk.device-provisioning.clearing-activation-lock-and-account-locks
name: clearing-activation-lock-and-account-locks
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, activation-lock-removal, activation-lock, factory-reset-protection, recovery-lock, apple-business-manager, offboarding]
level: practitioner
status: draft
description: "Clear device locks that block reuse: Apple Activation Lock via user, MDM bypass code or Apple request, Android FRP, Mac Recovery Lock and firmware passwords."
sources:
  - "https://support.apple.com/en-us/108794"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/device-activation-lock-disable"
  - "https://support.google.com/android/answer/9459346"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# clearing-activation-lock-and-account-locks

## Apple Activation Lock (iPhone, iPad, Mac)
Tied to the Apple Account that turned on Find My. After erase, the device asks for that
account's password.
1. **Best**: the user signs out of Find My before handing back (Settings > [name] > Find My
   > off), or removes the device at icloud.com/find.
2. **Supervised devices (ADE)**: MDM can store a bypass code when it allows Activation Lock;
   Intune > device > **Disable Activation Lock** (iOS) clears it. Enter the code shown in
   Intune at the lock screen if prompted. For Macs, MDM can also escrow a bypass code.
3. **Organisation-owned without a code**: request removal from Apple with proof of
   purchase through Apple's Activation Lock support process; slow, so prevent it.
Prevention: ADE enrolment with supervision, and a policy that disallows personal Find My
on corporate devices or captures the bypass code.

## Mac locks beyond Activation Lock
- **Recovery Lock** (Apple silicon) or firmware password (Intel): set by MDM; retrieve the
  password from Intune/Jamf device record before working in Recovery.
- FileVault: personal recovery key escrowed in MDM.

## Android Factory Reset Protection
- After a reset not done from settings or MDM, FRP asks for the last Google account on the
  device.
- Corporate: MDM wipe from Intune avoids FRP for fully managed devices; set enterprise
  FRP accounts via policy so IT can unlock. Samsung devices can also be released via Knox.
- Personal account on a corporate device: the user must remove the account before return.

## Windows
No activation lock, but BIOS/UEFI supervisor passwords (vendor tools hold them) and
BitLocker recovery keys (Entra/Intune) can block a technician; retrieve before starting.

## Gotchas
- Removing a device from Apple Business Manager does not clear Activation Lock.
- Do not ship locked devices to ITAD; they lose resale value and may be rejected.

## Verify
The device completes setup to the home screen/desktop with a new account (or re-enrols
via ADE/zero-touch), and the asset record notes the lock cleared and how.
