---
id: creative-arts.visual-art.digital-illustration.perspective-rulers-and-symmetry-tools
name: perspective-rulers-and-symmetry-tools
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, digital-inking, digital-line-art, perspective-ruler, symmetry-tool, assistant-tool, krita-assistants, clip-studio-paint, vanishing-point, snapping]
level: practitioner
status: draft
description: "Use perspective rulers and symmetry: Krita's Assistant Tool (vanishing points, perspective, ellipse) with snapping, Clip Studio's perspective and symmetry rulers, and layer-specific rulers."
sources: ["https://docs.krita.org/en/reference_manual/tools/assistant.html", "https://docs.krita.org/en/reference_manual/tools/multibrush.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Perspective rulers and symmetry tools

**Goal:** accurate perspective and mirrored drawing in Krita and Clip Studio Paint
(Krita Manual: Assistant Tool, Multibrush; CSP user guide: Rulers).

## Krita
- **Assistant Tool**: add assistants: *Vanishing Point*, *Perspective* (grid from
  a quad), *Two-point/Three-point* (newer versions), *Parallel ruler*, *Ellipse*,
  *Concentric ellipse*, *Fish eye*, *Spline*.
- Place handles; enable **snapping** in the brush's tool options ("Snap to assistants",
  with Snap single for one assistant per stroke).
- Toggle assistant visibility with the canvas decoration buttons; save/load
  assistant sets (.paintingassistant) for reuse.
- **Symmetry**: canvas mirror buttons (horizontal/vertical) on the toolbar; the
  **Multibrush** tool for radial symmetry with N axes.

## Clip Studio Paint
- **Perspective ruler** (Ruler tool > Perspective ruler): 1/2/3-point; drag
  guide lines to set vanishing points; eye level line. Snapping toggled per ruler
  (Snap to special ruler) and per layer ("show in all layers" / same folder / edit layer only).
- **Symmetry ruler**: line-symmetric or radial with number of lines.
- Other rulers: concentric circle, parallel lines, focus lines (speed lines).

## Workflow tips
- Put rulers on a dedicated construction layer, or set them to "show in same folder"
  so they affect only relevant layers.
- Turn snapping off for organic elements.
- For very distant VPs, zoom out and place VPs off canvas (both apps allow this).

## Gotchas
- Snapping left on: hair and foliage snap to perspective lines.
- Rulers attached to a layer you deleted.

## Verify
- [ ] Perspective rulers match the scene's horizon and VPs.
- [ ] Snapping enabled only while drawing structure.
