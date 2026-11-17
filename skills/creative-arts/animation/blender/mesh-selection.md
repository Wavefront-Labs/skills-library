---
id: creative-arts.animation.blender.mesh-selection
name: mesh-selection
category: creative-arts
field: animation
product: blender
tags: [blender, selection, select-loops, select-similar, select-linked, select-all-by-trait, checker-deselect, select-sharp-edges, grow-shrink, select-random, edit-mode, mesh-editing]
level: practitioner
status: draft
description: "Fast, exact mesh selection in Blender Edit mode: loops/rings/paths, Select Similar and By Trait, linked/boundary, grow/shrink, checker, random, hide/reveal, selection to vertex group."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/index.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/all_by_trait.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/similar.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/loops.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mesh-selection

Goal: select exactly the geometry you mean in one or two actions. Most "modelling speed" is selection speed.

## Modes and basics

- `1` / `2` / `3` vertex / edge / face mode; `Shift` + number adds a mode (multi-mode). Switching from face to vertex *expands* (all verts of faces); vertex → face *contracts* (only fully-selected faces). `Ctrl` + number switch with expansion/contraction options in the header popover.
- `A` all, `Alt A` none, `Ctrl I` invert. `Shift` click toggle, `Ctrl` click = **shortest path** between active and clicked (works with `Ctrl Shift` click to fill region), the `Select → Select Shortest Path` redo panel has *Fill Region* and *Checker (Nth)* options.
- Tools: `W` cycles Tweak / Box / Circle / Lasso (`B` box, `C` circle with wheel for radius; `Esc` exits). Box in X-ray (`Alt Z`) selects through the mesh; without X-ray only visible elements — the classic "half my verts weren't selected" cause.
- `Ctrl Numpad +` / `-` grow / shrink one ring. `Select → Select More/Less → Next/Previous Active` (`Shift Ctrl Numpad+/-`) walks along a loop one element at a time from two selected.

## Loops, rings, borders

- `Alt` click edge → **edge loop** (follows quads; stops at poles/n-gons); on faces: face loop depending on which edge you click; `Alt` click near a vertex in vertex mode chooses the loop by proximity.
- `Ctrl Alt` click → **edge ring** (perpendicular). `Shift Alt` click adds a loop.
- `Alt` click a **boundary** edge selects the whole open border (4.x: *Select Loops → Select Boundary Loop* in the menu converts a face selection to its outline).
- `Select → Select Loops → Edge Loops / Edge Rings / Select Loop Inner-Region` — *Loop Inner-Region* fills the faces inside a closed edge loop; *Boundary Loop* does the reverse.
- Loop Cut (`Ctrl R`) preview shows where a loop would go — hover a ring and press to also select the resulting loop.

## Linked and islands

- `L` hover → select linked island (delimit by *Seam / Sharp / Material / UV / Normal* in the redo panel; defaults to Seam, which is why `L` sometimes stops at a seam). `Shift L` deselect linked. `Ctrl L` select linked of current selection.
- `Select → Select Linked → Linked Flat Faces` (`Shift Ctrl Alt F`) grows across faces within an angle — selects a planar cap or a whole cylinder side.
- `P → Loose Parts / Selection / By Material` separates after selection.

## Select Similar (`Shift G`)

Vertex: *Normal, Amount of Adjacent Faces, Vertex Groups, Amount of Connecting Edges, Vertex Crease*. Edge: *Length, Direction, Amount of Faces Around an Edge, Face Angles, Crease, Bevel, Seam, Sharp, Freestyle*. Face: *Material, Area, Polygon Sides, Perimeter, Normal, Coplanar, Smooth/Flat, Face Map, Freestyle*. Each has *Threshold* and *Compare* (Equal/Greater/Less) in the redo panel. Bread-and-butter: select one face of a material → `Shift G → Material`; one tri → `Shift G → Polygon Sides` to find all triangles; one sharp edge → `Shift G → Sharp`.

## Select All by Trait

