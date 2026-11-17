---
id: creative-arts.comics-and-sequential-art.webcomics.webtoon-canvas-width-and-image-slicing
name: webtoon-canvas-width-and-image-slicing
category: creative-arts
field: comics-and-sequential-art
product: webcomics
tags: [webcomics, vertical-scroll, webtoon-format, webtoon-canvas-size, image-slicing, working-resolution, 800px-width]
level: practitioner
status: draft
description: "Set up vertical-scroll canvases: working width vs 800 px upload width, tall canvas segments, slicing into upload-sized images without cutting through text, and naming slices."
sources:
  - https://webtoons-static.pstatic.net/creator101/en/pdf/Creators-Resource-Handbook-Updated.pdf
  - https://www.webtoons.com/en/creators101/webtoon-canvas
  - https://help.clip-studio.com/en-us/First_Topic.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Webtoon canvas width and image slicing

**Goal:** a working file that exports to the platform's image limits cleanly, with no
slice cutting through a face or balloon.

## Know the target
- WEBTOON's creator handbook gives the upload image limit as up to **800 px wide and
  1280 px tall** per image; larger images are automatically reduced/sliced by the
  system. Check the current dashboard/help centre before publishing; specs change.
- Other platforms (Tapas, etc.) have their own widths; keep a master you can export to
  each.

## Working canvas
- Work **larger than upload width** (commonly 1600 px wide, i.e. 2x, or more) at
  ~300-600 dpi equivalent for future print, then downscale to 800 px on export. Line
  art and text stay sharp.
- Height: draw an episode as one tall canvas or several tall segments (e.g. 1600 x
  10,000-20,000 px each) to keep file sizes manageable.
- CSP has a Webtoon canvas preset and webtoon export that splits output for you (see
  the CSP user guide, Comics and webtoons chapter).

## Slicing
1. Downscale a copy to 800 px wide.
2. Slice into images up to 1280 px tall (or the current limit).
3. Move slice boundaries into empty space/gutters: never cut through a balloon,
   face or SFX. Readers see seams briefly while images load.
4. Name sequentially: `ep012_001.jpg`, `ep012_002.jpg`... (zero-padded).
5. Export JPEG (quality ~80-90) or PNG per platform limits and episode size cap.

## Verify
- [ ] Slices at or below platform limits; total episode size under the cap.
- [ ] No slice boundary crosses text or faces.
- [ ] Files named in order.
