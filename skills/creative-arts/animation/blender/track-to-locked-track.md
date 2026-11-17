---
id: creative-arts.animation.blender.track-to-locked-track
name: track-to-locked-track
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, track-to, track-to-constraint, locked-track, damped-track, aim-constraint, eye-aim]
level: practitioner
status: docs-checked
description: "Aim objects and bones in Blender with Track To (track and up axes, Target Z), Damped Track (swing rotation) and Locked Track (rotate around one axis)."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/tracking/track_to.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/tracking/locked_track.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/tracking/damped_track.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# track-to-locked-track

Goal: pick the aim constraint that gives stable orientation for the job.

## Track To

- **Track Axis**: the owner's local axis that points at the target (for bones typically Y; a negative axis points away). **Up**: the local axis that should point upwards in the world. **Target Z**: align the Up axis to the target's Z axis instead of the global one.
- Track Axis and Up must differ, otherwise the constraint stops working and its icon turns red.
- If the owner is almost directly above the target the roll becomes unstable; the manual recommends Damped Track for that case.

## Damped Track

- Only a **Track Axis** (typically Y for bones). It uses a pure swing rotation to minimise rolling around the tracking axis, with no Up axis.

## Locked Track

- **Track Axis** points at the target while the **Locked Axis** keeps its orientation: the owner can only rotate around that one axis, and the other two stay in their original plane. Track Axis and Locked Axis must differ (red icon otherwise). Manual examples: distant tree billboards that face the camera but stay upright, a compass needle that spins horizontally towards a magnet.
- It can be combined with other Track constraints: a Damped Track first orients the X/Y plane toward one target, then a Locked Track rotates within that plane toward another.

## Recipes

- **Camera aim**: Empty `cam_target`, Track To on the camera with Track Axis set to the camera's viewing direction and Up set to its up axis. Animate the empty, not camera rotation.
- **Eyes**: each eye bone Damped Track (Track Axis Y) to its own target; both targets parented to a master `eyes` control.
- **Piston**: cylinder A Locked Track to B, B Locked Track to A, Locked Axis = hinge axis.

## Gotchas

- Track Axis and Up (or Locked Axis) set to the same axis disable the constraint.
- Influence below 1 blends the aim with the owner's own rotation.

## Verify

Move the target around the owner, including overhead: owner aims correctly, no sudden flip (Track To may roll unstably directly overhead).

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Track To, Damped Track and Locked Track pages: Track Axis, Up, Target Z, Locked Axis, red-icon rule for identical axes, overhead instability and the Damped Track recommendation, the Damped then Locked Track combination. Removed unconfirmed camera axis defaults, keyframe override and bone Up-axis claims.

Method: documentation only; no commands were run.
