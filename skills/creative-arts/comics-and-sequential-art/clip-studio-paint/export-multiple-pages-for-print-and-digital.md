---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.export-multiple-pages-for-print-and-digital
name: export-multiple-pages-for-print-and-digital
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-export, csp-multi-page-export, csp-print-export, batch-export, output-range, monochrome-2-tone, cmyk-export, pdf-export]
level: practitioner
status: draft
description: "Batch-export a CSP story: File > Export multiple pages, format choice, output range (trim vs bleed), colour mode (monochrome 2-tone, greyscale, RGB, CMYK), resolution scaling and naming."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://www.clipstudio.net/en/functions/
  - https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Export multiple pages for print and digital

**Goal:** every page of a story exported in one pass, matching printer or platform specs.

## Batch export
File > **Export multiple pages** > Batch export (multi-page export features depend on
edition; EX covers full story workflows). Choose:
- **Format**: TIFF or PSD for print handoff, PNG/JPEG for digital, PDF where supported.
- **Pages**: all or a range.
- **File naming**: prefix + page number with zero padding.

## Output settings dialog
| Setting | Print | Digital |
|---|---|---|
| Output range | include bleed (to the bleed edge) | inside trim (finished size) |
| Expression colour | Monochrome 2-tone (B/W books) / CMYK (colour, if printer wants it) | RGB |
| Resolution / scaling | 600-1200 dpi for monochrome, 300-400 for colour | scale to pixel width (e.g. phone/platform size) |
| Text, paper, guides | output text; exclude guides, nombre unless wanted; paper layer white | same |
| Tone output | "output tones as dots" behaviour per expression colour | greyscale-friendly |

## Colour notes
- CMYK export uses the profile set in File > Preferences/Color conversion settings;
  confirm the printer's profile, or export RGB and convert in Photoshop.
- Ensure line art is K-only if exporting CMYK directly (check in Photoshop channels).

## Verify
- [ ] File count equals page count; names sort correctly.
- [ ] Open a sample: size includes bleed (print) or trim (digital); correct colour mode
  and dpi.
- [ ] Tones render as dots in monochrome output.
