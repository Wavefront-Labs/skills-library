---
id: computing-software.it-support-helpdesk.apple-device-management.user-enrollment-managed-boundary
name: user-enrollment-managed-boundary
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, user-enrollment, user-enrollment-managed-boundary, byod, privacy]
level: practitioner
status: docs-checked
description: "What account-driven User Enrolment separates and removes on a BYOD device: enrolment discovery, per-app data separation, backup and app rules."
sources:
  - "https://support.apple.com/guide/deployment/dep23db2037d/web"
  - "https://support.apple.com/guide/deployment/dep4d9e9cd26/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/device.erase.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/device.lostmode.enable.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# user-enrollment-managed-boundary

Goal: set expectations with BYOD owners and configure without overreach.

- Account-driven User Enrolment (iOS 15, iPadOS 15, macOS 14, visionOS 1.1 or later) applies only a limited set of payloads and restrictions, and IT can manage only the organisation's accounts, settings and information, never a personal account. A personal and a Managed Apple Account can both be signed in, with work and personal data separated.
- After enrolment the OS creates separate encryption keys on the device; if the user or the MDM service unenrols the device, the OS destroys them. Data cryptographically separated: managed app data containers (iOS 15, iPadOS 15, macOS 14, visionOS 1.1), Calendar (iOS 16, iPadOS 16.1, macOS 13), keychain items (the third-party Mac app must use the Data Protection Keychain API), Mail attachments and body, Notes, and Reminders (iOS 17, iPadOS 17, macOS 14).
- Unenrolment: all configurations and settings go with the enrolment profile, and managed apps are always removed. Apps installed before enrolment cannot be converted to managed apps. Restoring from a backup does not restore the enrolment. A user signed in with a personal Apple Account cannot accept a managed app invitation.
- Not available: `EraseDevice` and `EnableLostMode` are forbidden for User Enrolment, and attestation omits serial number and UDID to protect privacy.
- Enrolment steps: the user opens Settings > General > VPN & Device Management (System Settings > General > Device Management on Mac) and taps Sign In to Work or School Account. The device finds the service by requesting `https://<domain>/.well-known/com.apple.remotemanagement` with query parameters `user-identifier` and `model-family`, following HTTP 3xx redirects. The server returns JSON with `Servers`, each having `Version` (`mdm-byod` for User Enrolment, `mdm-adde` for account-driven Device Enrolment) and `BaseURL`, with `Content-Type: application/json`. The device then POSTs to `BaseURL`, authenticates for an access token, and the user signs in with the Managed Apple Account to finish.
- The access token is sent in the Authorisation header on later requests and can expire, prompting the user to reauthenticate; Enrolment SSO on iPhone, iPad and Apple Vision Pro reduces prompts.

Gotcha: do not promise users a remote wipe or location lookup; the service can only unenrol and remove its managed data.

Verify:
- The profile list on the device shows only the user-enrolment profile and its managed payloads.
- After unenrolment, work apps and data are gone and personal apps and data remain.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "User Enrolment and device management" and "Account-driven enrolment methods with Apple devices" (process stages, well-known discovery, JSON keys, data separation table, app and backup rules), plus the apple/device-management `device.erase.yaml` and `device.lostmode.enable.yaml` (User Enrolment forbidden). Removed as unconfirmed: "separate APFS volume", "cannot read personal apps / get full IMEI / locate", the open-in restriction advice and the welcome-page source. Not confirmed on any page read: whether DeviceInformation hides hardware identifiers in general (only the attestation note is confirmed).
Method: documentation only; no commands were run.
