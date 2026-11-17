---
id: computing-software.ar-vr-development.unity-xr.xr-plugin-management-setup
name: xr-plugin-management-setup
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-xr-plugin-management, xr-plugin-management-setup]
level: practitioner
status: draft
description: "Install XR Plug-in Management and enable a provider for each build target."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enable XR Plug-in Management per platform
**Goal:** Install XR Plug-in Management and enable a provider for each build target.

- Project Settings > XR Plug-in Management > Install, then tick the provider per platform tab (Windows/Mac/Linux standalone, Android).
- The OpenXR provider is the cross-vendor default; Oculus provider remains for some Meta-specific features.
- Initialize XR on Startup can be turned off to start XR manually with the XRGeneralSettings manager.

## Gotchas
- Provider settings are per build target tab; ticking it on Standalone does not enable Android.

## Self-check
Entering Play mode shows the headset view with a provider listed in the Console on init.
