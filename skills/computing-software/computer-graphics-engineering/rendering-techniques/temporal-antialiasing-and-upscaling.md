---
id: computing-software.computer-graphics-engineering.rendering-techniques.temporal-antialiasing-and-upscaling
name: temporal-antialiasing-and-upscaling
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [rendering-techniques, taa, temporal-antialiasing, dlss, fsr, xess, upscaling, motion-vectors, ghosting, jitter, history-buffer, clamping, reprojection, temporal-stability, taa-ghosting, history-clamping]
level: advanced
status: draft
description: "Implement TAA and hook up upscalers (DLSS/FSR/XeSS) correctly: sub-pixel jitter, motion vectors, history reprojection and clamping, and the ghosting/flicker failure modes."
sources: ["https://alextardif.com/TAA.html", "https://developer.nvidia.com/dlss", "https://gpuopen.com/fidelityfx-superresolution/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temporal antialiasing and upscaling

**Goal:** accumulate sub-pixel detail over frames (TAA) or hand a low-res frame
to an upscaler (DLSS/FSR/XeSS) without the ghosting, flicker, or blur that's the
signature failure of a badly wired temporal pipeline.

## TAA mechanics
- **Jitter**: offset the projection matrix by a sub-pixel amount each frame
  (typically a low-discrepancy sequence — Halton — over 8-16 frames) so each
  frame samples a slightly different sub-pixel position.
- **History buffer**: keep the previous frame's resolved color. Each frame,
  **reproject** the history using per-pixel motion vectors (where did this pixel's
  content come from last frame) and blend with the current frame's jittered
  sample — this accumulation is what builds up anti-aliased detail over time.
- **Motion vectors** must cover everything that moves: camera motion (cheap,
  derivable from view matrices) AND per-object/per-vertex motion (skinned meshes,
  vertex-animated foliage) — static-camera-only motion vectors are a common
  shortcut that breaks TAA on any moving object, producing trailing ghosts behind
  it.

## Ghosting and ghost-busting
**Ghosting** = stale history data lingering where it shouldn't (trailing smear
behind moving objects, or disocclusion reveals showing old background content).
Mitigations, used together not alone:
- **Neighbourhood clamping**: clamp the reprojected history sample to the min/max
  color range of the current frame's local neighbourhood (AABB clipping in YCoCg
  or similar) — rejects history that's wildly inconsistent with what's actually
  there now.
- **Disocclusion rejection**: detect where reprojection points to a
  previously-occluded pixel (depth mismatch between history and current) and fall
  back to current-frame-only (no history blend) for that pixel.
- **Velocity-based blend weight**: reduce history weight (favour current frame
  more) where motion vector magnitude is large — fast-moving content ages out of
  the history faster, trading less anti-aliasing for less ghosting on motion.

## Upscalers (DLSS / FSR / XeSS)
These are TAA's logic taken further: render at a lower internal resolution,
upscale+anti-alias in one pass using the same core inputs (jittered low-res
color, depth, motion vectors) plus (for DLSS/XeSS) a trained network.
- **Motion vector quality is the single biggest quality lever** across all three
  — incorrect or missing motion vectors on particles, transparents, or
  vertex-animated content causes visible smearing/ghosting specifically on those
  elements even when the rest of the scene looks sharp.
- **Reactive/transparency masks** (DLSS, FSR): a per-pixel mask telling the
  upscaler which pixels are "unstable" (particles, decals, alpha-blended effects
  without reliable motion vectors) so it blends them with less temporal
  confidence — skipping this makes smoke/fire/particles look smeared or flickery
  even when geometry upscales cleanly.
- Sharpening is usually a separate post-upscale step (or an exposed parameter) —
  over-sharpening re-introduces aliasing-like artefacts the upscaler just removed.

## Failure modes
- **Flicker** on thin/high-frequency detail (foliage, wires, specular highlights)
  that falls below the jitter pattern's effective sampling — detail appears and
  disappears frame to frame instead of stabilising. Often needs a specular/
  highlight-aware clamp or increasing jitter sequence length.
- **Blurring fine detail** from over-aggressive history blend weight — a
  trade-off dial, not a bug, but needs tuning per project rather than left at
  a sample's default.

## Verify
- [ ] Motion vectors verified present and correct for every moving element
      (camera, skinned meshes, vertex-animated foliage, particles) — not just
      camera motion.
- [ ] Ghosting tested explicitly: a fast-moving object against a static,
      detailed background, checked for trailing smear.
- [ ] Disocclusion regions (object moves, reveals background) checked for stale
      content rather than correctly falling back to current-frame data.
- [ ] Reactive/transparency mask populated for particles/decals if using a
      commercial upscaler, not left at default (all-opaque) assumptions.
