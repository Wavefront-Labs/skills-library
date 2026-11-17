---
id: creative-arts.animation.blender.eevee-depth-of-field
name: eevee-depth-of-field
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, eevee-dof, dof-max-size, depth-of-field]
level: practitioner
status: docs-checked
description: "Tune EEVEE depth of field quality: max size, sprite threshold, neighbor rejection, jitter camera sample count, and over-blur; camera optics live on the camera."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/depth_of_field.html
  - https://docs.blender.org/api/current/bpy.types.SceneEEVEE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eevee-depth-of-field

Goal: EEVEE depth of field that matches the camera settings without halos or noise.

The optical settings (focus, aperture) are on the camera (camera settings in Properties); this skill covers the quality settings in Render Properties > Depth of Field. In the 3D viewport, depth of field only works in Camera View.

## How it works

EEVEE uses a post-process filter plus an optional sample-based method:
- Post-process: a blur pass (cannot make good bokeh for highlights), then a sprite-based pass that only improves very bright isolated highlights, because it is too slow to apply everywhere.
- Sample-based (Jitter Camera): randomises the camera position for every sample; more accurate but needs many samples for a smooth result.

## Settings

- **Max Size** (pixels): maximum size of the post-process effect; lower is faster. 0 disables the post-process effect but not the sample-based method.
- **Sprite Threshold**: minimum brightness for a pixel to be considered by the sprite pass. Higher improves performance but reduces highlight quality. Brightness is in the scene's referred colour space.
- **Neighbor Rejection**: maximum intensity considered in sprite neighbourhood rejection; set to a brightness above which differences are small after colour management. Lower improves performance but reduces highlight quality.
- **Jitter Camera**: randomises the camera position every render sample (final render only per the API description). It can change the actual sample count: the count follows (ring_count^2 + ring_count) * 3 + 1 for a hexaweb pattern whose ring count is chosen so the pattern holds at least the sample count set in Sampling, so it can grow quickly.
- **Over-blur**: scales the post-process radius to reduce artifacts from undersampling; higher values soften the bokeh shape.

## Workflow

1. Set focus and aperture on the camera and look through Camera View.
2. Raise Max Size only if large blur gets cut off.
3. For accurate bokeh in finals, enable Jitter Camera and raise render samples; add Over-blur if a sample pattern remains visible.
4. For post flexibility, render sharp with a depth pass and use the compositor Defocus node (see comp-defocus-bokeh). Use a focus empty for animated focus (see focus-pull).

## Verify

Render a frame with a sharp subject and a blurry background with highlights. The subject edges should be clean and the highlights should show the aperture shape.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Depth of Field) and the SceneEEVEE properties in the 5.2 source. Confirmed: Max Size (0 disables post-process), Sprite Threshold, Neighbor Rejection, Jitter Camera and its sample formula, Over-blur, Camera View note. Wrong claims removed: "Denoise Amount" and "High Quality Slight Defocus" settings do not exist in the 5.2 properties. Removed unconfirmed: default Max Size, sample recommendations, halo behaviour on hair.
Method: documentation only; no commands were run.
