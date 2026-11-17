---
id: creative-arts.graphic-design.poster-and-campaign-graphics.large-format-print-resolution
name: large-format-print-resolution
category: creative-arts
field: graphic-design
product: poster-and-campaign-graphics
tags: [graphic-design, poster-and-campaign-graphics, large-format-print, billboard, banner-print, ppi-at-scale, scaling, viewing-distance, vector-artwork]
level: practitioner
status: draft
description: "Prepare large-format artwork: build at reduced scale, choose effective ppi by viewing distance, prefer vector, set bleed and grommet margins, and confirm with the printer."
sources:
  - https://helpx.adobe.com/photoshop/user-guide.html
  - https://helpx.adobe.com/illustrator/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Large-format print resolution and scaling

**Goal:** posters, banners, hoardings and vehicle graphics that look sharp at their viewing distance without enormous files.

## Rules of thumb (confirm with the printer)
- **Required resolution falls as viewing distance rises.** A poster read at arm's length may want 150-300 ppi at final size; a banner read from several metres is commonly supplied at roughly 50-100 ppi at final size; billboards viewed from tens of metres are often supplied far lower. These are typical practice, not a standard; ask the printer for the minimum ppi at final size.
- **Vector artwork** (logos, type, flat shapes) stays sharp at any size; use it wherever possible and outline or embed fonts as the printer instructs.

## Scaling the file
1. Ask whether the printer wants full size or a fixed fraction (1:2, 1:4, 1:10 are common). **Effective ppi at final size = file ppi divided by the scale factor** (a 1:10 file at 300 ppi is 30 ppi at final size).
2. Photoshop: **Image > Image Size**, uncheck Resample to read the effective ppi at the final width without changing pixels; resample only if you must (Preserve Details for upscales) and inspect the result.
3. Illustrator: set the artboard to the scaled size; raster effects use **Effect > Document Raster Effects Settings**, which must be set for the print ppi at that scale.
4. Start from the highest-resolution source image; avoid heavy sharpening that exaggerates at scale.

## Layout details
- **Bleed:** large formats often need more bleed than the 3 mm used for small prints; follow the printer's spec.
- **Safe zone** from the edge for text, plus extra margin where grommets, hems or pole pockets will be added.
- **Seams** on wall graphics and vehicle wraps: panels are printed in widths with overlap; keep faces and text away from seams.
- **Colour:** large solid areas show banding and rich-black differences; use the printer's recommended black and profile and ask for a proof of a swatch area.

## Self-check
Compute final-size ppi for every raster image; build on the printer's template; proof a 1:1 crop of a critical area.
