---
id: creative-arts.graphic-design.adobe-indesign.pdf-export-presets-for-print
name: pdf-export-presets-for-print
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, preflight, indesign-export, pdf-export-presets, joboptions, compression-settings, marks-and-bleeds, output-colour-conversion, high-quality-print, press-quality]
level: practitioner
status: draft
description: "Configure and share InDesign PDF export presets for print: standard choice, compression and downsampling, marks and bleeds, colour conversion, and loading printers' .joboptions."
sources:
  - https://helpx.adobe.com/indesign/using/pdf-options.html
  - https://helpx.adobe.com/indesign/using/exporting-publishing-pdf.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PDF export presets for print

**Goal:** a saved preset per output type so every PDF to the printer is identical and correct.

## Start from the right base (File > Adobe PDF Presets > Define)
| Preset | Use |
|---|---|
| **[PDF/X-4:2008]** | modern print default: live transparency, RGB allowed with output intent |
| [PDF/X-1a:2001] | older RIPs / printers demanding flattened CMYK |
| [Press Quality] | print without PDF/X compliance (some digital printers) |
| [High Quality Print] | desktop/office printing, proofs |
| [Smallest File Size] | screen review only |
Click **New** based on the closest one; name it `Printer-X_PDFX4_3mm`.

## Key panels
- **General:** Compatibility (Acrobat 7/PDF 1.6 for X-4); Pages vs Spreads (pages for print, unless told); Optimize for Fast Web View off for print.
- **Compression:** colour/greyscale **Bicubic Downsampling to 300 ppi for images above 450 ppi**; compression
  Automatic (JPEG) Maximum quality or ZIP; monochrome 1200 ppi CCITT Group 4. Never downsample below the printer's spec.
- **Marks and Bleeds:** Crop Marks on, Bleed Marks optional, Registration/Colour bars if asked; **Offset** >= bleed
  (e.g. 3 mm offset for 3 mm bleed so marks do not intrude); **Use Document Bleed Settings**; Include Slug Area if needed.
- **Output:** Color Conversion: **No Color Conversion** (X-4, keep RGB with profiles) or **Convert to Destination
  (Preserve Numbers)** with the printer's profile; Profile Inclusion Policy per standard; **Output Intent** = printer's profile.
  Ink Manager for spot-to-process if required.
- **Advanced:** Fonts subset below 100%; Transparency Flattener preset [High Resolution] (X-1a only).

## Share
- Define dialog > **Export** saves a `.joboptions` file; **Load** imports the printer's preset - use theirs when offered.
- The same .joboptions works in Illustrator, Photoshop and Acrobat Distiller.

## Gotchas
- Spreads exported for a printer who imposes themselves = rejected files. Ask.
- Marks inside the bleed (offset smaller than bleed) contaminate the bleed area.
- Downsampling too aggressively (e.g. 150 ppi "to make it smaller") ruins print quality.

## Verify
- [ ] Preset named for the job and printer; settings match the spec sheet.
- [ ] Output PDF opened in Acrobat: bleed and marks visible, PDF/X standard shown in Standards panel.
