---
id: creative-arts.photography-fine-art.adobe-lightroom.panorama-merge-projections
name: panorama-merge-projections
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, panorama-merge, photo-merge, boundary-warp, projection, lightroom-classic]
level: practitioner
status: draft
description: "Stitch panoramas in Lightroom Classic: spherical, cylindrical and perspective projections, boundary warp, fill edges, auto crop and producing a raw pano DNG."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Create panoramas)", "https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Panorama merge projections

Photo > Photo Merge > **Panorama** (Ctrl/Cmd+M). Output: a raw-like DNG with full editing latitude.

## Projections
- **Spherical**: maps to the inside of a sphere; best for very wide (>120 deg) or multi-row panoramas.
- **Cylindrical**: keeps verticals straight; good for wide horizontal panos of landscapes and cityscapes.
- **Perspective**: keeps straight lines straight as in a rectilinear lens; only for narrower panoramas (architecture, < ~90 deg) or it stretches the edges badly.
- Lightroom auto-selects a projection; try all three in the preview.

## Edges
- **Boundary Warp** (0-100): warps the image to fill the rectangle instead of cropping. Watch for bending horizons and buildings.
- **Fill Edges**: content-aware fills transparent edges; check for repeated patterns.
- **Auto Crop**: crops to the largest rectangle without transparency.
- Create Stack groups sources and result.

## Capture tips that make Lightroom merges succeed
- Overlap 30-50%; manual exposure, manual WB, manual focus, same focal length.
- Rotate around the lens's no-parallax point (nodal slide) for close foregrounds.
- Shoot vertically (portrait orientation) for more height.

## Gotchas
- Apply lens profile corrections before merging (or let Lightroom apply them); keep identical on all frames.
- Merges fail with too little overlap or featureless sky: add a frame with a cloud or a manual control point in Photoshop/PTGui.
- Very large panos can exceed 65,000 px; Lightroom caps output at 65,000 px on the long side (512 MP).

## Verify
- [ ] At 100%, stitch seams show no doubled edges; horizon level and verticals vertical.
