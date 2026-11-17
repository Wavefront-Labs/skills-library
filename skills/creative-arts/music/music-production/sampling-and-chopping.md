---
id: creative-arts.music.music-production.sampling-and-chopping
name: sampling-and-chopping
category: creative-arts
field: music
product: music-production
tags: [music-production, beatmaking, sound-design, sampling, sample-chopping, slicing, transient-detection, time-stretch, pitch-shift, mpc, simpler, sampler, flipping-samples, crate-digging, warp]
level: practitioner
status: draft
description: "Sample and chop audio for beats: choosing sources, slicing by transient or grid, re-sequencing, time-stretch vs repitch, and filtering and layering the flip."
sources: ["https://www.ableton.com/en/live-manual/12/live-instrument-reference/ (Simpler slice mode)", "https://www.ableton.com/en/live-manual/12/audio-clips-tempo-and-warping/", "https://www.akaipro.com/ (MPC user guide - chop modes)", "https://support.apple.com/guide/logicpro/ (Quick Sampler)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sampling and chopping

**Goal:** turn a recording into new musical material (a "flip") that grooves and sits in
key.

## 1. Choosing source material
- Look for open passages: intros, breakdowns, solo instruments, drum breaks with nothing else playing.
- Note key and tempo (detect, then confirm by ear).
- Legal status: see sample-clearance skill **before** releasing.

## 2. Two ways to fit it to the beat
| Method | How | Character |
|---|---|---|
| **Repitch (varispeed)** | speed and pitch change together (Ableton warp off/Re-Pitch mode, MPC/SP-1200 style) | classic, warm; changes key |
| **Time-stretch** | tempo changes, pitch kept (Complex/Complex Pro, Elastique) | flexible; artefacts at large stretches |
- Repitching up a few semitones is the classic hip-hop chipmunk soul sound.

## 3. Chopping
1. Load into a slicer: Ableton Simpler (Slice mode by Transient/Beat/Region/Manual), Logic Quick Sampler (Slice), MPC Chop.
2. Slice by **transient** for drums and staccato parts; by **beat/grid** for loops; manually for melodic phrases.
3. Set each slice's mode: one-shot (plays to end) vs gate (stops on release); add short fades to stop clicks.
4. Re-sequence slices on pads/piano roll into a new phrase; reverse, repitch or retrigger single slices for variation.

## 4. Making it sit
- **Filter**: high-pass the sample (~150-300 Hz) to leave room for your own bass and kick; low-pass for a muffled, distant vibe.
- Layer your own drums, bass and instruments in the sample's key.
- Add saturation/bit reduction to glue sampled and new elements together.
- Chop out the original's drums if they clash with yours (or filter them out).

## Gotchas
- Clicks at slice boundaries: zero-crossing snapping or 2-5 ms fades.
- Stretching vocals a lot sounds phasey; repitch or choose a different section.
- Ignoring the sample's key and tuning (old records are often not A=440): tune your instruments to the sample.

## Verify
- Loop 8 bars: no clicks, the flip grooves, and new instruments are in tune with the sample.
- A/B against the original: your flip should be recognisably new, not just a loop with drums.
