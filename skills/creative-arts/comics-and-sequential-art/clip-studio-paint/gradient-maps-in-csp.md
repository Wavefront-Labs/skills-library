---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.gradient-maps-in-csp
name: gradient-maps-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-colouring, csp-gradient-map, correction-layer, greyscale-to-colour, colour-grading]
level: practitioner
status: draft
description: "Colour and grade comic art with gradient maps in Clip Studio Paint: correction layer, gradient sets, greyscale painting to colour, blending modes and clipping per element."
sources:
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gradient maps

A gradient map remaps luminance to colours: dark values take the left end of the gradient, light values
the right end.

## Create
- **Layer > New correction layer > Gradient map** (non-destructive, editable), or Edit > Tonal correction >
  Gradient map (destructive on the current layer).
- Choose a gradient set (CSP ships sets and Clip Studio Assets has many), or edit nodes: click below the
  bar to add colour stops.

## Uses
1. **Greyscale to colour**: paint values in grey, then gradient-map them (skin: dark red-brown to warm
   light peach; foliage: dark blue-green to yellow-green). Clip the map to the element's layer or folder.
2. **Colour grading/mood**: correction layer over the finished page at low opacity in Overlay, Soft
   light or Color mode for a unified palette (night, sunset, flashback sepia).
3. **Monochrome to duotone** for flashbacks or covers.

## Tips
- Gradient maps work on luminance; a well-separated value painting matters more than colours.
- Combine with layer masks to limit areas.
- Save custom gradients to a gradient set for series consistency.

## Gotchas
- Applied directly to flats, all flat colours of similar value merge; clip to specific layers.
- Destructive Tonal correction can't be tweaked later; prefer correction layers.

## Verify
- [ ] Values still read in greyscale; mood matches neighbouring pages.
