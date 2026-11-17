---
id: creative-arts.animation.blender.select-interior-faces
name: select-interior-faces
category: creative-arts
field: animation
product: blender
tags: [blender, selection, select-interior-faces, select-loose, select-non-manifold, mesh-cleanup, manifold]
level: practitioner
status: docs-checked
description: "Find broken Blender mesh geometry with Select All by Trait (Interior Faces, Loose, Non Manifold, Faces by Sides) and clean up with Merge by Distance, Delete Loose, Fill Holes."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/all_by_trait.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# select-interior-faces

Goal: find the geometry that breaks booleans, 3D prints, subdivision and game exports.

## Select > Select All by Trait

- **Interior Faces**: selects faces that may have been created inside the mesh instead of on its surface; specifically faces with "abnormal" neighbours (several neighbours on the same edge) plus any "normal" neighbours of those faces. Delete them, then fill if needed.
- **Loose Geometry**: depending on select mode, vertices not part of any edge, edges not part of any face, or faces sharing no edge with another face. Mesh > Clean Up > Delete Loose removes loose vertices, edges and optionally faces.
- **Non Manifold** (Vertex and Edge modes only) options:
  - *Extend* (add to the selection),
  - *Wire* (edges with no faces),
  - *Boundaries* (edges at boundaries and holes),
  - *Multiple Faces* (edges belonging to three or more faces),
  - *Non Contiguous* (edges belonging to exactly two faces with opposite normals),
  - *Vertices* (isolated vertices, vertices of Wire or Multiple Faces edges, or the only vertex joining two faces).
- **Faces by Sides** (count set in the redo panel) and **Poles by Count** help find stray n-gons, triangles and irregular vertices.

## Cleanup sequence

1. Mesh > Clean Up > Merge by Distance.
2. Select Interior Faces, delete them.
3. Select Loose Geometry, delete (or Delete Loose).
4. Non Manifold with Boundaries off: fix Multiple Faces and Non Contiguous edges, for example by recalculating normals or rebuilding.
5. Non Manifold with Boundaries on: close holes with Mesh > Clean Up > Fill Holes (the *Sides* option limits hole size; 0 fills all) or Grid Fill for large holes.

## Gotchas

- Non Manifold is unavailable in Face select mode; switch to Vertex or Edge mode.
- Intentionally open meshes (planes, cloth) are non-manifold by design.

## Verify

After cleanup, Non Manifold with all toggles selects nothing on a mesh meant to be watertight.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Select All by Trait and Clean Up pages: every Non Manifold option, Interior Faces definition, Loose Geometry, Fill Holes Sides. Corrected: Interior Faces definition (abnormal neighbours, not every edge shared by 3+ faces). Removed the Non Manifold shortcut, loose-geometry checkboxes, Mirror modifier note and the 3D-Print Toolbox claim, which are not in the manual pages checked.
Method: documentation only; no commands were run.
