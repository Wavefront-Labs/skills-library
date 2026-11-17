---
id: creative-arts.photography-fine-art.art-photography.focus-stacking-capture-and-blending
name: focus-stacking-capture-and-blending
category: creative-arts
field: photography-fine-art
product: art-photography
tags: [art-photography, depth-of-field, focus-stacking, focus-bracketing, helicon-focus, zerene-stacker, photoshop-auto-blend, macro-photography, landscape-focus]
level: practitioner
status: draft
description: "Shoot a focus-bracketed sequence (manual or in-camera) and blend it in Helicon Focus, Zerene Stacker or Photoshop without halos or misalignment."
sources: ["https://helpx.adobe.com/photoshop/using/combine-images-auto-blend-layers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Focus stacking: capture and blend

## Capture
1. Tripod, manual exposure, manual white balance, fixed ISO; disable stabilisation.
2. Aperture at the lens sweet spot (often f/5.6-f/8) - stacking replaces stopping down.
3. Focus nearest point, step to farthest, overlapping the DoF of each frame. In-camera
   focus bracketing (Nikon focus shift, Canon focus bracketing, Olympus/OM) sets step size
   and count automatically - use a small step for macro, larger for landscape.
4. Landscape: often 3-6 frames (near foreground, mid, far). Macro: 20-200 frames, use a
   focusing rail when the lens's focus breathing changes framing too much.
5. Wind: shoot fast, or shoot the moving element (grass) separately once and mask it in.

## Blend
- **Photoshop:** Load Files into Stack (Auto-Align), select layers, Edit > Auto-Blend
  Layers > Stack Images, Seamless Tones and Colors. Good for few frames; can smear.
- **Helicon Focus:** Method B (depth map) for smooth, Method C (pyramid) for complex
  overlapping edges; retouch from source frames with the brush.
- **Zerene Stacker:** PMax (detail, more halos/noise) and DMap (clean tones); combine both
  and retouch.
- Export a 16-bit TIFF; bring back to Lightroom.

## Failure modes
- Halos around edges in front of distant background: retouch from a single source frame.
- Focus breathing makes frames different sizes: enable alignment/scale correction.
- Moving clouds/water: mask a single frame for those areas.

## Verify
- [ ] 100% inspection shows no soft bands between frames, no ghost edges.
