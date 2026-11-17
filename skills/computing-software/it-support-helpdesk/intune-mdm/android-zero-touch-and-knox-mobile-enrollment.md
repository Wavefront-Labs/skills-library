---
id: computing-software.it-support-helpdesk.intune-mdm.android-zero-touch-and-knox-mobile-enrollment
name: android-zero-touch-and-knox-mobile-enrollment
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, android-zero-touch-enrollment, zero-touch, knox-mobile-enrollment, kme, samsung-knox, reseller, dpc-extras, intune]
level: practitioner
status: docs-checked
description: "Use Android zero-touch enrollment with Intune: reseller registration, linking the account or portal config with DPC extras JSON, CSV assignment, KME precedence and failures."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/android-dedicated-devices-fully-managed-enroll"
  - "https://support.google.com/work/android/answer/7514005"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# android-zero-touch-and-knox-mobile-enrollment

Zero-touch makes a corporate Android device provision itself on first boot, or the next factory
reset, once it is registered and has a configuration. Samsung Knox Mobile Enrollment (KME) is
a separate Samsung service with the same purpose; Intune's page only says Samsung devices must
run supported Knox versions.

## Prerequisites (Google)
- Device bought from an authorised zero-touch reseller (not a consumer store), Android 9 or
  later (Pixel on 7.0 and Android 8 compatible devices also qualify), GMS compatible with
  Google Play services always enabled.
- A zero-touch account created by the reseller from a Google Account tied to your corporate
  email, not a personal Gmail. Enable 2-Step Verification on it.
- An EMM supporting company-owned devices.

## Option A: link the account in Intune (fully managed default)
1. Add the **update app sync** permission to the role (Tenant administration > Roles >
   Properties > Permissions > Android Enterprise) and enable corporate-owned, fully managed
   enrollment.
2. Devices > By platform > Android > Device onboarding > Enrollment > Bulk enrollment methods >
   **Zero-touch enrollment**. Sign in with the Google account given to the reseller, choose the
   account, **Link**, and add support information.
3. Intune creates a default configuration for fully managed devices and applies it to zero-touch
   devices without one. It overrides the portal's default configuration. For corporate-owned
   work profile or dedicated devices, do not link; use the portal instead.

## Option B: configure in the zero-touch portal
Configurations > Add Configuration: choose **Microsoft Intune** as the EMM DPC and paste this
into DPC extras, replacing the token (keep the double quotes):
```json
{
"android.app.extra.PROVISIONING_DEVICE_ADMIN_COMPONENT_NAME": "com.google.android.apps.work.clouddpc/.receivers.CloudDeviceAdminReceiver",
"android.app.extra.PROVISIONING_DEVICE_ADMIN_SIGNATURE_CHECKSUM": "I5YvS0O5hXY46mb01BlRjq4oJJGs2kuUcHvVkAPEXlg",
"android.app.extra.PROVISIONING_DEVICE_ADMIN_PACKAGE_DOWNLOAD_LOCATION": "https://play.google.com/managed/downloadManagingApp?identifier=setup",
"android.app.extra.PROVISIONING_ADMIN_EXTRAS_BUNDLE": {
    "com.google.android.apps.work.clouddpc.EXTRA_ENROLLMENT_TOKEN": "YourEnrollmentToken"
}
}
```
Add company name, support email, phone and an optional message (shown before provisioning).
Set a default configuration for future devices, or apply per device (Devices > Edit, by IMEI
or serial) or in bulk by CSV (limit 50 MB; `profileid` of 0 removes the configuration).
Roles: only Owner, Admin and Manager can create configurations.

The token comes from a fully managed, dedicated or work profile enrollment profile; Intune's
token page lets you export its JSON for zero-touch.

## Failures
- Device does not provision: not registered (check IMEI in the portal, else ask the reseller),
  configuration shows **No config**, or no data connection to Google servers (roaming data is
  blocked by default). After fixing registration or configuration, factory reset.
- If a configured device skips zero-touch, it resets itself after the first Google connection,
  with a warning an hour before.
- Registered in both zero-touch and KME: the device enrolls with KME. Remove the KME
  configuration for the device to use zero-touch.
- Dual-SIM: reseller should register the numerically lowest IMEI.
- Transfer or resale: deregister (Remove) in the portal; re-registering needs the reseller.
- Do not restart mid-enrollment (Intune warns the device may not register).

## Checked
Date: 2026-11-08. Read in full: Intune "Enroll your Android Enterprise dedicated, fully managed, or corporate-owned with work profile devices" (updated 2026-10-02) and Google "Zero-touch enrollment for IT admins". The Samsung Knox Mobile Enrollment page returned no content, so KME setup steps were removed (the Knox Admin Portal and Deployment App details are unconfirmed). Also removed: the portal URL, "Android Device Policy" as the DPC name and the shortened extras JSON, and the data-only SIM and token-secrecy notes.
Method: documentation only; no commands were run.
