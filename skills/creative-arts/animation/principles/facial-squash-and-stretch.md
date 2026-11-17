---
id: creative-arts.animation.principles.facial-squash-and-stretch
name: facial-squash-and-stretch
category: creative-arts
field: animation
product: principles
tags: [animation, facial-squash-stretch, squash-and-stretch, facial-animation, jaw, cranium, dialogue, takes, blendshapes, face-rig]
level: practitioner
status: draft
description: "Squash and stretch the face as two masses (cranium and jaw) so dialogue, blinks and takes have life without breaking the character's volume or model."
sources:
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://books.google.com/books?vid=ISBN9781560100843
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Facial squash and stretch

Goal: the face compresses and extends with the action - smiles squash, gasps stretch -
while the head keeps its volume and stays on model.

## The model: two masses
Treat the head as a fixed **cranium** and a moving **jaw/cheek mass** joined by flesh.
- Jaw opens -> lower face stretches, cheeks thin, the eye mass is pulled slightly down,
  the cranium itself does not grow.
- Jaw closes on a smile or an "m/b/p" -> lower face squashes, cheeks bulge up into the
  lower lids, the eyes narrow.
- The total area of the head stays roughly constant (Preston Blair's volume rule).

## Where to use it
1. **Dialogue** - open vowels (ah, oh) stretch; closed consonants and smiles squash. Alternate
   keeps lip sync from looking like a hinged puppet.
2. **Blinks** - in broad styles the upper face squashes slightly as the lids close and
   recovers on open.
3. **Takes** - anticipation squash (face compresses, eyes shut), then the take stretch (jaw
   drops, brows fly up, head elongates), then settle to a held reaction. Two to four frames of
   squash before a strong stretch.
4. **Head turns and nods** - a slight squash at the bottom of a nod adds weight.

## Calibrating to the style
- Realistic and CG feature: 5-10 % change, mostly in cheeks and jaw. Rig: jaw-driven
  corrective shapes, cheek puff, a head-squash control with volume preservation.
- Broad TV cartoon: 20-40 %, cranium may deform too on takes.
- Anime and iconic styles: often none except on comedic takes - check the style guide.

## Failure modes
- Scaling the whole head uniformly: reads as the head inflating, not flesh moving.
- Eyes and brows sliding off the skull while the jaw stretches: lock eye position to the
  cranium mass and only pull lids.
- Squash and stretch on every syllable at equal strength: the face jitters. Accent the
  stressed syllables only.
- Losing the jaw hinge: the chin should travel on an arc around the ear, not straight down.

## Verify
- [ ] Overlay the extremes: head area roughly equal.
- [ ] Jaw path traces an arc pivoting near the ear.
- [ ] Stressed syllables get the biggest stretch; others are small.
- [ ] Freeze any frame: still on model for the show's stylization level.

Related: `creative-arts.animation.principles.lip-sync-offset`,
`creative-arts.animation.character-design.expression-design`,
`creative-arts.animation.principles.takes-and-double-takes`.
