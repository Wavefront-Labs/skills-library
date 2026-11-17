---
id: computing-software.game-programming.unity.urp-volume-post-processing
name: urp-volume-post-processing
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-urp, urp-volume, post-processing, volume-profile, game-programming]
level: practitioner
status: docs-checked
description: "Set up URP post-processing with the Volume framework: global vs local volumes, profiles, default volumes, camera enable and Volume Mask."
sources: ["https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/manual/Volumes.html", "https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.0/manual/integration-with-post-processing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URP Volume post-processing

**Goal:** bloom, colour grading, vignette and similar effects configured per area through the Volume framework.

## Pieces
- **Volume** component: attach to any GameObject (a scene can hold many, and a GameObject can hold several).
  Dedicated GameObjects exist for Global Volume, Box Volume, Sphere Volume and Convex Mesh Volume.
- **Volume Profile**: referenced by each Volume; holds scene properties in one or more **Volume Overrides**
  (for example Vignette, Tonemapping, Bloom).
- **Global volumes** affect the camera everywhere. **Local volumes** affect the camera only when it is near the
  bounds of the collider on the parent GameObject.
- At runtime URP goes through all enabled Volume components on active GameObjects, works out each one's
  contribution from the camera position and the Volume properties, and interpolates values from all volumes with
  a non-zero contribution.

## Default volumes
Every URP scene has two default global volumes: the project Default Volume (profile set in Project Settings >
Graphics > URP > Default Volume Profile) and a global volume for the active quality level (profile set in the
active URP Asset > Volumes > Volume Profile). URP evaluates them only when a scene first loads or the quality
level changes, not every frame, so scenes that rely only on default volumes cost less at runtime. They have the
lowest priority, so any volume you add overrides them.

## Add post-processing to a scene
New URP scenes do not use post-processing by default (some URP examples and scene templates do).
1. Select a Camera and enable **Post Processing** in the Inspector.
2. Add a GameObject with a Volume component, for example GameObject > Volume > Global Volume.
3. In the Volume component select **New** to create a Volume Profile.
4. Select **Add Override** and choose an effect such as Bloom, then enable and adjust its settings.
Effects from a volume apply to a camera only if the camera's **Volume Mask** contains the layer the volume's
GameObject is on.

## Gotchas
- Effect not visible: check the camera's Post Processing toggle, the camera's Volume Mask against the volume's
  layer, and that the override is enabled in the profile.
- Runtime changes to volumes from script (profile instances, weights) are not covered by the pages checked here;
  consult the Volume scripting API before relying on them.

## Verify
- [ ] The effect shows in the Game view with the camera's Post Processing enabled and a matching Volume Mask.

## Checked
Date 2026-11-09. Read in full as fetched text: URP 17.0 "Understand volumes in URP" and "Add post-processing in
URP". Confirmed volume types, global vs local behaviour, contribution and interpolation, default volumes and their
paths, evaluation timing and priority, the setup steps and the Volume Mask rule.
Removed as unconfirmed: the runtime override script (`profile`, `sharedProfile`, `TryGet`, `weight`, `Override`),
Priority and Blend Distance property descriptions, HDR and grading mode notes, mobile performance advice, camera
stacking behaviour and the Memory Profiler verification step.
Method: documentation only; no commands were run.
