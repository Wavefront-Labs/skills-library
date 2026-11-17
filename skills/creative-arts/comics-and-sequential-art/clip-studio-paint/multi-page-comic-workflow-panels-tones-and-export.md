---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.multi-page-comic-workflow-panels-tones-and-export
name: multi-page-comic-workflow-panels-tones-and-export
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp, clip-studio-paint-ex, clip-studio-paint-pro, manga-studio, comics-and-sequential-art, comics, manga, webtoon, multi-page, story-panel, page-manager, frame-border, frame-border-folder, divide-frame, panel-tool, vector-layer, vector-eraser, stabilization, tone-layer, screentone, lpi, refer-other-layers, close-gap, fill, 3d-model, 3d-drawing-figure, pose, perspective-ruler, batch-export, export-multiple-pages, bleed, trim, canvas-presets, cmyk-preview]
level: practitioner
status: draft
description: "Making a comic in Clip Studio Paint: multi-page project set-up with bleed, frame border folders, vector inking, refer-layer fills for flats, tone layers, 3D posing, and batch export for print or web."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clip Studio Paint: multi-page comic workflow, panels, tones and export

**Goal:** set up and finish a multi-page comic in Clip Studio Paint (CSP) with the
features that make it the default comic tool: page management, frame (panel) folders,
vector line art, tones and batch export.

> **Version note.** Menu names below follow CSP 2.x/3.x in English as I understand them;
> they move between versions and translations. **Multi-page management and batch export
> of many pages are EX features** (PRO has a limited page count — *verify current limits
> on the vendor's comparison page*). Everything here is unverified against a specific
> build; check against your version.

## 1. Project set-up
- **File › New**, choose the comic/manga use (the illustration preset has no page tools).
- Set **finished size**, **bleed width** (e.g. 3 mm, from your printer), and **resolution**
  (e.g. 600 dpi for monochrome, 350 dpi for colour — *use the publisher's spec*).
- For multi-page: tick **Multiple pages**, set page count, binding side (right for manga),
  start page (left/right), and spread options.
- The **default expression colour** (monochrome / grey / colour) matters for tones and
  export; monochrome projects output 1-bit line art.
- For vertical scroll (webtoon) choose the webtoon preset and canvas width; see
  creative-arts.comics-and-sequential-art.webcomics.vertical-scroll-episodes-and-serial-pacing.

## 2. Pages and the story workflow
- The page manager window shows all pages as thumbnails; double-click to open one.
- Add/move/delete pages from the **Story** menu. Text (dialogue) can be managed per page;
  *the Story editor for batch text editing is EX-only, as I understand it.*
- Draft your name/thumbnails on a low-opacity layer, or import rough pages.

## 3. Panels (frame borders)
- **Layer › New Layer › Frame Border** (or the Frame Border tool) creates a **frame border
  folder**: layers inside are clipped to the panel automatically.
- Use the **Divide frame border** tool to split a panel by dragging across it; gutter
  widths are set in its tool property.
- Each panel is its own folder; drawing outside spills into the next panel only if you
  move layers out.
- Edit borders with the Object tool; adjust line thickness for borderless/thick borders.

## 4. Inking on vector layers
- Ink on **vector layers**: lines can be re-thickened (Correct line width), re-shaped,
  and erased with **Vector eraser › Erase up to intersection**, which removes the stray
  overshoot between crossings in one click.
- Raise **Stabilization** in the pen's Tool property (and Post-correction) for smooth
  long strokes; too high causes lag.
- Pencils on a raster layer set to a **layer colour** of blue and reduced opacity; hide
  them for export.

## 5. Flats and colour
- **Fill tool › Refer other layers**, with **Close gap** on, fills areas bounded by line
  art on another layer. Set the line art layer as the **reference layer** (lighthouse icon)
  for consistent fills.
- Turn **anti-aliasing off** for flats; *Area scaling* can extend fills under lines.
- See creative-arts.comics-and-sequential-art.comic-colouring.flatting-rendering-and-colour-continuity.

## 6. Tones
- Select an area and use **New tone** (from the selection launcher or Layer menu) to make a
  **tone layer**; set frequency (LPI) and dot type in the Layer Property palette.
- Tones are adjustable after creation (density/LPI) — don't scale them with Transform,
  which can cause moiré.
- Materials palette includes ready textures; check how they print.

## 7. 3D and rulers
- Drag a **3D drawing figure** or 3D object from the **Materials** palette onto the canvas;
  pose it, set camera angle and lens to match the panel, then draw over it on a new layer.
- Perspective rulers (Layer › Ruler/Frame › Create perspective ruler) snap lines to
  vanishing points. Toggle snapping when not needed.

## 8. Export
- **File › Export multiple pages › Batch export** (EX) writes every page with chosen
  format, size, colour depth, and whether to include bleed/trim marks.
- Single page: **File › Export (single layer)** with output preview showing size and colour.
- Export settings: hide draft layers, choose **monochrome 2-bit/1-bit** or greyscale for
  print, sRGB for web. *Confirm which layers are marked "output" vs "draft".*

## Gotchas
- Starting in the Illustration preset and finding no page tools.
- Drawing outside a frame folder and losing art to clipping.
- Scaling tone layers → moiré.
- Forgetting draft layers are excluded from export, or that they're *included* if not set as draft.
- Mixing versions: files saved in newer versions may not open in older ones.

## Verify
- [ ] Project created with the correct size, bleed, dpi and binding.
- [ ] Each panel is a frame border folder; gutters consistent.
- [ ] Inks on vector layers; stray overshoots cleaned with vector erase.
- [ ] Flats filled with Refer-other-layers; tones set by LPI, unscaled.
- [ ] Batch export output checked at print size (and web size) before delivery.
