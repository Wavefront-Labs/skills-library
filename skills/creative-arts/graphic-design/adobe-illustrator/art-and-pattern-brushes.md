---
id: creative-arts.graphic-design.adobe-illustrator.art-and-pattern-brushes
name: art-and-pattern-brushes
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-brushes, art-brush, pattern-brush, scatter-brush, calligraphic-brush, bristle-brush, brush-options, corner-tiles, expand-appearance]
level: practitioner
status: draft
description: "Create and apply Illustrator art and pattern brushes: building source art, stretch vs guides scaling, pattern tiles for corners, colourisation, and expanding brushes for output."
sources:
  - https://helpx.adobe.com/illustrator/using/brushes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Art and pattern brushes

**Goal:** custom strokes (ink lines, ribbons, borders, chains, stitches) you can apply to any path.

## Brush types (Window > Brushes)
| Type | Does | Use for |
|---|---|---|
| **Art** | stretches one artwork along the path | tapered ink strokes, ribbons, banners |
| **Pattern** | repeats tiles along the path, with special corner/end tiles | borders, frames, chains, stitching |
| Scatter | sprinkles copies along the path | confetti, stars |
| Calligraphic | elliptical nib | quick pen strokes |
| Bristle | painterly hairs (heavy, transparency) | rough paint looks - avoid for print |

## Make an art brush
1. Draw the source horizontally (e.g. a tapered stroke shape). No raster images, no gradients
   in older versions (gradients allowed since 2018 in art brushes, still not in pattern).
2. Select it, Brushes panel > New Brush > Art Brush.
3. **Scale options:** Scale Proportionately, **Stretch to Fit Stroke Length**, or
   **Stretch Between Guides** - set the guides around the middle section so the ends (arrowhead,
   ribbon tail) stay undistorted while only the middle stretches.
4. **Colorization:** None (keeps original colours), Tints, Tints and Shades, or **Hue Shift**
   (uses the key colour; stroke colour then recolours the brush).

## Make a pattern brush
1. Create the side tile; for clean joins its left and right edges must meet seamlessly.
2. Drag the side tile into the Swatches panel; also make outer corner, inner corner, start
   and end tiles if needed (Illustrator can auto-generate corners: Auto-Centered,
   Auto-Between, Auto-Sliced, Auto-Overlap).
3. New Brush > Pattern Brush; assign tiles. **Fit:** Stretch to fit, Add space to fit, or
   Approximate path (adjusts path slightly so tiles fit exactly).

## Apply and edit
Select a path, click the brush. Stroke weight scales the brush. Double-click the brush to
edit; choose Apply to Strokes to update existing uses. Options of Selected Object (panel
icon) changes only the selected path.

## Output
Brushes are live appearances. Before sending to print or cutters, or to avoid surprises in
other apps, **Object > Expand Appearance** on a copy. SVG export expands brushes anyway.

## Verify
- [ ] Brush ends undistorted at different path lengths (Stretch Between Guides set right).
- [ ] Pattern corners join without gaps on a rectangle test.
- [ ] Expanded copy kept for output.
