---
id: creative-arts.animation.blender.precision-drawing-tools
name: precision-drawing-tools
category: creative-arts
field: animation
product: blender
tags: [blender, precision-drawing-tools, pdt, cad-tools, precision-modeling, bundled-addons]
level: advanced
status: gated
description: "Model with Precision Drawing Tools (PDT): absolute, delta, direction and percent inputs, working planes, command line entries, intersections, fillets and pivot tools."
sources:
  - https://docs.blender.org/manual/en/4.1/addons/3d_view/precision_drawing_tools/index.html
  - https://docs.blender.org/manual/en/4.1/addons/3d_view/precision_drawing_tools/command.html
  - https://extensions.blender.org/add-ons/precision-drawing-tools-pdt/
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# precision-drawing-tools

Goal: CAD-style exact placement of vertices, edges and objects by typed coordinates.

## Install

PDT is listed on extensions.blender.org as "Precision Drawing Tools (PDT)" (listing shows minimum Blender 4.2). The manual page used here is the Blender 4.1 manual, the last version that documented it. Whether the extension's panel matches that page was not checked. (gated: unconfirmed, source is paywalled or blocked)

## Design panel

- **Operation** (4.1 manual): Cursor, Pivot Point, Move, New Vertex, Extrude Vertices, Split Edges, Duplicate Geometry, Extrude Geometry.
- Operators: Absolute (world coordinates), Delta (incremental), Direction (distance and angle), Percent (for example split an edge at 25 percent), and Intersect (for example a new vertex at the intersection of two selected edges, with the working plane set).
- **Working Plane**: for example Front (X-Z), as used in the manual's examples.
- Enter X/Y/Z or Distance/Angle/Percent and click the matching operator button.

## Command line

The PDT command input (activated by Return after clicking in the box) takes two letters followed by numbers separated by commas. Primary letters: C cursor, D duplicate, E extrude geometry, F fillet, G grab (move), N new vertex, P pivot, S split edges, V extrude vertices only, M maths. Secondary letters: A absolute, D delta, I direction (distance and angle, valid angle range +-180), P percent. Examples from the 4.1 manual:
- `cd-1.5,,`: cursor delta, negative 1.5 in X (zeros may be omitted, so `cd2,,1` is valid).
- `ei2,135.6`: extrude geometry 2 units at 135.6 degrees from the positive view X axis.
- `sp30`: split an edge at 30 percent of the way along it.
- `na1.5,,1.2`: new vertex at absolute X 1.5, Y 0, Z 1.2.
- `fv1.5,6,0.5`: fillet vertices with radius 1.5, 6 segments, profile 0.5.
Move is G (for example `gi1.5,38.75`), not M. Expressions are not evaluated in ordinary commands; the separate Maths command (`M` plus X, Y, Z, D, A, P or O) evaluates an expression into an input field, for example `mx(1.2*sin(radians(54)))`.

## Other tools

- **Fillet**: the manual's fillet command takes radius, number of segments and profile (0 to 1) and works on vertices (`fv`) or edges (`fe`).
- **Pivot Point** operations place the pivot point; the 4.1 manual also documents View Control, Holes in Faces and a PDT Parts Library (parts stored in a separate .blend, which the manual describes as an early-stage feature).

## Gotchas

- Commands need enough selected vertices or objects and enough values; otherwise PDT reports an error message (manual). Missing or invalid values in other cases become 0.
- The working plane controls what distance and angle mean (the manual's Move example sets the plane to Front (X-Z)).
- Inputs are in scene units (practice); set the unit scale before modelling.

## Verify

Compare the resulting coordinates with the typed values in the Sidebar Item tab.

## Checked

2026-10-27, Blender manual 4.1 (add-on docs) and extensions.blender.org. Confirmed against the Blender 4.1 manual pages for Precision Drawing Tools (index, operations, command line; docs.blender.org/manual/en/4.1, fetched on this date) and the extensions.blender.org listing (id precision_drawing_tools_pdt, minimum Blender 4.2). Wrong claims fixed: Move is G, not M (M is Maths); ordinary commands do not evaluate expressions. The 4.2+ extension UI itself is unconfirmed and gated; the Tangents and Intersect-count claims were removed.

Method: documentation only; no commands were run.
