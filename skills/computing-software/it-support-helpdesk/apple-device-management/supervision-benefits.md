---
id: computing-software.it-support-helpdesk.apple-device-management.supervision-benefits
name: supervision-benefits
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, supervised-ios, supervision-benefits, supervision, supervised-mode]
level: practitioner
status: docs-checked
description: "Explain what supervision unlocks on Apple devices and how a device becomes supervised through Automated Device Enrolment or Apple Configurator."
sources:
  - "https://support.apple.com/guide/deployment/about-device-supervision-dep1d89f0bff/web"
  - "https://support.apple.com/guide/deployment/automated-device-enrollment-management-dep73069dd57/web"
  - "https://support.apple.com/guide/deployment/restrictions-for-supervised-devices-dep6b5ae23e9/web"
  - "https://support.apple.com/guide/deployment/lock-and-locate-devices-depb980a0be4/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# supervision-benefits

Goal: use supervision for organisation-owned devices.
- Automated Device Enrolment supervises devices automatically: iPhone on iOS 13 or later, iPad on iPadOS 13.1 or later, Mac on macOS 10.14.4 or later, Apple TV on tvOS 13 or later, plus Apple Vision Pro and Apple Watch. A Mac on macOS 11 or later is supervised when enrolled by any automated, device or account-driven enrolment.
- Manual supervision with Apple Configurator erases the device.
- What it unlocks: the "Device management restrictions for supervised Apple devices" page lists the restrictions that need supervision, for example App Lock, restricting app usage, installing apps, removing apps and adding VPN configurations. Check that page for each restriction before relying on it.
- Managed Lost Mode is for supervised iPhone and iPad.
- Visible to the user: Settings shows "This [iPhone] [iPad] is supervised. [Organisation] can monitor your internet traffic and locate this device", below the Search field.
- The Automated Device Enrolment option "Prevent unenrollment" stops a user removing management from a supervised device.
Practice: supervise organisation-owned devices from day one through Automated Device Enrolment, because supervising later through Configurator means an erase; keep user-owned devices on User Enrolment, unsupervised.
Gotcha: supervising an existing device erases it, so schedule it with user data backed up.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
- Read in full: Apple Platform Deployment "About device supervision", "Device management restrictions for supervised Apple devices" and "Lock and locate Apple devices"; the "Prevent unenrollment" row of "Automated Device Enrolment and device management" (the rest of that page was searched, not read in full).
- Removed as unconfirmed: "content filter" as a supervised-only feature (the web content filter payload does not require supervision on iOS 16 or later), "silent app install", "Single App Mode" named as a restriction (App Lock is listed), the "Settings > General > About" check and the inventory Verify steps.
- The original sources were not real pages (they served the guide's welcome page) and were replaced.
