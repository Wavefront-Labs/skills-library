---
id: creative-arts.animation.blender.nla-transitions-meta
name: nla-transitions-meta
category: creative-arts
field: animation
product: blender
tags: [blender, nla, nla-transitions, transition-strip, blend-in-out, nla-meta-strips, meta-strips, auto-blend, clip-sequencing]
level: practitioner
status: docs-checked
description: "Sequence clips smoothly in Blender's NLA: blend in/out and auto blend, transition strips between two strips on one track, and grouping strips into meta strips."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/nla/strips.html
  - https://docs.blender.org/manual/en/5.2/editors/nla/sidebar.html
  - https://docs.blender.org/manual/en/5.2/editors/nla/editing/strip.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# nla-transitions-meta

Goal: idle to walk to run blends without visible pops, and manageable groups of strips.

## Blend in/out (Sidebar > Strip > Active Strip)

- **Blend In / Out**: frames it takes the strip's influence to ramp up at the start and wind down at the end.
- **Auto Blend In/Out**: calculates Blend In/Out from strips on the track above or below that overlap the strip in time. Overlap strips on adjacent tracks and enable it.
- Set the upper strip's Blending (Replace or Combine) and Extrapolation (Hold Forward or Nothing); see `nla-blending-extrapolation`.

## Transition strips

- A transition strip interpolates between two neighbouring action strips. Select both and use Add > Transition (Shift-T).
- For more control use overlapping tracks with Blend In/Out or an animated influence.

## Meta strips

- Strip > **Make Meta** (Ctrl-G) groups the selected strips; **Remove Meta** (Ctrl-Alt-G) ungroups them.
- A meta strip lets you move, scale and copy the strips as one unit. Make Single User does not recurse into meta strips.

## Matching poses

Before blending locomotion, line up contact phases between clips (offset strips so the contacts coincide) to avoid foot sliding. Strip > Transform > Swap (Alt-F) swaps the order of selected strips in a track.

## Gotchas

- Transitions above a tweaked strip can break keyframe remapping for channels the transition affects.
- Auto Blend looks at overlapping strips on the tracks above or below, so put overlapping blends on adjacent tracks.

## Verify

Scrub through the blend region: no pop, stable foot contacts, and the influence curve visible when Animated Influence is used.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source), NLA Strips, Sidebar and Editing Strips pages: Blend In/Out and Auto Blend definitions, Transition strips (Add > Transition, Shift-T), Make Meta / Remove Meta with Ctrl-G and Ctrl-Alt-G, Swap. Corrected: meta strips are Strip > Make Meta, not "Add > Add Meta-Strips"; transition strips need two neighbouring strips and are not described as filling a gap. Removed as unconfirmed: 8-12 frame overlap, missing-channel snap claim.
Method: documentation only; no commands were run.
