---
id: creative-arts.animation.principles.mouth-shapes-and-chart
name: mouth-shapes-and-chart
category: creative-arts
field: animation
product: principles
tags: [animation, lip-sync, mouth-shapes, mouth-chart, visemes, phonemes, preston-blair, dialogue, 2d, blendshapes]
level: practitioner
status: draft
description: "Use a mouth chart for lip sync: the standard shape set (Preston Blair style and Rhubarb A-X), mapping sounds to shapes, and simplifying shapes for style and speed."
sources:
  - https://books.google.com/books?vid=ISBN9781560100843
  - https://github.com/DanielSWolf/rhubarb-lip-sync
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mouth shapes and the mouth chart

Goal: a small, consistent set of mouth shapes that covers speech, mapped from sounds, so
lip sync is fast and readable.

## A standard set (Preston Blair style / Rhubarb lettering)
| Shape | Sounds | Description |
|---|---|---|
| Closed (A/X) | M, B, P, rest | lips together |
| Slightly open, teeth (B) | most consonants: K, S, T, D, N, G, EE | narrow, teeth visible |
| Open (C) | EH, AE | mid open |
| Wide open (D) | AA, AH | jaw dropped |
| Rounded (E) | AO, ER | slightly rounded |
| Pucker (F) | OO, W, UW | small round |
| F/V (G) | F, V | upper teeth on lower lip |
| L/TH (H) | L, TH | tongue visible on upper teeth |
Rhubarb Lip Sync outputs exactly these letters A-H plus X (idle).

## Mapping rules
- Map sounds by **what you see**, not what you hear: many consonants share one shape.
- Shapes are interpreted per character: a wide-mouthed character's "open" differs from a
  small-mouthed one's. Draw each character's own chart (on the model sheet).
- Hold vowels; let consonants be 1-2 frames transitions.
- Keep **closures** on at least 1-2 frames even if fast.

## Simplifying
- Fast speech: drop small consonant shapes, keep vowels and closures.
- Limited/anime: 3 shapes (closed, half, open) can work if timing is right.
- Realistic CG: shapes become visemes on a facial rig plus jaw; corners (wide/narrow) controlled
  separately from jaw open.

## Failure modes
- Shape on every letter: "chattering" mouth.
- Using the same open shape for all vowels: monotone.
- Mouth shapes not matching the character's design (off-model mouths).

## Verify
- [ ] Every closure shows a closed mouth.
- [ ] Vowel shapes vary with the sound (AH vs OO vs EE).
- [ ] Character's mouth chart exists and is used consistently.

Related: `creative-arts.animation.principles.track-reading`,
`creative-arts.animation.character-design.model-sheet-turnaround`.
