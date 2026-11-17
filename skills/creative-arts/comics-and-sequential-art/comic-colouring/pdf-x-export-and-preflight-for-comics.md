---
id: creative-arts.comics-and-sequential-art.comic-colouring.pdf-x-export-and-preflight-for-comics
name: pdf-x-export-and-preflight-for-comics
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, print-production, print-specs, pdf-x, preflight, pdf-x-1a, pdf-x-4, acrobat-preflight, indesign-export]
level: practitioner
status: draft
description: "Export print-ready comic PDFs: PDF/X-1a vs PDF/X-4, bleed and marks settings, embedded fonts, image resolution and colour checks with Acrobat Preflight and Output Preview."
sources:
  - https://en.wikipedia.org/wiki/PDF/X
  - https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf
  - https://helpx.adobe.com/acrobat/using/analyzing-documents-preflight-tool-acrobat.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PDF/X export and preflight for comics

**Goal:** a PDF the printer accepts first time.

## Choose the standard (printer decides)
- **PDF/X-1a**: CMYK/spot only, no transparency (flattened), fonts embedded. Many
  printers and POD services ask for it.
- **PDF/X-4**: allows live transparency and ICC-based colour; newer RIPs prefer it.
- Use exactly what the printer's spec says.

## Export settings (InDesign/Illustrator/Photoshop "Save As PDF" with a PDF/X preset)
- Preset: PDF/X-1a:2001 or PDF/X-4:2008 (or as specified).
- **Bleed**: include document bleed (e.g. 0.125 in) on all sides.
- **Marks**: crop marks only if requested; many POD services want none.
- Pages, not spreads (unless requested).
- Compression: no downsampling below your art resolution (or downsample only above
  ~450 ppi for colour, keep line art at 1200).
- Output intent/destination profile = the printer's profile.

## Preflight
1. Acrobat Pro: Print Production > Preflight, run a PDF/X profile (and the printer's
   profile if they provide one).
2. Output Preview: check separations; line art and lettering on the Black plate only,
   overprinting; total area coverage under the printer's limit.
3. Check page size = trim, TrimBox and BleedBox set correctly.
4. Fonts embedded (or outlined).
5. Page count and order; covers as separate file if required (with spine).

## Common rejections
- No bleed or bleed too small.
- RGB images in an X-1a file.
- Low-resolution images (e.g. 72 ppi placed art).
- Fonts not embedded.
- Total ink over the limit in dark scenes.

## Verify
- [ ] Preflight passes with no errors.
- [ ] Separations, ink coverage and boxes correct.
- [ ] Matches the printer spec sheet line by line.
