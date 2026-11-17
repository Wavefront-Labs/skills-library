---
id: creative-arts.graphic-design.information-design.exploded-and-cutaway-views
name: exploded-and-cutaway-views
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, exploded-view, cutaway, technical-illustration, axonometric, assembly-diagram, callout-numbers]
level: advanced
status: draft
description: "Draw exploded and cutaway technical views: choose an axonometric view, separate parts along assembly axes, add explosion lines, callouts and a parts key."
sources:
  - https://helpx.adobe.com/illustrator/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exploded and cutaway technical views

**Goal:** a drawing that shows how parts fit together (exploded) or what is inside (cutaway) with correct relationships and legible callouts.

## 1. Choose the projection
- **Isometric or another axonometric view** keeps parallel lines parallel and is easy to measure; use perspective only for a more pictorial feel.
- Pick the viewing angle that shows the most parts and hides the least; keep it the same across a series.

## 2. Exploded view
1. Start from the assembled drawing (from CAD export or traced from a photo or scan).
2. Identify the **assembly direction** of each part (usually along a fastener axis) and move parts along that line only.
3. Separate in assembly order, spacing proportionally to part size so the diagram reads as one object; keep overlaps minimal.
4. Draw **explosion lines** (thin dash-dot or thin solid) through the centre axes of holes, shafts and fasteners to show alignment.
5. Hide lines that are hidden by nearer parts, or reduce their weight; check overlaps with a white stroke or Pathfinder.

## 3. Cutaway view
- Remove a clean wedge or section from the outer shell to reveal inside parts; the cut face shows a flat tone or hatching, with interior parts in line.
- Use stronger line weight on the silhouette, lighter on interior detail, and consistent light direction for shading.

## 4. Callouts and key
- Number parts with callout leader lines that do not cross; place numbers around the outside in order, with a **parts key** (number, name, quantity).
- Keep type consistent in size; numbers legible at the final print size.

## 5. Illustrator workflow
- Layers: Outline, Detail, Fill, Callouts. Use the Pen tool, Pathfinder, and **Object > Path > Offset Path** for walls and flanges.
- Group each part so it moves as a unit along the assembly axis (use **Object > Transform > Move** with an angle for exact travel).
- Use global colour swatches to colour code assemblies.

## Failure modes
- Parts shifted off their assembly axis.
- Inconsistent viewing angles between parts.
- Callout leaders crossing parts.

## Self-check
Check each moved part still lines up with its explosion line, and that the parts list numbers match the numbers on the drawing.
