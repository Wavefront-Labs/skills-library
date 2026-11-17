---
id: computing-software.ar-vr-development.unity-xr.haptics-impulse-unity
name: haptics-impulse-unity
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, haptics-impulse-unity]
level: practitioner
status: draft
description: "Trigger rumble from XRI or from the InputDevice."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Send controller haptics
**Goal:** Trigger rumble from XRI or from the InputDevice.

- XR Controller / Haptic Impulse Player: `SendHapticImpulse(amplitude, duration)`.
- In older API: `InputDevice.SendHapticImpulse(0, amp, duration)` after checking `TryGetHapticCapabilities`.
- Use short pulses on hover and stronger on select.

## Gotchas
- Not every device supports haptics; check capabilities.

## Self-check
Hovering triggers a short pulse on the correct hand only.
