---
id: creative-arts.animation.blender.tool-mouse-position
name: tool-mouse-position
category: creative-arts
field: animation
product: blender
tags: [blender, tool-mouse-position, mouse-position, viewport-transform, node-tools, geometry-nodes]
level: advanced
status: docs-checked
description: "Build interactive geometry node tools from the cursor and view: Mouse Position, Viewport Transform matrices, mouse-to-3D raycasts and view-aligned operations."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/tools.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/input/scene/mouse_position.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/input/scene/viewport_transform.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/matrix/project_point.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# tool-mouse-position

Goal: tools that act where the user points (place an object under the cursor, cut along view, select by screen region).

## Inputs (tools only)

- **Mouse Position** node: *Mouse X* / *Mouse Y* (region-space pixels, from 0 at the left and bottom), *Region Width* and *Region Height*. Enable *Wait for Click* on the node group to wait for a click before running the operator from a menu.
- **Viewport Transform** node: *Projection* (the viewport's perspective or orthographic projection matrix), *View* (view direction and location) and *Is Orthographic*.
- Both nodes work only in the Tool context. The Self Object node returns the active object inside a tool node group.

## Mouse to 3D ray

```
ndc = (mouse / region_size) * 2 - 1                 (x, y in -1..1)
inv = Invert Matrix(Projection × View)
near = Transform Point(inv, (ndc.x, ndc.y, -1)) ; far = Transform Point(inv, (ndc.x, ndc.y, 1))
dir = normalize(far - near)
Raycast(target geometry, Source = near, Direction = dir) → Hit Position
```
Use the Multiply Matrices and Invert Matrix nodes, then the **Project Point** node for the points: it multiplies a projection matrix by the point and divides by the absolute value of W (perspective division), which Transform Point does not describe. The ray recipe above is a sketch (practice); test it in both perspective and orthographic views.

## Uses

- Place or instance geometry at the hit position under the cursor.
- View-aligned operations: transform the geometry into view space with the View matrix, operate in 2D, transform back.
- Screen-space selection: project points with Projection × View, compare with mouse position and radius.

## Gotchas

- Use *Wait for Click* when the tool is launched from a menu, so the mouse position is the click you make after launching it.
- Geometry in a tool is in object space while the View and Projection matrices are in world/view space: bring them into the same space before comparing (practice).

## Verify

Run the tool with *Wait for Click*, click over the mesh: geometry appears under the cursor from perspective and orthographic views.

## Checked

Blender 5.2 manual (blender-v5.2-release, modeling/geometry_nodes), read 2026-10-27.
- Mouse Position outputs (Mouse X/Y in region pixels, Region Width/Height), Wait for Click tip, Tool-context-only nodes, Viewport Transform outputs (Projection, View, Is Orthographic), Self Object returning the active object in tools, and the existence of Multiply Matrices, Invert Matrix, Transform Point and Project Point nodes.
- Corrected: Project Point performs the perspective division; Transform Point only applies a transformation matrix. Removed as unconfirmed: the 4.2 availability tag, the run-once/no-live-drag claim and the menu-click position claim.

Method: documentation only; no commands were run.
