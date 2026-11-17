---
id: creative-arts.animation.color.group-and-timeline-grading
name: group-and-timeline-grading
category: creative-arts
field: animation
product: color
tags: [group-grading, timeline-grading, groups, pre-clip, post-clip, resolve, look-and-matching, sequence-look]
level: practitioner
status: draft
description: "Grade sequences and whole episodes at once with Resolve groups (pre-clip, post-clip) and timeline-level nodes, so look changes are one edit, not two hundred."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Group and timeline-level grading

**Goal:** separate per-shot correction from sequence looks and show looks, each at its own level.

## The four levels in Resolve

| Level | Applies to | Typical use |
|---|---|---|
| Group Pre-Clip | all clips in the group, before the clip grade | shared input correction (e.g. a render-version offset) |
| Clip | that clip | balance, match, secondaries |
| Group Post-Clip | all clips in the group, after the clip grade | the sequence look from the colour script |
| Timeline | every clip in the timeline, last | show look, output LUT, limiter |

Switch level with the node editor's dropdown (Clip / Group Pre-Clip / Group Post-Clip / Timeline).

## Setting up groups

Select clips in the Color page thumbnail timeline > right-click > *Add into a New Group* (name it by sequence:
`SQ020_NIGHT`). A clip can be in only one group; plan groups by look, not by edit order, when a sequence
intercuts two locations.

## Workflow

1. Timeline node: show look LUT (`creative-arts.animation.color.creative-look-luts`) and output transform, so every
   shot is seen through it from the start.
2. Group post-clip: sequence mood (night blue, flashback desaturated).
3. Clip: matching only.
4. The director's sequence-wide note becomes one node change at the group level.

## Gotchas

- Copying a clip grade does not copy group membership or group grades; the target needs to be in the group.
- Exporting clip-level DRX does not include group/timeline nodes; for vendor hand-offs, flatten (render) or export
  each level.
- Timeline-level nodes are per timeline: a new conform timeline needs them copied (or the timeline duplicated).

## Verify

Toggle the group post-clip level off for a sequence: all its shots return to the neutral matched state together;
toggling back restores the look identically across shots.
