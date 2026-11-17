---
id: computing-software.it-support-helpdesk.apple-device-management.single-app-mode
name: single-app-mode
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, single-app-mode, app-lock, kiosk]
level: practitioner
status: docs-checked
description: "Lock supervised iPhone, iPad and Apple TV to one app with the App Lock payload, and know that Autonomous Single App Mode is a separate macOS-only payload."
sources:
  - "https://support.apple.com/guide/deployment/app-lock-payload-settings-dep80a981/web"
  - "https://support.apple.com/guide/deployment/autonomous-single-app-mode-payload-settings-dep8a42c4c4a/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.app.lock.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.asam.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# single-app-mode

Goal: purpose-built kiosks that run one app.
- App Lock payload `com.apple.app.lock`: forces the selected app to open and prevents use of other apps; the app reopens immediately after a restart. Supported on iOS, iPadOS, Shared iPad and tvOS, with Automated Device Enrolment, on supervised devices (iOS 6.0 or later, tvOS 10.2 or later); not allowed with User Enrolment. Only one App Lock payload can be on a device.
- Required key: `App` dictionary with `Identifier` (the app bundle identifier). Optional `Options` (iOS 7.0 or later) the user cannot change, all booleans defaulting to false: `DisableTouch`, `DisableDeviceRotation`, `DisableVolumeButtons`, `DisableRingerSwitch`, `DisableSleepWakeButton`, `DisableAutoLock`, `EnableVoiceOver`, `EnableZoom`, `EnableInvertColors`, `EnableAssistiveTouch`, `EnableSpeakSelection`, `EnableMonoAudio`, `EnableVoiceControl` (iOS 13.0 or later). Optional `UserEnabledOptions` (`VoiceControl`, `VoiceOver`, `Zoom`, `InvertColors`, `AssistiveTouch`) lets the user toggle those accessibility features.
- Install the target app first: Apple says to use the payload only after the app is installed. `DisableAutoLock` stops the device sleeping after an idle period.
- Autonomous Single App Mode is a different payload, `com.apple.asam`, and is macOS only (10.13.4 or later). It lists `AllowedApplications`, each with `BundleIdentifier` and `TeamIdentifier`, which are the apps allowed to put themselves in single app mode. It needs user-approved MDM, allows only one such payload, and grants the listed apps low-level system access including keystroke monitoring, so get the values from the app developer.
- Exit: the device stays locked to the app until the profile is removed, so keep a way to remove or replace the profile from the MDM.
Practice: test the app for crashes and offline behaviour before deployment, because a locked device that cannot recover needs a physical visit.
Gotcha: the device returns to the locked app on wake or restart, so only removing the profile frees it; agree the remote exit before rollout.
Verify: removing the App Lock profile returns the device to normal use.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
- Read in full: Apple Platform Deployment "App Lock payload settings" and "Autonomous Single App Mode payload settings for Mac", and the apple/device-management YAML for `com.apple.app.lock` and `com.apple.asam` (keys, defaults, OS minimums, supervised and User Enrolment rules, notes).
- Corrected: the original said Autonomous Single App Mode locks supervised iPads and was allowed through `com.apple.asam`; Apple documents `com.apple.asam` as macOS only. Removed the "long timeout" advice, the "home button does not exit" Verify step, and the admin-PIN managed-app suggestion, none of which the pages confirm.
- The original source URL (single-app-mode-depa1a6dbfd5) is not a real page (it serves the guide's welcome page), so it was replaced.
