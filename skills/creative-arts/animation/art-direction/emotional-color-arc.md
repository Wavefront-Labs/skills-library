---
id: creative-arts.animation.art-direction.emotional-color-arc
name: emotional-color-arc
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, color-script, emotional-color-arc, mood, saturation, value-key, film-structure]
level: advanced
status: draft
description: "Plot a film's emotional curve and map it to value key, saturation and temperature so the color script rises and falls with the story, not the locations."
sources:
  - https://www.khanacademy.org/computing/pixar
  - https://books.google.com/books?vid=ISBN9781138014152
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Emotional color arc

Goal: the colour of the film follows the audience's feelings, beat by beat, so the same location can look
different at the start and end of the story.

## 1. Draw the emotion curve first (no colour yet)
1. List the sequences in order (from the beat sheet or story reel), one column each.
2. For each, score the dominant emotion on two axes: **intensity** (0-10) and **valence** (warm/safe
   vs cold/threatening). Plot both as lines on a strip the width of the color script.
3. Mark the three to five peaks the director cares most about (catalyst, midpoint, all-is-lost, climax,
   final image). These get the most extreme colour; everything else stays more neutral so they can.

## 2. Map emotion to visual variables (pick a rule set, write it down)
| Story variable | Visual variable (typical; invert if the film argues otherwise) |
|---|---|
| Intensity | contrast range and saturation (low = compressed, greyed; high = full range, saturated accents) |
| Safety / warmth | hue temperature and softness of light |
| Isolation | desaturation and cool dominant, single warm accent on the hero |
| Truth revealed | clarity - haze lifts, edges sharpen |

Bruce Block's contrast/affinity rule: affinity (similar colours across shots) calms, contrast excites.
Use affinity in calm stretches so the contrast peaks feel earned.

## 3. Tie colour to character and theme, not to places
- Give the protagonist's emotional state a colour family (e.g. desaturated blue-grey while they believe the
  lie, warming as they change). Locations then get lit *into* that family.
- Revisit a location at two points of the arc and let the change carry meaning (the home that felt cold
  in act 1 glows at the end).

## 4. Failure modes
- Every sequence at full saturation: nothing reads as a peak. Keep 60-70% of the film restrained.
- Colour chosen per location ("the forest is green"): the film becomes a travelogue.
- Arc that contradicts the edit: re-score from the current reel, not the script.

## Verify
- [ ] Emotion curve drawn and agreed with the director before painting.
- [ ] Written mapping table (emotion -> value, saturation, hue) on the color script sheet.
- [ ] Peaks are visibly the most extreme panels when the whole strip is viewed at thumbnail size.
- [ ] At least one location changes colour meaning between acts.

Related: `creative-arts.animation.art-direction.color-script`,
`creative-arts.animation.color.color-scripting-and-key-frames`,
`creative-arts.animation.art-direction.contrast-escalation-toward-climax`.
