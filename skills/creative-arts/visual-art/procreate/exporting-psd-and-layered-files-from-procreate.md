---
id: creative-arts.visual-art.procreate.exporting-psd-and-layered-files-from-procreate
name: exporting-psd-and-layered-files-from-procreate
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, procreate-export, psd-export, layered-files, share-layers, procreate-file, photoshop-compatibility, blend-mode-compatibility, file-transfer]
level: intro
status: draft
description: "Export layered work from Procreate: .procreate vs PSD, what survives in Photoshop (blend modes, masks, groups, text), sharing layers as files or PDF, and checking the file on the desktop."
sources: ["https://procreate.com/handbook/procreate/actions/actions-share/", "https://procreate.com/handbook", "https://helpx.adobe.com/photoshop/using/layer-basics.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exporting PSD and layered files from Procreate

**Goal:** move Procreate work to Photoshop or other desktop apps with layers intact
(Procreate Handbook, Actions > Share).

## Formats (Actions > Share)
- **Procreate** (.procreate): full native file incl. time-lapse; for backup and
  other iPads.
- **PSD**: layered Photoshop document; opens in Photoshop, Affinity, Krita, Clip
  Studio and others.
- **PDF**, **JPEG**, **PNG**, **TIFF**: flattened (PDF can be multi-page with
  Share Layers).
- **Share Layers**: export each layer as PNG files, a multi-page PDF, animated GIF/
  PNG/MP4 (for animation workflows).

## What carries into PSD
- Layer names, order, opacity, visibility, **groups**, most **blend modes**, layer
  masks and clipping masks: generally preserved (verify; mappings change between
  versions).
- **Text layers** become raster in PSD (in recent versions text may stay editable in
  some cases; check).
- Procreate-only features (some blend behaviours, reference layer status, drawing
  guides, Animation Assist settings) do not transfer.

## Steps
1. Duplicate the artwork in the Gallery (safety copy).
2. Actions > Share > PSD; choose Save to Files, AirDrop, cloud or app.
3. Open on desktop; compare to a flattened PNG export side by side for blend-mode
   differences; fix in Photoshop if needed.

## Gotchas
- Huge canvases with many layers make very large PSDs; trim hidden unused layers first.
- Colour profile: the canvas profile (sRGB/P3) is embedded; ensure the desktop app
  honours it.

## Verify
- [ ] PSD opens with layer names, groups and masks.
- [ ] Visual match with a flattened PNG export.
