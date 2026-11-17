---
id: computing-software.cybersecurity-defensive.endpoint-security.windows-autopilot
name: windows-autopilot
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [autopilot, windows-autopilot, intune-enrollment, device-preparation, zero-touch, mobile-device-management, enrollment-restrictions]
level: practitioner
status: docs-checked
description: "Windows Autopilot and Autopilot device preparation: what each requires, enrollment time grouping, corporate identifiers, and the limits of Intune enrollment restrictions."
sources: ["https://learn.microsoft.com/en-us/autopilot/overview", "https://learn.microsoft.com/en-us/autopilot/device-preparation/overview", "https://learn.microsoft.com/en-us/mem/intune/enrollment/enrollment-restrictions-set"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Autopilot enrolment

## Windows Autopilot (classic)
- Uses the OEM-optimized Windows already on the device instead of re-imaging, then applies settings and policies, installs apps and can change the Windows edition.
- Can join devices to Microsoft Entra ID or to Active Directory via Microsoft Entra hybrid join, auto-enroll them into MDM such as Intune (configuration requires Entra ID P1 or P2), assign them to configuration groups by profile, and customize OOBE.
- Autopilot Reset prepares an existing device for a new user and helps in break/fix cases.

## Autopilot device preparation
- Requires Windows 11 (24H2 or later; 23H2 or 22H2 with KB5035942 or later) and Microsoft Entra ID; only Entra join is supported.
- If a device is also registered as a classic Autopilot device: unassociated, the classic profile takes precedence; associated, device preparation runs. To use device preparation on a registered device without associating it, deregister it first.
- Enrollment time grouping: when the user authenticates, the device is added to the device security group named in the profile and receives the assigned apps, PowerShell scripts and policies. Only apps and scripts selected in the profile deploy during OOBE; policies are synced but not tracked as applied during deployment.
- By default users are standard non-administrator users.
- Corporate identifiers (serial number, manufacturer, model uploaded in Intune) ensure only trusted devices go through device preparation. They are required only if you use enrollment restrictions to block personal Windows enrolments.
- Device association binds a physical Windows 11 device to the tenant before enrollment and marks it corporate-owned.

## Enrollment restrictions (Intune)
- Types: device platform restrictions (platform, version, manufacturer, ownership) and device limit restrictions (1 to 15 devices per user).
- Microsoft states enrollment restrictions are not security features: compromised devices can misrepresent their character; they are a best-effort barrier for non-malicious users.
- Platform restriction changes depend on Entra-to-Intune group and filter updates that typically take up to 15 minutes.

## Verify
- [ ] A test device reaches the desktop with the intended apps and scripts from the profile.
- [ ] Personal Windows device enrolment is blocked in a test, with corporate identifiers in place for expected devices.

## Checked
2026-11-01. Confirmed against Microsoft Learn: Windows Autopilot overview, Autopilot device preparation overview, and Intune enrollment restrictions. Removed (not stated on these pages): `Get-WindowsAutopilotInfo`, group tags, deployment-mode details and TPM attestation, ESP blocking-app advice and the `mdmdiagnosticstool` command, deregistering resold devices, the Entra join permission and Conditional Access advice. The enrollment-status page fetched with almost no content.
Method: documentation only; no commands were run.
