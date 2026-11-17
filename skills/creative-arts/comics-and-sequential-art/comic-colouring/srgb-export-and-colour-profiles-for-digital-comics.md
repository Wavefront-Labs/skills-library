---
id: creative-arts.comics-and-sequential-art.comic-colouring.srgb-export-and-colour-profiles-for-digital-comics
name: srgb-export-and-colour-profiles-for-digital-comics
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, digital-comic-colour, srgb-export, colour-profile, embed-profile, export-as, webtoon, digital-distribution]
level: practitioner
status: draft
description: "Export comic pages for screens: convert to sRGB, embed or strip profiles deliberately, JPEG/PNG choices, and avoid colour shifts on web and webtoon platforms."
sources:
  - https://helpx.adobe.com/photoshop/using/converting-between-color-modes.html
  - https://webtoons-static.pstatic.net/creator101/en/pdf/Creators-Resource-Handbook-Updated.pdf
  - https://en.wikipedia.org/wiki/Webcomic
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sRGB export and colour profiles for digital comics

**Goal:** colours on readers' phones and browsers match what you approved.

## Rules
1. **Convert to sRGB** for web/app delivery (Edit > Convert to Profile > sRGB IEC61966-2.1).
   Wide-gamut working spaces (Adobe RGB, Display P3) look oversaturated or dull when a
   platform ignores the profile.
2. If working in CMYK for print, make the digital edition from the RGB master, not from
   CMYK files (CMYK -> RGB loses saturation).
3. **Embed the sRGB profile** or strip it consistently; most platforms assume sRGB.
   Photoshop Export As has "Convert to sRGB" and "Embed Color Profile" options.

## Format
- **JPEG** quality ~80-90% for painted/gradient pages; small size, good quality.
- **PNG** for flat colour and crisp line art with large flat areas (no JPEG artefacts),
  but check platform size limits.
- Check platform requirements (e.g. WEBTOON CANVAS image width/size limits in the
  creator handbook).

## Check
- View exports in a browser and on a phone, not only in your editor.
- Compare against the master in Photoshop's proof set to Monitor RGB / Internet
  Standard RGB.

## Gotchas
- Exporting CMYK JPEGs: many browsers/platforms display them wrongly or reject them.
- Saving with "Save for Web" legacy defaults that strip profiles from a non-sRGB file
  causes colour shifts.

## Verify
- [ ] Exports are sRGB, correct format and size.
- [ ] Phone and browser view matches the approved master.
