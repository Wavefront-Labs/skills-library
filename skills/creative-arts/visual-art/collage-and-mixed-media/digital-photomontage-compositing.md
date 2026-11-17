---
id: creative-arts.visual-art.collage-and-mixed-media.digital-photomontage-compositing
name: digital-photomontage-compositing
category: creative-arts
field: visual-art
product: collage-and-mixed-media
tags: [visual-art, collage-and-mixed-media, digital-collage, digital-photomontage, compositing, layer-masks, select-subject, colour-grading, photoshop, krita, affinity-photo]
level: practitioner
status: draft
description: "Composite a digital collage or photomontage with layers and masks: clean cutouts, matched light and perspective, colour grading and shared grain."
sources: ["https://docs.krita.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Digital photomontage and compositing

**Goal:** combine images so they read as one scene, in Photoshop, Affinity Photo, Krita, GIMP or similar.

## Workflow
1. **Plan** the horizon line, light direction and scale before sourcing images. Keep source files and names organised.
2. **Cut out non-destructively.** Make selections (automatic subject selection is a start; refine by hand with a pen or lasso tool, and check hair and fine edges), then apply as a **layer mask**, not an eraser, so the edge can be repainted.
3. **Edge quality.** Feather the mask very slightly (a fraction of a pixel to a pixel or two at normal resolution) and remove light fringing from the original background by shifting or shrinking the mask or painting out the halo.
4. **Match perspective and scale.** Match the camera angle and horizon, and size figures relative to the scene.
5. **Match light.** Add a soft shadow below objects, tint edges toward the scene's key light, and match contrast with Curves or Levels adjustment layers clipped to the subject.
6. **Grade the whole image** with a single colour look using adjustment layers on top; add shared grain or texture last to bind the pieces.
7. **Output.** Keep a layered master (PSD, KRA, TIFF) and export a flattened copy in the resolution needed. Convert to the right colour profile for print or web.

## Gotchas
- Mixed-resolution sources look wrong when one piece is upscaled; resample deliberately or keep the scale consistent.
- Cutouts from heavily compressed images show noise at the edges.
- Using other people's images carries licensing and rights issues (see the sourcing skill in this folder).

## Verify
- [ ] Zooming to 100% shows no halos or hard edges where a mask meets the scene.
- [ ] Shadows and highlights agree on a single light direction.
