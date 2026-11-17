---
id: creative-arts.animation.sound-design.mic-phase-alignment
name: mic-phase-alignment
category: creative-arts
field: animation
product: sound-design
tags: [phase-alignment, polarity, comb-filtering, multi-mic, dialogue-editing, ensemble-record, auto-align, vo-recording]
level: advanced
status: draft
description: "Fix phase and polarity problems when a VO or ensemble record has several mics: detect comb filtering, flip polarity, time-align tracks and choose one mic."
sources:
  - https://docs.izotope.com/rx/en/
  - https://www.soundradix.com/products/auto-align-2/
  - https://www.routledge.com/Dialogue-Editing-for-Motion-Pictures-A-Guide-to-the-Invisible-Art/Purcell/p/book/9781138289796
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Phase and polarity between mics

**Goal:** when two microphones capture the same voice (an ensemble record, a close mic plus a room mic, a lav plus
a boom on a reference shoot), combining them does not thin or hollow the sound.

## The problem

The same sound reaches mics at different times. Summed, some frequencies cancel (comb filtering): the voice sounds
phasey, thin, "in a tube". A 1 ms delay (about 34 cm path difference) puts the first cancellation at 500 Hz.

## Detect

- Sum the two tracks to mono and solo; then flip one track's polarity. If the sum gets fuller with the flip, a
  polarity inversion exists (wiring or a mic pointed the other way).
- Zoom in on a sharp transient (a "t" or a clap at the top of the session): offset between waveforms = time
  difference.
- A phase correlation meter near 0 or negative on a mono source means trouble.

## Fix

1. **Polarity:** flip with the channel's polarity (often labelled Ø) button or a trim plug-in.
2. **Time:** slide the farther mic earlier by the measured offset (sample-accurate nudge), or use Sound Radix Auto-Align
   or RX *Dialogue Contour/Ambience Match* type tools for alignment.
3. **Choose:** for animation dialogue, the usual answer is to use **only the close mic** per actor; room mics are for
   ensemble feel and are often discarded in the edit.

## Ensemble records in animation

Recording actors together gives better performances but each mic picks up the other actors (bleed). Isolate with
booth gobos, use cardioid/hypercardioid mics pointed away from others, and cut each actor's own mic in the edit,
muting it when they are not speaking (see `creative-arts.animation.voice-tts.vo-recording-session`).

## Verify

Mono sum of the aligned mics is as full or fuller than the close mic alone (no hollow mid-range), and the
correlation meter stays positive during speech.
