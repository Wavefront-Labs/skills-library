---
id: creative-arts.graphic-design.adobe-photoshop.export-as-and-quick-export
name: export-as-and-quick-export
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-export, export-as, quick-export, png, jpeg, webp, svg, srgb, retina, 2x-export, file-size, metadata]
level: practitioner
status: draft
description: "Export screen assets from Photoshop with Export As and Quick Export: format choice, quality, 1x/2x scales, sRGB conversion, metadata, and checking file weight before delivery."
sources:
  - https://helpx.adobe.com/photoshop/using/export-artboards-layers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Export As and Quick Export

**Goal:** light, colour-correct screen images at the sizes developers and platforms need.

## Export As (File > Export > Export As, Alt+Shift+Ctrl+W / Opt+Shift+Cmd+W)
Works on the whole document, selected artboards or selected layers (right-click layers >
Export As).
1. **Format:**
   - **JPEG** - photos; quality 60-80% is usually invisible loss. No transparency.
   - **PNG** - flat graphics, UI, anything with transparency. Tick "Smaller File (8-bit)"
     for simple flat art; leave 24-bit for gradients and soft shadows.
   - **WebP** (Photoshop 23.2+) - smaller than JPEG at similar quality; check that the target
     platform accepts it.
   - **GIF** - only for legacy simple animation; prefer PNG.
   - SVG is no longer reliable from Photoshop; produce SVG in Illustrator.
2. **Scale / suffix:** add 1x and 2x (and 3x for native mobile) with suffixes `@2x` - one click
   produces the whole set.
3. **Image Size / Canvas Size:** resize on export without touching the PSD.
4. **Metadata:** None (strips camera/GPS data; smaller files) or Copyright and Contact Info.
5. **Color Space:** tick **Convert to sRGB** and **Embed Color Profile** for web; the export
   then looks right in all browsers.
6. Check the estimated file size in the preview panel before saving.

## Quick Export
File > Export > Quick Export as PNG uses defaults set in Preferences > Export (format,
location, metadata, colour space). Set PNG/JPEG + quality + "Export files to an assets
folder next to the current document" once, then it is one click.

## Exporting layers and groups
Right-click layers > Export As exports each layer or group as its own file, trimmed to its
pixels. For repeatable exports with naming, use Generate > Image Assets (see that skill).

## Gotchas
- Export As ignores slices; for sliced legacy layouts use Save for Web (Legacy).
- Exporting a CMYK document converts to RGB; check colours look as intended.
- A layer effect extending beyond the layer (drop shadow) is included in the trim; extra
  transparent padding can surprise developers - check exported dimensions.
- Large photos for web: resize to the largest displayed size x2, not the camera original.

## Verify
- [ ] Open the exported file in a browser: colours match the PSD, edges clean.
- [ ] Dimensions and suffixes match the developer spec; file weight within budget (e.g. hero < 300 KB).
