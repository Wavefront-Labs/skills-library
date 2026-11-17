---
id: creative-arts.graphic-design.poster-and-campaign-graphics.limited-palette-colour-impact
name: limited-palette-colour-impact
category: creative-arts
field: graphic-design
product: poster-and-campaign-graphics
tags: [graphic-design, poster-and-campaign-graphics, limited-palette, colour-impact, duotone, spot-colour, two-colour-poster, riso-style]
level: practitioner
status: draft
description: "Get impact from two or three inks: choose a palette by role, build duotones, use Multiply overprint for riso looks, and check contrast and print behaviour."
sources:
  - https://helpx.adobe.com/photoshop/user-guide.html
  - https://helpx.adobe.com/illustrator/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Limited palettes and colour impact

**Goal:** a poster or campaign with strong colour identity from 2-4 colours (plus paper), cheaper to print and easier to keep consistent.

## 1. Choose by role
- **Background/paper**, **primary** (dominant mass), **accent** (small, high-energy), optionally a dark **ink** for text.
- A common heuristic is roughly 60/30/10 area split among dominant/secondary/accent. It is a starting point, not a rule.
- Keep luminance contrast strong between text and its background; saturated hues of similar lightness vibrate against each other.

## 2. Build in the app
- **Illustrator:** create global swatches (or spot swatches for real inks), then recolour via **Edit > Edit Colors > Recolor Artwork**; editing a global swatch updates every use.
- **Duotone from a photo (Photoshop):** convert to Grayscale, then **Image > Mode > Duotone**, choose Duotone, pick the two ink colours and shape the curves; or use a **Gradient Map** adjustment layer for non-destructive control.
- **Riso or screenprint look:** put each ink on its own layer with blend mode **Multiply** so overlaps make a third colour; use halftone or grain textures for tints.

## 3. Print behaviour
- If printing with spot inks (Pantone/PMS or risograph inks), design with spot swatches and one separation per ink; on-screen mixes will not match exactly. Proof with the printer's swatch book or a physical proof.
- If printed in CMYK, convert deliberately and check saturated oranges, greens and blues for gamut loss.
- Overprint and trapping matter where spot colours touch; ask the printer.

## Failure modes
- Palette looks good on screen but two colours merge when printed or in greyscale.
- Too many near-duplicate tints; fix the tint steps (for example 100/60/30%).

## Self-check
Greyscale conversion: foreground, text and background keep distinct tones. Proof on the actual paper stock.
