---
id: computing-software.it-support-helpdesk.intune-mdm.android-aosp-enrollment-and-system-updates
name: android-aosp-enrollment-and-system-updates
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, aosp-enrollment, android-system-updates, android-enterprise, fota, rugged-devices, headsets]
level: practitioner
status: docs-checked
description: "Enroll userless AOSP devices (such as RealWear headsets) in Intune, and control Android system updates and Zebra LifeGuard OTA firmware deployments."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/android-aosp-corporate-owned-userless-enroll"
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/device-restrictions-android-for-work"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/zebra-lifeguard-ota-integration"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# android-aosp-enrollment-and-system-updates

## AOSP enrollment
- For devices built on the Android Open Source Project that do not use Google Mobile Services.
  Microsoft's article walks through RealWear devices as the worked example.
- Choose Corporate-owned, userless devices in the Android Open Source Project (AOSP) section
  of the Intune enrollment settings, then create an enrollment profile.
- The profile has a token expiration date, up to 90 days ahead. Intune shows the token as a
  **QR code**; the plain-text token it also generates cannot enroll devices.
- Wi-Fi details in the profile are required for RealWear, which cannot connect on its own.
  Skip the vendor's first-time setup; the Intune QR code is all the device needs.
- During device setup, scan the QR code to enroll. Tokens can be viewed again under Tokens.
- Check the device model against Microsoft's supported-device list before buying in bulk.
- AOSP management is not supported in Intune operated by 21Vianet.

## Android system updates
- A device restrictions profile (System update) offers Automatic, Postponed (30 days) and
  Maintenance window options. Postponed does not stop manufacturers or carriers exempting
  important security updates.
- **Freeze periods** are optional (MM/DD start and end, up to 90 days long). Updates and
  security patches, including manual checks, are blocked during the freeze. Recurring freeze
  periods must be separated by at least 60 days.
- These control the OS update prompt; the OEM still decides when an update exists.
- For devices the profile does not cover, use compliance minimum OS version and patch level.

## FOTA for Zebra devices
- Intune integrates with **Zebra LifeGuard Over-the-Air (LG OTA)** so firmware updates for
  supported Zebra devices are managed from the Intune admin center, through Zebra's APIs.
- Create and manage deployments under Devices > By platform > Android > Manage updates >
  Android FOTA deployments. Non-Zebra or not-enrolled devices in the assigned group are
  left out of the reports.
- Test new firmware on a pilot group with your line-of-business apps first.

## Verify
AOSP devices show in Intune after QR enrollment; a pilot device takes an update in its
maintenance window and none take updates during a freeze period.

## Checked
2026-11-01. Confirmed against the three Learn pages in sources: userless AOSP profile, 90-day
token, QR vs plain-text token, RealWear Wi-Fi requirement, 21Vianet exclusion, System update
options, 30-day postpone, freeze period format (up to 90 days, 60-day separation), Zebra LG OTA
and the Android FOTA deployments path. Removed: user-associated mode, named non-RealWear
devices, device-specific gesture steps, "basic compliance" and Managed Google Play statements,
Samsung Knox E-FOTA, and menu paths not in the pages.
Method: documentation only; no commands were run.
