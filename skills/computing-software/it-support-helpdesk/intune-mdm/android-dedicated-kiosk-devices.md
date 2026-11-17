---
id: computing-software.it-support-helpdesk.intune-mdm.android-dedicated-kiosk-devices
name: android-dedicated-kiosk-devices
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, android-dedicated-device, kiosk-mode, cosu, managed-home-screen, shared-device-mode, android-enterprise, intune]
level: practitioner
status: docs-checked
description: "Set up Android dedicated (kiosk) devices in Intune: enrollment profile and token, dynamic group, single and multi-app kiosk with Managed Home Screen, shared mode, exit-kiosk."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/android-kiosk-enroll"
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/device-restrictions-android-for-work"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-configuration-managed-home-screen-app"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# android-dedicated-kiosk-devices

Dedicated devices are corporate-owned, single-purpose Android Enterprise devices
(digital signage, ticket printing, inventory). They enrol without a user account and
are not associated with a user.

## Requirements
Android 8.0 or later, Google Mobile Services connectivity, Android Enterprise support,
MDM authority set to Intune, and the tenant connected to Managed Google Play.

## Enrollment
1. Intune admin center > Devices > Device onboarding > Enrollment > **Android** tab >
   Enrollment Profiles > **Corporate-owned dedicated devices** > Create profile. Token type:
   - *Corporate-owned dedicated device* (default): no user credentials at any point.
   - *Corporate-owned dedicated device with Microsoft Entra ID shared mode*: also
     deploys Microsoft Authenticator in Entra shared device mode (single sign-in and
     sign-out across integrated apps); Company Portal is installed as well.
2. Set the token expiration date (up to 65 years in the future). Expired profiles
   disappear from the list; use Filter and tick Inactive to see them.
3. Optionally pick a static Entra device group (not a user group) at enrollment time,
   or create a dynamic device group: Group type Security, Membership type Dynamic
   Device, rule property `enrollmentProfileName`, operator Equals, value = the profile
   name.
4. Get the token: select the profile > Token. It is a 20-digit string and a QR code.
   Token actions: Replace, Revoke (expires immediately), Export (JSON for Google Zero
   Touch or Knox Mobile Enrollment). None of these affect already enrolled devices.

The Microsoft Intune app installs automatically during enrollment and cannot be
uninstalled. Only apps assigned as **Required** install on dedicated devices; to remove
an app, delete the required deployment or add an uninstall deployment.

## Kiosk configuration (Device restrictions profile > Device experience)
Device experience type > Kiosk mode (dedicated and fully managed).

| Mode | Setup |
|---|---|
| Single app | The one app must be added in Intune and assigned to the dedicated device group; the device starts only that app |
| Multi-app | Managed Home Screen (MHS) from Google Play must be added and assigned; every package you want launchable must also be added and assigned. Apps added to the profile appear as icons on MHS |

Managed Home Screen app configuration keys (MHS page) include: Show Wi-Fi setting,
Show Bluetooth setting (both default FALSE), Enable screen saver, Exit lock task mode
password (4-6 digits, set through a device configuration profile), Enable auto sign out
(default FALSE; with Entra shared device mode it signs the user out of all participating
apps) and Auto sign out time (default 300 seconds). Auto sign-out needs the Overlay
permission, so it does not work properly if Notification windows is set to Disable in
device restrictions.

Kiosk mode removes the status bar, navigation buttons and lock screen by default. To
allow a dialer or push notifications, use Enabled system navigation features and System
notifications and information (Android 9.0 and newer). Kiosk mode does not stop the kiosk
app launching other installed apps, including Settings, so uninstall unneeded apps.

## Support
- Locked out / "Contact your IT admin. This phone will be erased." in multi-app mode:
  every app in the policy must be Required and assigned to the device.
- Leaving kiosk mode (Leave kiosk mode enabled, 4-6 digit code): keep pressing the back
  button until the Exit kiosk button shows, select it, enter the code, then select
  Managed Home Screen to relock.
- Revoked or replaced tokens do not affect enrolled devices; new enrollments use the new token.

## Updates
System update options on the Device restrictions profile: Device Default, Automatic,
Postponed (30 days) and Maintenance window (daily window; the page recommends it for
kiosks because single-app foreground apps can then be updated). Freeze periods can block
updates.

## Verify
A newly enrolled device appears in the dynamic group, starts the kiosk layout, and only
the allowed apps launch.

## Checked
Date: 2026-11-07. Read in full: the Intune dedicated device enrollment article. Read
sections of the Android device restrictions article (System update, kiosk Device
experience, Leave kiosk mode) and searched the Managed Home Screen article for exit,
Wi-Fi, Bluetooth, screen saver and sign-out keys (the MHS article is 63k characters and
the restrictions article 105k, so they were not read end to end).
Corrections: token expiry was "max 90 days" (page: up to 65 years); dynamic rule now
uses the documented property/operator form. Removed unconfirmed claims: `afw#setup`
enrollment string, "MHS waits for a missing app" loop, MHS exit via back button in the
top corner, Conditional Access limitation, system apps blocked by package name allow
list, remote lock/wipe advice, and "show tiles so staff can reconnect" wording.
Method: documentation only; no commands were run.
