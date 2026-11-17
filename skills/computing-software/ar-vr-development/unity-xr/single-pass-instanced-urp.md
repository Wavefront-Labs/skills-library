---
id: computing-software.ar-vr-development.unity-xr.single-pass-instanced-urp
name: single-pass-instanced-urp
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-xr-rendering, single-pass-instanced-urp]
level: advanced
status: draft
description: "Render both eyes in one pass to cut CPU cost."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use single pass instanced stereo in URP
**Goal:** Render both eyes in one pass to cut CPU cost.

- In XR Plug-in Management > provider settings set Render Mode to Single Pass Instanced (or Multiview on Android).
- Custom shaders need stereo support macros (UNITY_VERTEX_INPUT_INSTANCE_ID, UNITY_VERTEX_OUTPUT_STEREO).
- Check post-processing and camera stacking for stereo support.

## Gotchas
- Shaders without stereo macros render in one eye only.

## Self-check
Frame Debugger shows one draw per object for both eyes.
