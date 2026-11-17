---
id: creative-arts.visual-art.procreate.canvas-setup-and-export-for-print-and-web
name: canvas-setup-and-export-for-print-and-web
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, ipad, apple-pencil, custom-canvas, canvas-size, dpi, layer-limit, colour-profile, display-p3, cmyk, time-lapse, export, psd, png, tiff, jpeg, pdf, digital-art, art-prints]
level: intro
status: docs-checked
description: "Set up Procreate canvases you won't regret: size and DPI, the layer-limit trade-off, colour profile choice, time-lapse settings, and exporting PSD, PNG, TIFF and PDF."
sources:
  - https://help.procreate.com/procreate/handbook/gallery/gallery-create
  - https://help.procreate.com/procreate/handbook/colors/colors-profiles
  - https://help.procreate.com/procreate/handbook/actions/actions-share
  - https://help.procreate.com/procreate/handbook/actions/actions-video
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Canvas setup and export for print and web

**Goal:** choose canvas settings at the start that still work when the piece is printed
large, posted online, or opened in Photoshop.

## 1. Size and DPI: decide the biggest use first
- A custom canvas lets you set width, height and DPI, in millimetres, centimetres, inches
  or pixels. The upper size limit depends on your iPad model.
- Print pixels = inches x DPI. Ask your printer for the DPI they need rather than assuming.
- Start at the largest size you might need; upscaling later resamples pixels.
- Presets include Screen Size, Square, 4K, A4 paper, 4 x 6 Photo and US Paper. Swipe left
  on a preset and tap Edit to change it in the Custom Canvas screen.

## 2. The layer-limit trade-off
Changing canvas size changes the Maximum Layers available: larger canvases allow fewer
layers. You can check the limit while editing the canvas, and it depends on your iPad,
so check before promising a client a size.

## 3. Colour profile
- RGB suits artwork for screens; CMYK suits artwork destined for print.
- Procreate includes seventeen profiles; the defaults are Display P3 and Generic CMYK. You
  can import your own. Display P3 allows more saturated greens, reds and oranges.
- You can change the profile later (Actions > Canvas > Canvas information > Color profile)
  only within the same space: RGB to CMYK or the reverse is not possible. Changing it can
  dramatically affect the time-lapse, so do it after the artwork is finished.
- Decide RGB or CMYK at canvas creation, and run a test print to judge colour.

## 4. Time-lapse
- Enabled by default for a new canvas, at 1080p on the Good quality setting, and these
  settings cannot change mid-project. Each canvas can use 1080p up to 4K and quality from
  Low to Lossless.
- Toggle Time-lapse Recording off in Actions to pause it for one artwork; Help > Advanced
  Settings has an iPad setting that disables it for all artworks (anything drawn while
  disabled cannot be recovered).
- Export either Full length or 30 Seconds (frames removed to speed it up).
- A transparent-background time-lapse needs the sRGB IEC61966-2.1 profile with HEVC enabled.

## 5. Export formats (Actions > Share)
- **Procreate:** native file keeping layers, masks, effects, canvas info and time-lapse.
- **PSD:** layered, keeps layer names, opacity, visibility and blend modes.
- **PDF:** Good, Better or Best quality, suited to digital distribution and print houses.
- **JPEG:** flattened, small. **PNG:** flattened, lossless, keeps transparency.
  **TIFF:** flattened, quality preserved, common in print workflows.
- **Share Layers** exports only visible layers: multi-page PDF, one PNG per layer, or
  animated GIF/PNG/MP4/HEVC with each layer as a frame.

## Verify
- [ ] Canvas pixel size covers the largest intended print at the printer's DPI.
- [ ] Layer count at that size is enough for your workflow.
- [ ] RGB or CMYK chosen deliberately before starting.
- [ ] Time-lapse resolution and quality chosen before starting, if you need the video.
- [ ] A Procreate-format export exists outside the app as a backup.

## Checked
2026-11-01. Confirmed on the Procreate Handbook pages in sources: canvas units, size and
layer relationship, presets, profiles and their change limits, time-lapse defaults and
export, share formats. Removed as not stated there: worked pixel sizes, web size ranges,
sRGB-for-web advice, PSD blend-mode caveats, backup and iCloud claims, per-format
recommendations beyond the pages.
Method: documentation only; no commands were run.
