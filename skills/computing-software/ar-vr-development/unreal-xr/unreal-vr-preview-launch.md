---
id: computing-software.ar-vr-development.unreal-xr.unreal-vr-preview-launch
name: unreal-vr-preview-launch
category: computing-software
field: ar-vr-development
product: unreal-xr
tags: [unreal-xr, unreal-vr-preview-launch]
level: practitioner
status: draft
description: "Test in the editor on a headset."
sources: ['https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-xr-experiences-in-unreal-engine']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Launch VR Preview and standalone
**Goal:** Test in the editor on a headset.

- Play dropdown > VR Preview; for a packaged check use Launch with -vr or a standalone game with VR enabled.
- Use `stereo on` console command in a non-VR window to approximate stereo.
- Check log for OpenXR instance creation lines.

## Gotchas
- Editor VR Preview costs more than a packaged build; do not profile there.

## Self-check
Log shows the OpenXR runtime name and a headset-tracked camera.
