---
id: computing-software.ar-vr-development.unity-xr.android-quest-build-settings
name: android-quest-build-settings
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-xr-build-quest, android-quest-build-settings]
level: practitioner
status: draft
description: "Set the player settings for a Quest-class headset."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configure Android builds for standalone headsets
**Goal:** Set the player settings for a Quest-class headset.

- Switch Build Target to Android; Scripting Backend IL2CPP, Target Architecture ARM64, a recent Minimum API level for the device.
- Enable the OpenXR provider on the Android tab and add the headset's interaction profile and feature set.
- Use URP with a mobile-friendly asset; Vulkan or OpenGL ES 3 as the vendor recommends.

## Gotchas
- Missing ARM64 is the usual reason a device rejects the APK.

## Self-check
adb install runs and the app starts in the headset.
