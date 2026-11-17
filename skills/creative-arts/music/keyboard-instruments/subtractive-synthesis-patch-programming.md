---
id: creative-arts.music.keyboard-instruments.subtractive-synthesis-patch-programming
name: subtractive-synthesis-patch-programming
category: creative-arts
field: music
product: keyboard-instruments
tags: [keyboard-instruments, music-production, synthesizer, sound-design, subtractive-synthesis, synth-programming, oscillator, filter, cutoff, resonance, envelope, adsr, lfo, vca, minimoog, juno, patch-design, init-patch]
level: practitioner
status: draft
description: "Program classic subtractive synth patches from an init patch: oscillators, filter cutoff and resonance, envelopes, LFOs and modulation, with recipes for bass, lead, pad and pluck."
sources: ["Gordon Reid, Synth Secrets (Sound On Sound series) https://www.soundonsound.com/series/synth-secrets", "https://www.moogmusic.com/ (Minimoog Model D manual - signal flow)", "https://www.ableton.com/en/live-manual/12/live-instrument-reference/ (Analog and Drift)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subtractive synthesis patch programming

**Goal:** build any common analogue-style sound from an initialised patch, knowing which
control does what.

## 1. Signal flow
**Oscillators (VCO)** -> **mixer** -> **filter (VCF)** -> **amplifier (VCA)**, with
**envelopes (EG)** and **LFOs** modulating pitch, filter cutoff and amplitude.

- Waveforms: saw (bright, all harmonics: brass, strings, leads), square/pulse (hollow; PWM for movement), triangle/sine (soft, sub), noise (percussion, wind).
- Filter: low-pass 24 dB/oct (Moog-like, fat) or 12 dB/oct (brighter, Oberheim/SEM). **Cutoff** sets brightness; **resonance** emphasises the cutoff, self-oscillates at max.
- **ADSR**: Attack, Decay, Sustain (level), Release. Amp EG shapes loudness; filter EG (with EG amount) shapes brightness over time.

## 2. Always start from INIT
Initialise the patch (one saw, filter open, amp EG A0 D0 S100 R short) and build up; editing a complex preset hides what's doing what.

## 3. Recipes
| Sound | Oscillators | Filter | Envelopes / mod |
|---|---|---|---|
| **Bass** (Moog-style) | 2 saws or saw+square, osc 2 -1 octave, slight detune | LP24, cutoff low, res 20-30% | filter EG fast decay, moderate amount; amp A0 D mid S high R short; mono, legato glide optional |
| **Lead** | saw + saw detuned 5-10 cents | LP, cutoff mid-high | vibrato via LFO (5-6 Hz) on mod wheel; glide 30-80 ms |
| **Pad** | 2 saws detuned, + PWM square | LP12, cutoff mid, low res | amp A 300-800 ms, R 1-2 s; slow LFO on cutoff or PWM; chorus effect |
| **Pluck** | saw or square | LP, cutoff low | filter EG A0 D 150-300 ms S0, amount high; amp D similar, S0 |
| **Brass** | saws | LP | filter EG attack 50-100 ms ("blat"), amp sustain high |

## 4. Performance controls
- Velocity -> filter cutoff/EG amount for expressive brightness.
- Mod wheel -> vibrato depth; aftertouch -> filter or vibrato.
- Key tracking on the filter keeps high notes bright.

## Gotchas
- Too much resonance + low cutoff on a bass loses the fundamental; check in context.
- Detune too wide = out of tune; 3-12 cents is the useful range.
- Big chorus/reverb on mono bass patches smears the low end.

## Verify
- Save each recipe as a user patch, then play it in a mix context; adjust cutoff with the track playing, not solo.
- Recreate a reference sound by ear and A/B at matched level.
