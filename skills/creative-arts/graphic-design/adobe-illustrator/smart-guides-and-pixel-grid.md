---
id: creative-arts.graphic-design.adobe-illustrator.smart-guides-and-pixel-grid
name: smart-guides-and-pixel-grid
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, ai-document-setup, smart-guides, pixel-perfect, align-to-pixel-grid, guides, grids]
level: practitioner
status: draft
description: "Place artwork precisely in Illustrator with guides, smart guides, grids and pixel-grid alignment for crisp screen icons and UI assets."
sources:
  - https://helpx.adobe.com/illustrator/using/grids-guides.html
  - https://helpx.adobe.com/illustrator/using/pixel-perfect.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Guides, smart guides and pixel-grid alignment

## Rulers and guides
- Ctrl/Cmd+R rulers; drag guides out. Double-click a guide's position in the Control/Properties
  panel to type exact coordinates.
- Any path can become a guide: View > Guides > Make Guides (Ctrl/Cmd+5) - e.g. a circle guide for a logo.
- Lock guides: Ctrl/Cmd+Alt+; . Hide: Ctrl/Cmd+; .

## Smart guides (Ctrl/Cmd+U)
- Snap to anchors, paths, centres and intersections with live measurement labels.
- Preferences > Smart Guides: Alignment, Object Highlighting, Measurement Labels, Spacing Guides
  (equal-spacing hints), snapping tolerance.
- Turn off temporarily when nudging tiny distances; they snap to nearby objects unexpectedly.

## Grid
- View > Show Grid (Ctrl/Cmd+'), Snap to Grid. Preferences > Guides & Grid: gridline every 10 px, subdivisions 10.

## Pixel-perfect for screen
- View > Pixel Preview (Ctrl/Cmd+Alt+Y) to see anti-aliasing.
- Object > Make Pixel Perfect (or Align to Pixel Grid in the Properties/Transform panel) snaps
  horizontal and vertical segments to whole pixels.
- Snap to Pixel in View menu for drawing; Align Art to Pixel Grid on creation/transformation (Preferences > General).
- Strokes: odd-width strokes (1 px) on pixel boundaries blur; align stroke to inside or position half-pixel.

## Gotchas
- Pixel grid alignment applies only to RGB pixel-unit documents with the Web/Mobile profile behaviour.
- Rotated objects cannot be fully pixel-aligned.

## Verify
- [ ] Icon at 100% in Pixel Preview shows no grey half-pixel edges on straight lines.
