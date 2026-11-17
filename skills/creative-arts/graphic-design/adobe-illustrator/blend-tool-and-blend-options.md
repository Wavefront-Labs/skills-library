---
id: creative-arts.graphic-design.adobe-illustrator.blend-tool-and-blend-options
name: blend-tool-and-blend-options
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, blend-tool, blends, specified-steps, specified-distance, smooth-color, replace-spine, reverse-front-to-back, illustrator-effects]
level: practitioner
status: draft
description: "Create Illustrator blends between shapes and colours: smooth colour vs specified steps or distance, editing the spine, replacing it with a path, and expanding for output."
sources:
  - https://helpx.adobe.com/illustrator/using/blending-objects.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blend tool and blend options

**Goal:** intermediate shapes or colours generated between two or more objects, live and editable:
stepped repeats (dotted ribbons, 3D-looking type), smooth shading, or evenly spaced copies along a path.

## Make a blend
- **Blend tool (W):** click the first object, then the second (click a matching anchor point on each for a
  controlled twist). Or select objects and Object > **Blend > Make** (Ctrl/Cmd+Alt/Option+B).
- Double-click the Blend tool (or Object > Blend > **Blend Options**) for spacing:
  - **Smooth Color:** Illustrator calculates steps for a smooth transition. Good for soft shading.
  - **Specified Steps:** exact number of intermediates (stepped retro type, halftone rows).
  - **Specified Distance:** fixed distance between steps (evenly spaced dots or stitches along a path).
  - **Orientation:** Align to Page or **Align to Path** (objects rotate with the spine).

## Edit
- Direct Selection on an end object changes colour, size or position; the blend updates live.
- The **spine** is a straight path between the end objects; edit it with the Pen and Direct Selection tools.
- **Replace Spine:** select the blend and a separate path, Object > Blend > Replace Spine. Use for text-like
  ribbon strokes or objects running around a circle.
- **Reverse Spine** swaps start and end; **Reverse Front to Back** swaps stacking order.
- Blends of strokes on open paths give smooth line-art transitions (op-art patterns, contour lines).

## Output
- Object > Blend > **Expand** turns the blend into a group of real objects (needed for some cutters, plotters
  and for editing one step). Keep an unexpanded copy on a hidden layer.
- Smooth Color blends between spot colours can create many intermediate tints; check Separations Preview.
- For smooth shading on one shape, a gradient or gradient mesh is usually lighter than a smooth blend.

## Gotchas
- Blending objects with different point counts gives twisting; match point counts or click matching anchors.
- Too many steps on complex objects slow redraw and RIPs; prefer Specified Steps with a sensible number.
- Blends between gradients and patterns are unreliable; blend solid fills.

## Verify
- [ ] Steps or distance give the intended spacing at final size.
- [ ] Spine edits behave; expanded copy exists if the vendor needs live objects.
