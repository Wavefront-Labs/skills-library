---
id: computing-software.software-engineering.mobile-development.play-target-api-level-requirements
name: play-target-api-level-requirements
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, target-sdk, targetsdkversion, google-play-policy, behavior-changes, api-level]
level: practitioner
status: docs-checked
description: "Meet Google Play target API level deadlines: new apps and updates versus existing apps, per-form-factor levels, the extension, and migrating via the behavior-change pages."
sources: ["https://support.google.com/googleplay/android-developer/answer/11926878", "https://developer.android.com/google/play/requirements/target-sdk", "https://developer.android.com/about/versions/16/behavior-changes-16"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Play target API level requirements

Each app declares `targetSdkVersion` (the target API level) in the manifest; it indicates how
the app is meant to run on different Android versions. A recent target still lets the app run
down to its `minSdkVersion`. Confirm or change the value in the app's Gradle file or the
`android:targetSdkVersion` attribute of `<uses-sdk>`.

## The requirement (as stated on the pages when read)
Starting August 31, 2026:
- New apps and app updates must target Android 16 (API 36) or higher. Wear OS and Android
  Automotive OS apps must target Android 15 (API 35) or higher; Android TV and Android XR apps
  Android 14 (API 34) or higher.
- Existing apps must target Android 15 (API 35) or higher to stay available to new users on
  devices running a higher Android version than the app's target. Lower-targeting apps are
  available only on devices running the same or a lower Android version than their target.
- An extension to November 1, 2026 can be requested; the form is reached through Play Console
  (affected apps get a link in their Notifications).
- Exception: permanently private apps restricted to one organisation for internal distribution.
- The support page defines a new app as not yet published on Google Play, and an app update as
  a new version submitted for review to replace the existing app.

Numbers change each year: read the support page for the current table rather than relying on
this summary.

## Migration routine
1. Read the behavior-change page for each Android version between the current and new target
   (the target-SDK page links Android 13 to 16 changes; older versions have their own lists).
2. Bump `targetSdkVersion`, then test the changed areas for that level.
3. Example from the Android 16 page: apps targeting API 36 cannot opt out of edge-to-edge
   (`windowOptOutEdgeToEdgeEnforcement` is deprecated and disabled); Android 15 introduced
   the enforcement for apps targeting 35. BODY_SENSORS use moves to the
   `android.permissions.health` permissions at target 36.
4. The Android 16 page notes the app compatibility framework lets you enable individual compat
   flags for testing (for example `UNIVERSAL_RESIZABLE_BY_DEFAULT`).

## Checked
Confirmed in the support page, the target-SDK page and the Android 16 behavior-changes page:
dates, per-form-factor levels, existing-app availability rule, extension date, exception,
definitions, edge-to-edge and BODY_SENSORS changes, compat-flag testing. Removed as not stated:
the compileSdk/minSdk table, the "within one year of release" pattern, the Developer options
menu path, the staged-rollout and Android vitals advice, and the `aapt2` verify command.
Method: docs-only read of cited pages, 2026-11-08
