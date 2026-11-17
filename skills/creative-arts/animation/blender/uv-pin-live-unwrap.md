---
id: creative-arts.animation.blender.uv-pin-live-unwrap
name: uv-pin-live-unwrap
category: creative-arts
field: animation
product: blender
tags: [blender, uv, unwrap, uv-pin, live-unwrap, pin-uvs, uv-editor]
level: practitioner
status: docs-checked
description: "Shape UV islands in Blender with Pin (P), Unpin (Alt P), Invert Pins, Live Unwrap, Align (Shift W) and Follow Active Quads, and keep the shape when re-unwrapping."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/uv.html
  - https://docs.blender.org/manual/en/latest/editors/uv/selecting.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/tools/tool_settings.html
  - https://docs.blender.org/manual/en/latest/editors/uv/sidebar.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# uv-pin-live-unwrap

Goal: shape islands deliberately (straight edges, aligned layouts) and keep that shape when re-unwrapping.

## Pinning

- UV Editor: select UVs, `P` Pin, `Alt P` Unpin (UV > Pin/Unpin). Pinned UVs do not move between unwrap operations, so you can lock parts of a layout in shape or place.
- Pinning works best with the Unwrap methods on organic objects, for example pinning midline UVs of a Mirror-modifier model and aligning them on X.
- Select > All by Trait > Pinned (`Shift P`) finds them; Box Select Pinned (`Ctrl B`) box-selects only pinned UVs; UV > **Invert Pins** pins unpinned selected UVs and unpins pinned selected ones.
- The Pinch and Relax sculpt tools do not move pinned UVs, so pin borders or interior holes to protect them. The Grab tool can move pinned UVs.

## Live Unwrap

- With Live Unwrap on and two or more UVs pinned, moving or scaling the pinned UVs unwraps the model interactively; use it to fit an island to a shape.
- Separately, Sidebar > Tool > Options > UVs > **Live Unwrap** (3D Viewport) recalculates the unwrap each time an edge's seam state changes.

## Straightening recipes

- Rectangular island: pin the corners at a rectangle (type coordinates in the Image tab's UV Vertex panel; enable Pixel Coordinates in the View tab for pixel units), then unwrap.
- Grid island: Follow Active Quads from one straightened quad (U menu).
- Align a border: select UVs and use UV > Align (`Shift W`, Straighten or Align options), then pin and unwrap.

## Gotchas

- Too few pins leave an island free to rotate; too many may cause distortion near pins.
- Minimum Stretch has *No Flip*: disallowing flipped faces can matter when pins are present.

## Verify

Re-unwrap: pinned points stay in place; check the Display Stretch overlay around pins.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the UV Operators, Selecting UVs, UV Sidebar and Tool Settings pages: pin/unpin shortcuts, Select Pinned, Box Select Pinned, Invert Pins, Pinch/Relax/Grab behaviour, Live Unwrap, Align, Pixel Coordinates. Removed unconfirmed pin colours, per-map storage, a generic cost warning, and the claim that pins ignore projection methods.
Method: documentation only; no commands were run.
