---
id: creative-arts.animation.blender.smooth-flatten-scrape
name: smooth-flatten-scrape
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, smooth-flatten-scrape, flatten-brush, scrape-brush, multiplane-scrape, fill-brush, planes, hard-surface-sculpt]
level: practitioner
status: docs-checked
description: "Plane down and refine sculpts in Blender with Smooth, Flatten/Contrast, Scrape/Fill, Multiplane Scrape and the Plane brush type: Height, Depth, plane offset and trim."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/smooth.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/plane.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/multiplane_scrape.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/brushes.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/brush_settings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# smooth-flatten-scrape

Goal: subtractive and planing passes that turn lumpy clay into defined planes.

## Smooth (hold Shift with any brush)

- The brush named Smooth is used whenever you hold Shift while sculpting; to change its strength or behaviour, switch to the Smooth brush and edit its settings. The Smooth brush has its own shortcut, S.
- Strength is relative to mesh density: if you add resolution, raise the strength.
- Direction (Ctrl): Smooth or Enhance Details (smoothing in the opposite direction).
- Deformation: *Laplacian* (default; smooths surface and volume) or *Surface* (smooths only the surface and preserves volume) with **Shape Preservation**, **Per-Vertex Displacement** and **Iterations**.
- The same operations exist as Smooth and Surface Smooth Mesh Filters for all unmasked areas.

## Plane-family brush assets (brush type: Plane)

- **Flatten/Contrast**: pushes vertices to an average height to flatten; inverted pushes them away for contrast.
- **Plateau**: like Flatten with locked orientation and depth for a consistently flat surface.
- **Fill/Deepen**: pushes surfaces up toward a flat plane; with Ctrl deepens existing holes.
- **Scrape/Fill** (Shift-T): pushes surfaces inward; with Ctrl fills. The manual calls it the most common brush for flattening meshes.
- **Trim**: pushes surfaces inward toward a locked direction; depth set by going deeper along the stroke.
- Plane type settings: **Height** (range of influence above the brush plane), **Depth** (below it), **Inversion Mode** (Invert Displacement increases contrast; Swap Height and Depth exchanges the two), **Stabilize Normal** and **Stabilize Plane** (0 reacts immediately, 1 keeps orientation or position constant through the stroke).
- General settings that matter here: **Plane Offset** (shifts the averaged plane above or below), **Plane Trim** (ignore vertices further than the trim distance from the offset plane), and **Sculpt Plane** (Area Plane, View Plane, X/Y/Z) plus **Original Normal** and **Original Plane** (keep using the stroke-start normal or plane).

## Scrape Multiplane

Scrapes with two angled planes at once, creating a sharp edge between them; good for hard-surface forms. **Plane Angle** sets the angle between the planes (Ctrl inverts it). **Dynamic Mode** updates the angle from the surface under the brush; Plane Angle then sets how much the angle grows with pen pressure, and Ctrl locks the angle to 0 degrees. **Show Cursor Preview** displays the two planes.

## Gotchas

- Plane Trim limits how far from the plane vertices are affected, which keeps strokes from gouging.
- Front Faces Only (Advanced) limits the brush to vertices facing the viewer.

## Verify

Cavity or matcap shading from a raking angle shows flat facets where intended and no chatter marks.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/brushes (smooth, plane, multiplane_scrape, brushes list) and brush/brush_settings: Smooth behaviour on Shift and S, Strength relative to density, Laplacian and Surface settings, Plane family brush names and shortcut Shift-T for Scrape/Fill, Height, Depth, Inversion Mode, Stabilize options, Plane Offset and Trim, Sculpt Plane, Multiplane Scrape controls. Removed the unconfirmed 4.3 gate for the Planes brush, the 60 to 120 degree range, the 0.3 smooth strength and Dyntopo collapse remarks.
Method: documentation only; no commands were run.
