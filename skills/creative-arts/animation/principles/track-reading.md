---
id: creative-arts.animation.principles.track-reading
name: track-reading
category: creative-arts
field: animation
product: principles
tags: [animation, lip-sync, track-reading, phonetic-breakdown, exposure-sheet, x-sheet, dialogue, audio, waveform, papagayo, rhubarb]
level: practitioner
status: draft
description: "Break down a dialogue track frame by frame onto an exposure sheet or timeline: phonetic spelling, finding accents, and tools that speed it up."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://github.com/DanielSWolf/rhubarb-lip-sync
  - https://en.wikipedia.org/wiki/Exposure_sheet
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Track reading

Goal: know exactly which sound occurs on which frame before animating dialogue. In 2D
production this is a job (track reader / sheet timer); in CG the animator usually does it.

## Method
1. **Listen** many times. Mark phrases, pauses, breaths and the stressed syllables (accents).
2. **Load the audio** with a waveform and scrub at frame resolution (Blender sequencer/
   timeline with audio scrubbing on; Maya Time Slider with sound; Toon Boom/Harmony sound
   column; any NLE).
3. **Spell phonetically**, not by spelling: "enough" = EE-N-UH-F. Write the sound where it begins.
4. **Mark on the sheet**: in the dialogue column of the x-sheet, write each phonetic sound at
   the frame it starts, with a line to its end. Mark accents with a symbol or underline.
5. **Mark breaths and mouth-closed frames** (m/b/p closures, pauses).

## What matters most
- **Vowels** (open shapes) carry visible lip sync; consonants are mostly brief transitions.
- **Closures** (m, b, p) must be exact - lips must touch.
- **F/V** (teeth on lip) and **OO/W** (pucker) are the other visible shapes.
- **Accents** drive head and body moves (see dialogue accents skill).

## Tools
- Automatic breakdown: Rhubarb Lip Sync (command line, outputs mouth shapes A-H/X with
  times), Papagayo; treat as a first pass, then correct by ear.
- Export as a timed list and import to the rig or x-sheet.

## Failure modes
- Reading by spelling instead of sound.
- Missing closures inside words ("number").
- Track offset errors (audio start not aligned to frame 1) - verify sync on the first
  hard consonant.

## Verify
- [ ] Every syllable has a start frame on the sheet.
- [ ] All m/b/p closures marked.
- [ ] Accents marked and match what the director hears as emphasis.

Related: `creative-arts.animation.principles.mouth-shapes-and-chart`,
`creative-arts.animation.principles.lip-sync-offset`,
`creative-arts.animation.principles.applying-timing-and-spacing`.
