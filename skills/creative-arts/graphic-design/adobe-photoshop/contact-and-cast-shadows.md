---
id: creative-arts.graphic-design.adobe-photoshop.contact-and-cast-shadows
name: contact-and-cast-shadows
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, compositing, cast-shadows, contact-shadow, ambient-occlusion, multiply-blend, photo-manipulation]
level: practitioner
status: draft
description: "Ground composited objects with contact shadows and cast shadows: light direction, multiply layers, falloff with blur and gradient masks, and colour-matched shadow tone."
sources:
  - https://helpx.adobe.com/photoshop/using/blending-modes.html
  - https://helpx.adobe.com/photoshop/using/applying-specific-blurs.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Contact and cast shadows

**Goal:** a cut-out object sits on the surface instead of floating.

## Two shadows, always
1. **Contact (occlusion) shadow** - the dark sliver where object meets surface. Tight, dark, short.
2. **Cast shadow** - shape thrown away from the light; longer, softer the further from the object.

## Contact shadow
- New layer below the object, blend mode **Multiply**.
- Soft round brush, 0% hardness, low flow (10-20%), colour sampled from the darkest shadow
  in the plate (never pure black). Paint a thin line along the contact edge.
- Add a second, wider and lighter pass for ambient occlusion.

## Cast shadow
1. Duplicate the object, Lock Transparent, fill with the shadow colour, unlock.
2. Edit > Transform > Distort: flip and skew it along the light direction so its base stays
   attached to the object's base. Length/angle follows existing shadows in the plate.
3. Blend mode Multiply, opacity to match existing shadows (sample their darkness with Info panel).
4. Falloff: Filter > Blur Gallery > Tilt-Shift or a gradient mask so the shadow is sharp
   near the object and softens/lightens with distance. Convert to smart object first to keep it editable.

## Matching
- Shadow colour carries ambient light: outdoors it is slightly blue, indoors warm. Sample from the plate.
- Overcast plate = no hard cast shadow; only soft occlusion.
- Shadows fall onto other surfaces (walls, steps) - break the shape with Warp where it crosses.

## Verify
- [ ] Shadow direction matches every other shadow in the plate.
- [ ] Darkest value of the new shadow matches the plate's darkest shadow (Info panel).
- [ ] At 25% zoom the object reads as grounded.
