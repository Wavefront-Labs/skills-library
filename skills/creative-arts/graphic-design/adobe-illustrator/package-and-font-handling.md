---
id: creative-arts.graphic-design.adobe-illustrator.package-and-font-handling
name: package-and-font-handling
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-export, illustrator-package, find-font, resolve-missing-fonts, adobe-fonts, embed-images, handoff, font-sharing]
level: practitioner
status: draft
description: "Hand off Illustrator files completely: File > Package, resolving missing fonts, Adobe Fonts behaviour, linking vs embedding images, and licence-aware font sharing."
sources:
  - https://helpx.adobe.com/illustrator/using/package-files.html
  - https://helpx.adobe.com/illustrator/using/missing-fonts.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Package and font handling

**Goal:** the recipient opens your Illustrator file and sees exactly what you saw - no missing images or fonts.

## Before packaging
- **Type > Find Font:** lists every font used; replace stray or substituted fonts.
- **Type > Resolve Missing Fonts** (on open, pink highlights show missing fonts): activate from Adobe
  Fonts if available, or install the licensed font; do not just accept substitutes.
- **Links panel:** relink missing (red) and update modified (yellow) images.
- Delete unused swatches, symbols, brushes, graphic styles (panel menus: Select All Unused).

## File > Package
1. Save the file first. File > **Package**.
2. Options: **Copy Links**, **Collect links in separate folder**, **Relink linked files to document**,
   **Copy Fonts used in document (except Adobe Fonts and non-Adobe CJK fonts)**, **Create Report**.
3. Result: folder with the AI file, `Links` and `Fonts` folders and a report listing fonts, colours, links.
Zip the folder for transfer.

## Fonts and licences
- Desktop font licences often allow sending fonts to a **service provider** (printer) for output only,
  but not to another designer or the client. Check the EULA (see font licensing skill).
- **Adobe Fonts** are not packaged: the recipient activates them with their own Creative Cloud account.
- For recipients without the fonts who do not need to edit text: deliver a PDF with embedded fonts, or
  outlined copies (see create outlines skill).

## Linking vs embedding images
- **Linked** keeps AI files small and lets you update images; must be packaged.
- **Embedded** (Links panel menu > Embed Image) travels with the file; larger, and edits require
  unembedding. Use for small final assets or when handing a single self-contained file.

## Gotchas
- Packaging does not include images inside placed PDFs/AI files' own links - check nested assets.
- Variable fonts and font collections may not package as expected; check the Fonts folder.
- Recipients on a different OS: TrueType/OpenType work cross-platform; old PostScript Type 1 fonts are no longer supported in Adobe apps (since 2023).

## Verify
- [ ] Package folder opened on another machine shows no missing fonts or links.
- [ ] Report reviewed; font sharing within licence terms.
