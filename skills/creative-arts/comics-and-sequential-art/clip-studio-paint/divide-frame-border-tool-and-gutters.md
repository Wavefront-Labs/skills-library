---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.divide-frame-border-tool-and-gutters
name: divide-frame-border-tool-and-gutters
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-frame-border, csp-divide-frame, frame-border-tool, gutter-width, panel-layout, frame-gap]
level: practitioner
status: draft
description: "Panel a page in Clip Studio Paint: create a frame border folder, divide it with the divide/cut frame border tool, set horizontal and vertical gaps, and adjust borders with the Object tool."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://tips.clip-studio.com/en-us
  - https://www.clipstudio.net/en/functions/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Divide frame border tool and gutters

**Goal:** fast, consistent panel layouts with exact gutters.

## Steps
1. Create a frame border: Layer > New layer > Frame Border folder (or the Frame border
   tool > Rectangle frame drawn around the base frame). It defaults to the base frame.
2. Select the **Divide frame border** sub tool (called "Cut frame border" in some
   versions) under the Frame border tool.
3. In Tool property set **Horizontal gap** and **Vertical gap** (gutter widths). Many
   artists use a larger horizontal gap (between tiers) than vertical.
4. Drag across the frame to split it: horizontal drags create tiers, vertical drags
   split panels. Hold Shift for straight 90/45-degree cuts; angled drags create slanted
   gutters.
5. Each new panel becomes its own frame border folder in the Layer palette.

## Adjusting
- **Object tool** (Operation > Object): select a frame border; drag control points or
  edges; gaps between adjoining panels can move together.
- Change line width of the border in the frame's tool property with the Object tool.
- Merge/delete panels by deleting folders and re-dividing.

## Tips
- Turn snapping off if borders jump to rulers unexpectedly (View > Snap to ruler).
- Save a good layout as a material (drag frame folders to the Material palette) to
  reuse as a template.

## Verify
- [ ] Gutters match chosen measurements on every page.
- [ ] Each panel is its own frame folder (for masking art).
