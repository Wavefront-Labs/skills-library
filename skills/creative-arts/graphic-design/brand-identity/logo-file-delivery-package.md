---
id: creative-arts.graphic-design.brand-identity.logo-file-delivery-package
name: logo-file-delivery-package
category: creative-arts
field: graphic-design
product: brand-identity
tags: [graphic-design, brand-identity, brand-assets, logo-file-formats, logo-package, svg, eps, pdf, png, file-naming, colour-versions, brand-guidelines]
level: practitioner
status: draft
description: "Deliver a complete logo file package: versions, colour variants, vector and raster formats for print and screen, colour spaces, file naming, folder structure and a readme."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/SVG
  - https://helpx.adobe.com/illustrator/using/exporting-artwork.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logo file delivery package

**Goal:** a logo folder anyone (printer, web developer, sign maker, office admin) can open and pick the
right file without help.

## Matrix to produce
- **Versions:** primary (horizontal), stacked, symbol only, wordmark only, with tagline if approved.
- **Colour variants:** full colour, one-colour black, one-colour white (reversed), one-colour brand colour;
  each in spot, CMYK and RGB where relevant.
- **Formats:**
| Format | Colour space | For |
|---|---|---|
| AI / PDF (vector) | spot and CMYK | print, signage, master files |
| EPS (vector) | CMYK / spot | legacy suppliers who ask for it |
| SVG | RGB/HEX | web, apps, Figma |
| PNG transparent | sRGB | Office, social, general screen use (e.g. 500, 1000, 2000 px wide) |
| JPG | sRGB | where transparency is not supported (white background) |
| ICO / favicon set | sRGB | websites |

## Prep rules
- Text outlined, strokes expanded, no hidden objects, artboard trimmed to the logo plus clear space (or tight,
  but be consistent and state which).
- SVG: clean IDs, `viewBox` set, no embedded raster, minified (SVGO), title for accessibility.
- PNG at sizes in pixels with no unwanted halo around white versions.

## Naming and folders
- Pattern: `brand_logo-primary_fullcolour_rgb.svg`, `brand_logo-symbol_white_cmyk.pdf`.
- Folders: `/Print (CMYK, Spot)`, `/Screen (RGB)`, `/Source`, plus a **README** (PDF or TXT) explaining which
  file to use when, colour specs and clear-space rules (or link to guidelines).

## Gotchas
- White logos look invisible in file browsers; name clearly and include a preview sheet.
- RGB files sent to printers and CMYK files used on websites cause most colour complaints.
- Clients forward old versions; mark the package with version and date and ask them to remove old files.

## Verify
- [ ] Every version x colour x format combination present and opens correctly.
- [ ] A test placement in Word, a web page and InDesign uses the right file with no artefacts.
