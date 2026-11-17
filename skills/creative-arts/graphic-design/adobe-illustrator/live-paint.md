---
id: creative-arts.graphic-design.adobe-illustrator.live-paint
name: live-paint
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-color, illustrator-swatches, live-paint, live-paint-bucket, gap-options, colouring-line-art, comic-colouring, expand-live-paint]
level: practitioner
status: draft
description: "Colour line art with Illustrator Live Paint: Live Paint groups, bucket fills for faces and edges, gap options for open art, merging paths and expanding for output."
sources:
  - https://helpx.adobe.com/illustrator/using/live-paint-groups.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Live Paint

**Goal:** colour line drawings like a colouring book - fill enclosed regions without building closed shapes.

## Make a Live Paint group
1. Select the line art (strokes and/or shapes, including traced art).
2. **Live Paint Bucket (K)** and click the selection, or Object > Live Paint > Make (Alt/Option+Ctrl/Cmd+X).
3. The art becomes a Live Paint group: every region bounded by paths is a **face**, every segment between
   intersections is an **edge**.

## Painting
- Hover: the face highlights red. Click to fill with the current fill colour.
- The cursor shows three swatches; **left/right arrow keys** cycle through swatches without leaving the tool.
- Drag across several faces to fill them in one go; double-click fills across edges of the same colour;
  triple-click fills all faces with the same colour.
- **Edges:** double-click the tool for options, tick Paint Strokes; Shift+click an edge to colour or
  remove (set stroke None) - delete construction lines visually without breaking the regions.
- **Live Paint Selection tool (Shift+L)** selects faces/edges for changing colour via Swatches.

## Gap options (Object > Live Paint > Gap Options)
Sketchy line art rarely closes. Set **Paint stops at** Small/Medium/Large gaps or a custom distance;
preview shows gaps detected; **Close gaps with paths** makes them permanent.

## Editing the drawing
- Draw new paths and **Merge** them into the group (select both, Object > Live Paint > Merge) - new
  regions form automatically; fills reflow.
- Edit paths with Direct Selection; fills follow the new boundaries.

## Output
Object > Live Paint > **Expand** converts to ordinary filled shapes and strokes (grouped). Needed
for many exports, recolouring workflows and other apps. Keep a live copy.

## Gotchas
- Live Paint groups cannot contain text, images or brushes directly - outline text, expand brushes first.
- Large detailed groups slow down; split into several groups.
- Fills hidden behind white areas still exist; check in Outline mode after expanding.

## Verify
- [ ] All regions filled, no gaps leaking colour into neighbours.
- [ ] Expanded copy produced for output; live version kept for edits.
