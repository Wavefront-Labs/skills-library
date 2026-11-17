---
id: computing-software.it-support-helpdesk.apple-device-management.setup-assistant-panes
name: setup-assistant-panes
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, ade-enrollment, setup-assistant-panes, setup-assistant, skip-keys]
level: practitioner
status: docs-checked
description: "Choose Setup Assistant panes to skip in an ADE enrolment profile using Apple's skip keys, hold the device with DeviceConfigured, and the Setup Assistant payload."
sources:
  - "https://support.apple.com/guide/deployment/dep73069dd57/web"
  - "https://support.apple.com/guide/deployment/dep35f523c44/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/other/skipkeys.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/device.configured.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# setup-assistant-panes

Goal: shorten first start-up while keeping the security steps you need.

- Panes to skip are set in the Automated Device Enrolment options ("Setup Assistant panes to skip": iOS 7, iPadOS 7, macOS 10.9, tvOS 10.2, visionOS 2 and later). The skip keys in Apple's definition include: `Privacy` (macOS 10.13.4), `Siri` (macOS 10.12), `Diagnostics`, `Payment` (Apple Pay), `ScreenTime` (macOS 10.15), `Appearance` (macOS 10.14), `Restore`, `TOS`, `Location` (macOS 10.11), `Passcode`, `FileVault` (macOS 10.10), `AppleID`, `Biometric` (Touch ID or Face ID), `iCloudDiagnostics` (macOS 10.12.4), `iCloudStorage` (macOS 10.13.4), `SoftwareUpdate` (macOS 15.4), `Welcome` (macOS 15.0) and `Accessibility` (macOS 11.0; it only skips the pane when Setup Assistant runs for a new user login, not at initial set-up). The full list is in Apple's `skipkeys.yaml`; there is no `Registration` key.
- Some panes cannot always be skipped because they appear before the device retrieves the cloud configuration: `Keyboard`, `SpokenLanguage`, `TermsOfAddress`, `AccessibilityAppearance` and `SafetyAndHandling`.
- Keys can be deprecated or removed: `Wallpaper` is macOS 14.1 and removed in macOS 26.0; `DisplayTone` is deprecated from iOS 15 and macOS 12.
- "Hold device in Setup Assistant" (await configuration) keeps the device in Setup Assistant until the MDM service sends `DeviceConfigured` (iOS 9.0, macOS 10.11, tvOS 10.2, visionOS 2.0; ADE devices only; forbidden for User Enrolment). It only works on ADE devices whose cloud configuration is set to await configuration.
- For Enforce FileVault in Setup Assistant (macOS 14 or later) use together with holding the device, so the service has the needed information before proceeding.
- Separately, the Setup Assistant payload `com.apple.SetupAssistant.managed` (iOS, iPadOS, Shared iPad, macOS device and user; all three enrolment types; one per user or device) has Mac settings that hide Appearance, Apple Account, Data and privacy, iCloud Desktop and Documents, Screen Time, Siri, Touch ID and True Tone panes, plus a "Set-up items" list of panes to skip.
- Auto Advance on Mac (macOS 11 or later) skips every pane when no other panes are enabled.

Gotcha: a pane that is not in the skip list shows until you add it; check the skip keys against the newest OS version, as Apple adds and removes keys.

Verify:
- A test device on the newest OS reaches the Home Screen or desktop with no unplanned panes.
- No device stays at the Remote Management step longer than normal sync time; if it does, check that `DeviceConfigured` is being sent.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Automated Device Enrolment and device management" and "Set-Up Assistant device management payload settings", plus the apple/device-management `skipkeys.yaml` and `device.configured.yaml`. Removed as unconfirmed: the `Registration` key, the Jamf prestage behaviour, the assumption that `Terms` is the key name (the key is `TOS`) and the advice not to skip FileVault. Only the keys quoted above were checked key by key.
Method: documentation only; no commands were run.
