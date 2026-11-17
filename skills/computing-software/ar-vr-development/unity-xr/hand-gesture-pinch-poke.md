---
id: computing-software.ar-vr-development.unity-xr.hand-gesture-pinch-poke
name: hand-gesture-pinch-poke
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, hand-gesture-pinch-poke]
level: advanced
status: draft
description: "Drive interactions from hand-tracking pinch and poke."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pinch and poke interaction with hands
**Goal:** Drive interactions from hand-tracking pinch and poke.

- XRI hand interaction uses the Hand Interaction profile and the XR Hands samples (Gestures, Hand Visualizer).
- Pinch strength drives select; the Poke interactor uses the index fingertip.
- Provide a controller fallback.

## Gotchas
- Hand input differs per runtime; test on target hardware (confirm profile names in the XRI samples).

## Self-check
Pinching grabs the cube; releasing drops it.
