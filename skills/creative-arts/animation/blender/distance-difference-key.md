---
id: creative-arts.animation.blender.distance-difference-key
name: distance-difference-key
category: creative-arts
field: animation
product: blender
tags: [blender, keying, keyer, distance-key, difference-key, clean-plate]
level: practitioner
status: docs-checked
description: "Special-case keys: Distance Key (Key Color, RGB or YCC, Tolerance, Falloff) and Difference Key (Image 1, clean plate Image 2), with limits and when to use the Keying node."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/keying/distance_key.html
  - https://docs.blender.org/manual/en/latest/compositing/types/keying/difference_key.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# distance-difference-key

Goal: keys for unusual cases: non-green screens, or a locked camera with a clean plate.

## Distance Key node (Keying category)

Alpha is based on the 3D distance between each pixel colour and the **Key Color** in a colour space. Works well for singling out a specific colour that is not necessarily green.
- **Color Space**: RGB or YCC (in YCC only the Cb and Cr channels are used for the distance).
- **Tolerance**: how close a pixel must be to count as an absolute match.
- **Falloff**: with a high value, pixels closer to the key colour are more transparent than those further away; with a low value, anything within tolerance is simply transparent.
- Outputs: **Image** and **Matte**.

## Difference Key node (Keying category)

Isolates foreground content by comparing it with a reference background.
- **Image 1**: foreground content against the background to be removed.
- **Image 2**: the reference background (a clean plate).
- **Tolerance**: pixels matching the reference within this threshold become transparent.
- **Falloff**: raise to make nearby pixels partially transparent for a smoother edge.
- Outputs: Image and Matte.

Uses: locked-off camera shots with a clean plate, removing people from a background, extracting a subject without a screen.

## Tips

- Difference keys depend on the plate and the shot matching; noise or lighting changes produce false matte areas. Test with the Matte output.
- The subject's shadows differ from the clean plate too, so they become part of the matte. Useful for shadow transfer, a problem otherwise.

## When to use the Keying node instead

Green or blue screens are what the Keying node is built for: it does chroma keying and despill in one node (see keying-node-settings).

## Verify

Check the matte with a Viewer, sampling the background (should be 0) and the subject's darkest areas (should be 1). Then composite over a new background.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Distance Key inputs and Color Space, Tolerance, Falloff semantics; Difference Key Image 1, Image 2, Tolerance, Falloff; the Keying node is the one-stop green and blue screen node. Removed the pre-blur advice, the generous-tolerance advice and the brightness-versus-colour claim for YCC.
Method: documentation only; no commands were run.
