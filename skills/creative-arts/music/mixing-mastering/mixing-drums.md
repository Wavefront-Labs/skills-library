---
id: creative-arts.music.mixing-mastering.mixing-drums
name: mixing-drums
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, mixdown, drum-mixing, overheads, kick-eq, snare-eq, drum-bus, parallel-drum-compression, gating-toms, drum-samples, sample-replacement, phase-alignment, room-mics]
level: practitioner
status: draft
description: "Mix multitrack drums: phase alignment, overheads-first balance, kick and snare EQ and compression, toms and rooms, drum bus, parallel compression and samples."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), chapters on balance, compression and EQ for drums", "https://www.slatedigital.com/ (Trigger sample replacement manual)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mixing drums

**Goal:** a punchy, coherent drum sound that supports the song.

## 1. Phase and polarity first
- Check snare top vs bottom (bottom inverted), kick in vs out, close mics vs overheads (flip polarity or nudge to align; choose the fullest).
- Alignment plugins (Sound Radix Auto-Align) or manual time nudging of close mics to overheads; nudge cautiously - overheads define the image.

## 2. Build the balance
1. **Overheads** first: they are the kit's picture. High-pass gently (~100-200 Hz depending on how much kick/snare body you want from them).
2. Add **kick** and **snare** close mics to give weight and punch.
3. **Toms**: strip silence or gate/expand them (or edit out the non-hit parts) to reduce bleed; level for fills.
4. **Room** mics: compressed for excitement and size.

## 3. EQ starting points
| Drum | Cut | Boost |
|---|---|---|
| Kick | 300-500 Hz boxiness | 50-80 Hz weight; 2-5 kHz beater click |
| Snare | 400-800 Hz ring/box (narrow) | 150-250 Hz body; 5-8 kHz crack |
| Toms | 300-600 Hz box | 80-150 Hz body; 3-5 kHz attack |
| Overheads | low-mids if muddy | 8-12 kHz air (careful with harsh cymbals) |

## 4. Compression
- Kick and snare: medium-slow attack (10-30 ms) to keep the transient, release with the groove, 3-6 dB GR.
- **Drum bus**: gentle glue (2:1-4:1, 1-3 dB).
- **Parallel (New York) compression**: send the drums to a bus, compress hard (10+ dB GR, fast attack), blend under the dry kit for density.

## 5. Samples
- Reinforce weak kick/snare with samples (Trigger, Drumagog, or MIDI from audio); blend with the original, align phase, use velocity-sensitive multi-sampled hits so dynamics remain.

## Gotchas
- Soloing drums and making them huge: in context they may swamp the mix.
- Over-gating toms cuts off resonance; use expansion or manual editing.
- Cymbals harsh after compression; use de-essing or dynamic EQ on overheads around 3-6 kHz.

## Verify
- Mono check: no loss of snare body or kick punch.
- Kit sounds coherent (one kit in one room) not a collection of close mics.
