---
id: creative-arts.animation.editorial.match-cuts-and-graphic-cuts
name: match-cuts-and-graphic-cuts
category: creative-arts
field: animation
product: editorial
tags: [match-cut, graphic-match, match-on-action, continuity-editing, transitions, layout-handoff, storyboarding]
level: practitioner
status: draft
description: "Plan and execute match-on-action and graphic match cuts in animation: matching screen position, shape and motion vector across the cut, and briefing layout."
sources:
  - https://www.mheducation.com/highered/product/film-art-introduction-bordwell-thompson/M9781260056082.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Match cuts and graphic cuts

**Goal:** a cut the audience feels as continuous (match on action) or as a deliberate rhyme between two images
(graphic match).

## Types

| Cut | What matches | Example |
|---|---|---|
| Match on action | a movement continues across the cut from a new angle | a character sits: wide to close, the sit continues |
| Graphic match | shape, position, colour or composition | a spinning coin cuts to a spinning planet |
| Motion match | direction and speed of movement | a whip pan out of one scene into a whip pan into the next |
| Sound match | a sound bridges two images | a scream becomes a kettle whistle |

## Doing it in animation (you control both sides)

1. **Board both shots with an overlay:** story draws the end pose of A and start pose of B on onion-skin so the
   matched element sits in the same screen position.
2. **Brief layout numerically:** give the frame, the matched element's screen position (e.g. centre x 960 y 420) and
   scale; layout locks both cameras to it.
3. **Animate across the cut:** on match on action, overlap the action by 2-4 frames (B starts slightly before where A
   ended); the eye loses a few frames at a cut, so exact continuity reads as a hiccup.
4. Cut **during** the movement, ideally at its fastest point, not at a hold.

## In the NLE

Stack shot B above A, set opacity 50% and align the matched element frame by frame, then trim to the overlap and
restore opacity. Onion-skin comparison is the fastest check.

## Gotchas

- Screen direction must hold across a match cut (180-degree rule) unless the reversal is the point.
- Lighting/colour that differs a lot between shots makes a graphic match look accidental; ask art direction for a
  shared value (see `creative-arts.animation.art-direction.value-matching-across-cuts`).

## Verify

Played at speed, viewers in a screening do not notice the match-on-action cut; for graphic matches the matched shape
sits within a few percent of the same screen position on both sides.
