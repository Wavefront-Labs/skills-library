---
id: computing-software.it-support-helpdesk.apple-device-management.enrollment-types-compared
name: enrollment-types-compared
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, user-enrollment, enrollment-types-compared, enrollment-types, supervision]
level: practitioner
status: docs-checked
description: "Choose between Apple's four enrolment methods: account-driven User and Device Enrolment, profile-based Device Enrolment and ADE, with OS minimums and supervision outcome."
sources:
  - "https://support.apple.com/guide/deployment/dep08f54fcf6/web"
  - "https://support.apple.com/guide/deployment/dep23db2037d/web"
  - "https://support.apple.com/guide/deployment/depd1c27dfe6/web"
  - "https://support.apple.com/guide/deployment/dep73069dd57/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# enrollment-types-compared

Goal: pick the right enrolment method for each ownership model.

| Method | Minimum OS | Supervised on enrolment | Enforceable restrictions |
|---|---|---|---|
| Account-driven User Enrolment | iOS 15, iPadOS 15, macOS 14, visionOS 1.1 | No | Curated list |
| Account-driven Device Enrolment | iOS 17, iPadOS 17, macOS 14, visionOS 1.1 | No on iPhone, iPad, Apple Vision Pro; yes on Mac | Unsupervised only |
| Profile-based Device Enrolment | iOS 4, iPadOS 13.1, OS X 10.7, tvOS 9 | No on iPhone, iPad, Apple TV; yes on Mac | Unsupervised only |
| Automated Device Enrolment | iOS 13, iPadOS 13.1, macOS 10.14.4, tvOS 13, watchOS 10, visionOS 2.0 | Yes | All |

- Account-driven User Enrolment is for BYOD: the user owns the device, only a limited set of payloads and restrictions apply, and IT manages only organisation accounts, settings and information, never a personal account. It works with accounts created in Apple School Manager or Apple Business, or federated accounts linked to an IdP such as Google Workspace or Microsoft Entra ID.
- Device Enrolment lets users enrol manually and allows more payloads than User Enrolment, including erasing the device. A Mac on macOS 11 or later is supervised by Device Enrolment. Account-driven: the user signs in with a Managed Apple Account in Settings or System Settings. Profile-based: the user installs an enrolment profile. Removing the enrolment profile removes everything based on it.
- Automated Device Enrolment is for devices the organisation owns, offers all payloads and restrictions, and can stop the user removing the enrolment (see ade-device-assignment).
- Account-driven User and Device Enrolment give the user the most privacy and separation; profile-based Device Enrolment and ADE give IT the most control.
- Not every MDM service offers every method; check the vendor's documentation.

Gotcha: neither flavour of Device Enrolment supervises an iPhone, iPad or Apple Vision Pro (a Mac is supervised); only Automated Device Enrolment does, so supervised-only controls need ADE.

Verify:
- A matrix of ownership model to enrolment method exists in the runbook, with the minimum OS per row.
- Inventory records the enrolment method per device.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Enrolment methods for Apple devices" (method table, privacy table), "User Enrolment and device management", "Device Enrolment and device management" and "Automated Device Enrolment and device management". The privacy table rendered without its tick marks, so no per-ability claims are made beyond the "Enforceable restrictions" row. Removed as unconfirmed: the Apple Configurator USB-to-ABM description, "legacy, user removable", "separate managed volume", "limited commands" detail, procurement-checklist advice and the claim that a method cannot be changed in place. Replaced the welcome-page source with the real pages.
Method: documentation only; no commands were run.
