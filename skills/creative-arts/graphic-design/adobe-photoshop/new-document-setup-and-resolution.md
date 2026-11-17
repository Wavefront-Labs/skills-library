---
id: creative-arts.graphic-design.adobe-photoshop.new-document-setup-and-resolution
name: new-document-setup-and-resolution
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-document-setup, photoshop-new-document, document-resolution-ppi, ppi, dpi, colour-mode, rgb, cmyk, bit-depth, print-size, pixel-dimensions, bleed]
level: practitioner
status: draft
description: "Set up a Photoshop document for its destination: pixel dimensions, ppi for print, colour mode, bit depth, profile and bleed guides."
sources:
  - https://helpx.adobe.com/photoshop/using/create-documents.html
  - https://helpx.adobe.com/photoshop/using/image-size-resolution.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# New document setup and resolution

**Goal:** a canvas that is already the right size, resolution and colour space for the
final output, so you never upsample a finished design or rebuild it in another mode.

## Decide from the output backwards
| Destination | Set up as | Notes |
|---|---|---|
| Offset/digital print | final trim + bleed at **300 ppi** (250-350 is fine), RGB working or CMYK if printer insists | Large-format viewed from metres away: 100-150 ppi at final size is plenty |
| Screen / web | pixel dimensions; ppi is **ignored** (72 is a convention) | Design at 1x, export 2x for high-density screens, or design at 2x |
| Video / motion stills | 1920x1080 or 3840x2160, sRGB or Rec.709 | Check broadcast safe areas |
| Social | the platform's pixel size (e.g. 1080x1350 portrait feed) | See a social-specs skill |

**Pixels = inches x ppi.** An A4 page (210 x 297 mm) with 3 mm bleed is 216 x 303 mm, so
at 300 ppi: 216/25.4*300 = 2551 x 3579 px.

## New Document dialog (File > New, Ctrl/Cmd+N)
1. Pick a preset tab (Print, Web, Mobile, Film & Video) or type width/height and units.
2. **Resolution:** 300 Pixels/Inch for print; leave 72 for screen.
3. **Color Mode:** RGB 8-bit for most work. 16-bit for heavy tonal edits or gradients
   (avoids banding; filters slower). CMYK only when the printer requires CMYK files and
   you will not repurpose for screen. Keeping RGB and converting at export is the
   flexible route (see the colour management skills).
4. **Advanced options > Color Profile:** sRGB for screen; Adobe RGB or your working space
   for print-bound photography. **Pixel Aspect Ratio:** Square.
5. **Artboards** checkbox if you need several sizes in one file.
6. Save the setup as a **preset** (download icon next to the name) for repeat jobs.

## Bleed in Photoshop
Photoshop has no bleed setting. Add it to the canvas size (3 mm / 0.125 in each side),
then drag guides at the trim (View > Guides > New Guide Layout with margins = bleed) and
a second set at the safe area (another 3-5 mm in). Keep text inside the safe guides.

## Gotchas
- Changing ppi in Image Size **with Resample on** changes pixels; with it **off** it only
  changes print size. Know which you want.
- Placing a 72 ppi stock image in a 300 ppi doc makes it physically 4x larger; scaling it
  down is fine, scaling up beyond 100% softens it.
- Text and shape layers are vector inside Photoshop but rasterise at export to JPEG/PNG; a
  PDF save can keep them vector (Photoshop PDF, preserve editing off for size).

## Verify
- [ ] Image > Image Size shows the final print size at >= 300 ppi (or the exact pixel size for screen).
- [ ] Mode and profile shown in the document tab / Edit > Assign Profile dialog are what you chose.
- [ ] Bleed and safe guides present for print; no critical content outside safe.
