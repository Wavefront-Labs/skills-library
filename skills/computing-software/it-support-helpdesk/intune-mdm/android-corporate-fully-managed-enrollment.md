---
id: computing-software.it-support-helpdesk.intune-mdm.android-corporate-fully-managed-enrollment
name: android-corporate-fully-managed-enrollment
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, android-fully-managed, android-enterprise, qr-code-enrollment, afw-setup, dpc-identifier, nfc-enrollment, corporate-owned, intune]
level: practitioner
status: docs-checked
description: "Enroll corporate Android phones as fully managed in Intune: enrollment profile and token, QR code, afw#setup and NFC methods, factory reset protection and enrollment pitfalls."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/android-fully-managed-enroll"
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/android-dedicated-devices-fully-managed-enroll"
  - "https://developers.google.com/android/management/provision-device"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# android-corporate-fully-managed-enrollment

Fully managed (COBO) devices are company-owned and tied to a single user; Intune manages the
whole device and can enforce controls a work profile cannot, such as Managed Google Play
only app installs, blocking uninstall of managed apps and preventing factory reset by the user.
Enroll new or factory-reset devices.

## Prerequisites
- Android 10.0 or later, with Google Mobile Services connectivity. No OEM restriction if
  those hold.
- Intune standalone tenant with the MDM authority set to Intune, connected to an Android
  Enterprise (Managed Google Play) account.
- If a Conditional Access policy requires a compliant device and applies to All cloud apps,
  Android and Browsers, exclude the Microsoft Intune cloud app: setup authenticates the user
  in a Chrome tab.

## Enrollment profile and token
Intune admin center > Devices > Enrollment > Android tab > Android Enterprise > Enrollment
Profiles > **Corporate-owned, fully managed user devices** > Create policy.
- Intune generates a default profile named **Default Fully Managed Profile** with a token.
- Token type: **Corporate-owned, fully managed (default)** or **via staging** (for a vendor
  or you to pre-provision; user finishes by signing in to the Intune app). Only the staging
  token has an expiration date (up to 65 years ahead). Enrollment time grouping is not
  supported with the staging token.
- Device name template variables include `{{SERIAL}}`, `{{SERIALLAST4DIGITS}}`,
  `{{DEVICETYPE}}`, `{{ENROLLMENTDATETIME}}`, `{{UPNPREFIX}}`, `{{USERNAME}}` and `{{RAND:x}}`
  (x from 1 to 9). Names may contain letters, numbers and hyphens. Edits affect only new
  enrollments.
- Dynamic groups on `enrollmentProfileName` cannot be used with the default profile. For
  targeting policies and apps only, an assignment filter is the simpler option.
- Select a token to **Replace** (new token as the old one nears expiry), **Revoke** (expires
  it at once; enrolled devices unaffected) or **Export** (JSON for zero-touch or Knox).

## Enrollment methods
| Method | How |
|---|---|
| QR code | After wiping, tap the first screen repeatedly (Google: six taps in the same spot) to launch the QR reader; scan the profile QR. Android 9+ has a reader preinstalled; zoom the browser if scanning fails. Recommended for most scenarios |
| Token / DPC identifier | At the Google sign-in screen enter `afw#setup` (installs Android Device Policy), then scan the QR or type the token. For devices where QR or NFC is not available. The token works for all Intune-licensed users |
| NFC | Specially formatted tag or programmer app. Not supported for corporate-owned work profile (COPE) on Android 11 |
| Zero-touch | Needs a purchase through an authorised zero-touch reseller; link the account in the admin center or configure in the zero-touch portal with Microsoft Intune as the DPC and the token in the DPC extras |
| Knox Mobile Enrollment | Samsung devices on supported Knox versions |

Microsoft Authenticator installs automatically during enrollment and cannot be uninstalled.
Tell users not to restart mid-enrollment: a restarted device can look enrolled but not be
protected by Intune policy.

## Factory reset protection (FRP)
With **Factory reset protection emails** configured:
| Reset route | Fully managed (COBO) |
|---|---|
| Settings > Factory data reset | no FRP |
| Recovery/bootloader reset | FRP applies |
| Intune wipe | no FRP |

For COPE on Android 15, a Settings reset with FRP emails configured needs the Google account
re-entered. Plan reprovisioning around this.

## Verify
Intune shows the device with ownership Corporate, the fully managed enrollment type, a
primary user, and compliance evaluated.

## Checked
Date: 2026-11-08. Read in full: both Intune pages (fully managed setup, updated 2026-05-19; enroll dedicated/fully managed/COPE, updated 2026-10-02) and the Google Android Management provisioning page. Confirmed: Android 10 minimum, default profile name, token types and expiry, naming variables, dynamic group limit, token actions, QR/afw#setup/NFC/zero-touch/token details, FRP table, Authenticator and restart notes. Removed as unconfirmed: "NFC deprecated on Android 8+", network endpoint causes for the stuck setup screen, consumer account blocking, ownership-change reset, the "one token per tenant" claim and the QR failure causes.
Method: documentation only; no commands were run.
