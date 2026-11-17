---
id: creative-arts.visual-art.digital-illustration.rendering-light-with-layers-and-blend-modes
name: rendering-light-with-layers-and-blend-modes
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, digital-painting, rendering, lighting, light-and-shadow, blend-modes, multiply, screen, overlay, add, linear-dodge, colour-dodge, clipping-mask, flats, flatting, value-check, greyscale, photoshop, procreate, clip-studio-paint, krita, rim-light, ambient-occlusion, paint-over]
level: practitioner
status: draft
description: "Render form and light in a digital painting: flat-colour base, multiply shadow and add/screen light layers, value checks in greyscale, clipping masks, and when to flatten and paint over."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rendering light with layers and blend modes

**Goal:** turn a line drawing or silhouette into a lit, three-dimensional
illustration quickly and controllably, then finish it with painting rather than
leaving it looking "layered". Works in Photoshop, Clip Studio Paint, Krita and
Procreate (blend mode names differ slightly).

## 1. Decide the light before you paint
Write it down: key light **direction**, **colour/temperature** (warm sun, cool
moonlight), **hardness** (hard-edged shadows = small/distant source), and the
**ambient/fill** colour (often the sky or environment colour). Optionally add a
**rim light** from behind. Every later layer serves these choices.

## 2. Flats
- Fill each material/object with flat local colour on its own layer (or one layer
  with clean, selectable regions). Aim for mid-values — not too dark, or shadows
  have nowhere to go.
- Group flats; keep a hidden **ID/selection layer** with distinct colours per region
  for fast selection.

## 3. Shadow layer (Multiply)
- New layer above flats, **clipped** (clipping mask) to them, mode **Multiply**.
- Pick one colour for the shadow — a desaturated version of the ambient/fill
  colour (e.g. a muted blue-purple for outdoor daylight), not grey or black.
- Paint shadow shapes with a hard brush: form shadows (turning away from light)
  and cast shadows (blocked by other objects). Design the **shapes**; don't blend yet.
- Soften selected edges where the form turns gradually (cheeks, cylinders); keep
  cast shadows sharper near the caster.

## 4. Light layers (Screen / Add / Overlay)
- **Ambient occlusion** (optional): a Multiply layer with soft dark in contact
  points and creases.
- **Key light**: a clipped **Add (Linear Dodge)** or **Screen** layer, warm colour,
  painted where light hits most directly. Add is stronger and burns toward white;
  use low opacity.
- **Rim/bounce light**: another Add/Screen layer, thin and along edges facing the
  secondary source.
- **Overlay/Soft Light** layers to shift overall colour temperature or glow.

## 5. Check values
Add a temporary **adjustment layer** at the top (hue/saturation with saturation 0,
or a black fill in Color/Saturation mode) to view greyscale. Check:
- Is the focal point the area of highest value contrast?
- Do the light side and shadow side separate as two clear value groups?
- Is the silhouette readable at thumbnail size (zoom out to 10–20%)?
Toggle off before continuing.

## 6. Paint over
Blend-mode layers give a correct but mechanical look. When the lighting reads,
**merge a copy** (or flatten into a new paint layer) and paint on top with normal
brushes: unify edges, add texture, reflected colour, specular highlights, and
lost-and-found edges. Keep the layered version saved in case you need to revise.

## Gotchas
- **Multiply on saturated flats** produces muddy, over-saturated shadows; reduce
  layer opacity or desaturate the shadow colour.
- **Add/Screen on light flats** blows out to white. Keep flats mid-value.
- **Blend modes behave differently across apps** and colour profiles; expect small
  differences moving between Procreate and desktop.
- **Pillow shading** (lighting each object from its own centre) — check that all
  lighting obeys one direction.
- Working too zoomed in. Use a second small window/navigator of the whole image.
- **Colour profile on export**: sRGB for web; check CMYK conversion for print.

## Verify
- [ ] Light direction, colour and hardness are consistent across every object.
- [ ] Shadows use a coloured ambient tone, not black.
- [ ] Greyscale check shows clear light/shadow grouping and a focal point.
- [ ] Thumbnail-size view still reads.
- [ ] A final paint-over pass unifies edges and texture.
