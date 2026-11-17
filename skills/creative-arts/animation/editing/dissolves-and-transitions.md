---
id: creative-arts.animation.editing.dissolves-and-transitions
name: dissolves-and-transitions
category: creative-arts
field: animation
product: editing
tags: [dissolves, cross-dissolve, transitions, fades, dip-to-black, handles, premiere-pro, resolve, avid, edit-effects]
level: practitioner
status: draft
description: "Add dissolves, fades and dips in an animation cut: default durations, alignment, the handle frames they consume, and how to tell production to render them."
sources:
  - https://helpx.adobe.com/premiere-pro/using/applying-transitions.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dissolves and transitions

**Goal:** use dissolves deliberately (time passing, a dream, a soft scene change) and make sure animation renders
enough frames to support them.

## Applying

- **Premiere:** Ctrl/Cmd+D applies the default video transition (Cross Dissolve), Ctrl/Cmd+Shift+D the default audio
  crossfade (Constant Power). Default duration in Preferences > Timeline (set it in frames, e.g. 24). Alignment:
  *Center at Cut*, *Start at Cut* or *End at Cut*.
- **Resolve:** Ctrl/Cmd+T adds the standard transition; set the default under Preferences > User > Editing.
- **Avid:** Quick Transition (\\) with position and duration fields.

## Handles

A centred 24-frame dissolve needs 12 frames **past** the outgoing shot's out point and 12 **before** the incoming
shot's in point. If the media is not there, Premiere repeats the last frame (transition shows a diagonal-line
warning) and Resolve refuses or shortens the transition. In animation those frames must be animated, so:

1. Mark the dissolve in the cut and in the turnover/EDL (EDL event type `D` with duration).
2. Tell layout/animation the shot needs N extra frames of head or tail (overlap) for the dissolve.
3. Until they arrive, use *End at Cut*/*Start at Cut* on whichever side has frames.

## Craft rules

- A dissolve says "time passed"; use a straight cut inside a continuous scene.
- Dip to black (fade out, fade in) separates acts and ad breaks; broadcast ad breaks usually want a short black.
- Mid-dissolve frames double-expose line art and look muddy on bright frames; shorter dissolves (8-12 frames) suit
  limited animation, 24-48 frames suit painted backgrounds.
- Audio: crossfade under the dissolve, or prelap the incoming scene's sound (J-cut) which is usually stronger.

## Verify

Play the dissolve and step through its middle: no frozen frames on either side, and the EDL lists the transition
with the right duration for the online conform (see `creative-arts.animation.editing.editorial-version-control-and-conform`).
