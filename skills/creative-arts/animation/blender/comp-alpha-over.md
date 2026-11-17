---
id: creative-arts.animation.blender.comp-alpha-over
name: comp-alpha-over
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, alpha-over, premultiplied, straight-alpha, compositing]
level: practitioner
status: docs-checked
description: "Layer images with Alpha Over: Over, Disjoint and Conjoint types, Straight Alpha option, premultiplied renders, Alpha Convert node, and fixing dark or light fringes."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/color/alpha_over.html
  - https://docs.blender.org/manual/en/latest/compositing/types/color/alpha_convert.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/film.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# comp-alpha-over

Goal: clean edges when layering foreground over background.

## Alpha Over node (Color category)

Inputs: **Background**, **Foreground**, **Factor** (foreground opacity, 0 to 1), **Type** and **Straight Alpha**.
- **Type**: **Over** (standard), **Disjoint Over** (assumes the background has been held out by the foreground, cleaner edges when stacking several layers) or **Conjoint Over** (assumes the foreground overlaps the background).
- **Straight Alpha**: enable only when the foreground has been explicitly converted to straight (non-premultiplied) alpha. Most images in the compositor are premultiplied, so leave it off in most cases.

## Which alpha is which

Premultiplied alpha is the standard in Blender rendering and compositing. Render layers are premultiplied, and images loaded into rendering or compositing are converted to premultiplied. To do an operation on straight alpha (typically colour correction), use the **Alpha Convert** node with **Type** set to To Straight or To Premultiplied. If you convert to straight in the compositor, convert back to premultiplied before the Group Output node, or artifacts can appear.

## Fringes

- **Dark halo** around the foreground: a premultiplied image being treated as straight. Turn Straight Alpha off.
- **Light or coloured halo**: a straight image being treated as premultiplied. Convert it with Alpha Convert (To Premultiplied) or enable Straight Alpha if the foreground really is straight.
- Grading premultiplied images: colour correction on premultiplied edges changes them. Convert to straight with Alpha Convert, grade, then convert back.

## Gotchas

- **Film > Transparent** (Render Properties) must be on to render the background transparent, otherwise there is nothing to composite over.
- An RGB image with no alpha covers everything beneath it.

## Verify

Place a soft-edged render over a white and then a black background. No dark or light ring should show at the edges on either.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Alpha Over inputs Background, Foreground, Factor, Type (Over, Disjoint Over, Conjoint Over) and Straight Alpha; premultiplied is the standard; Alpha Convert node and its To Premultiplied and To Straight types; Film > Transparent renders the background transparent. Removed the unconfirmed Convert Premultiplied checkbox, Premultiplied slider and the table of PNG/EXR alpha types.
Method: documentation only; no commands were run.
