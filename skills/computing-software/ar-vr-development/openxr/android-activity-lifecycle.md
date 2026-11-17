---
id: computing-software.ar-vr-development.openxr.android-activity-lifecycle
name: android-activity-lifecycle
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, android-activity-lifecycle]
level: advanced
status: draft
description: "Keep Android pause/resume consistent with XR session states."
sources: ['https://www.khronos.org/openxr/', 'https://registry.khronos.org/OpenXR/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Map Android lifecycle to the session
**Goal:** Keep Android pause/resume consistent with XR session states.

- On pause, expect STOPPING/IDLE; do not destroy the instance unless exiting.
- Stop rendering threads on `onPause`; resume on READY.
- Recreate swapchains if the runtime invalidated them after a long pause.

## Gotchas
- Calling EGL or Vulkan from a paused surface crashes on some devices.

## Self-check
Home-button round trip returns to rendering with no leaks.
