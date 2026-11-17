---
id: creative-arts.animation.blender.triangulate-modifier
name: triangulate-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, triangulate-modifier, triangulate, modifiers, game-export, baking, quad-method, ngon-method]
level: practitioner
status: verified
description: "Lock triangulation with Blender's Triangulate modifier so bakes and exports agree: quad method, n-gon method, minimum vertices and Keep Normals."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/triangulate.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/triangulate_faces.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# triangulate-modifier

Goal: the low-poly that you bake a normal map onto and the mesh the game engine renders must have *identical* triangulation, or the baked normals show seams and dents. The Triangulate modifier makes that deterministic.

## Settings

- **Quad Method**: *Beauty* (nice triangles, slower), *Fixed* (split on the 1st and 3rd vertices), *Fixed Alternate* (2nd and 4th), *Shortest Diagonal*, *Longest Diagonal* (the manual calls this preferred for cloth simulations). Pick one method and use the same triangles for baking and export.
- **N-gon Method**: *Beauty* or *Clip* (ear clipping, the method used for viewport tessellation).
- **Minimum Vertices**: minimum vertex count a face needs to be triangulated; 5 leaves quads alone and triangulates only n-gons.
- **Keep Normals**: tries to preserve custom normals; the 5.2 documentation warns that shading may not be fully preserved and that the *Fixed* method usually gives the best result here; the 4.5.14 tooltip only says "Try to preserve custom normals". Defaults when added from Python: Shortest Diagonal, Beauty, Minimum Vertices 4, Keep Normals off.

## Workflow (bake-safe game asset)

1. Stack: ...edits → Weighted Normal → **Triangulate (Keep Normals on)** last.
2. Bake from the triangulated result.
3. Export with the exporter's modifier-application option on, so the engine receives the same triangles, and avoid re-triangulating in the engine.

## Gotchas

- Triangulating before Subdivision Surface gives star-shaped poles and pinching; keep it after subdivision or don't subdivide.
- Edit-mode equivalent is *Face → Triangulate Faces* (`Ctrl T`), which is destructive.

## Verify

- Statistics overlay: Faces = Tris after the modifier.
- Wireframe overlay shows diagonals; compare against the engine import's wireframe.
- Bake, apply the normal map, inspect at grazing angles for diagonal seams — none if triangulation matches.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST: Triangulate modifier and Triangulate Faces pages) and rna_modifier.cc from the 5.2 release branch. Confirmed: Quad Method options and meanings, N-gon Method Beauty and Clip, Minimum Vertices, Keep Normals tooltip (Fixed usually best), Face > Triangulate Faces on Ctrl T, and that the modifier does the same as the Edit Mode tool. Corrected: Longest Diagonal is not a 4.x-only addition, and the Shortest Diagonal recommendation was unconfirmed. Removed as unconfirmed: the Beauty default, the skinned-mesh and lost-normals claims, the Cycles bake statement and Alt J. Modifier order advice is modelling practice.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: the Quad Method enum has exactly Beauty, Fixed, Fixed Alternate, Shortest Diagonal and Longest Diagonal, and N-gon Method Beauty and Clip; a cube gives 12 triangles; Minimum Vertices 5 leaves all 6 quads alone; a 6-gon with Minimum Vertices 5 gives 4 triangles with either n-gon method; the Fixed and Fixed Alternate descriptions are the first/third and 2nd/4th vertices; Ctrl T maps to the Edit Mode quads_convert_to_tris operator in the default keymap.

Method: manual text confirmed from documentation; Triangulate behaviour run headless in Blender 4.5.14.
