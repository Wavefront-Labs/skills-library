---
id: computing-software.computer-graphics-engineering.shader-programming.post-processing-shader-effects
name: post-processing-shader-effects
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [shader-programming, post-processing, bloom, depth-of-field, motion-blur, screen-space, gaussian-blur, bokeh, chromatic-aberration, vignette, color-grading, luts, fullscreen-pass]
level: advanced
status: draft
description: "Write the standard screen-space post-processing shaders correctly: separable blur for bloom, depth-of-field/bokeh, motion blur from velocity, and LUT-based color grading, with the common artefacts."
sources: ["https://learnopengl.com/Advanced-Lighting/Bloom", "https://catlikecoding.com/unity/tutorials/advanced-rendering/depth-of-field/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-processing shader effects

**Goal:** implement the standard screen-space effects (bloom, DoF, motion blur,
color grading) with the right structure — most of these have a naive version
that "looks like" the effect but is wrong (too slow, wrong halo, breaks on edges).

## Bloom: separable blur, not a 2D kernel
- Extract bright pixels (threshold, or better, a soft knee curve rather than a
  hard cutoff to avoid a visible edge where bloom turns on) into a lower-resolution
  target.
- Blur with a **separable Gaussian**: one horizontal pass + one vertical pass,
  each a 1D kernel — O(n) per pixel instead of O(n²) for a true 2D kernel, the
  standard reason every blur-based effect is implemented this way.
- Do the blur at **progressively downsampled mip levels** and composite them
  back up (a mip chain of blurred results, as in Unreal/Call of Duty-style
  bloom) rather than one huge single-resolution blur kernel — gives a wide, soft
  glow cheaply; a single-pass wide-radius blur at full resolution is far more
  expensive for a similar look.
- Composite additively in **linear HDR space**, before tone mapping — bloom
  added after tone mapping looks flat and doesn't blend with the base image's
  highlights correctly.

## Depth of field
- Simple approach: blur radius per pixel derived from **circle of confusion**
  (function of pixel depth, focus distance, aperture) — blur more as a pixel's
  depth deviates from the focal plane.
- **Bokeh shape** (hexagonal/circular highlights in out-of-focus bright points)
  needs more than a Gaussian blur — a proper bokeh pass samples in the aperture
  shape (disc/polygon sampling kernel) rather than approximating with repeated
  Gaussian blur, which just produces a soft blob, not distinct bokeh shapes.
- **Foreground/background bleeding**: naive single-pass blur lets a sharp
  foreground object bleed blur from behind it onto itself (or vice versa) at
  depth discontinuities — proper DoF separates near/far blur layers or uses a
  depth-aware blur that doesn't sample across a large depth discontinuity.

## Motion blur
- **Per-object/camera velocity buffer** (same motion vectors as TAA — see
  `rendering-techniques.temporal-antialiasing-and-upscaling`) drives a blur along
  each pixel's velocity direction, sampling several steps along that vector.
- Missing or zero motion vectors on a moving object (common bug: motion vectors
  computed for camera motion only) makes that object render *sharp* while
  everything else blurs — visually wrong in the opposite direction from what
  you'd expect (looks like the object is pasted on top).
- Clamp sample count/step size — unbounded blur length on very fast motion either
  costs too much or produces a smeared mess; most engines cap blur length in pixels.

## Color grading via LUTs
- A 3D LUT (commonly 32×32×32, encoded as a 2D texture atlas) maps input color →
  graded output color — apply **after** tone mapping, on the final display-range
  image, trilinear-sampled.
- Author/export LUTs from the same tone-mapping operator used in-engine (bake a
  neutral grading pass through the actual engine pipeline first) — a LUT
  authored against a different tone curve than what's actually running shifts
  contrast/saturation unpredictably.

## Verify
- [ ] Bloom composited in linear HDR space before tone mapping, confirmed by
      checking bloom intensity doesn't shift when exposure changes downstream.
- [ ] Blur passes implemented as separable (two 1D passes), not a single large
      2D kernel, for any Gaussian-based effect.
- [ ] Motion blur checked on a moving object specifically (not just camera pans)
      to confirm per-object motion vectors are populated.
- [ ] DoF checked at a depth discontinuity (sharp foreground object against
      blurred background) for bleeding artefacts.
