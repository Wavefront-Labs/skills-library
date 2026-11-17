---
id: creative-arts.animation.blender.freestyle
name: freestyle
category: creative-arts
field: animation
product: blender
tags: [blender, freestyle, freestyle-lines, line-sets, line-style, npr, outline, edge-marks, crease-lines, contour, silhouette, render-lines, line-art]
level: advanced
status: docs-checked
description: "Freestyle line rendering: enabling per view layer, line sets (edge types, visibility, marks, collections), line style tabs and modifiers, render pass, and Line Art comparison."
sources:
  - https://docs.blender.org/manual/en/latest/render/freestyle/index.html
  - https://docs.blender.org/manual/en/latest/render/freestyle/view_layer/line_set.html
  - https://docs.blender.org/manual/en/latest/render/freestyle/view_layer/line_style/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# freestyle

Goal: render-time ink lines (silhouettes, creases, marked edges) with art-directable stroke styles, optionally as a separate pass you can composite.

## Freestyle vs Line Art

Freestyle is an edge/line based non-photorealistic render engine that works from mesh data and Z-depth at render time. Line Art is a Grease Pencil modifier (Generate) that produces editable Grease Pencil strokes in the scene (see `creative-arts.animation.blender.line-art`). Freestyle suits stills and stroke looks needing its modifiers; Line Art suits when you want strokes as scene data.

## Enabling

- Render Properties → **Freestyle** checkbox; *Line Thickness Mode*: *Absolute* (pixels, with *Line Thickness*) or *Relative* (scaled by vertical resolution relative to 480 px).
- View Layer Properties → **Freestyle** panel (header checkbox enables it per view layer): *Control Mode* (*Parameter Editor* or *Python Scripting*), *View Map Cache*, *As Render Pass*, and edge detection: *Crease Angle*, *Culling*, *Face Smoothness*, *Sphere Radius*, *Kr Derivative Epsilon*.
- There is one view map per view layer; a view map can have several line sets; each line set uses one line style (shareable).

## Line sets (View Layer Properties → Freestyle Line Set)

- *Select By*: Image Border, Visibility (Visible, Hidden, Quantitative Invisibility with Start/End), Edge Types, Face Marks, Collection.
- Edge types: Silhouette, Crease, Border, Edge Mark, Contour, External Contour, Material Boundary, Suggestive Contour, Ridge & Valley. Pick at least one; the *X* excludes a type.
- Mark edges in Edit Mode with `Ctrl E` → *Mark Freestyle Edge*; mark faces with `Ctrl F` → Face Data → *Mark Freestyle Face*.
- Details: `creative-arts.animation.blender.freestyle-line-set-selection`.

## Line style (View Layer Properties → Freestyle Line Style)

Tabs: Strokes, Color, Alpha, Thickness, Geometry, Texture.
- **Strokes**: Caps, Chaining (Plain or Sketchy with Rounds, Same Object), Splitting, Sorting, Selection, Dashed Line.
- **Color / Alpha / Thickness**: base value plus modifiers (Along Stroke, Crease Angle, Curvature 3D, Distance from Camera, Distance from Object, Material, Noise, Tangent; Calligraphy for thickness), each with *Mix* and *Influence*.
- **Geometry** modifiers: Sampling, Bezier Curve, Simplification, Sinus Displacement, Spatial Noise, Perlin Noise 1D/2D, Backbone Stretcher, Tip Remover, Polygonization, Guiding Lines, Blueprint, 2D Offset, 2D Transform.
- **Texture**: *Use Nodes*, *Spacing Along Stroke*; nodes *UV Along Stroke* and *Line Style Output* map a texture along strokes.
- Modifiers apply top to bottom. See `freestyle-geometry-modifiers` and `freestyle-thickness-color`.

## Compositing

*As Render Pass* renders the lines as a render pass instead of on top of the image; composite with an Alpha Over node. See `freestyle-pass`.

## Gotchas

- Known limitations (manual): memory demanding (all mesh objects in a view layer are loaded at once); only faced mesh objects; no edges at face intersections; no Z depth in the result; panoramic cameras not supported.
- Silhouette cannot render open meshes (planes, open cylinders); use Border or Crease there.
- *Culling* saves time and memory but may reduce quality; *Image Border* selection saves render time but can break continuity when geometry enters or leaves view.
- Edge Mark edges only draw when *Edge Mark* is enabled in the line set.
- *View Map Cache* is shared by all view layers and scenes, so it only helps when one Freestyle view layer renders repeatedly.

## Verify

- With Crease and Silhouette on a cube, lines appear in the render; marking one edge and selecting only *Edge Mark* draws just that edge.
- With *As Render Pass* on, the lines no longer sit on the image until composited with Alpha Over.

## Checked

2026-10-27 against the Blender 5.2 manual (Freestyle introduction, Render Properties, View Layer, Line Set, Line Style Strokes, Thickness, Color and Texture pages). Confirmed panel and tab names, edge types, marking shortcuts, modifier names, limitations and As Render Pass behaviour. Removed the unconfirmed 134 degree default, speed and preview comparisons, numeric style recipes, Film Transparent and Holdout, instancing, EEVEE and motion blur claims.
Method: documentation only; no commands were run.
