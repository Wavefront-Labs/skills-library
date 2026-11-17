---
id: computing-software.computer-graphics-engineering.rendering-techniques.taa-projection-jitter-sequences
name: taa-projection-jitter-sequences
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, antialiasing, halton-jitter, projection-jitter, taa, subpixel-jitter, motion-vectors, upscaling]
level: practitioner
status: docs-checked
description: "Jitter the projection for temporal upscalers as FSR 2 specifies: Halton(2,3) phases, 8*n^2 sequence length, projection offset conversion, un-jittered motion vectors."
sources: ["https://github.com/GPUOpen-Effects/FidelityFX-FSR2/blob/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Projection jitter sequences

Source: the FidelityFX Super Resolution 2 (FSR 2) README, "Camera jitter" and input sections.

## 1. Sequence and length
- FSR 2 relies on the application to apply sub-pixel jitter while rendering, typically in the
  camera projection matrix. Its helper functions `ffxFsr2GetJitterPhaseCount(renderWidth,
  displayWidth)` and `ffxFsr2GetJitterOffset(&x, &y, phase, sequenceLength)` implement a
  Halton(2,3) sequence, chosen to give spatially separated points covering the available space.
  The offsets returned are in unit pixel space.
- Sequence length per quality mode (scaling factor per dimension): Quality 1.5x gives 18,
  Balanced 1.7x gives 23, Performance 2.0x gives 32, Ultra performance 3.0x gives 72. A custom
  factor n gives `ceil(8 * n^2)`.
- If you use your own sequence, it must never generate a null vector (0 in both X and Y), and
  you must set the `jitterOffset` field of the dispatch description to the offset actually
  applied for that frame.

## 2. Apply to the projection
Convert the pixel-space offset to a projection offset, then composite it with a translation:
```cpp
jitterX =  2.0f * jitterX / (float)renderWidth;
jitterY = -2.0f * jitterY / (float)renderHeight;
jitteredProjectionMatrix = translateMatrix(identity, Vector3(jitterX, jitterY, 0)) * projectionMatrix;
```
(as listed in the README; note the sign flip on Y).
- Apply jitter to all rendering: opaque, alpha-transparent and ray traced objects. For ray
  traced rendering, apply the sub-pixel jitter to the ray origin, often the camera position.
- All inputs provided at render resolution, except motion vectors, should be rendered with
  jitter.

## 3. Motion vectors
Motion vectors should not have jitter applied, unless the
`FFX_FSR2_ENABLE_MOTION_VECTORS_JITTER_CANCELLATION` flag is set.

## 4. Camera cuts
On a camera jump cut, set `reset` to true for the first frame of the discontinuous camera
transformation so the accumulated history is cleared.

## Gotchas
- Jitter values reported to the upscaler must match what was applied to the projection,
  including sign convention.

## Verify
- [ ] Static scene converges to a stable image; the reported jitterOffset matches the projection offset.

## Checked

Method: docs-checked 2026-11-09 against the FSR 2 README (camera jitter, inputs and jump cut sections read). Dropped the standalone Halton code, the 8-16 native TAA sample claim, the DLSS and Epic pages (unreadable or not read), the list of what not to jitter (shadow maps, UI), the orthographic note and the "reset index" gotcha.
