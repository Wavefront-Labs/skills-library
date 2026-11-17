---
id: creative-arts.music.mixing-mastering.multiband-compression
name: multiband-compression
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, compression, dynamics-processing, multiband-compression, crossover-frequencies, frequency-selective-dynamics, ott, mastering-dynamics, low-end-control, de-harsh, band-solo]
level: advanced
status: draft
description: "Use multiband compression in mixing and mastering: crossovers, per-band threshold and timing, low-end and harshness control, and over-processing traps like OTT."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. Frequency-Selective Dynamics", "Bob Katz, Mastering Audio (3rd ed.), multiband compression", "https://www.fabfilter.com/help/pro-mb/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multiband compression

**Goal:** control dynamics in one frequency range without affecting others.

## 1. When to use it
- Low end that swells on certain notes (bass, full mixes).
- Low-mid build-up only in dense sections.
- Harshness/sibilance on a bus or master.
- Sound design: OTT-style upward/downward multiband for extreme density in EDM.
- Prefer dynamic EQ for narrow, single-frequency problems; multiband for broader ranges.

## 2. Setup
1. Use the fewest bands needed (often 1 active band; others bypassed).
2. **Crossovers** at sensible points: e.g. 120 Hz (low), 120 Hz-2 kHz (mid), 2-8 kHz (presence), 8 kHz+ (air). **Solo bands** to hear what each contains.
3. Per band: threshold for 1-3 dB GR (mastering) or more for mix fixes; ratio 2:1-4:1.
4. Timing by frequency: lows need **slower attack and release** (low-frequency cycles are long; fast release causes distortion), highs can be faster.
5. Makeup per band; level-match the whole processor.

## 3. Mastering use
- Gentle: 1-2 dB on the low band to steady the bass; 1 dB on the presence band to tame harsh peaks. Big moves mean the mix needs fixing.
- Linear-phase crossovers avoid phase shifts at crossover points (with added latency/pre-ringing).

## 4. OTT and creative multiband
- Xfer OTT / Ableton Multiband Dynamics "OTT" preset: upward and downward compression on 3 bands; use with low Depth (20-40%) on synths and FX for brightness and density. On whole mixes it usually destroys dynamics.

## Gotchas
- Too many bands working = unnatural tonal shifts as the music changes ("pumping EQ").
- Fast low-band release = distortion of bass waveforms.
- Crossover phase artefacts with minimum-phase multiband on sources with lots of energy at the crossover.

## Verify
- Band GR meters active only where the problem occurs.
- Level-matched A/B over the loudest and quietest sections: tonal balance consistent, no pumping.
