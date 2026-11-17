---
id: creative-arts.photography-fine-art.adobe-lightroom.export-colour-space-and-file-format
name: export-colour-space-and-file-format
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, export-color-space, lightroom-export, file-format, bit-depth, srgb, lightroom-classic]
level: practitioner
status: draft
description: "Pick export colour space and file format in Lightroom Classic: sRGB vs Adobe RGB vs ProPhoto, JPEG vs TIFF vs PNG vs AVIF/JXL, bit depth and compression."
sources: ["https://helpx.adobe.com/lightroom-classic/desktop/export-photos/exporting-photos-basic-workflow.html", "https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/hdr-output.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export colour space and file format

## Colour space
- **sRGB**: web, social, email, most consumer labs and online competitions. Anything uncolour-managed assumes sRGB.
- **Adobe RGB (1998)**: larger greens/cyans; for pro labs and publishers who request it.
- **ProPhoto RGB**: Lightroom's working space; for 16-bit TIFF masters and round-trips to Photoshop. Never as 8-bit JPEG (banding, dull colours elsewhere).
- **Display P3**: wide-gamut screens (Apple devices); good for AVIF/JPEG XL web delivery to modern browsers.
- **Other...**: a paper/printer ICC profile when a lab requests conversion to their profile.

## Format
| Format | Use | Notes |
|---|---|---|
| JPEG | Delivery, web, labs | 8-bit, Quality 80-90 web, 100 lab |
| TIFF | Masters, print, archive | 16-bit; compression ZIP (lossless); no layers |
| PSD | Photoshop masters | 16-bit; "Maximize compatibility" in PS for previews |
| PNG | Graphics, lossless web | Large files for photos |
| DNG | Raw archiving or sharing an editable raw | Embed fast load data; lossy DNG options exist |
| AVIF / JPEG XL | Modern web, HDR output | Check client support |
| Original | Exact copy of source + XMP | Archiving |

## HDR export
With HDR editing on, JPEG export can include a gain map; AVIF/JPEG XL/TIFF hold HDR data directly. Use only when the destination displays HDR.

## Gotchas
- Choosing ProPhoto 8-bit is the most common export error.
- Lightroom embeds the profile in exports; never strip it.

## Verify
- [ ] Open the export in Photoshop: Image > Mode bit depth and Edit > Assign Profile show the intended space.
