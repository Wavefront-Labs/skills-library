---
id: computing-software.it-support-helpdesk.intune-mdm.intune-enrollment-error-codes
name: intune-enrollment-error-codes
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, enrollment-error-codes, enrollment-failures, 80180014, 8018000a, 0x8007064c, enrollment-restrictions, intune]
level: practitioner
status: docs-checked
description: "Decode documented Intune enrollment errors on Windows, iOS/iPadOS and Android: cause and fix for already-enrolled, licence, restriction, UPN, APNs and ADE token errors."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/mem/intune/device-enrollment/troubleshoot-windows-enrollment-errors
  - https://learn.microsoft.com/en-us/troubleshoot/mem/intune/device-enrollment/troubleshoot-ios-enrollment-errors
  - https://learn.microsoft.com/en-us/troubleshoot/mem/intune/device-enrollment/troubleshoot-android-enrollment
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# intune-enrollment-error-codes

## First look
- Windows device: Event Viewer > Applications and Services Logs > Microsoft > Windows > DeviceManagement-Enterprise-Diagnostics-Provider > Admin.
- Auto-enrollment by Group Policy: Task Scheduler > Microsoft > Windows > EnterpriseMgmt, last run result of the enrollment task.

## Windows
| Code or message | Cause (per Microsoft) | Fix |
|---|---|---|
| `0x8007064c` "The machine is already enrolled" | Previously enrolled, cloned image of an enrolled PC, or old account certificate still present | Delete the Intune cert issued by Sc_Online_Issuing from Local computer > Personal > Certificates; delete `HKLM\SOFTWARE\Microsoft\OnlineManagement` and sub keys; re-enroll. Back up the registry first |
| `8018000a` "The device is already enrolled" | A different user already enrolled or joined the device | Settings > Accounts > Work Access shows the other connection; sign in as that user, remove it, then enroll |
| "This account is not allowed on this phone" | User has no valid Intune licence | Assign a licence, then enroll |
| "MDM Terms of Use endpoint is not correctly configured" | No valid Intune or Office 365 licence when both MDM for Microsoft 365 and Intune are used, or blank terms URL in Entra | Assign a licence, or in Entra > Mobility (MDM and MAM) > Microsoft Intune use Restore default MDM URLs |
| `80180026` | MDM automatic enrollment is on and the Intune PC agent is installed | Set MDM user scope to None, or uninstall the Intune PC client |
| `0x80cf4017` | Client software out of date | Download the current client software from the Intune admin site |
| `0x80180014` "Your organization does not support this version of Windows" | Windows MDM enrollment disabled in the tenant | Devices > Enrollment restrictions > the device type restriction > Properties > Platform settings > Allow for Windows (MDM) |
| "A setup failure has occurred during bulk enrollment" | Accounts in the provisioning package are not allowed to join devices to Entra | Entra > Devices > Device Settings: Users may join devices set to All or Selected (add the package accounts) |
| `0x8018002b` (Event 76 "Auto MDM Enroll: Failed") | UPN has an unverified or non-routable domain such as .local, or MDM user scope is None | Set a valid UPN suffix and delta sync, or set MDM user scope to All or Some |
| `0x80180022` (Autopilot) | Device runs Windows Home | Move to Pro or higher |
| `0x801C03EA` (Autopilot) | TPM 2.0 chip not yet upgraded to 2.0; or device in two groups with different Autopilot profiles | Upgrade the TPM; remove the extra profile assignment |
| `0x800705b4` (Autopilot self-deploying) | No physical TPM 2.0 (virtual TPM or TPM 1.2 fail), or Windows older than build 1709 (1809 for hybrid join) | Use a device that meets both |
| `80070774` (hybrid Autopilot) | Assign user feature used in a hybrid join profile, or the Autopilot object's Entra device was deleted | Unassign the user; if it persists check ODJ Connector Event ID 30132 (OU delegation); delete and reimport the Autopilot object if its Entra device was deleted |
| OOBEIDPS | Proxy or firewall blocks the identity provider | Allow Autopilot network requirements |

## iOS and iPadOS
| Message | Meaning and fix (per Microsoft) |
|---|---|
| NoEnrollmentPolicy | APNs certificate missing, invalid or expired; check iOS/iPadOS is enabled as a platform |
| DeviceCapReached | Too many devices enrolled; the user removes one in the Company Portal |
| Company Portal Temporarily Unavailable / Workplace Join failed | Company Portal out of date or corrupted; remove, validate credentials, reinstall |
| APNSCertificateNotValid / AccountNotOnboarded | APNs certificate steps incomplete or certificate expired. Renew it; do not replace it, or all iOS/iPadOS devices must re-enroll |
| DeviceTypeNotSupported | Non-iOS device, or iOS/iPadOS below 8.0 |
| UserLicenseTypeInvalid | Wrong licence type for the MDM authority, or user not in a required group |
| MdmAuthorityNotDefined | MDM authority not set in Intune |
| User Name Not Recognized | No valid Intune licence for the user |
| "configuration ... couldn't be downloaded: Invalid Profile" | Device type restriction blocks it; Enrollment restrictions > Platform settings > Allow for iOS/iPadOS |
| `XPC_TYPE_ERROR Connection invalid` (ADE) | Connection issue between the device and the Apple ADE service; change network, contact Apple if persistent |
| ADE enrollment does not start | Profile created before the ADE token was uploaded; edit the profile, then Sync now on the token |
| ADE stuck at user login | MFA with Setup Assistant (legacy); disable MFA or use Setup Assistant with modern authentication |

ADE token sync errors on the same page (expired or invalid token, access denied, terms not accepted, invalid cursor) are listed with causes; terms must be accepted by an Administrator role user in Apple Business Manager or Apple School Manager.

## Android
| Symptom | Microsoft's guidance |
|---|---|
| Can't create a work profile | Existing work profile (Settings > Passwords & accounts > Work) or OEM restriction; test with the Test DPC app and ask the manufacturer |
| Encryption required at enrollment | Expected; Google requires an encrypted device for a work profile |
| Wipe missing on a work profile device | Expected; only Retire (removes the work profile) is available. Wipe is supported for corporate-owned with work profile |
| Managed Google Play last sync not updated | Expected; trigger a sync manually |

## Method
1. Reproduce once and capture the exact code and time.
2. Match the code to the tables above and the log in First look.
3. Fix the cause (licence, restriction, record) rather than repeating attempts.

## Checked
Date: 2026-11-08. Read in full: Microsoft Learn "Troubleshooting Windows device enrollment errors in Intune", "Troubleshooting iOS/iPadOS device enrollment errors in Microsoft Intune" and "Troubleshooting Android Enterprise device enrollment in Intune" (all updated 2026-03-30). Corrections: 80180014 is the tenant platform restriction message, not a deleted Autopilot device; 80180026 is the Intune PC agent conflict only; 8018002b also covers MDM scope None. Removed as unconfirmed: codes 80180018, 80180003, 801c0003, 80180005, the device limit default of 5, the Intune Enrollment failures report path, iOS "Device already enrolled" and ADE Apple Business Manager assignment advice, and the Android "Company Portal temporarily unavailable", "device type not supported" and fully managed QR token rows.
Method: documentation only; no commands were run.
