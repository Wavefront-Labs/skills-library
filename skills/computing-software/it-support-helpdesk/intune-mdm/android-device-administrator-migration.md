---
id: computing-software.it-support-helpdesk.intune-mdm.android-device-administrator-migration
name: android-device-administrator-migration
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, device-administrator-migration, android-device-administrator, android-enterprise, work-profile, gms, android-enrollment]
level: practitioner
status: docs-checked
description: "Move Android devices off legacy device administrator management in Intune: pick the target mode, use the block-device-administrator compliance setting, fix Resolve errors."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/android-move-device-admin-work-profile"
  - "https://developers.google.com/android/work/device-admin-deprecation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# android-device-administrator-migration

Android device administrator (DA) is the legacy management API. Intune states DA management is
deprecated and no longer available for devices with Google Mobile Services (GMS); support and
help stay available for some Android 15 and earlier devices without GMS. Google likewise
recommends work profile and managed device modes instead.

## Choose the target
| Current | Target | Reset needed? |
|---|---|---|
| Personal (BYOD), DA | Personally owned work profile | No. Intune's compliance-driven flow guides the user |
| Company-owned, DA | Fully managed (managed device) | Yes, factory reset (Google) |

Google suggests phased adoption for company-owned devices: enrol new ones as fully managed and
age DA devices out, since the reset is disruptive. "Big bang" waves are the alternative.

## Personal devices: compliance-driven move
Prerequisites:
- DA-enrolled devices have Android Company Portal 5.0.4720.0 or later.
- Intune tenant connected to an Android Enterprise account, and personally owned work profile
  enrollment allowed for the user group (check enrollment restrictions).
- Consider raising device limits: unenrolled DA records may not disappear at once, and the
  Microsoft Entra "Maximum number of devices per user" and Intune device limit can block the
  new enrollment.

Create the policy: Devices > Compliance > Create policy > Platform **Android device
administrator** > Compliance settings > Device Health > **Block devices managed with device
administrator = Yes**. Assign to a group of DA devices.

Actions for noncompliance:
- Mark device noncompliant: default 0 days (immediate). A grace period, for example 14 days,
  lets users see the flow without losing access yet.
- Push notification: opens Company Portal at **Update device settings**.
- Email: can include https://portal.manage.microsoft.com/UpdateSettings.aspx (US government:
  https://portal.manage.microsoft.us/UpdateSettings.aspx). Users must tap it on the Android
  device; pasting it into a browser does not open the app. Do not use URL shorteners.

When users tap **Resolve**, a checklist unenrolls DA, enrolls into the work profile and
resolves compliance issues.

## Troubleshooting
- Error after Resolve: Android Enterprise account not connected, enrollment restrictions block
  personally owned work profile, Android 4.4 or earlier, or an OEM that does not support work
  profile on that model.
- No Resolve button: the user enrolled in DA after being targeted by the policy. They should
  postpone setup and restart from the notification. Prevent it by blocking DA enrollment with
  enrollment restrictions.
- Error from the Update device settings link: not an Android device, no Company Portal,
  Company Portal older than 5.0.4720.0, or Android 6 or earlier.

## Verify
DA device count falls to zero and migrated devices appear as personally owned work profile
enrollments and compliant.

## Checked
Date: 2026-11-08. Read in full: Intune "Move Android devices from device administrator to personally owned work profile management" (updated 2026-04-09) and Google "Device admin deprecation" (updated 2025-08-28). The Intune end-of-support source URL returned 404 and was dropped. Removed as unconfirmed: the 31 Dec 2024 date, the device-list filter steps, non-GMS AOSP advice, "below Android 8" work profile claim, badge and Outlook user-comms claims, and the idea that DA Wi-Fi/email profiles do not carry over.
Method: documentation only; no commands were run.
