---
id: creative-arts.animation.voice-tts.mouth-chart-and-viseme-set-design
name: mouth-chart-and-viseme-set-design
category: creative-arts
field: animation
product: voice-tts
tags: [viseme-set, mouth-chart, visemes, phonemes, lip-sync, preston-blair, rhubarb-shapes]
level: practitioner
status: draft
description: "Design a mouth chart for 2D or 3D lip-sync: phoneme-to-viseme grouping, Preston Blair style sets, Rhubarb shape letters, drawing rules and naming for automation."
sources:
  - https://github.com/DanielSWolf/rhubarb-lip-sync
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Mouth chart and viseme set design

A **viseme** is a mouth shape that looks the same for a group of phonemes. A set of 6-12 shapes covers dialogue for most animation.

## Common sets
- **Preston Blair / classic cartoon set**: a roughly ten-shape chart (closed rest; "A/I"; "E"; "O"; "U"; "M/B/P"; "F/V"; "L/th"; "W/Q"; "C/D/G/K/N/R/S/T/Z" consonant shape). The exact count and letters differ in charts that copy it.
- **Rhubarb Lip Sync shapes** (a useful automation target): basic shapes **A** (closed: M, B, P), **B** (slightly open, teeth together: most consonants and EE), **C** (open: EH, AE), **D** (wide open: AA), **E** (rounded: AO, ER), **F** (puckered: UW, OW, W). Extended shapes: **G** (F, V: upper teeth on lower lip), **H** (long L), and **X** (idle/rest).
- 3D rigs often use blendshapes named for visemes (for example from the ARKit or MPEG-4 viseme sets) in place of swapped drawings.

## Design rules
1. Grouping is by **appearance**, not by sound: B/P/M share one closed shape, F/V share the lip-on-teeth shape.
2. Start with 6-8 shapes; add more only if the character design benefits.
3. Draw every shape for every head angle that the show uses (front, three-quarter, profile).
4. Exaggerate differences between neighbouring shapes so they read at the shot's size.
5. Keep jaw, lips and tongue consistent with character style; teeth-visible rules should match the design bible.
6. Provide a rest/idle shape with a clear difference from a closed M shape.

## Naming for automation
Use the same IDs in the art, rig and tools: for Rhubarb-compatible output, name drawings or blendshapes `A`...`H`, `X` (or map them in a table), so cues from `forced-alignment-of-transcript-to-audio.md` or Rhubarb map straight to frames or blendshape weights.

## Verify
- [ ] Mouth chart sheet signed off for every angle.
- [ ] Phoneme-to-shape table committed with the rig.
- [ ] Test line reads clearly without audio on a muted playback.
