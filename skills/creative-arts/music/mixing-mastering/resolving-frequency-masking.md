---
id: creative-arts.music.mixing-mastering.resolving-frequency-masking
name: resolving-frequency-masking
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, eq, equalisation, frequency-masking, unmasking, complementary-eq, spectrum-analyser, mud, low-mids, vocal-clarity, eq-carving, masking-detection, sidechain-eq]
level: practitioner
status: draft
description: "Find and fix instruments masking each other: hearing the clash, complementary EQ, carving space for the vocal, analyser masking views and arrangement fixes."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. Equalizing for a Reason", "https://www.izotope.com/en/learn/what-is-frequency-masking.html", "https://www.fabfilter.com/help/pro-q/using/spectrum-analyzer (collision detection)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resolving frequency masking

**Goal:** every important part audible, by stopping parts from covering each other's key
frequencies.

## 1. Hearing masking
- A part sounds fine solo but disappears or turns muddy in the mix.
- Mute/unmute candidates while listening to the masked part: the one that makes it reappear is the masker.
- Common pairs: vocal vs guitars/keys (1-4 kHz), kick vs bass (50-120 Hz), snare vs guitars (200-500 Hz and 2-5 kHz), pads vs everything (low-mids).

## 2. Fixes in order of preference
1. **Arrangement**: change octave, simplify, or mute one part in that section (see frequency-space arrangement skill).
2. **Balance**: is the masked part just too quiet?
3. **Complementary EQ**: identify each part's defining range; cut a few dB from the masker there and, if needed, boost the masked part slightly in the same band. E.g. guitars -2 dB at 3 kHz, vocal +1.5 dB at 3 kHz.
4. **High-pass** non-bass parts to clear the low end; low-mid cuts (200-500 Hz) on pads/guitars for clarity.
5. **Dynamic/sidechain EQ**: dip the masker only when the masked part plays (see dynamic EQ skill).
6. **Panning**: separate competing parts left/right.

## 3. Tools
- Analysers with inter-track display (Pro-Q's collision view, iZotope Neutron's masking meter) show overlapping energy; confirm by ear.
- EQ in context, not solo.

## Gotchas
- Cutting the same band from everything: a hole in the mix.
- Making every part bright: they mask each other in the highs instead.
- Boosting the masked part endlessly instead of cutting the masker.

## Verify
- With the fix, the masked part is clear at a lower fader level than before.
- Low-volume listening: key parts still distinct.
