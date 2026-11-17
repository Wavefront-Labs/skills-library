---
id: computing-software.it-support-helpdesk.apple-device-management.ade-device-assignment
name: ade-device-assignment
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, ade-enrollment, ade-device-assignment, ade, dep, prestage]
level: practitioner
status: docs-checked
description: "Automated Device Enrolment options an MDM service can set: prevent unenrolment, hold in Setup Assistant, Auto Advance, minimum OS and enforced FileVault, with OS minimums."
sources:
  - "https://support.apple.com/guide/deployment/dep73069dd57/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ade-device-assignment

Goal: organisation-owned devices enrol automatically at first start-up with the right options.

The MDM service sets these Automated Device Enrolment options (OS minimums from Apple's table):
- Prevent unenrollment: iOS 7, iPadOS 7, macOS 10.9, tvOS 10.2, visionOS 2. A supervised device cannot be unenrolled by the user, including from System Settings or the `profiles` tool on a Mac.
- Automatically advance through Setup Assistant (Auto Advance): macOS 11, tvOS 11.3, visionOS 2, with Language and Region options.
- Hold device in Setup Assistant: iOS 9, iPadOS 9, macOS 10.9, tvOS 10.2, visionOS 2, so the MDM service can apply critical configuration or apps first.
- Configuration web URL: iOS 13, iPadOS 13, macOS 10.15, visionOS 2. A URL the device loads in Setup Assistant for authentication, branding or consent text.
- Setup Assistant panes to skip: iOS 7, iPadOS 7, macOS 10.9, tvOS 10.2, visionOS 2.
- Enforce FileVault: macOS 14. Turns on FileVault in Setup Assistant; use together with holding the device in Setup Assistant so the service has what it needs.
- Shared iPad: Configure as Shared iPad and Number of Shared iPad users, iPadOS 9.3.
- Minimum OS version: the device guides the user through a software update before continuing Setup Assistant if it is below the version the service expects.

Auto Advance on a Mac needs macOS 11 or later, the serial number in Apple School Manager or Apple Business, the service applying the ADE settings including the Auto Advance key, an active Ethernet connection (initial configuration only), and access to the MDM service; power is recommended but not required. The user then enters a known username and password at the login window.

Enforced enrolment: a Mac with macOS 14 or later registered in Apple School Manager or Apple Business that does not enrol at first set-up shows a full-screen experience; "Not now" dismisses it once for eight hours, after which a user with the proper permissions in Apple School Manager or Apple Business needs to enrol it.

Highly Restricted Networks mode (iOS 17 or iPadOS 17 and later) must be approved by Apple in Apple Business, then an Organisation Administrator turns it on per device; it activates when the device goes through ADE.

Gotcha: Prevent unenrollment only protects a supervised device; Auto Advance only skips every pane when no other Setup Assistant panes are enabled.

Verify:
- The device is listed in Apple School Manager or Apple Business and assigned to the MDM service.
- A freshly erased device reaches the Remote Management step and ends up supervised.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Automated Device Enrolment and device management" (options table, Auto Advance, minimum version, enforced enrolment, Highly Restricted Networks). Removed as unconfirmed: all Jamf Pro prestage menu paths and options, the SSO/OIDC/SAML note, the reseller delay claim, "move between prestages" behaviour, the "require authentication" wording and the learn.jamf.com source (page stub). Verify steps were rewritten.
Method: documentation only; no commands were run.
