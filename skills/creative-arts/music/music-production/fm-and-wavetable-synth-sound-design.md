---
id: creative-arts.music.music-production.fm-and-wavetable-synth-sound-design
name: fm-and-wavetable-synth-sound-design
category: creative-arts
field: music
product: music-production
tags: [music-production, beatmaking, sound-design, wavetable-synthesis, fm-synthesis, serum, vital, operator, dx7, wavetable-position, modulation-matrix, ratio, modulation-index, reese-bass, supersaw, synth-programming]
level: practitioner
status: draft
description: "Design sounds with wavetable and FM synthesis: position and warp, operator ratios and index, modulation routing, and recipes for bass, bells, plucks and pads."
sources: ["https://xferrecords.com/ (Serum manual)", "https://vital.audio/ (Vital manual)", "https://www.ableton.com/en/live-manual/12/live-instrument-reference/ (Operator and Wavetable)", "John Chowning, The Synthesis of Complex Audio Spectra by Means of Frequency Modulation (JAES, 1973)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FM and wavetable synth sound design

**Goal:** build modern synth sounds deliberately with wavetable and FM engines.

## 1. Wavetable basics
- A wavetable is a series of single-cycle waveforms; **wavetable position** scans through them. Modulating position (with an envelope or LFO) creates evolving timbre.
- **Warp** modes (Serum/Vital: sync, bend, FM from another osc, PWM, mirror) reshape the wave further.
- Unison: 4-8 voices, detune 10-25%, blend for width (supersaw).
- Modulation matrix: drag sources (ENV, LFO, velocity, macro) onto targets; set amount and polarity.

## 2. FM basics
- A **modulator** oscillator varies the frequency of a **carrier**. Two key controls:
  - **Ratio** (modulator : carrier frequency). Integer ratios (1:1, 2:1, 3:1) = harmonic tones; non-integer (1.41, 3.5) = inharmonic, metallic, bell-like.
  - **Index** (modulator level): more = brighter, more sidebands.
- Envelope on the modulator level = brightness that changes over time (like a filter envelope).
- Algorithms (DX7 has 32; Operator has 11) define which operators modulate which.

## 3. Recipes
| Sound | Engine | Recipe |
|---|---|---|
| **Reese bass** | wavetable | 2 saws detuned (or unison 2-4), low-pass, slow LFO on detune or filter; distortion |
| **Supersaw lead** | wavetable | saw table, 7 unison voices, detune ~20%, chorus, reverb |
| **FM bell / EP** | FM | carrier + modulator ratio 1:3.5 (bell) or 1:1 with short mod envelope (EP); mod level decays fast |
| **FM bass** | FM | ratio 1:1 or 2:1, index moderate, short mod decay for a "pluck" growl |
| **Growl / wobble** | wavetable | LFO (synced 1/4-1/16) on wavetable position + filter; macro for intensity; OTT/multiband compression |
| **Evolving pad** | wavetable | slow LFO on position, long attack/release, unison, reverb |

## 4. Workflow
- Start from INIT; one oscillator, then add.
- Assign 4-8 **macros** to the most musical controls for automation in the arrangement.
- Resample (bounce to audio) and process further for unique textures.

## Gotchas
- Wide unison and stereo detune on bass = phasey low end; keep the sub mono (separate sub oscillator, unison off).
- High FM index aliases at high notes; use keytracking on the index or oversampling.

## Verify
- Play across the keyboard: the sound stays usable in its intended range.
- Check mono compatibility and CPU load before committing.
