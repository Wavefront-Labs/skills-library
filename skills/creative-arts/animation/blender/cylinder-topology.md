---
id: creative-arts.animation.blender.cylinder-topology
name: cylinder-topology
category: creative-arts
field: animation
product: blender
tags: [blender, cylinder-topology, cylinder-holes, curved-surface-cuts, hard-surface, subdivision-surface]
level: advanced
status: docs-checked
description: "Cut holes and attach cylinders cleanly on subdivided meshes: matching segment counts, circle from quad grid, holes on curved surfaces and keeping shading clean."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/inset_faces.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/transform/to_sphere.html
  - https://extensions.blender.org/add-ons/looptools/
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cylinder-topology

Goal: round holes, bosses and pipes on subdivision models without pinching or wobble.

## Segment count rule

Choose cylinder segment counts that match the surrounding grid: a hole in a 4-quad patch needs 8 edges around; in a 3×3 patch (12 border edges) use 12. The hole's vertex count must equal the count of border edges you connect to, so every new face is a quad.

## Hole from a quad grid (flat surface)

1. Select a patch of quads (2×2 for 8 edges, 3×3 for 12).
2. *LoopTools → Circle* (an add-on, available as an extension after 4.1), or `Shift Alt S` (*To Sphere*) at factor 1, to make the inner border round.
3. Inset (`I`) once for a support loop, then delete or extrude the centre inward.
4. Add a support loop around the outer rim (Loop Cut or Inset) for subdivision.

## Cylinder meeting a flat surface

Bridge the cylinder end loop to the hole loop (*Edge → Bridge Edge Loops*) when counts match. For a T-junction pipe, cut the hole with the same number of segments as the pipe.

## Curved surfaces

- Option A: model the hole on a flat panel, then bend it onto the curve (Simple Deform Bend or Shrinkwrap onto the curved target) before final cleanup.
- Option B: cut with a Boolean on a high-segment base, then use Weighted Normal / Data Transfer normals from the uncut shape to keep shading smooth.
- Make the base cylinder's segment count a multiple of the hole's footprint so the hole lands on a regular grid.

## Gotchas

- Triangles and ngons around the hole on curved, subdivided areas show as dents in reflections.
- LoopTools *Circle* fits a circle to the selected vertices (its *Best Fit* option); on curved surfaces flatten first or the circle tilts.
- Very dense surrounding geometry is not better: more edges near the hole increase ripples.

## Verify

Matcap or a striped reflection (Material Preview with a striped HDRI) shows straight, unbroken highlight lines passing the hole; the hole stays round after subdivision.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST) and the Blender 4.1 LoopTools page plus its extensions.blender.org listing. Confirmed: Inset shortcut I; To Sphere shortcut Shift Alt S; Edge > Bridge Edge Loops; LoopTools Circle with a best-fit option, which became an extension after 4.1; Simple Deform Bend and Shrinkwrap modifiers exist. Removed: the list of common segment counts, which no documentation covers. The segment-matching rule is modelling practice and is not documented in the manual.

Method: documentation only; no commands were run.
