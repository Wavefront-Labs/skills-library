---
id: computing-software.ar-vr-development.unity-xr.continuous-snap-turn-move
name: continuous-snap-turn-move
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, continuous-snap-turn-move]
level: practitioner
status: draft
description: "Add comfort-tuned smooth move and snap turn."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Continuous move and turn
**Goal:** Add comfort-tuned smooth move and snap turn.

- Add Continuous Move Provider (speed, forward source = head or hand) and Snap Turn Provider (turn amount, e.g. 45 degrees) or Continuous Turn Provider.
- Bind thumbstick Vector2 actions through the Input System.
- Offer comfort options such as vignette (see comfort skills) and let the player pick snap versus smooth.

## Gotchas
- Continuous locomotion is a common cause of VR sickness; ship snap turn as default.

## Self-check
Thumbstick moves relative to look direction without drift when released.
