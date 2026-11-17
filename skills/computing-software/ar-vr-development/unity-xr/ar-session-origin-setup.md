---
id: computing-software.ar-vr-development.unity-xr.ar-session-origin-setup
name: ar-session-origin-setup
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-ar-foundation-session, ar-session-origin-setup]
level: practitioner
status: draft
description: "Create the scene objects that run an AR session."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Set up AR Session and XR Origin
**Goal:** Create the scene objects that run an AR session.

- Add an AR Session (lifecycle) and XR Origin (AR) with AR Camera; add manager components for the features you use.
- Enable the ARCore XR Plug-in (Android) or ARKit XR Plug-in (iOS) in XR Plug-in Management.
- Only enable managers you use; each adds cost.

## Gotchas
- Camera and session must exist before managers start; managers in the same scene run in parallel to AR Session.

## Self-check
Camera feed appears with tracking on device.
