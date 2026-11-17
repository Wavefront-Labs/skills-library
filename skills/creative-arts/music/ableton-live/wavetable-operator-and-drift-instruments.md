---
id: creative-arts.music.ableton-live.wavetable-operator-and-drift-instruments
name: wavetable-operator-and-drift-instruments
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, instrument-rack, ableton-wavetable, operator-synth, drift, meld, wavetable-position, fm-algorithms, mod-matrix, live-instruments, sound-design, synthesizer]
level: practitioner
status: draft
description: "Program Live's synths: Wavetable (position, mod matrix), Operator (FM algorithms, ratios) and Drift (fast analogue-style patches), with starting recipes."
sources: ["https://www.ableton.com/en/live-manual/12/live-instrument-reference/ (Wavetable, Operator, Drift, Meld)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wavetable, Operator and Drift (Live instruments)

**Goal:** know which Live synth to reach for and how to get a sound out of each fast.

## 1. Wavetable
- Two wavetable oscillators + sub; choose a table category and table; **Position** scans through the wavetable. Effect modes per oscillator (FM, Classic: PW/Sync, Modern: warp/fold).
- Two filters (serial/parallel/split), three envelopes, two LFOs, MIDI mod sources (velocity, note, pitch bend, pressure, slide).
- **Mod Matrix** tab: route sources to destinations with amounts (e.g. Env 2 -> Osc 1 Position).
- Unison modes (Classic, Shimmer, Noise, Phase Sync, Position Spread, Random Note) with voices and amount.
- Recipe, evolving pad: Osc 1 position modulated by LFO 1 (slow), unison Position Spread, amp attack ~400 ms, release ~2 s.

## 2. Operator
- Four oscillators (A-D) and **11 algorithms** (shown as icons): which oscillators are carriers (heard) and which modulate others.
- Each oscillator: waveform, **Coarse/Fine ratio**, level, its own envelope. Modulator level = FM index (brightness).
- Recipes: FM bell - algorithm with B modulating A, B coarse 3.5 (or Fine detune), B envelope fast decay; FM bass - B modulating A at ratio 1 or 2, short decay on B; electric piano - ratio 1:14 for tine attack with fast decay.
- Also usable for simple subtractive sounds (one saw oscillator + filter) and sub basses (sine).

## 3. Drift (Live 11.3+)
- Lightweight analogue-style synth: two oscillators with shape control, filter (types I and II), envelopes, LFO, cycling envelope, and a compact mod matrix; low CPU.
- Recipe, classic bass: Osc 1 saw + Osc 2 square -1 octave, filter low cutoff with envelope, mono with glide.
- Great for quick patches and MPE (per-note Slide/Pressure).

## 4. Meld (Live 12)
- Bi-timbral MPE-capable synth with two engines (many oscillator types) and scale awareness; use for complex textures.

## Gotchas
- Unison on bass patches widens the low end; keep subs mono.
- Operator's algorithm choice matters more than any knob; check which oscillators are audible before tweaking.

## Verify
- Save presets (User Library) and test across the keyboard range and velocities.
- CPU check with many voices (Wavetable/Meld are heavier than Drift).
