---
id: computing-software.ar-vr-development.unity-xr.ray-direct-poke-interactors
name: ray-direct-poke-interactors
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-xri-interactors, ray-direct-poke-interactors]
level: practitioner
status: draft
description: "Match the interactor type to the interaction distance."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pick ray, direct, poke and gaze interactors
**Goal:** Match the interactor type to the interaction distance.

- XR Ray Interactor for distant select, XR Direct Interactor (XR Grab Interactor in XRI 3) for touching, Poke Interactor for UI buttons, Gaze interactor for look-based select.
- Each needs a collider or ray settings, an Interaction Manager and input actions for select and activate.
- Use the Near-Far Interactor in XRI 3 to unify near and far.

## Gotchas
- Missing XR Interaction Manager means nothing interacts.

## Self-check
Hovering an interactable highlights it and select grabs it.