`Select → Select All by Trait →`
- **Non Manifold** (`Shift Ctrl Alt M`, options Wire/Boundaries/Multiple Faces/Non Contiguous/Vertices) — the print/boolean health check.
- **Loose Geometry** (verts with no edges, edges with no faces) — delete after Boolean/Knife.
- **Interior Faces** (faces surrounded by others) — Boolean leftovers.
- **Faces by Sides** (number of vertices, Equal/Greater/…: find n-gons: Greater than 4; tris: Equal 3).
- **Ungrouped Vertices** (no vertex group — find unweighted verts before skinning).
- *Sharp Edges* by angle (`Select → Select Sharp Edges`, angle 30°) — to Mark Sharp or Seam.
- *Select by Attribute* (4.x) — boolean attribute → selection (from GN or a stored selection).

## Patterns

- **Checker Deselect** (`Select → Checker Deselect`, *Nth* 2, *Skip*, *Offset*) on a loop → every other vertex; combined with loop selection it gives even subdivisions and alternating extrusions.
- **Select Random** (percentage, seed) for organic variation (scatter displace).
- **Select Mirror** (`Shift Ctrl M`, axis, *Extend*) — selects the symmetric counterpart; the *Topology Mirror* option in Tool settings → Options enables mirror by topology for asymmetric-coordinate meshes.
- *Side of Active* (`Select → Side of Active`, axis, sign) — everything left/right of a vertex.
- *Select Axis* via the same menu: all verts on one side of the active.
- Edge *Select Sharp Edges* + `Ctrl E → Mark Seam` = seams in one go on hard-surface.

## Hiding to simplify

`H` hide selected, `Shift H` hide unselected, `Alt H` reveal (reveal selects revealed — `Alt A` after). Hidden geometry is excluded from all operations including Box select in X-ray, Loop Cut and Smooth, which is how you work on an inner mouth without grabbing the lips. Hidden state persists in Object mode; *Mesh → Show/Hide* in the menu.

## Selection → data

- `Ctrl G` → *Assign to New Group* turns a selection into a vertex group (and the group is a reusable selection: *Select* button in the panel; `Shift` to add).
- `Ctrl E → Mark Seam / Sharp / Crease`, `Ctrl F → Smooth/Flat`, `M → Merge`, `Numpad .` frames the selection.
- Store selections: Vertex groups (verts) or Face Sets in sculpt mode; 4.x boolean attributes via `Select → Select by Attribute` / `Mesh → Attributes → Store Selection`? (use Geometry Nodes *Store Named Attribute* on *Selection*). The *Select Sets* behaviour from Maya isn't native; vertex groups are the convention.

## Python

```python
import bmesh, bpy
bm = bmesh.from_edit_mesh(bpy.context.object.data)
for f in bm.faces: f.select = len(f.verts) > 4   # select n-gons
bm.select_flush_mode(); bmesh.update_edit_mesh(bpy.context.object.data)
```
`bpy.ops.mesh.select_similar(type='MATERIAL')`, `select_all(action='INVERT')`, `select_non_manifold()`, `select_nth(skip=1, nth=1)` reproduce the menu.

## Gotchas

- Non-X-ray box select misses back faces; `Alt Z` first.
- `L` stops at seams unless you change *Delimit* in the redo panel (and Blender remembers the last delimit).
- Alt-click loop selection on a mesh with *Emulate 3 Button Mouse* on conflicts with Alt-orbit; turn emulation off.
- Select Similar thresholds are absolute: *Area* with 0.0 threshold matches only exactly equal faces; use 0.01.
- Hidden faces are still exported and rendered; reveal before saving a publish.

## Verify

- A full edge loop selects around a cylinder with one `Alt` click; a ring with `Ctrl Alt`.
- `Select All by Trait → Non Manifold` returns 0 on a mesh you intend to print or Boolean.
- Checker Deselect on a 16-vert loop leaves 8 selected, alternating.
- Select Mirror picks the symmetric counterpart with no stray verts on the centre line.
