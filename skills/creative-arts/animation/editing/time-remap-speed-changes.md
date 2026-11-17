---
id: creative-arts.animation.editing.time-remap-speed-changes
name: time-remap-speed-changes
category: creative-arts
field: animation
product: editing
tags: [time-remap, edit-effects, speed-change, retime, frame-blending, optical-flow, constant-speed, speed-ramp, frame-sampling, premiere, resolve]
level: practitioner
status: draft
description: "Retime clips in the edit (constant speed, speed ramps, time remapping) with the right frame interpolation for animation: frame sampling vs blending vs optical flow."
sources:
  - https://helpx.adobe.com/premiere-pro/using/time-remapping.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Time remapping and speed changes in the edit

**Goal:** adjust timing in the cut (hold a beat, speed up an action, ramp into slow motion) and communicate
the change accurately to animation, because editorial retimes on rendered animation are usually temporary.

## Tools

- **Constant speed**: Premiere Clip - Speed/Duration (Ctrl/Cmd+R), Resolve Change Clip Speed (R). Keep "Ripple
  edit, shifting trailing clips" consistent with your intent.
- **Variable speed / ramps**: Premiere Time Remapping (keyframes on the clip's speed rubber band), Resolve Retime
  Controls (Ctrl/Cmd+R on the clip) with speed points and Retime Curve.
- **Freeze frame / hold**: Premiere Frame Hold Segment; Resolve Freeze Frame.

## Interpolation choice (matters most for animation)

| Mode | Result | For animation |
|---|---|---|
| Frame sampling (nearest) | repeats/drops whole frames | best for drawn/stepped animation: keeps clean drawings |
| Frame blending | cross-dissolves neighbouring frames | ghosting on line art; avoid |
| Optical flow | synthesises in-betweens | smears line art and flat colour; artefacts on overlapping limbs |

Use frame sampling for 2D and stylised work; optical flow only for smooth CG camera moves as a temp.

## Communicate retimes

- An editorial retime on an animated shot is a note to animation, not a final fix: list it in the change list
  with the speed ratio or the new frame count, plus a reference movie.
- For held frames, give the frame number to hold and duration.
- Lighting and FX re-render at the new timing once animation updates.

## Gotchas

- Speed changes on linked audio change pitch unless "Maintain audio pitch" is on; dialogue usually needs a
  re-cut instead.
- Retimed clips often fail AAF/XML exchange (`creative-arts.animation.editing.editorial-version-control-and-conform`);
  render or document them.
- 50% on 24 fps animation on twos becomes "on fours": readable as stutter.

## Verify

Frame-step the retimed section: no blended/ghosted frames (if sampling), the duration matches the intended
frame count, and the change list records the retime.
