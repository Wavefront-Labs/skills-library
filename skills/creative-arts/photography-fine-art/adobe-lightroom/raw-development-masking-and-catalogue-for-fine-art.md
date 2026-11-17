---
id: creative-arts.photography-fine-art.adobe-lightroom.raw-development-masking-and-catalogue-for-fine-art
name: raw-development-masking-and-catalogue-for-fine-art
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, lightroom, lightroom-classic, raw-processing, develop-module, camera-profile, adobe-standard, white-balance, tone-curve, hsl, colour-grading, masking, ai-masking, select-subject, select-sky, linear-gradient, radial-gradient, virtual-copy, snapshots, presets, catalogue, collections, keywords, xmp-sidecar, backup, capture-one, darktable, raw-editor]
level: practitioner
status: draft
description: "Lightroom Classic for fine-art work: a global-to-local raw development order, AI and gradient masking, virtual copies and snapshots for versions, and a catalogue/backup structure that survives years."
sources: ["Adobe Lightroom Classic user guide (helpx.adobe.com)", "Panel names checked from memory against recent Lightroom Classic versions; confirm in your version"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Raw development, masking and catalogue for fine-art work

**Goal:** develop raw files in Lightroom Classic to a deliberate, repeatable look, keep
every version recoverable, and manage a long-term archive. The same order applies in
Capture One or darktable (tag-equivalents above).

## 1. Import and catalogue structure
- **One master catalogue** for the archive, files organised by date folders
  (`YYYY/YYYY-MM-DD_shoot-name`). Lightroom references files; it doesn't contain them.
- On import: *Add* (files already in place) or *Copy* to your archive drive; apply
  copyright metadata preset and broad keywords.
- **Collections** (and smart collections) for projects/series — never reorganise
  folders to make a project; use collections.
- Turn on **automatically write changes into XMP** (Catalog Settings › Metadata) if you
  want edits stored beside raws too — extra safety at a small speed cost.
- Back up the catalogue (Lightroom prompts on exit) **and** the image drive separately;
  the catalogue backup does not include images.

## 2. Development order (global → local)
1. **Profile** (Basic panel, top): pick Adobe Color/Neutral/Standard or a camera-
   matching profile first; everything else builds on it.
2. **Lens corrections:** enable profile corrections and remove chromatic aberration.
3. **Crop and straighten / Transform** (Upright for architecture).
4. **White balance** — a neutral starting point, then a deliberate creative choice.
5. **Exposure, contrast, highlights, shadows, whites, blacks.** Hold Alt/Option while
   dragging whites/blacks to see clipping.
6. **Tone curve** for the signature contrast; **HSL/Colour Mixer** to control individual
   hues; **Colour Grading** wheels for shadow/midtone/highlight tints.
7. **Detail:** sharpening (use the masking slider with Alt/Option held to restrict to
   edges) and noise reduction (Denoise for high-ISO raws).
8. **Local adjustments** (Masking panel) last.

## 3. Masking
- **AI masks:** Select Subject, Select Sky, Background, People (with face/skin parts),
  Objects. Fast starting points; check edges at 100% (hair, branches).
- **Linear gradient** for skies and foregrounds; **radial gradient** for vignettes and
  light emphasis; **brush** to refine.
- **Intersect/subtract** masks (e.g. sky AND luminance range) to target precisely.
- Range masks (luminance/colour) help keep adjustments off highlights or a hue.
- Name masks ("sky −0.4", "face dodge") — essential when revisiting months later.
- Think like a darkroom printer: dodge and burn to guide the eye, subtly.

## 4. Versions
- **Virtual copies** for alternate interpretations (colour vs. B&W, crops) without
  duplicating files.
- **Snapshots** to freeze milestones ("print version 2026-03"); History is not a safe
  long-term record.
- Save your look as a **preset** only after it works on several images; apply then
  adjust per image.

## 5. Export / print hand-off
- Export TIFF 16-bit in a wide gamut (ProPhoto RGB or Adobe RGB) for printing or
  further editing; sRGB JPEG for web.
- Soft-proof before printing (see the fine-art-printing skill,
  `creative-arts.photography-fine-art.fine-art-printing.soft-proofing-paper-choice-and-editioning`).

## Gotchas
- Moving or renaming folders in the OS (outside Lightroom) breaks links — do it inside
  the Folders panel.
- Heavy AI masks and Denoise slow older machines; build previews in advance.
- Uncertain: panel names and features evolve with versions (e.g. Colour Mixer vs HSL
  naming); confirm in your version.

## Verify
- [ ] Catalogue and images backed up separately, tested restore.
- [ ] Edits follow global → local order; profile chosen first.
- [ ] No unintended clipping (Alt-drag check / histogram).
- [ ] Masks named; edges inspected at 100%.
- [ ] Final versions saved as snapshots or virtual copies.
