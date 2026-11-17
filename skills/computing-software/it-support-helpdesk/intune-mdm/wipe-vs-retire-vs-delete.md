---
id: computing-software.it-support-helpdesk.intune-mdm.wipe-vs-retire-vs-delete
name: wipe-vs-retire-vs-delete
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, wipe-vs-retire, remote-wipe, retire, delete-device, factory-reset, remote-actions, intune]
level: practitioner
status: docs-checked
description: "Choose the right Intune remote action: Wipe (factory reset), Retire (remove company data), Delete (remove record and retire); Windows wipe options, daily limits, roles."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/devices-wipe"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/device-management"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wipe-vs-retire-vs-delete

| Action | Microsoft's description |
|---|---|
| **Wipe** | Restores a device to factory settings and removes all data and settings. |
| **Retire** | Removes company data and settings from a device, and leaves personal data intact. |
| **Delete** | Removes a device from Intune management, removes any company data, and retires the device. |

- For MDM devices, Delete immediately hides the device from the admin center and starts a
  Retire. A Completed status on a delete action means the server side is done; it does not
  confirm the client finished the Retire.
- Retire, Wipe and Delete take precedence over all other pending actions; a device with
  several pending actions carries out only that one.
- Daily tenant limits, cumulative across single, bulk and Graph requests: Wipe 500, Retire
  1,000, Delete 1,000 (contact Microsoft support to change). Bulk actions cover up to 100
  devices (Devices > All devices > Bulk device actions).
- Devices must be enrolled and online to receive remote commands. Check status under
  Devices > Device actions.

## Wipe details
- Run: Devices > All devices > device > Remove data > Wipe. Roles: Help Desk Operator, School
  Administrator, or a custom role with Remote tasks/Wipe plus read access to managed devices.
- Platforms: Android Enterprise COSU, COBO and COPE, AOSP, ChromeOS, iOS/iPadOS, macOS,
  tvOS 10.2+, visionOS 1.1+, Windows.
- **Windows options**:
  - Keep enrollment state and user account: resets to factory settings preserving user
    data, accounts and key settings; MDM policies are removed but the device stays
    enrolled (doWipePersistUserData CSP node).
  - Continue to wipe even if the device loses power: deletes user data, settings and MDM
    policies, overwrites free space (doWipeProtected). Can leave some devices unable to
    start; use only on corporate devices where full data destruction is required.
  - No options: factory reset (doWipe). If interrupted it tries to roll back; if rollback
    fails the device may need a full Windows reinstall.
- **macOS**: enter a 6-digit Recovery PIN (needed to reinstall the OS on devices without a
  T2 chip; not visible after the wipe) and an Obliteration Behavior (Default, Do not
  obliterate, Obliterate with warning, Always obliterate) as the fallback if Erase All
  Content and Settings fails.
- **iOS/iPadOS eSIM**: the cellular plan is kept by default; select the option to remove it.
  Android COBO/COSU/COPE eSIMs also kept by default.
- **ChromeOS**: remove user profiles only, or factory reset (powerwash); deprovision first
  or the device re-enrolls when it reaches Wi-Fi.
- **Android notes**: admin wipe does not preserve Factory Reset Protection data by default.
  On fully managed Samsung devices the Factory Reset restriction must not be Block, or the
  device loses contact with Intune without resetting. On Zebra Android devices Wipe removes
  only corporate data; use StageNow or OEM Config to factory reset.
- A multiple administrative approval access policy may require a second administrator.
- Afterwards, consider removing the device from Windows Autopilot and from Entra ID.

## Checked
Date: 2026-11-07. Read in full: "Wipe devices with Microsoft Intune" (updated 2026-09-25) and "Device actions" (updated
2026-09-16). The device-delete source returned 404 and was dropped. Corrections: Delete does not wait for a later check-in; for
MDM devices it hides the record immediately and starts a Retire. Removed as unconfirmed: the effect table for Retire per platform
(Wi-Fi/VPN/certs, "cloud-joined PC usually needs wipe"), "default wipe reaches OOBE and Autopilot re-enrolls", Activation Lock
bypass, "offline devices stay Pending indefinitely", "delete does not remove the Autopilot or Entra object" (the page only
suggests removing them manually), the locked-ADE retire claim, the decision rules and the Verify step.
Method: documentation only; no commands were run.
