---
id: computing-software.ar-vr-development.unreal-xr.unreal-quest-packaging
name: unreal-quest-packaging
category: computing-software
field: ar-vr-development
product: unreal-xr
tags: [unreal-xr, unreal-xr-android-package, unreal-quest-packaging]
level: advanced
status: draft
description: "Package a standalone headset build."
sources: ['https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-xr-experiences-in-unreal-engine']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Package an Android XR build
**Goal:** Package a standalone headset build.

- Install Android SDK/NDK via Android Studio per the engine's required version; use Project Settings > Platforms > Android SDK to point to them.
- Enable OpenXR (or the vendor plugin), set Package for Meta Quest or target API per docs.
- Package, then install via adb and check logcat.

## Gotchas
- SDK/NDK version mismatches are the usual cause of packaging failure; use the version listed in the engine docs for your release.

## Self-check
APK launches into the immersive experience.
