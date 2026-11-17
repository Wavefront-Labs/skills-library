---
id: computing-software.ar-vr-development.unity-xr.ar-tracked-image-library
name: ar-tracked-image-library
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, ar-tracked-image-library]
level: advanced
status: draft
description: "Detect known images with ARTrackedImageManager."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Track images with a reference library
**Goal:** Detect known images with ARTrackedImageManager.

- Create an XRReferenceImageLibrary asset; add textures with physical sizes (metres).
- Assign it to ARTrackedImageManager; handle `trackablesChanged`.
- Use high-contrast, non-repeating images.

## Gotchas
- Providers limit the number of images tracked at once; check maxNumberOfMovingImages.

## Self-check
Printed image spawns content aligned to it.
