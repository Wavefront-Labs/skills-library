---
id: creative-arts.animation.blender.keying-screen
name: keying-screen
category: creative-arts
field: animation
product: blender
tags: [blender, keying, keyer, keying-screen, motion-tracking, green-screen]
level: practitioner
status: docs-checked
description: "Handle uneven green screens with the Keying Screen node: tracking markers in a separate object, Movie Clip, Tracking Object, Smoothness, and the Screen output into Key Color."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/keying/keying_screen.html
  - https://docs.blender.org/manual/en/latest/compositing/types/keying/keying.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# keying-screen

Goal: key footage where the screen colour changes across the frame (falloff, hot spots, shadows).

## How it works

The Keying Screen node creates a gradient plate from colours sampled at motion tracking points on a movie clip. Used as the Keying node's Key Color (or similar), it gives each pixel a local screen colour to key against, which helps with uneven green screens.

## Steps

1. In the Movie Clip Editor, open the Sidebar and Toolbar to show the tracking tools.
2. Create a new tracking object in the Objects selector (Object panel), because tracks used for gradients are not useful for camera solving.
3. Place tracking markers on bare screen areas across the frame. Tracks may be tracked or moved manually so the gradient updates over time; a marker that is not enabled on a frame is not used for that frame's gradient. Tracks can have an offset to make featureless screens easier to track.
4. In the compositor add the **Keying Screen** node (Keying category): choose the **Movie Clip** and the **Tracking Object**, and set **Smoothness**.
5. Connect its **Screen** output to the **Key Color** input of the Keying node.

## Tips

- Disable markers on frames where the subject passes over them so they do not sample the subject's colour.
- View the Screen output directly: it should look like a smooth version of the empty screen.
- With a Keying Screen the Keying node's Black Level can stay low.

## Gotchas

- The gradient is only as good as screen coverage; large empty areas between markers are interpolated.
- Check the node output on the first and last frames of the shot.

## Verify

Compare the matte with a single eyedropped key colour against the Keying Screen version. Dark corners and hot spots should key evenly with the screen.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Keying Screen Smoothness input, Movie Clip and Tracking Object properties, Screen output, the separate tracking object for gradient tracks, per-frame marker enabling, and its use as Keying node Key Color. Removed the marker-position advice for edges and the locked-camera static-marker claim.
Method: documentation only; no commands were run.
