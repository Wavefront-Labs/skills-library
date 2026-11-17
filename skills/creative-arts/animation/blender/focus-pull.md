---
id: creative-arts.animation.blender.focus-pull
name: focus-pull
category: creative-arts
field: animation
product: blender
tags: [blender, camera-animation, focus-pull, rack-focus, dof, focus-object, f-stop, depth-of-field]
level: practitioner
status: docs-checked
description: "Animate focus in Blender: focus object vs focus distance, a focus Empty keyed between subjects for rack focus, F-Stop and checking the result."
sources:
  - https://docs.blender.org/manual/en/latest/render/cameras.html#depth-of-field
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# focus-pull

Goal: shift attention between subjects with a rack focus that reads clearly.

## Setup

- Camera data > Depth of Field ON. **Focus on Object**: an Empty `focus_target` (better than focusing on a character mesh origin). **F-Stop**: lower values give a strong depth of field effect. Longer focal lengths and closer subjects make the shift more visible.

## Rack focus

1. Place the focus empty on subject A's eyes at frame 100; key location.
2. A few frames later, snap the empty to subject B's eyes (select eye vertex/bone, Shift S > Cursor to Selected, then empty Selection to Cursor); key.
3. Ease the pull with Bezier handles in the Graph Editor, or hold with Constant interpolation then pull fast.
Alternative: parent the empty with two Child Of constraints to A and B heads with keyed influence (constant interpolation) and a separate short location blend.

## Without an object

Animate **Focus Distance** directly (Focus Object overrides it when set); enable Viewport Display > **Limits** on the camera to show the focus point as a yellow cross, which can be dragged if the viewport camera DOF-distance gizmo is on. In the viewport, hover over Focus Distance and press E to sample a point with the depth picker.

## Checking

- Check in camera view with a rendered viewport, then render a few frames at final quality.

## Gotchas

- Focus empty parented to an animating head stays on the head — good — but parented focus on the camera follows the camera, not the subject.

## Verify

Scrub in camera view: subject A sharp before the pull, B sharp after, transition time as planned.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST), render/cameras (Depth of Field: Focus Object overrides distance, Focus Distance picker with E, Show Limits cross and gizmo, F-Stop, Blades). Removed unconfirmed f-stop values, timings, viewport DOF overlay and compositing claims.
Method: documentation only; no commands were run.
