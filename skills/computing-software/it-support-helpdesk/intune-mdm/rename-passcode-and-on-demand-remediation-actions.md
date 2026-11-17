---
id: computing-software.it-support-helpdesk.intune-mdm.rename-passcode-and-on-demand-remediation-actions
name: rename-passcode-and-on-demand-remediation-actions
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, rename-device, passcode-reset, on-demand-remediation, remote-actions, intune-device-actions]
level: practitioner
status: docs-checked
description: "Use Intune device actions for renaming devices, resetting Android passcodes, and running a remediation script on demand, with platform limits and checks."
sources:
  - "https://learn.microsoft.com/en-us/intune/device-management/inventory-and-status/rename-device"
  - "https://learn.microsoft.com/en-us/intune/device-management/actions/reset-passcode"
  - "https://learn.microsoft.com/en-us/intune/device-management/tools/deploy-remediations"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rename-passcode-and-on-demand-remediation-actions

## Rename device
- Devices > All devices > pick the device > **Properties** > Edit > change the device name.
  Supported: Android Enterprise corporate-owned (fully managed, dedicated, COPE), supervised
  iOS/iPadOS, corporate-owned macOS and corporate-owned Windows. For Windows set **Restart
  after rename** to Yes if you want the device restarted.
- Windows names: 63 characters or fewer, letters/numbers/hyphens, not only numbers, no
  spaces. iOS/iPadOS and macOS: letters, numbers, hyphens, at least one letter or hyphen.
- Entra hybrid joined Windows devices can't be renamed from Intune; use domain-based methods.
- The rename changes the Device name in the admin center, not the Management name or the
  Company Portal name. On Android it changes only the admin-center name, and the portal list
  can take 10 minutes or more to update.
- iOS/iPadOS with an enrollment profile Device Name Template reverts to the template at the
  next sync.
- Bulk rename uses Bulk Device Actions and the name must include `{{serialnumber}}` or
  `{{rand:x}}`.

## Reset passcode (Android only)
Devices > All devices > device > **Secure** > **Reset passcode**; the new passcode shows in
the admin center for seven days and must be entered on the device.
| Platform | Reset type |
|---|---|
| Android Enterprise dedicated (COSU), AOSP | Device-level |
| Android Enterprise fully managed (COBO), COPE, personal work profile | Work profile |
- A passcode requirement must be enforced by a device configuration policy first, or the
  reset fails.
- Roles: Help Desk Operator, School Administrator, or a custom role with Remote Tasks/Reset
  Passcode.
- The reset passcode page covers Android only. The device actions list shows Remove passcode for iOS/iPadOS; see its own page.
- Verify identity first (help desk social engineering is common here).

## Run remediation on demand (preview)
- Device > ... > **Run remediation (preview)**: pick a script package and run it on a single
  Windows device. Remediations must already be configured; the package need not be assigned.
- Needs Intune Admin or a role with Run remediation (under Remote tasks).
- Remediations require users with a Windows Enterprise E3 or E5 licence (included in
  Microsoft 365 F3, E3 or E5).
- Only one Run remediation action at a time per device; several in quick succession can
  overwrite each other.
- The device does not receive the action if offline or unable to reach Intune or WNS.

## Verify
The rename appears in the device list, the user enters the issued passcode, and remediation
status on the device shows the run result.

## Checked
2026-11-01. Confirmed against the Intune Learn pages for rename device, reset passcode and
Remediations: platforms, Windows 63-character limit, hybrid-join exclusion, Android-only
passcode table, seven-day display, licences, one-action-at-a-time and offline behaviour.
Removed: the 15-character Windows limit (docs say 63), the macOS passcode row
and the iOS passcode detail, "iPhone unavailable" and the 60-minute claim, and the claim that actions queue
when offline (the Remediations page says the device won't receive it).
Method: documentation only; no commands were run.
