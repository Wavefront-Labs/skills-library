---
id: creative-arts.graphic-design.adobe-photoshop.matching-grain-and-depth-of-field
name: matching-grain-and-depth-of-field
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, compositing, grain-matching, noise, depth-of-field, lens-blur, photo-manipulation]
level: advanced
status: draft
description: "Make composited elements share the plate's grain, sharpness and depth of field: noise analysis per channel, add-noise and grain layers, and blur by distance."
sources:
  - https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html
  - https://helpx.adobe.com/photoshop/using/add-noise-filter.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matching grain and depth of field

**Goal:** remove the "pasted-in" look caused by different noise, sharpness and focus.

## Inspect at 100-200%
- View each channel (Ctrl/Cmd+3/4/5). Blue channel usually carries the most noise in digital
  photos. Compare plate and insert channel by channel.
- Compare edge sharpness: a clean studio cut-out is often much sharper than the plate.

## Match sharpness first
- If the insert is sharper, soften slightly (Gaussian Blur 0.3-0.8 px as a smart filter) until
  edge contrast matches comparable edges in the plate at the same distance.
- If the plate is sharper, prefer a better source over heavy sharpening.

## Match depth of field
- Decide the insert's distance from the focal plane. Objects at the same depth as blurred
  plate areas must carry the same blur.
- Filter > Blur > **Lens Blur** (smart filter) gives bokeh-like defocus; Gaussian blur looks wrong
  on highlights. Use a depth map (gradient in a channel) for objects receding in depth.

## Match grain
1. Remove existing noise from the insert if it differs in character (Camera Raw Filter > Detail > Noise Reduction).
2. Add matched grain over the insert only: new layer filled with 50% grey, Overlay mode,
   Filter > Noise > Add Noise (Gaussian, Monochromatic off for colour noise), clip to insert.
3. Alternatively apply grain to the whole flattened composite (Camera Raw Filter > Effects >
   Grain) so all elements share one grain structure - most reliable final unifier.
- Scale grain size to the plate: an upscaled plate has bigger grain clumps.

## Gotchas
- Compare at the final output size; matching at 300% wastes time.
- JPEG plates have compression blocks; a pristine insert looks fake next to them.

## Verify
- [ ] Each channel shows similar noise across the seam.
- [ ] Toggling the grain layer off makes the insert visibly "cleaner" than the plate.
