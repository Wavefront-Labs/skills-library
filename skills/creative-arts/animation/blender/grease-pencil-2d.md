---
id: creative-arts.animation.blender.grease-pencil-2d
name: grease-pencil-2d
category: creative-arts
field: animation
product: blender
tags: [grease-pencil, 2d, gpencil, line-art, 2d-in-3d, boards, effects, overlay, drawing-on-2s, gp-materials, hybrid, cel, blender]
level: advanced
status: docs-checked
description: "Blender Grease Pencil for 2D-in-3D: boards, hand-drawn FX, hybrid overlays held in 3D space, the Line Art modifier, drawing on 2s, and GP materials for cel."
sources: [https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/stroke_placement.html, https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/drawing_planes.html, https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html, https://docs.blender.org/manual/en/latest/grease_pencil/properties/onion_skinning.html, https://docs.blender.org/manual/en/latest/grease_pencil/materials/properties.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SKILL: Grease Pencil (2D-in-3D)

Grease Pencil (GP) is Blender's 2D drawing system that lives inside 3D space: strokes belong to an object with
transforms, materials and modifiers, so drawn elements sit in the same scene as the 3D cast and sets. For a cel show
that gives hand-drawn effects, 2D accents, signage and board art that move with the camera because they are in the scene.

Pairs: `storyboarding`, `toon-effects-animation`, `cel-shading`, `particles-fx`, `smoke-fire-fx`, `twelve-principles`,
`layout-blocking`.

## What GP is good for on a cel show
Reach for GP when the thing wants to be drawn, not simulated or modeled:
- Boards and 2D blockout boards kept in the shot file (see `storyboarding`).
- Hand-drawn FX: impact flashes, speed lines, smoke puffs, sparkles, splashes (the language `toon-effects-animation`
  describes).
- 2D accents and overlays: signage, logos, chalk marks, map lines, emotive symbols (sweat drops, anger marks).
- Hybrid 2D inserts: a 2D creature or a drawn detail on a 3D character.
- Line Art: a modifier that generates GP strokes from 3D geometry, a cel outline you can art-direct as strokes.

## Placement: where new strokes land
Two separate selectors in Draw mode, both affecting only new strokes (existing strokes do not move):
- **Stroke Placement**: Origin (at the GP object origin), 3D Cursor, Surface (sticks to mesh surfaces, with an Offset
  from the surface and an option to project only onto selected objects), or Stroke (sticks to other strokes).
- **Drawing Plane**: View (current viewport orientation), Front (X-Z), Side (Y-Z), Top (X-Y) or Cursor (3D cursor
  orientation). Enable the Canvas viewport overlay to see the plane in use.
- Placement is the whole trick of 2D-in-3D: a flat overlay and a depth-anchored element are different choices. Make the
  choice on purpose per element, and test under the real shot camera.
- Parent a GP object to a 3D object or an empty so the 2D element rides with what it belongs to (a sign on a wall, a
  sweat drop by a head).

## Drawing on 2s (and other holds)
Cel animation lives on 2s: a new drawing every two frames, for a hand-made cadence.
- Create drawings only on every second frame; each drawing holds until the next. For slow FX, 3s or 4s can read as
  crafted where 1s looks too smooth and digital (a house style, not a rule).
- Use onion skinning to see ghosts of the keyframes before and after the current frame while drawing the inbetween.
  Onion skinning is toggled per layer, with the main switch in the viewport overlays.
- GP has interpolation tools. Use them to rough an inbetween you then redraw rather than as the final cadence.
- Keep timing on the dope sheet and spacing/volume in the drawings (same split as `animation-blocking-to-polish`).

## GP materials (the cel look)
A GP material has a Stroke part (the line) and a Fill part (the enclosed area); either or both can be enabled, and each
has a Holdout option.
- Stroke: line colour; keep it at the show's line colour for consistency with `cel-shading`'s outline.
- Fill: flat-fills the closed shape, which is how a drawn puff or splash gets its solid cel colour.
- Define the show's GP palette once and reuse it across all GP objects; an off-palette fill breaks the unified look.

## Line Art: outlines from 3D geometry as strokes
The Line Art modifier generates strokes from a scene, a collection or a single object, and needs an active camera.
Lines are generated only on portions visible from that camera.
- Source Type is Scene, Collection or Object. Output goes to a chosen Layer with a chosen Material, Line Radius and
  Opacity; Fill Strokes makes filled shapes instead of outlines.
- Edge types you can enable: Contour (with Silhouette and Individual Silhouette variants), Crease (with a Crease
  Threshold), Intersections, Material Borders, Edge Marks (Freestyle edge marks), Loose and Light Contour. Pick them to
  match the show's line language.
- Output is GP strokes, so it can be thickened, tapered or hand-corrected per shot.
- Each Line Art modifier runs its own occlusion calculation, so several of them in one stack make evaluation much
  slower; the Use Cache option reuses data from the first one but makes some settings unavailable.
- Line Art can be baked over the scene frame range (Bake Line Art, Bake All, Clear Baked Line Art) so it is not
  recalculated; bake before a heavy or headless render and check the result frame by frame.

## Modifiers: non-destructive 2D
GP has its own modifier stack. Ones this skill relies on: Thickness and Noise (Deform) for line weight and hand-wobble,
Build (Generate) to reveal strokes over time, Offset (Deform), Array and Mirror (Generate) to repeat and mirror
stroke groups, and Time Offset (Edit) to retime or loop a layer's drawings. Check each modifier's page for its settings.

## Pipeline integration
- Boards to shots: a GP board drawn in the shot file can sit on a hidden layer as reference while `layout-blocking`
  builds the 3D.
- FX division of labour: drawn FX in GP here; volumetric or simulated FX in `smoke-fire-fx`, `particles-fx`,
  `fluid-water-fx`. Many shots use both.
- In Blender's view layer passes there is a Grease Pencil pass that outputs only the visible strokes and fills, for
  separate compositing. Verify in a test render before relying on it.

## Common failures
- Everything on the View plane, so nothing parallaxes and the 2D floats off the world when the camera moves.
- Off-palette GP fills and strokes that break the cel look.
- Animating on 1s so drawn FX reads as sterile tween.
- Unbaked Line Art that differs between interactive and batch render.
- Using GP for what should be simulated, and vice versa.

## Verify
- [ ] Each element's placement and parenting is chosen on purpose (camera-locked overlay or depth-anchored in-world).
- [ ] In-world GP parallaxes and occludes correctly under the shot's real camera move.
- [ ] Hand-drawn FX are on 2s (or chosen holds), checked with onion skin for volume and arcs.
- [ ] GP materials use the shared palette.
- [ ] Line Art uses the intended edge types and is baked before render.
- [ ] A test render reproduces the GP identically to the viewport.

## Checked
Date: 2026-11-01. Confirmed against the Blender manual (Stroke Placement, Drawing Plane, Line Art modifier, Onion
Skinning, Grease Pencil material pages and the modifier index): placement and plane options, Line Art source types,
edge types, per-modifier occlusion cost, Use Cache and baking, Stroke/Fill/Holdout on GP materials, existence of the
named modifiers, per-layer onion skinning, and the Grease Pencil render pass. Removed: claims about EEVEE Next
depth-compositing of GP, headless determinism, and modifier ordering above Line Art, which no page states.
Method: documentation only; no commands were run.
