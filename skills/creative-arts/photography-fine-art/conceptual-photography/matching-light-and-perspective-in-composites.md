---
id: creative-arts.photography-fine-art.conceptual-photography.matching-light-and-perspective-in-composites
name: matching-light-and-perspective-in-composites
category: creative-arts
field: photography-fine-art
product: conceptual-photography
tags: [conceptual-photography, photo-compositing, light-matching, perspective-matching, horizon-line, vanishing-point, contact-shadows]
level: practitioner
status: draft
description: "Match light direction, hardness, colour and perspective (horizon line, vanishing points, lens) between composite elements so they look photographed together."
sources: ["https://helpx.adobe.com/photoshop/user-guide.html", "Hunter, Biver, Fuqua, Light Science and Magic, 5th ed.", "https://helpx.adobe.com/photoshop/using/vanishing-point.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matching light and perspective in composites

## Perspective
1. Find the plate's **horizon line** (eye level): extend converging horizontal lines to their vanishing points.
2. All elements must share that horizon - the camera height relative to each object must match.
   People standing on the same ground: their eyes sit on the horizon if the camera was at eye height.
3. Match focal length/distance: wide-angle elements pasted into telephoto plates look wrong.
4. Scale by ground-contact position, not by guess.

## Light
- **Direction**: compare shadow angles and highlight sides.
- **Hardness**: shadow edge sharpness must match.
- **Colour**: key and fill colours (warm sun, blue sky fill); sample highlights and shadows.
- **Contrast**: ratio of lit to shadow side.

## Fixes in Photoshop
- Adjust with Curves clipped to the element (per channel for colour; match black and white points to
  plate values - check with the Info panel).
- Paint **contact shadows** and cast shadows on a multiply layer using the plate's shadow colour.
- Add light wrap: blur the background onto the element's edges at low opacity (Screen).
- Match grain and sharpness last.

## Gotchas
- Elements lit from the wrong side cannot be fixed convincingly; reshoot.
- Missing contact shadows make figures float.

## Verify
- [ ] Shadow direction/hardness consistent; horizon consistent; edges blend at 100% and at print size.
