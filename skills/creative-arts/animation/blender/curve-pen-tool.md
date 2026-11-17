---
id: creative-arts.animation.blender.curve-pen-tool
name: curve-pen-tool
category: creative-arts
field: animation
product: blender
tags: [blender, curve-object, curve-pen, curve-draw-tool, curve-extrude, bezier, curve-modeling]
level: practitioner
status: docs-checked
description: "Draw Blender curves fast: Curve Pen gestures (click, Ctrl insert/delete, drag handles, close spline), Draw tool with surface depth, extrude (E) and Make Segment (F)."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/curves/tools/pen.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/tools/draw.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/editing/control_points.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# curve-pen-tool

Goal: lay down curves like in a vector editor, or sketch them onto surfaces.

## Curve Pen (toolbar, Edit mode of a curve)

- **Extrude Point**: `LMB` click adds a new point connected to an existing point. **Extrude Handle Type** is Vector or Auto; it switches to Align when handles are moved.
- **Delete Point**: `Ctrl-LMB` on a point. **Insert Point**: `Ctrl-LMB` on a segment (click and drag to shape the inserted handles).
- **Move Segment**: `LMB` drag on a segment adjusts the handles without moving control points. **Move Point**: `LMB` drag a point or handle; with a spline end selected, dragging in empty space extrudes a point and moves its handle.
- **Select Point**: click to select one point or handle at a time.
- **Close Spline**: click the two end points consecutively. **Close Spline Method**: None, On Press (drag to adjust the end handle), On Click (not triggered by click-drag).
- **Toggle Vector**: double-click a handle (Vector/Auto). **Cycle Handle Type**: double-click a control point.
- Modifier keys while dragging a handle: `Left Shift` Free/Align toggle, `Left Ctrl` move the adjacent handle, `Spacebar` move the whole point, `Right Ctrl` mirror onto the opposite handle, `Left Alt` lock handle angle (length only).
- The gestures are tool preferences (Preferences > Keymap > 3D View > Curve > 3D View Tool: Edit Curve, Curve Pen); turn off the ones you trigger by accident.

## Draw tool

- Free-hand curves. **Type**: *Poly* (Bezier with straight segments, auto handles) or *Bezier* (Tolerance, Method Refit/Split, Detect Corners).
- **Depth**: *Cursor* (depth under the cursor) or *Surface* (draw on other objects; Project Onto Selected, Offset, Absolute Offset, Only First with a Plane of Normal to Surface, Tangent to Surface or View).
- **Use Pressure**, **Radius Min/Max** and **Taper Start/End** control radius along the stroke.
- Redo panel after drawing: Error, Fit Method (Refit/Split), Corner Angle, Cyclic. Lower values follow the stroke more closely; higher values give smoother, lighter curves.

## Classic editing

- `E` Extrude Curve and Move from selected points.
- `F` Make Segment connects two loose points or end points, joining curves of the same type (Bezier with Bezier, NURBS with NURBS).
- Segments > Subdivide adds points to selected segments (Number of Cuts).

## Verify

Handles overlay shows the expected types; the result is one continuous spline (`L` Select Linked selects all its points).

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Curve Pen, Draw and Control Points pages, curve Segments page). Confirmed: every Curve Pen gesture and modifier key listed, Close Spline Method options, Draw tool Type/Depth/Surface options and redo-panel fields, E and F operators, Subdivide. Corrected: Alt-drag does not move points (plain drag does), Shift-drag toggles Free/Align, double-click on the first point is not the close gesture, the Draw tool has no Pressure/Cyclic-detection fields as named (Use Pressure, Detect Corners), and the Ctrl-RMB point-add and numeric Tolerance advice were removed as unconfirmed.
Method: documentation only; no commands were run.
