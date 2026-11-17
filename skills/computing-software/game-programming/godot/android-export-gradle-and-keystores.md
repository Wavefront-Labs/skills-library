---
id: computing-software.game-programming.godot.android-export-gradle-and-keystores
name: android-export-gradle-and-keystores
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-export, godot-android-export, android-keystore, gradle-build, game-programming]
level: practitioner
status: docs-checked
description: "Export Godot games to Android: SDK/JDK setup, debug and release keystores, Gradle builds vs prebuilt templates, AAB for Play, permissions, architectures and adb debugging."
sources: ["https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html", "https://docs.godotengine.org/en/stable/tutorials/export/android_gradle_build.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Android export: Gradle builds and keystores

**Goal:** signed APK/AAB builds that install, pass Play Console checks and can be debugged on device.

## One-time setup
- Install OpenJDK 17 and the Android SDK (the docs list the exact `sdkmanager` packages for your Godot version; platform-tools must be present). Set Editor Settings > Export > Android > **Java SDK Path** and
  **Android SDK Path**.
- Debug keystore: see the export docs for creating one with `keytool` or letting Godot generate it.
- Release keystore (keep it safe and backed up):
  `keytool -v -genkey -keystore release.keystore -alias mygame -keyalg RSA -validity 10000`.

## Export preset
- Package: unique name (`com.studio.game`), version code and version name.
- Keystore > Release: path, user (alias), password. Prefer env vars in CI:
  `GODOT_ANDROID_KEYSTORE_RELEASE_PATH`, `GODOT_ANDROID_KEYSTORE_RELEASE_USER` (and the matching password variable listed in the docs).
- Architectures and permissions: enable only what you need (see the export preset options).
- Screen orientation and immersive mode are export options.

## Gradle build vs standard
- **Pre-built template**: the default export method.
- **Gradle build**: creates a Gradle-based Android project under `res://android/build`; required to export an AAB.
- Export an APK for sideloading and an **AAB** for Google Play.

## CI
`godot --headless --export-release "Android" build/game.aab` with the Gradle build template installed and the SDK and keystore paths configured.

## Debugging
- Use one-click deploy with USB debugging enabled on the device, and `adb logcat` for device logs.

## Gotchas
- Google Play requires an AAB for new apps (the docs say after August 2021) and enforces a minimum target API level; check Play's current requirement against your Godot version.
- Increment the version code on every upload.

## Verify
- [ ] `apksigner verify --print-certs` (or bundletool) shows the release certificate.
- [ ] Fresh install from internal testing track launches on a low-end test device.

## Checked

2026-10-28. Confirmed against: Exporting for Android and Gradle build pages (OpenJDK 17, Java SDK Path and Android SDK Path editor settings with platform-tools/adb, keytool release command, GODOT_ANDROID_KEYSTORE_RELEASE_PATH and _USER variables, AAB needs a Gradle build, res://android/build, Play AAB requirement after August 2021).

Removed or rewritten: the debug keytool one-liner, architecture and permission lists, plugin and SDK-version claims about the Gradle template, ANDROID_HOME, the logcat filter, adb reverse behaviour and the Vulkan/Compatibility advice.

Method: documentation only; no commands were run.
