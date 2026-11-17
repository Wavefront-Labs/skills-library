---
id: creative-arts.music.composition.music-stems-delivery-and-cue-sheets
name: music-stems-delivery-and-cue-sheets
category: creative-arts
field: music
product: composition
tags: [composition, media-composition, music-stems-delivery, music-cue-sheet, dub-delivery, stems, pro-tools, cue-sheet]
level: practitioner
status: draft
description: "Deliver score to the dub stage: stem layout, naming, sample rate and timecode start, Pro Tools session prep, and the music cue sheet for PROs."
sources: ["https://www.ascap.com/help/royalties-and-payment/cue-sheets", "https://www.bmi.com/creators/detail/cue_sheets", "Richard Davis, Complete Guide to Film Scoring (Berklee Press)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Music stems delivery and cue sheets

**Goal:** the re-recording mixer can rebalance any cue without calling you, and the
cue sheet makes sure royalties are paid.

## 1. Agree the spec in writing
Sample rate/bit depth (48 kHz/24-bit is standard for picture), frame rate, timecode
start, channel format (stereo, 5.1, 7.1.2/Atmos), stem layout, file naming and whether
a printed full mix is also wanted.

## 2. Typical stem layout per cue
`DRUMS/PERC`, `BASS/LOW`, `STRINGS`, `BRASS`, `WINDS`, `SYNTHS/FX`, `CHOIR/VOX`,
`SOLO/FEATURE` - plus the **full mix**. The sum of stems must null against the full mix
(phase-invert test).
- Print effects (reverb) into each stem rather than on a shared return, or deliver the
  reverb as its own stem.
- No master-bus limiting on stems; the dub decides final level.

## 3. File and session prep
- Name: `1M03_v2_STRINGS_51.wav` (cue, version, stem, format).
- Every file starts at the cue's timecode start (spot as **broadcast WAV** with
  timestamp) or at a common two-pop/start mark.
- Include a few seconds of pre-roll and full reverb tails.
- Pro Tools: one track per stem, cues placed at timecode, clip names matching files.

## 4. Music cue sheet
A cue sheet lists every piece of music in the final cut, for the PROs (ASCAP, BMI,
PRS etc.). Per cue: cue number, title, composer(s) with PRO and share, publisher(s),
**usage** (background instrumental, background vocal, visual vocal, main/end title,
logo), and **timing** (duration used in the final cut, not the written length).
It is usually filed by the production company or its music supervisor after the final
mix; the composer checks it.

## Gotchas
- Delivering stems that do not sum to the approved mix is the most common rejection.
- Durations on the cue sheet must come from the final locked cut.
- Source songs licensed from others also go on the cue sheet with their own owners.

## Verify
- [ ] Stems null against the full mix for every cue.
- [ ] Files are timestamped and start at the cue's timecode.
- [ ] Cue sheet usages and durations match the final cut.
