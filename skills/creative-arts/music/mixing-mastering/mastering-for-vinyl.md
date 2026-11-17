---
id: creative-arts.music.mixing-mastering.mastering-for-vinyl
name: mastering-for-vinyl
category: creative-arts
field: music
product: mixing-mastering
tags: [mastering, mixing-mastering, vinyl-mastering, lacquer-cutting, side-length, inner-groove-distortion, sibilance, mono-bass, riaa, test-pressing, dmm, vinyl-premaster, phase-and-low-end]
level: advanced
status: draft
description: "Prepare a vinyl premaster: side timing limits, mono low end, sibilance and high-frequency limits, inner-groove planning, loudness, and test-pressing checks."
sources: ["Bob Katz, Mastering Audio (3rd ed.), ch. on vinyl", "https://www.gzvinyl.com/ (pressing plant technical guidelines)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mastering for vinyl

**Goal:** a premaster that cuts cleanly and plays back well on real turntables.

## 1. Physical limits
- **Side length**: louder and bassier = wider grooves = less time. Guidelines (12-inch, 33 1/3 rpm): up to ~18-20 minutes per side for good level; 22+ minutes needs lower level or compromises. 45 rpm 12-inch: ~12 minutes per side, better fidelity.
- **Inner groove**: the groove speed falls toward the centre, so high-frequency detail and level suffer; put quieter, less bright songs last on each side.

## 2. Premaster preparation
- **Low end**: keep bass **mono** below ~150-300 Hz (out-of-phase bass makes vertical groove motion that can make the stylus jump). The cutting engineer may use an elliptical EQ; better to fix in the mix.
- **Sibilance and highs**: strong 5-10 kHz content (sibilance, bright hi-hats) can distort or be limited by the cutting head; de-ess and tame harsh highs.
- **Loudness**: no need for heavy streaming-style limiting; leave dynamics. A dedicated vinyl master with less limiting is common (peaks around -3 to -1 dBFS, no brickwall crushing).
- Deliver 24-bit, 96/48/44.1 kHz WAV per side or per track with a track list, side order, gaps and timings, and notes (fades, segues).

## 3. Working with the cutting engineer
- Supply reference notes and the digital master for comparison.
- Approve **test pressings**: listen for noise, distortion (especially inner tracks), skipping, side balance, and that levels match between sides.

## Gotchas
- Sending the streaming master (heavily limited, stereo bass, bright): distortion, reduced level and possibly skipping.
- Overlong sides forcing a low cut level and more surface noise.
- Wide stereo phasey content in the lows.

## Verify
- Side durations within the plant's guidelines; correlation meter positive in the low end.
- Test pressing approved after playback on more than one turntable.
