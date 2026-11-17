---
id: computing-software.ar-vr-development.unity-xr.openxr-feature-groups-profiles
name: openxr-feature-groups-profiles
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, openxr-feature-groups-profiles]
level: practitioner
status: draft
description: "Add interaction profiles and feature sets in the OpenXR settings."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choose OpenXR interaction profiles and features
**Goal:** Add interaction profiles and feature sets in the OpenXR settings.

- Project Settings > XR Plug-in Management > OpenXR: add Interaction Profiles (for example Oculus Touch Controller Profile, HTC Vive, Valve Index) for the controllers you ship for.
- Enable only the features you use (hand tracking, Meta Quest features) to avoid unsupported extension errors.
- The Validation window flags missing project settings.

## Gotchas
- An unlisted profile means the controller pose and buttons never bind.

## Self-check
Controllers track in Play mode on each target device.
