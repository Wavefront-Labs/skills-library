---
id: creative-arts.graphic-design.poster-and-campaign-graphics.image-and-headline-integration
name: image-and-headline-integration
category: creative-arts
field: graphic-design
product: poster-and-campaign-graphics
tags: [graphic-design, poster-and-campaign-graphics, image-text-integration, headline-on-image, text-on-image, scrim, subject-masking, poster]
level: practitioner
status: draft
description: "Place a headline with a photo so both work: choose quiet space, add contrast by tone or a scrim, or mask the subject in front of the text for depth."
sources:
  - https://helpx.adobe.com/photoshop/user-guide.html
  - https://www.w3.org/WAI/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Integrating image and headline

**Goal:** headline and picture read as one composition, with the text legible at the intended viewing distance.

## 1. Choose or crop the image for the text
- Find the **quiet area** (sky, wall, out-of-focus background, plain clothing) and put the headline there. If the photo has none, crop or extend the canvas (Photoshop's content-aware and generative fill features can extend a background; inspect results for artefacts).
- Do not run text across a face or the focal point.
- Line the text up with something in the picture (horizon, building edge, eye line) so it looks placed.

## 2. Get contrast
- Compare headline and background luminance, not just hue. For screen graphics aim for at least the WCAG 4.5:1 contrast ratio for normal text (3:1 for large text); print has no formal ratio but the same logic holds.
- If the background is busy: a **scrim** (a gradient layer from black at roughly 40-60% opacity to transparent behind the text), a subtle **Multiply** colour overlay on the whole photo, or a tonal shape under the text.
- A drop shadow is a weak primary fix; it blurs at small sizes.

## 3. Text behind the subject (depth effect)
1. Place the photo and set the headline above it.
2. Duplicate the photo layer, move it above the type, and add a layer mask that reveals only the subject (**Select > Subject**, refine with **Select and Mask**, check hair and edges at 100%).
3. The type now sits between background and subject. Keep enough of each letter visible that the word still reads.

## 4. Match style
Pick accent colours from the image with the Eyedropper; keep the typeface character in tune with the mood of the picture.

## Failure modes
- Fuzzy mask edges on the cut-out subject.
- Light grey text over a mid-tone photo.
- Small text pushed into the busiest area.

## Self-check
Convert to greyscale and view small: the headline must still stand out; if it only works in colour, increase tonal contrast.
