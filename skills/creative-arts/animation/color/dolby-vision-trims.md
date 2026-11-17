---
id: creative-arts.animation.color.dolby-vision-trims
name: dolby-vision-trims
category: creative-arts
field: animation
product: color
tags: [dolby-vision, hdr, analysis, trim-pass, cmu, metadata-xml, sdr-trim, 100-nit-target, davinci-resolve, netflix]
level: sme
status: draft
description: "Master Dolby Vision in Resolve Studio: analysis, 100-nit SDR trim pass, per-shot trims, mastering display settings and exporting the metadata XML with the IMF."
sources:
  - https://partnerhelp.netflixstudios.com/hc/en-us
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dolby Vision trims

**Goal:** a PQ HDR master plus Dolby Vision dynamic metadata, so each consumer display
(from 100-nit SDR to 4000-nit HDR) gets a per-shot tone map the colourist approved.

## Concepts

- **Analysis (L1)**: per-shot min/average/max luminance computed from the HDR image. Automatic.
- **Trims (L2/L8)**: colourist adjustments (lift/gamma/gain, saturation, chroma weight, mid
  contrast) per target display. The 100-nit SDR trim is the key one; others are interpolated.
- **Mastering display (L6/L0)**: peak, primaries (P3-D65 typical) of the HDR reference.
- **Metadata XML**: delivered alongside or embedded in the IMF.

## Resolve Studio workflow

1. Project Settings - Colour Management: enable Dolby Vision, version 4.0 (or as spec requires),
   mastering display (e.g. 1000-nit P3 D65 ST.2084).
2. Grade HDR first, finish it.
3. Colour - Dolby Vision palette: **Analyse All Shots**. Re-analyse after any grade change.
4. Select the 100-nit target; monitor the SDR derivative (on a second display via CMU or
   Resolve's own tone mapping output). Trim shot by shot: typically lift shadows slightly, reduce
   gain for blown highlights, adjust saturation where tone mapping desaturates.
5. Optionally trim a 600-nit or 1000-nit target if the spec asks.
6. Export the XML (Timeline - Export - Dolby XML) and the IMF/master with DV metadata.

## Animation notes

- Big flat bright areas (daylight skies, white rooms) analyse with high average luminance; the
  automatic map dims them strongly in SDR. Expect to raise gain in those shots' SDR trims.
- Bright saturated colours (magic glows) clip hue in SDR; use saturation and chroma weight trims.
- Keep character skin and costume colours consistent shot to shot across the SDR trim; compare with
  the SDR reference stills from look development.

## Gotchas

- Changing an HDR grade after trimming invalidates analysis; re-analyse and re-check trims.
- Shot boundaries in the metadata must match the cuts; analysis on a flattened file needs scene
  detection and a conform check.
- Validate the XML (Dolby's metafier/metadata tools, or the facility's QC) before delivery.

## Verify

Play the SDR derivative through the whole episode: no shot jumps in brightness at cuts, highlights
hold detail, and the Dolby XML validates.
