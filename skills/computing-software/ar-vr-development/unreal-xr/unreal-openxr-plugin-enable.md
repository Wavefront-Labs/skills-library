---
id: computing-software.ar-vr-development.unreal-xr.unreal-openxr-plugin-enable
name: unreal-openxr-plugin-enable
category: computing-software
field: ar-vr-development
product: unreal-xr
tags: [unreal-xr, unreal-openxr-setup, unreal-openxr-plugin-enable]
level: practitioner
status: draft
description: "Turn on the OpenXR plugins and set the project for VR."
sources: ['https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-xr-experiences-in-unreal-engine']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enable the OpenXR plugin
**Goal:** Turn on the OpenXR plugins and set the project for VR.

- Edit > Plugins: enable OpenXR (and OpenXRHandTracking, OpenXREyeTracker if needed); restart the editor.
- Start from the VR Template to get the pawn and motion controllers.
- Disable other conflicting XR plugins for the same device to avoid duplicate runtimes.

## Gotchas
- The active OpenXR runtime on the PC decides which headset opens.

## Self-check
VR Preview shows the headset view.
