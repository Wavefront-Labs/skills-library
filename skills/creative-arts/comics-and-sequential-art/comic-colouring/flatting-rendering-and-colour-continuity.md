---
id: creative-arts.comics-and-sequential-art.comic-colouring.flatting-rendering-and-colour-continuity
name: flatting-rendering-and-colour-continuity
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, comic-coloring, comics-and-sequential-art, comics, colourist, colorist, flats, flatting, flatter, rendering, cel-shading, colour-holds, color-holds, palette, colour-script, mood, lighting, cmyk, rgb, rich-black, total-ink-coverage, colour-continuity, character-colour-sheet, photoshop, clip-studio-paint, multiply-layer, magic-wand, colour-profiles]
level: practitioner
status: draft
description: "Colouring comic pages: clean flats under multiply line art, rendering styles, palette per scene, colour holds, character colour sheets for continuity, and CMYK/RGB print-web output gotchas."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flatting, rendering and colour continuity

**Goal:** colour a sequence of pages so every scene has a deliberate mood, characters
stay consistent across the book, and the files print and display correctly.

## 1. File set-up
- Work at the resolution the publisher asks for (often 300–400 dpi for colour at print
  size; line art may be supplied at higher resolution). *Always confirm specs.*
- Line art layer on top, set to **Multiply**, so colours sit beneath the black lines.
- Decide colour mode: many colourists work in RGB for flexibility and convert to CMYK at
  the end with the printer's profile; others work in CMYK throughout for print-only books.

## 2. Flatting
**Flats** are solid, unshaded areas of colour that separate every object, used later as
selection masks.
1. On a "flats" layer below line art, fill every distinct area with a flat colour,
   anti-aliasing **off** so selections are clean.
2. Flats must go **under** the line, not stop at its edge, or white gaps appear when printed.
3. Use distinctive colours (they don't need to be final) so selections are easy.
4. Many pros hire flatters; tools like Clip Studio's "refer other layers" fill or
   Photoshop actions speed it up.
5. Check for gaps by zooming in, and toggle the line art off to confirm nothing is missing.

## 3. Colour script and mood
- Before rendering, decide a **palette per scene**: time of day, location, emotion. A thumbnail
  colour pass of the whole issue (tiny pages side by side) shows the rhythm.
- Limit the palette; dominant hue + accent colour reads stronger than everything saturated.
- Use temperature and value to lead the eye: the focal point gets the highest contrast.
- Flashbacks, dreams or special scenes can get a distinct treatment (e.g. sepia, limited hue).

## 4. Rendering
- **Cel/hard-shading:** flat colour + one or two hard-edged shadow tones; graphic, fast.
- **Soft/painted rendering:** airbrushed gradients, highlights, textures; slower, more volume.
- Light source consistent within a scene; shadows on a Multiply layer, highlights on
  Screen/Add or a separate light layer.
- **Colour holds:** lines coloured (not black) for effects like fire, light, glow or soft
  backgrounds — set on the line art layer with locked transparency.
- Don't render detail the inker already gave you.

## 5. Continuity
- Make a **character colour sheet**: swatches (hex or CMYK values) for skin, hair, eyes,
  costume, key props; lighting variants (day/night) if needed.
- Use the same swatch library across all pages; eye-dropping from old pages drifts.
- Keep a location palette too.

## 6. Output
- **Print:** convert to the printer's CMYK profile; watch total ink coverage (printers
  commonly cap it around 240–300%; *their spec wins*). Black line art often prints as
  100% K only; large black areas may use a **rich black** mix as the printer specifies.
- **Web:** sRGB, export JPG/PNG at web size. Saturated RGB colours (bright greens, blues)
  shift when converted to CMYK — soft-proof before committing to a palette for print.

## Gotchas
- Anti-aliased flats leaving halo pixels on selection.
- White gaps under lines because flats stopped short.
- Overrendering until linework vanishes.
- Characters changing hair colour between issues because nobody kept a colour sheet.
- Rich black used on fine text (misregistration blur).

## Verify
- [ ] Flats complete, aliasing off, extending under lines; no gaps.
- [ ] Scene palettes planned; the focal point has the strongest contrast.
- [ ] Colour sheet used; character colours match across pages.
- [ ] Files in the publisher's colour mode/resolution; ink coverage within spec.
- [ ] Soft-proofed for print; RGB web versions exported separately.
