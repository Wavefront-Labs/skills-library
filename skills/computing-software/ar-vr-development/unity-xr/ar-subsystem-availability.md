---
id: computing-software.ar-vr-development.unity-xr.ar-subsystem-availability
name: ar-subsystem-availability
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, ar-subsystem-availability]
level: practitioner
status: draft
description: "Verify device support and request camera permission before starting."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Check AR availability and permissions
**Goal:** Verify device support and request camera permission before starting.

- `ARSession.CheckAvailability()` as a coroutine, then `ARSession.Install()` if `NeedsInstall` (ARCore); inspect `ARSession.state`.
- Set the camera usage description for iOS; Android requests permission automatically with camera use.
- Disable the AR Session component until availability is confirmed.

## Gotchas
- Unsupported devices stay in `Unsupported` state; show a fallback.

## Self-check
State reaches SessionTracking on a supported phone.
