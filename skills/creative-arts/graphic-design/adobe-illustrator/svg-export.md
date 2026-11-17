---
id: creative-arts.graphic-design.adobe-illustrator.svg-export
name: svg-export
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-export, svg-export, svg, svgo, viewbox, css-properties, responsive-svg, icon-svg, web-graphics]
level: practitioner
status: draft
description: "Export clean, small SVGs from Illustrator: preparing art, Export As SVG options (styling, fonts, decimals, minify, responsive) and post-optimising with SVGO."
sources:
  - https://helpx.adobe.com/illustrator/using/svg.html
  - https://github.com/svg/svgo
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SVG export

**Goal:** SVG files that are small, render identically in browsers and are easy for developers to style.

## Prepare the art
- Artboard fitted to the art (Object > Artboards > Fit to Artwork Bounds) or to a fixed icon grid; the
  artboard becomes the `viewBox`.
- **Outline strokes** where stroke scaling matters, or keep strokes if devs will animate/style them.
- **Unite** overlapping shapes of the same colour (fewer paths); remove hidden/empty objects; expand
  appearances, brushes, symbols where needed.
- Convert text to outlines for logos/icons (or keep live text deliberately and specify fonts).
- Name layers/objects meaningfully - names become `id`s.

## File > Export > Export As > SVG (use Export As, not Save As)
| Option | Recommended |
|---|---|
| Styling | **Presentation Attributes** (most portable) or Internal CSS (classes, easier theming); avoid Inline Style |
| Font | Convert to Outlines (logos) or SVG with system fallbacks |
| Images | **Link** or Embed; prefer no raster in SVG |
| Object IDs | Layer Names / Minimal / Unique |
| Decimal | 1-2 for icons, 3 for detailed art |
| Minify | on for production |
| Responsive | on removes width/height so it scales to its container (developers often prefer explicit sizes for icons - ask) |

Export for Screens and Asset Export use the same SVG settings via their gear icon.

## Post-optimise
Run **SVGO** (CLI `npx svgo file.svg`, or SVGOMG web UI) to remove metadata, collapse groups, round
numbers. Check visually after: aggressive settings can merge paths or break masks.

## What SVG cannot do well
Freeform gradients, gradient meshes, many effects (drop shadows, blurs) export as **embedded rasters**
or heavy filters. Keep web icons to flat shapes and linear/radial gradients.

## Theming
For `currentColor` theming (icons that inherit text colour), set fill to black in Illustrator, export,
then replace `fill="#000"` with `fill="currentColor"` (or let devs do it in the build).

## Verify
- [ ] Open the SVG in a browser: looks identical to the artboard.
- [ ] Code inspection: no embedded `<image>` unless intended, sensible size (simple icon < 2 KB).
- [ ] viewBox matches the intended bounds/grid.
