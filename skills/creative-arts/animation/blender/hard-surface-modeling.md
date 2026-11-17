---
id: creative-arts.animation.blender.hard-surface-modeling
name: hard-surface-modeling
category: creative-arts
field: animation
product: blender
tags: [blender, hard-surface, bevel, supporting-loops, boolean, subsurf, shade-auto-smooth, mark-sharp, bevel-weight, non-destructive, modifiers, cel, inverted-hull, crt, props, vehicles]
level: advanced
status: docs-checked
description: "Clean hard-surface modeling in Blender: Bevel modifier with weights, Boolean solvers, Smooth by Angle shading, and normal and planarity cleanup."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/shading.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/smooth_by_angle.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/edge_data.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/normals.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# hard-surface-modeling

Goal: props, vehicles and mechanical objects that read crisp under stylised (banded) shading and take clean outlines, without melted corners, pinching or boolean garbage. Shading belongs to `creative-arts.animation.blender.cel-shading`; organic work belongs to `creative-arts.animation.blender.organic-sculpting`.

Banded shading amplifies normal errors, so the aim is clean, predictable normals and a clean silhouette.

## Pick a pipeline per object

1. **Subsurf cage:** all-quad cage, rounded edges held by supporting loops, one Subdivision Surface modifier. Smoothest; booleans fight it.
2. **Bevel modifier:** a lower-poly base with a Bevel modifier and Smooth by Angle shading, no subdivision. Boolean friendly, and usually safer for locked assets reused across files.

## Bevel modifier

- A non-destructive alternative to the Edit Mode bevel. *Segments* is the number of edge loops added along the bevel.
- *Limit Method:* None (all edges), Angle (only sharper edges), Weight (use an attribute; weight 0.0 means no bevel; by default the `bevel_weight_edge` and `bevel_weight_vert` attributes set in Edit Mode) or Vertex Group (an edge bevels only if both its vertices are in the group).
- Set edge Bevel Weight in Edit Mode with *Edge > Edge Bevel Weight*; the Edge menu pops up at the cursor with `Ctrl-E`, and the weight also appears in the Sidebar.
- *Width Type* options: Offset, Width, Depth, Percent, Absolute. *Clamp Overlap* limits each width so edges cannot cause overlapping intersections. *Loop Slide* lets the bevel slide along unbeveled edges; turning it off can give more even widths.
- *Harden Normals* adjusts the bevel faces' normals to match surrounding faces so those stay flat; it needs custom split normals (created automatically). *Face Strength* modes can feed a following Weighted Normal modifier. *Mark* Seam and Sharp keep those edge marks propagating through the bevel.

## Shade Auto Smooth

*Object > Shade Auto Smooth* adds a **Smooth by Angle** modifier (a Geometry Nodes asset from the bundled Essentials library; Shade Smooth or Shade Flat removes it). *Angle* is the maximum angle between face normals still considered smooth. *Ignore Sharpness* smooths all edges even if marked Sharp; leave it off so Sharp-marked edges stay hard. Tune the angle by eye.

A faint gradient on a flat panel is usually a non-planar face: *Mesh > Clean up > Make Planar Faces*, or *Split Non-Planar Faces*.

## Booleans

- Only manifold meshes are guaranteed proper results; non-manifold meshes often work but may glitch, and the Manifold solver does not work on them at all.
- *Solver:* Float is simple and fast but lacks support for overlapping geometry (it has an Overlap Threshold; Intersect is not allowed with a collection operand); Exact has full support for overlapping geometry and gives the best results but is much slower; Manifold is usually fastest but needs manifold meshes. Exact has *Self Intersection* and *Hole Tolerant* (enable Hole Tolerant only when Exact shows errors on non-manifold geometry, since it costs time) and a Materials option.
- The operand can be an Object or a Collection of mesh objects; an empty collection with Exact removes the mesh's interior (self-intersecting) geometry.
- Make cutters closed manifold meshes and extend them past both surfaces, rather than ending flush with a face.
- A boolean leaves no supporting loops around the cut, so a Subdivision Surface after it can round the seam unpredictably (practice, not stated by the manual). Preferred fixes: use the Bevel modifier pipeline for anything with holes, or apply the boolean and rebuild the cut by hand before subdividing. Apply live booleans on assets that must survive reuse, since the modifier depends on its cutter object.

## Cleanup after booleans

- *Mesh > Normals > Recalculate Outside* (`Shift-N`), *Recalculate Inside* (`Shift-Ctrl-N`).
- *Mesh > Clean up > Merge by Distance* and *Delete Loose*.
- The **Face Orientation** overlay shows the backside of faces in red; a red face on the outside of a mesh is most likely oriented wrongly (fix with Flip or Recalculate).

## Modifier order (practice)

Mirror first, then Boolean, then Bevel, then any Solidify, with Smooth by Angle last so it reads the final geometry (Shade Auto Smooth places it last).

## Outline friendliness (practice)

Avoid faces thinner than an outline's thickness, keep normals consistent, weld coincident vertices, and remove loose geometry so stray edges do not create floating line fragments.

## Checked

2026-11-09. Confirmed against the Bevel, Boolean and Smooth by Angle modifier pages, Shade Auto Smooth, Edge Data, Clean up, Normals and Overlays pages: all options, shortcuts and behaviours above. Items labelled practice are craft advice not stated by the manual. Removed: numeric values (segment counts, cutter segment counts, 30 degrees, 2 cm overlaps), Mark Sharp shortcut, Loop Cut shortcut, project-specific CRT worked example and outline pass specifics.
Method: documentation only; no commands were run.

## Verify

1. Face Orientation shows no red on outside faces.
2. Recalculate Outside changes nothing visible; Merge by Distance removes nothing.
3. No n-gons on any mesh under a Subdivision Surface modifier.
4. Banded shading on every bevel stays stable as the camera orbits.
5. Outline renders show one continuous line without black blobs at former boolean seams.
