---
id: creative-arts.animation.blender.snap-targets
name: snap-targets
category: creative-arts
field: animation
product: blender
tags: [blender, snapping, snap-targets, snap-to-face, snap-to-vertex, snap-base, face-project, face-nearest, increment-snap]
level: practitioner
status: docs-checked
description: "Pick the right Blender snap target and base: increment, grid, vertex, edge, face, volume, edge center, perpendicular, align rotation, absolute increment, and B for base."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/controls/snapping.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# snap-targets

Goal: precise placement — vertex to vertex, object onto a surface, edge to its midpoint — without typing coordinates.

## Header magnet popover

- **Snap Target** (several can be enabled with Shift-LMB): *Increment* (grid-cell steps from the original location), *Grid* (the displayed grid), *Vertex*, *Edge*, *Face* (surface of the face under the cursor, useful for retopology), *Volume* (a depth centred inside the object under the cursor), *Edge Center*, *Edge Perpendicular*, *Face Center*.
- **Snap Target for Individual Elements**: *Face Project* (each object or vertex snaps to the face found by projecting along the viewing direction) and *Face Nearest* (each snaps to the closest face, so occluded geometry can be targeted).
- **Snap Base**: *Closest* (bounding box corner in Object Mode, vertex in Edit Mode), *Center* (the pivot point), *Median* (average of selected origins or vertices), *Active* (origin or centre of the active element) - which point of the selection lands on the target.
- **Target Selection** (Edit Mode): *Include Active* (other elements of the active object; ignored with Proportional Editing), *Include Edited*, *Include Non-Edited*; plus *Exclude Non-Selectable*.
- **Align Rotation to Target**: rotates the selection so its Z axis aligns with the target normal.
- **Backface Culling**: excludes back-facing geometry. **Snap Peel Object** (Volume): treats a target made of intersecting islands as one whole and looks only at its outer surface. **Snap to Same Target** and **Face Nearest Steps** apply to Face Nearest.
- **Affect**: Move / Rotate / Scale; snapping is on for moving by default and can be enabled for rotating and scaling. **Rotation Increment** sets the angle for incremental rotation snapping.
- **Absolute Increment Snap** (Increment): snaps to the viewport grid instead of moving by grid-cell increments.

## Gestures

- Toggle snapping: `Shift Tab`. Holding `Ctrl` during a transform temporarily inverts snapping.
- **Set snap base interactively:** during a transform press `B` to set a new snap base at the snap point defined by the Snap Target.
- **Multiple snap points:** press `A` while a snap target is highlighted to mark it; with several marked the selection snaps to their average location, and marking one more than once gives it more weight.
- *Face Project* can bend a flat sheet to fit a curved surface; the manual points to Shrinkwrap for similar jobs.
- *Face Nearest* can snap to occluded geometry, unlike Face Project.

## Gotchas

- Increment moves in steps of the viewport grid cell size from the original position; use Absolute Increment Snap to land on the grid itself.
- If only Increment is enabled as the Snap Target, set-snap-base falls back to Vertex, Edge, Face and Edge Center targets.
- In Edit Mode, *Include Active* controls whether the selection can snap to other elements of its own object.

## Verify

Compare the location of the snapped vertex with the target vertex in the Sidebar; they should match.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against editors/3dview/controls/snapping.rst and modeling/transform/modal_map.rst: Snap Base and Snap Target lists with definitions, individual-element targets, Target Selection options, Align Rotation (Z to normal), Affect, Absolute Increment Snap, Shift Tab / Ctrl / B / A gestures. Wrong or changed: Face Project and Face Nearest are now a separate 'individual elements' group and the plain target is Face; Face Center exists; the manual names it Absolute Increment Snap; no 4.0+ gate stated. Removed unconfirmed retopology and evaluated-geometry claims.

Method: documentation only; no commands were run.
