---
id: creative-arts.animation.blender.knife-project-bisect
name: knife-project-bisect
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, knife, knife-project, bisect, knife-options, cut-through, panel-lines]
level: practitioner
status: docs-checked
description: "Cut precise lines into Blender meshes: Knife (K) controls and tool settings, Knife Project from curves, text or flat meshes, and Bisect with Fill and Clear Inner/Outer."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/knife_project.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/bisect.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# knife-project-bisect

Goal: draw cuts where you want them: panel lines, logos stamped into surfaces, clean planar splits.

## Knife (`K`, Mesh > Knife Topology Tool)

- Click `LMB` to place points; `Spacebar` or `Return` applies the cuts, `Esc` cancels. Double-click closes the loop. `RMB` ends the current path and starts a new one (snapping to earlier cuts). `Ctrl Z` undoes the last cutting line.
- Hold `Shift` to snap to edge midpoints and `Ctrl` to temporarily ignore snapping.
- Keys while cutting: `C` Cut Through (opposite of Occlude Geometry), `X`/`Y`/`Z` axis constraint (second press local axis, third press off), `S` cycle measurements, `V` X-Ray, `A` Angle Constraint (first press Screen, second Relative, third off; `R` picks a different reference line in Relative mode).
- Tool settings (only when using the Knife from the toolbar, not `K`): Occlude Geometry, Only Selected (`Shift K` starts with it on), X-Ray, Measurements, Angle Snapping (None, Screen, Relative) and Snap Increment.
- With multi-object editing, several objects can be cut at once. If cuts produce duplicate vertices, the doc suggests raising the viewport Clip Start.

## Knife Project (Mesh > Knife Project)

1. Make the cutter: a curve (text objects work) or a non-manifold mesh such as a flat shape or loose edges.
2. Put the view where the cutter projects as wanted; projection follows the viewing direction.
3. Select the object(s) to cut and enter Edit Mode.
4. `Ctrl LMB` the cutter object(s) in the viewport or Outliner (if Blender drops to Object Mode, enable Edit > Lock Object Modes).
5. Mesh > Knife Project. **Cut Through** projects through the whole mesh including hidden back faces.
6. Extrude or inset the result for embossed logos or panel lines.

Known limitation: when cutting several meshes in Edit Mode, geometry of one does not occlude another behind it.

## Bisect (Mesh > Bisect, or Toolbar > Knife > Bisect)

- Orient the view so the plane is a line, then drag with `LMB`. While dragging: `Spacebar` moves the line, `Ctrl` snaps rotation to 15 degree steps, `F` flips which side is "outer".
- Redo panel: **Plane Point / Plane Normal** (numeric), **Fill** (cap holes left by Clear), **Clear Inner / Clear Outer** (delete that side, including unselected geometry), **Axis Threshold** (vertices closer than this to the plane are reused).

## Verify

Select > Select All by Trait > Non Manifold shows no unexpected open edges after cutting.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Knife Topology Tool, Knife Project and Bisect pages. Corrected: Shift (not Ctrl) snaps to midpoints and Ctrl ignores snapping; C is Cut Through and A the angle constraint; RMB (not E) starts a new cut; the old Knife Project selection order (target first in Edit Mode, then Ctrl-click cutters). Removed the 3.0 rewrite remark, a non-existent Visible Measurements setting and unconfirmed gotchas.
Method: documentation only; no commands were run.
