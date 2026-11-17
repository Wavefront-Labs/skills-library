---
id: computing-software.it-support-helpdesk.apple-device-management.kiosk-lockdown-app-config
name: kiosk-lockdown-app-config
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, kiosk, lockdown, app-configuration]
level: practitioner
status: docs-checked
description: "Combine restrictions, Home Screen Layout, App Lock and managed app configuration for supervised iPad or iPhone kiosks."
sources:
  - "https://support.apple.com/guide/deployment/app-lock-payload-settings-dep80a981/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.homescreenlayout.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.applicationaccess.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/settings.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kiosk-lockdown-app-config

Goal: make a shared or public iPad kiosk hard to misuse and cheap to maintain.
- Pin the app: App Lock payload `com.apple.app.lock` with `App` > `Identifier` (see single-app-mode). It needs a supervised device and Automated Device Enrolment.
- Restrictions payload (`com.apple.applicationaccess`): `allowLockScreenControlCenter` false stops Control Center on the Lock Screen (default true); `allowNotificationsModification` false stops users changing notification settings (iOS 9.3 or later, supervised); `allowPasscodeModification` false stops users changing the passcode (iOS 9.0 or later, supervised, not for Shared iPad); `allowAppRemoval` false stops app deletion.
- Home Screen Layout payload `com.apple.homescreenlayout` (iOS 9.3 or later, supervised, one per device, not for User Enrolment): required `Pages` (arrays of icon dictionaries) and optional `Dock`; each item has `Type` (`Application`, `Folder` or `WebClip`) and, for apps, `BundleID`. Apple states the layout is locked and the user cannot change it.
- App settings: the Settings command with `Item` = `ApplicationConfiguration` takes the app `Identifier` and a `Configuration` dictionary for the app's own keys (for example a kiosk URL, if the app defines one). It requires the App Management access right and fails for apps managed by declarative device management.
Practice: install the kiosk app before the App Lock and layout profiles, and test the whole profile set on a spare device; keep that device pre-configured as a replacement.
Gotcha: automatic updates can interrupt a public display, so plan update timing in your MDM (see the software update skills).
Verify: after a restart the device returns straight to the pinned app.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
- Read in full: Apple Platform Deployment "App Lock payload settings"; the apple/device-management YAML for `com.apple.homescreenlayout`; the `ApplicationConfiguration` section of the Settings command YAML; for `com.apple.applicationaccess` I searched for and read the entries for `allowLockScreenControlCenter`, `allowNotificationsModification`, `allowPasscodeModification` rather than reading the whole file. `allowAppRemoval` is confirmed only by the Home Screen Layout YAML note ("set `allowAppRemoval` to `false` with Restrictions").
- Removed as unconfirmed: scheduled shutdown and wake, monitoring "status checks", naming devices by location, labelling and overnight update-window advice, and the "Kiosk restarts into the app" claim beyond what the App Lock page says (the app reopens after a restart).
- The original source URL (single-app-mode-depa1a6dbfd5) is not a real page and was replaced.
