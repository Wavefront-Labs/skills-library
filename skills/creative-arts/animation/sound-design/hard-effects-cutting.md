---
id: creative-arts.animation.sound-design.hard-effects-cutting
name: hard-effects-cutting
category: creative-arts
field: animation
product: sound-design
tags: [hard-effects, sfx-editing, effects-editing, sync-effects, track-layout, checkerboarding, sound-editing, spotting]
level: practitioner
status: draft
description: "Cut hard (sync) effects for an animated scene: spotting to frames, layering attack/body/tail, track layout for the mix and editing for impact over realism."
sources:
  - https://www.avid.com/pro-tools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hard effects cutting

**Goal:** every on-screen event that makes a sound (doors, impacts, vehicles, machines, explosions) has an
effect cut in sync, organised so the mixer can balance it.

## Hard effects vs other effects

- **Hard effects:** sync, tied to picture events.
- **Backgrounds:** continuous ambience (see `creative-arts.animation.sound-design.background-tracks-cutting`).
- **Foley:** performed human-scale sounds (feet, cloth, props).
- **Design:** non-literal (whooshes, tonal hits, magic) (see `creative-arts.animation.sound-design.whoosh-and-impact-design`).

## Cutting

1. Spot from the cut (spotting notes from `creative-arts.animation.editorial.spotting-sessions`).
2. Sync the transient to the frame of contact. Animation often has a "smear" or impact frame; the hit goes on the
   first frame of the impact drawing, not the anticipation.
3. Layer per event: **attack** (sharp transient, high), **body** (mid, the material), **tail** (low or
   reverberant decay). Three good layers beat ten.
4. Trim heads tight, leave tails natural; fade every edit (a few ms).
5. Pitch and level to the object's size; the same door sounds different on a giant than a mouse.

## Track layout

- Checkerboard: alternate effects across tracks (FX1, FX2, FX3...) so overlapping events and tails never share a
  track and can be mixed separately.
- Group by type when the mix is large: vehicles, weapons, impacts on separate track groups.
- Name clips meaningfully; mixers read clip names.

## Animation priorities

Impact over realism: animated action is exaggerated, so effects can be bigger and more stylised, but stay consistent
with the show's sound bible (realistic for an action drama, cartoony for slapstick:
`creative-arts.animation.sound-design.cartoon-sfx-vocabulary`).

## Verify

Mute dialogue and music: every visible event has a sound in sync within one frame, nothing overlaps on one track,
and effects levels before the mix leave headroom (peaks below about -6 dBFS).
