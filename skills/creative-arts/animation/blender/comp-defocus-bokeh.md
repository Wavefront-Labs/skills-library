---
id: creative-arts.animation.blender.comp-defocus-bokeh
name: comp-defocus-bokeh
category: creative-arts
field: animation
product: blender
tags: [blender, defocus, defocus-node, bokeh, z-defocus, depth-of-field, compositor]
level: practitioner
status: verified
description: "Do depth of field in post with the Defocus node and Z pass: F-Stop, Max Blur, bokeh blade count, No Z-buffer and Z Scale, camera focus Distance, and edge artefacts."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/filter/blur/defocus.html
  - https://docs.blender.org/manual/en/latest/compositing/types/filter/blur/bokeh_blur.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---
# comp-defocus-bokeh

Goal: flexible DOF after rendering, so focus can be changed without re-rendering.

## Render

Render sharp (camera depth of field off) with the **Depth** (Z) pass. The Defocus node uses the real camera data in the scene when supplied by a Render Layers node, so set the camera focus **Distance** (Camera > Depth of Field). Enable the camera Limits option to see the focal point as a yellow cross along the view direction.

## Defocus node (Filter > Blur)

Inputs: **Image**, **Z** (a Z-buffer, but a greyscale image or single value works as a mask too). Settings:
- **Bokeh Type**: Disk or 3 to 8 iris blades (Triangle, Square, Pentagon, Hexagon, Heptagon, Octagon). **Angle** rotates the shape and is disabled for Disk.
- **F-Stop**: controls the amount of blur like a real camera. The default of 128 is treated as infinity (everything in focus); halving the value doubles the blur. Disabled when No Z-buffer is on.
- **Max Blur**: caps the blur radius; the manual gives 0 as no limit, but a new node in Blender 4.5.14 has `blur_max` 16 (range 0 to 10000), so check it. Useful for performance.
- **Scene**: the linked scene supplying the camera.
- **No Z-buffer**: turn on when the Z input is not a real Z-buffer (enabled automatically when a non-image node is connected). **Z Scale** then scales the input, which directly sets the blur radius.

## Alternatives

- **Bokeh Blur** node with a **Bokeh Image** node for custom bokeh shapes.
- In-render depth of field (Cycles or EEVEE) handles things post DOF cannot. Use post DOF when flexibility matters more.

## Artefacts

- Post DOF cannot see behind foreground objects. For a focus pull between a near and a far object, render them as two passes, defocus each with the same Time node and one inverted (for example with a Map Value node and Size -1), then combine.
- Keep distance differences between visibly overlapping objects modest to reduce edge artefacts.
- At very low F-Stop values (below 5) oversampling is removed and objects at the focus distance can show stair-stepping. The manual suggests rendering at twice the size and scaling down, a small Blur, or setting the focus distance slightly off.

## Verify

Change the focus distance on the camera and re-run the comp. Focus should move to the expected object, with no hard halos at the subject's edges.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Defocus inputs and settings (Bokeh Type blade counts, Angle, F-Stop default 128, Max Blur 0, Scene, No Z-buffer, Z Scale), camera Distance and Limits, focus-pull and low f-stop aliasing hints. Removed the Threshold, Preview and Gamma Correction settings (not in the 5.2 page) and the claims about anti-aliased Z and transparency.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): CompositorNodeDefocus new node: bokeh CIRCLE (Disk) with items OCTAGON, HEPTAGON, HEXAGON, PENTAGON, SQUARE, TRIANGLE, CIRCLE; f_stop 128 (range 0 to 128); blur_max 16; z_scale 1; angle range 0 to 90 degrees; sockets Image and Z. 4.5.14 also still has Threshold, Preview and Gamma Correction properties on this node, which the 5.2 page omits. Not run (confirmed from the manual only): the camera Distance and Limits behaviour, artefact advice and the focus pull recipe.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
