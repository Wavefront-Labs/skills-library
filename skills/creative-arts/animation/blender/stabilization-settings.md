---
id: creative-arts.animation.blender.stabilization-settings
name: stabilization-settings
category: creative-arts
field: animation
product: blender
tags: [blender, stabilization, 2d-stabilization, stabilization-settings, stabilization-tracks, autoscale]
level: practitioner
status: docs-checked
description: "Stabilise footage in the Blender Movie Clip Editor: 2D Stabilization panel, track lists, anchor frame, autoscale, expected values, influence, Show Stable, Stabilize 2D node."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/stabilization/panel.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/stabilization/workflow.html
  - https://docs.blender.org/manual/en/latest/compositing/types/tracking/stabilize_2d.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# stabilization-settings

Goal: remove or reduce camera shake with the 2D stabilizer.

## Activate

Tracking mode, Sidebar > Stabilization tab > **2D Stabilization** panel: tick the panel header checkbox, and also enable **Show Stable** in the Clip Display popover to see it in the editor. Set up tracking points to detect the image movement.

## Panel settings

- **Anchor Frame**: other frames are adjusted relative to this frame's position, orientation and scale; pick a frame where the main subject is at its best.
- **Rotation** and **Scale** toggles (Stabilization Type): Rotation stabilizes rotation around a pivot that is the weighted average of the location tracks; Scale compensates scale changes relative to the centre of rotation.
- **Tracks for Stabilization**: *Location* list (compensates jumps) and, with Rotation on, a *Rotation/Scale* list (tilts and scale changes).
- **Autoscale** with **Max**: finds the smallest scale that removes empty black borders; Max limits it.
- **Expected Position / Rotation / Scale** (the position row is labelled Target in the 5.2 sidebar): known motion of the original shot that is subtracted or compensated, for example panning; animate these to let intended camera moves through. The scale value is inactive while Autoscale is on.
- **Influence** (Location, Rotation, Scale, 0 to 1): how much of the calculated compensation is applied. They do not affect the deliberate Expected values.
- **Interpolate**: Nearest, Bilinear or Bicubic (sub-pixel resampling; Bicubic is the highest quality and most expensive).
- Each track also has a **Stabilization Weight** (Track panel) controlling its influence, which can be animated to cross-fade between tracks.

## Workflow notes from the manual

- Start with one carefully tracked point on the main subject; add rotation only if needed; fix slow residual motion with Expected values before adding more markers.
- If more points are needed, aim for symmetry: location points above and below the horizon, rotation points diagonally opposed.
- Motion blur, rolling shutter, pumping autofocus and compression artefacts are hard to fix with stabilization.
- Stabilization parameters can be keyed with I over the control, but the curves cannot be edited graphically; adjust at the exact frame via the control's context menu.

## Output

The compositor **Stabilize 2D** node (Add > Tracking) applies the clip's stabilization: inputs Image and Frame, **Invert** (reverses the stabilization, for example to re-apply shake to CG), a **Filter** (Nearest, Bilinear, Bicubic, Anisotropic) and a Movie Clip property.

## Verify

Toggle Show Stable: features of the chosen tracks stay still and borders are covered by Autoscale or a planned crop.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/sidebar/stabilization/*, compositing/types/tracking/stabilize_2d) and the 5.2 source (space_clip.py 2D Stabilization panel, rna_tracking.cc stabilization properties). Fixed: option names (Rotation and Scale toggles, Expected values, Show Stable in Clip Display), sources entry (was the manual root). Removed unconfirmed claims: autoscale limit of 1.1 to 1.15 and the jello remark.
Method: documentation only; no commands were run.
