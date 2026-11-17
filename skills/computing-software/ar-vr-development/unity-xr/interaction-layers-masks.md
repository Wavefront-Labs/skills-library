---
id: computing-software.ar-vr-development.unity-xr.interaction-layers-masks
name: interaction-layers-masks
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, interaction-layers-masks]
level: practitioner
status: draft
description: "Use Interaction Layer Masks to control what each interactor can use."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Filter with interaction layers
**Goal:** Use Interaction Layer Masks to control what each interactor can use.

- Define layers in Project Settings > Physics > Interaction Layer Settings (XRI 2.x) and set the mask on both interactor and interactable.
- Both masks must overlap for interaction to occur.
- Use layers for hand-specific or socket-only items.

## Gotchas
- Interaction layers differ from Unity physics layers.

## Self-check
An item on layer A is ignored by an interactor masked to layer B.
