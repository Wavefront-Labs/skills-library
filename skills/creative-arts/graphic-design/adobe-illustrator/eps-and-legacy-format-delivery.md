---
id: creative-arts.graphic-design.adobe-illustrator.eps-and-legacy-format-delivery
name: eps-and-legacy-format-delivery
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-export, eps-export, legacy-formats, save-as-legacy, pdf-compatible, dxf, transparency-flattening, logo-delivery]
level: practitioner
status: draft
description: "Deliver Illustrator art to older workflows: EPS options and limits, legacy AI versions, DXF/DWG for CAD and cutters, and safe transparency flattening."
sources:
  - https://helpx.adobe.com/illustrator/using/saving-artwork.html
  - https://helpx.adobe.com/illustrator/using/exporting-artwork.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EPS and legacy format delivery

**Goal:** files that open correctly in old software, sign-shop RIPs, embroidery and CAD tools, without losing the art.

## Which format for whom
| Recipient | Send |
|---|---|
| Printers, publishers (modern) | PDF/X-4 or PDF with fonts embedded |
| Other designers on recent CC | AI (packaged) |
| Older Adobe versions | AI saved as legacy version (Save As > Version: CS6, CS5...) |
| Sign makers, promo product suppliers, some embroiderers | **EPS** (often asked for "vector logo") or PDF; outlined text |
| CAD, laser/CNC | **DXF/DWG** (File > Export > AutoCAD Interchange/Drawing) |
| Web | SVG (see SVG export skill) |

## EPS options (File > Save As > Illustrator EPS)
- **Version:** Illustrator CS6 EPS or older if asked.
- **Preview:** TIFF (8-bit colour) - some apps show only the preview, so it must exist.
- **Transparency:** EPS does not support live transparency; overlapping effects are **flattened** using
  the chosen preset ([High Resolution] for print). Check results: flattening can split objects and
  rasterise effects.
- **Embed Fonts** (for other applications) or better: outline text first.
- **Include CMYK PostScript in RGB files**; **Compatible Gradient and Gradient Mesh Printing** for old RIPs.
- Only the active or selected artboards are saved per EPS (Use Artboards option creates one file per artboard).

## Legacy AI
Save As > Illustrator, Version drop-down. Features newer than the target version (freeform gradients,
variable fonts, some effects) are expanded or lost - Illustrator warns. Keep your current-version master.

## DXF/DWG
Export > AutoCAD Interchange File (.dxf). Choose AutoCAD version, scale (1 unit = 1 mm), **Export Selected
Art Only**, outline text. CAD tools ignore fills and gradients - only paths matter. Close paths and remove
duplicates (see path cleanup skill) for cutters.

## Gotchas
- "Vector file please" requests from non-designers: an EPS of a raster logo is still raster - check source.
- EPS colour spaces: keep CMYK for print, spot colours preserved; RGB EPS can shift in old RIPs.
- macOS Preview and many modern viewers no longer render EPS - recipients may think it is broken.

## Verify
- [ ] Re-open the exported EPS/legacy AI and compare to the master at 200%.
- [ ] Text outlined (or fonts embedded) and transparency flattened acceptably.
