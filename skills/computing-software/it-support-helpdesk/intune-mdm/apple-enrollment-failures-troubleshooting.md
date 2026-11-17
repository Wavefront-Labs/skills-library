---
id: computing-software.it-support-helpdesk.intune-mdm.apple-enrollment-failures-troubleshooting
name: apple-enrollment-failures-troubleshooting
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, apple-enrollment-troubleshooting, ios-enrollment, profile-installation-failed, ade, apns, company-portal]
level: practitioner
status: docs-checked
description: "Diagnose iOS/iPadOS Intune enrollment failures: APNs and licence errors, device cap, ADE token sync errors, Invalid Profile, ADE not starting, MFA stuck at login."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/mem/intune/device-enrollment/troubleshoot-ios-enrollment-errors"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apple-enrollment-failures-troubleshooting

Start with the tenant-wide causes, since they break every device: an APNs certificate that is
missing or expired, an expired ADE token, and users without a valid Intune licence.

## Errors users see
| Error | Cause and fix |
|---|---|
| `NoEnrollmentPolicy` | APNs certificate missing, invalid or expired, or iOS/iPadOS not enabled as a platform. Check setup and renew the push certificate |
| `APNSCertificateNotValid` | APNs steps not done or certificate expired. **Renew** it, do not replace it: replacing forces every iOS/iPadOS device to re-enroll. Then re-enroll the device |
| `AccountNotOnboarded` | Same APNs causes; review creating the APNs certificate |
| `DeviceCapReached` | User must remove a currently enrolled device in Company Portal before enrolling another |
| `DeviceTypeNotSupported` | Not an iOS device, or older than iOS/iPadOS 8.0 |
| `UserLicenseTypeInvalid` | User not in a required group or wrong licence type for the MDM authority |
| `MdmAuthorityNotDefined` | MDM authority not set in Intune |
| Company Portal Temporarily Unavailable / Workplace Join failed | Company Portal out of date or corrupted: remove, reinstall from the App Store, re-enroll |
| "User Name Not Recognized" | No valid Intune licence: Microsoft 365 admin center > Users > Active users > Product licenses, then re-enroll |

## ADE token sync errors (Apple Business or School Manager)
| Error | Fix |
|---|---|
| Expired or invalid token | Renew the token; if that fails, contact Intune support, which may need a new public key uploaded under Preferences > MDM Server Settings in Apple |
| Access denied | Intune removed from the MDM server list, or token expired: check both |
| Terms and conditions not accepted | An Apple Administrator must accept the new terms in the Apple portal |
| Invalid support phone number, profile name or department | Edit the field in the enrollment profile |
| Invalid, expired or required cursor; internal server error | Contact Intune support, who can retry the sync |
| Apple profile not found | Create a new profile and assign it |

If uploading the token fails with "An error occurred while uploading the Enrollment Program
token", call Graph `GET https://graph.microsoft.com/beta/deviceManagement/depOnboardingSettings`
for the token GUID, then `.../depOnboardingSettings/<TokenGuid>/getEncryptionPublicKey`. Save the
value as a three-line `.pem` (BEGIN CERTIFICATE, the base64 on one line, END CERTIFICATE),
upload it to the MDM server in Apple (Edit > MDM Server Settings), download the new token and
refresh it in Intune.

## Other ADE problems
- **Invalid Profile / configuration couldn't be downloaded**: a device type restriction blocks
  iOS/iPadOS. Enrollment restrictions > Device type restrictions > All Users > Platform
  settings > Allow iOS/iPadOS.
- **ADE enrollment doesn't start**: the profile was created before the token was uploaded. Edit
  the profile (any change updates its modification time), then Enrollment program tokens >
  the token > Sync now.
- **Stuck at user login**: MFA does not work during ADE enrollment with Setup Assistant (legacy).
  Disable MFA or move to Setup Assistant with modern authentication.
- **User affinity ADE fails**: the WS-Trust 1.3 Username/Mixed endpoint must be enabled in the
  federation provider. For AD FS check with `Get-AdfsEndpoint -AddressPath
  "/adfs/services/trust/13/UsernameMixed"`.
- **`XPC_TYPE_ERROR Connection invalid`** in the device log: connection problem to the Apple ADE
  service. Fix the network or try another; contact Apple if it persists.
- **Government cloud users** signing in from another device are redirected to the public cloud.
  On the iOS device set Settings > Company Portal > Cloud to Government.

## Checked
Date: 2026-11-08. Read in full: Intune "Troubleshooting iOS/iPadOS device enrollment errors" (updated 2026-03-30). The Intune ADE policy page and Apple deployment intro were dropped as sources because nothing here depends on them. Removed as unconfirmed: network ports and endpoints, device-limit default and maximum, "Awaiting final configuration" advice, all macOS commands and the Mac Setup Assistant error, log collection steps, and the `profiles renew` and wipe-to-receive-profile gotchas.
Method: documentation only; no commands were run.
