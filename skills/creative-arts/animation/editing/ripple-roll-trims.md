---
id: creative-arts.animation.editing.ripple-roll-trims
name: ripple-roll-trims
category: creative-arts
field: animation
product: editing
tags: [ripple-trim, roll-trim, trimming, trim-tools, trim-mode, sync-locks, premiere-pro, avid, resolve, frame-trimming]
level: practitioner
status: draft
description: "Use ripple and roll trims precisely in Avid, Premiere and Resolve: keyboard trimming by frames, sync locks to keep dialogue in sync, and trim mode review loops."
sources:
  - https://helpx.adobe.com/premiere-pro/using/trimming-clips.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://www.avid.com/learn-and-support
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ripple and roll trims

**Goal:** change shot lengths and cut points by exact frame counts without breaking sync or leaving gaps.

## The two trims

| Trim | Changes | Sequence length |
|---|---|---|
| Ripple | one side of an edit (lengthens/shortens a clip); everything after moves | changes |
| Roll | moves the edit point; outgoing gets longer, incoming shorter (or vice versa) | unchanged |

## Shortcuts

- **Premiere**: Ripple Edit tool (B), Rolling Edit tool (N); Trim mode with Shift+T; nudge selected edit by
  frames with Ctrl/Cmd+Left/Right (trim -1/+1) and Ctrl/Cmd+Shift for multi-frame (default 5). Q/W ripple
  trim previous/next edit to playhead.
- **Resolve**: Trim Edit mode (T), select edit side with U / V (cycle); comma/period nudges 1 frame,
  Shift+comma/period multi-frame. Ripple vs roll determined by where you click the edit in trim mode.
- **Avid**: Trim mode (U), select A-side/B-side/both (P, ], [ in default keyboard), trim keys M , . / for -10,
  -1, +1, +10 frames, with play loop (6/space) to review.

## Keep sync

- **Sync locks** (Premiere/Avid: track sync lock toggles; Resolve: Auto-track selectors and linked selection)
  ensure that ripple trims on V1 ripple all locked audio tracks equally, so dialogue below later shots stays
  in sync.
- Trimming only picture of a linked clip (J/L cut) requires unlinking or the trim mode's link override
  (Alt/Option in Premiere) - see `creative-arts.animation.editing.dialogue-and-action-timing-splices`.

## Animation specifics

Shots in production have fixed animated lengths: a ripple that extends a shot beyond its rendered frames shows
freeze/black. Trim within the available media (handles), and send extensions as a change list.

## Verify

After trims, sequence length changed by exactly the intended frames (ripple) or not at all (roll); a dialogue
line later in the reel still matches the mouth/board it belongs to.
