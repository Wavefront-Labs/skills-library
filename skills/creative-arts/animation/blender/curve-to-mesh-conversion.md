---
id: creative-arts.animation.blender.curve-to-mesh-conversion
name: curve-to-mesh-conversion
category: creative-arts
field: animation
product: blender
tags: [blender, curve-object, curve-to-mesh-conversion, convert-curve, mesh-to-curve, convert-to-mesh, curves-to-mesh]
level: practitioner
status: docs-checked
description: "Convert between Blender curves and meshes: Object > Convert > Mesh / Curve (loose edges only), Set Spline Type, Decimate Curve, and the Curve to Mesh node."
sources:
  - https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/convert.html
  - https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/curve/operations/curve_to_mesh.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/editing/curve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# curve-to-mesh-conversion

Goal: finalise curve-based models as meshes, or turn mesh edges into editable curves.

## Object > Convert

- **Mesh**: converts the selected curve, metaball, surface or text object to a mesh. The defined resolution of these objects is taken into account, and faces and volumes created by closed and extruded curves are kept. Set the curve resolution (Shape panel) before converting.
- **Curve**: converts the selected mesh or text object to a curve. For meshes, only loose edges (edges not part of any face) are included. For text, the outlines are preserved. The result is a Poly curve by default; for smooth segments use Edit mode > Curve > **Set Spline Type** (Bezier, NURBS, Poly or Catmull Rom). The conversion is basic: the exact shape and point count are not preserved, and converting NURBS to Bezier needs at least six points (truncated if not a multiple of three).
- **Keep Original**: option shown for the Grease Pencil conversion in the manual; for the other conversions duplicate the object first if you want to keep it.
- **Grease Pencil**: converts curve, mesh or text objects to Grease Pencil strokes (Thickness, Stroke Offset, Export Faces options).

## Curve cleanup

- Curve > Clean Up > **Decimate Curve** (Ratio = percentage of control points to remove) works on Bezier curves only.

## Non-destructive: Geometry Nodes

- **Curve to Mesh** node: converts all splines to a mesh; optional *Profile Curve* is extruded along each spline (otherwise a chain of edges), *Scale* scales the profile per control point, *Fill Caps* fills the ends with n-gons when the profile is cyclic.
- Edges tagged sharp on the profile curve (Bezier Free or Vector handles) come out shaded sharp.
- **Mesh to Curve** converts mesh edges to curves inside a node tree.

## After conversion

Clean the mesh as for any mesh: Merge by Distance, shading, check normals.

## Verify

Statistics vertex count matches the chosen resolution; Select > All by Trait > Non Manifold lists only the intended open ends.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Object > Convert, Curve editing, Curve to Mesh node). Confirmed: Convert > Mesh uses defined resolution and keeps faces, Convert > Curve loose-edges-only and Poly default, Set Spline Type behaviour, Decimate Curve scope, Curve to Mesh inputs. Removed as unconfirmed: a Merge option on curve-to-mesh conversion, "Keep Original" on non-Grease-Pencil conversions, the Object > Convert > Curves entry since 4.3, and notes about Follow Path and bevel/taper objects after conversion.
Method: documentation only; no commands were run.
