---
id: computing-software.ar-vr-development.openxr.android-loader-init
name: android-loader-init
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-android-integration, android-loader-init]
level: advanced
status: docs-checked
description: "Pass the JavaVM and activity to the loader before creating an instance."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
  - https://github.com/KhronosGroup/OpenXR-SDK-Source/tree/main/specification/loader
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Initialise the Android loader
**Goal:** Pass the JavaVM and activity to the loader before creating an instance.

- Obtain `xrInitializeLoaderKHR` via `xrGetInstanceProcAddr` with `XR_NULL_HANDLE`, and call it with `XrLoaderInitInfoAndroidKHR` (`applicationVM` and `applicationContext`).
- Chain `XrInstanceCreateInfoAndroidKHR` (`applicationVM`, `applicationActivity`) into `xrCreateInstance`.
- The loader needs this initialisation before it can enumerate or create instances and discover API layers in the APK assets.

## Self-check
Instance created from an Android build on device.

## Checked

Date: 2026-11-02. Confirmed in the XR_KHR_loader_init, loader_init_android and android_create_instance pages and the loader API-layer chapter. Removed: the manifest/immersive category claim and the NativeActivity self-check detail.

Method: documentation only; no commands were run.
