---
id: creative-arts.graphic-design.adobe-photoshop.content-aware-scale
name: content-aware-scale
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-transform, content-aware-scale, protect-skin-tones, alpha-channel, format-adaptation]
level: practitioner
status: draft
description: "Resize or re-proportion images with Content-Aware Scale: protecting subjects with alpha channels and skin-tone protection, limits, and when to crop instead."
sources:
  - https://helpx.adobe.com/photoshop/using/content-aware-scaling.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Content-Aware Scale

**Goal:** change an image's proportions (e.g. 3:2 to 16:9 banner) without squashing the important content.

## Steps
1. Unlock the Background layer (or work on a normal layer). Smart objects are **not** supported -
   duplicate and rasterise a copy.
2. Enlarge canvas (Image > Canvas Size) if widening.
3. Select the subject, Select > Save Selection to an alpha channel.
4. Edit > **Content-Aware Scale** (Alt+Shift+Ctrl/Cmd+C).
5. Options bar: **Protect** = your alpha channel; toggle the person icon (**Protect Skin Tones**).
6. Drag handles; Amount slider mixes content-aware (100%) with normal scaling.
7. Commit.

## Limits
- Works by removing/adding low-detail areas (sky, sea, walls). Busy uniform detail (crowds,
  foliage, brick) produces visible artefacts.
- More than ~20-30% change usually shows. Combine: crop part of it, content-aware the rest.
- Straight lines (horizon, architecture) bend; protect them with the alpha channel.

## Alternatives
- Generative Expand for adding real new content at the edges.
- Plain crop when a tighter composition is acceptable.

## Verify
- [ ] Faces, products and logos are undistorted (compare with original).
- [ ] No repeated texture tiles or bent straight edges at 100%.
