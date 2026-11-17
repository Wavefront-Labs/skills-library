---
id: computing-software.it-support-helpdesk.intune-mdm.ade-token-and-enrollment-profiles
name: ade-token-and-enrollment-profiles
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, ade-token, automated-device-enrollment, apple-business-manager, enrollment-program-token, setup-assistant, await-configuration, apple-enrollment, intune, supervised-mode-capabilities, macos-ade-intune]
level: practitioner
status: docs-checked
description: "Create and assign Intune ADE enrollment policies for iOS/iPadOS and macOS: user affinity, authentication, supervision, locked enrollment, await final configuration."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/device-enrollment-program-enroll-ios"
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/device-enrollment-program-enroll-macos"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ade-token-and-enrollment-profiles

Automated Device Enrollment (ADE) enrolls new or wiped devices bought through Apple Business or Apple School Manager. Prerequisites: portal access, an active Apple token (`.p7m`), and an Apple MDM push certificate in Intune. Token creation, renewal and device sync are on Microsoft's "Set up an ADE token" and "Manage ADE devices" pages, which this skill does not cover. Wipe devices before enrollment.

## Create a policy
Intune admin center > Devices > Device onboarding > Enrollment > Apple mobile tab (iOS/iPadOS) or macOS tab > Enrollment program tokens > the token > Enrollment policies > Create policy. This replaces the older Profiles experience, which gets no new features. Limit: 1,000 enrollment policies per token. Name the policy clearly: the name can drive a dynamic Entra group with property `enrollmentProfileName`. An optional static Entra security group on the Device group tab provides enrollment time grouping (needs the enrollment time device membership assignment permission).

## Key settings
| Setting | Behaviour (per Learn) |
|---|---|
| User affinity | With user affinity: for user devices needing Company Portal. Without: kiosk, POS, shared devices (no Company Portal on macOS). iOS also has Microsoft Entra ID shared mode |
| Authentication (with affinity) | Setup Assistant with modern authentication (recommended; with just-in-time registration on iOS). Company Portal is the other iOS option. Setup Assistant (legacy) ended with the October 2026 (2610) service release and existing profiles migrate automatically |
| Supervised (iOS) | Yes gives more management options and disables Activation Lock by default; unsupervised devices need Apple Configurator to become supervised |
| Locked enrollment | Hides the control that removes the management profile. Devices added to ADE later (not bought through Apple Business) show the remove button for the first 30 days. On macOS it can't be changed without a wipe |
| Await final configuration | Yes locks the end of Setup Assistant while device configuration policies (not apps) install. Default Yes for new policies, No for existing. No fixed time limit; Microsoft saw most devices released within 15 minutes. Unavailable for iOS userless plus Shared iPad. On macOS, local account settings force it on |
| Device name template (iOS) | Up to 63 characters, e.g. `{{DEVICETYPE}}-{{SERIAL}}`; the only setting that changes without a factory reset |
| Setup Assistant panes | Hide or Show each; Department name and phone appear under About Configuration and Need Help |
| macOS local accounts | Local admin via LAPS (15-character random password, rotated every six months by default) and optional primary account prefill; needs user affinity, modern authentication and Await final configuration Yes |

Changing an existing policy applies to devices only after they are reset and reactivated (except the name template). Deploy the Company Portal for iOS as a required, device-licensed VPP app via Intune, not the App Store version.

## Assign
- Token > Devices > select devices > Assign policy; or token > Set Default Policy so every device syncing from the token gets one. A synced device with no policy fails enrollment when turned on.
- Enrollment restrictions: if the default All Users device type restriction blocks iOS/iPadOS, ADE shows Invalid Profile. Block only personally owned devices instead.
- iOS 14.5 and later: hide the Passcode and Touch ID/Face ID Setup Assistant screens (they don't work) and enforce passcodes through a configuration or compliance policy.
- If using platform SSO with macOS ADE, do not target the PSSO registration profile to userless devices.

## Gotchas
- A device assigned to a different MDM server in Apple Business never appears in this token (check the device record in Apple Business).
- An expired token or too few Company Portal VPP licences blocks enrollment.

## Verify
During Setup Assistant on a test device the Remote Management screen names your organisation, the device enrolls as intended (supervised for iOS), and Intune shows the assigned policy.

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the Intune pages device-enrollment-program-enroll-ios and -macos (read in full). Removed because the cited pages do not state them: ABM menu paths for MDM servers and Default device assignment, key-renewal steps and "tokens expire after one year", the 12-hour sync cadence and 15-minute Sync limit, Apple Configurator provisional-period details beyond the 30 days Intune states, and "supervised always required" (it is a choice). The Apple Business page cited earlier is a stub and was dropped as a source.
