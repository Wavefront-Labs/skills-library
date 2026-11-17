---
id: creative-arts.music.mixing-mastering.parallel-compression
name: parallel-compression
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, compression, dynamics-processing, parallel-compression, new-york-compression, upward-compression, drum-bus, vocal-parallel, dry-wet-mix, latency-compensation, density]
level: practitioner
status: draft
description: "Set up parallel (New York) compression on drums, vocals, bass or the mix: send/return or dry-wet methods, heavy compressor settings, EQ on the parallel path and blend levels."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. on parallel compression", "Bob Katz, Mastering Audio (3rd ed.), parallel/upward compression", "https://www.soundonsound.com/techniques/parallel-compression"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parallel compression

**Goal:** add density and sustain while keeping natural transients.

## 1. Why it works
Blending a heavily compressed copy with the dry signal raises the quiet details (decays,
ghost notes, room) while the dry transients stay intact: effectively **upward compression**.

## 2. Two ways to set it up
1. **Send/return (bus)**: send drums (or any group) to an aux with a compressor 100% wet; blend the aux fader under the dry. Keeps one compressor for many sources and allows EQ on the parallel path.
2. **Dry/wet knob** on the compressor (Mix control): quick and phase-safe within one plugin.
- Either way, the DAW's delay compensation must be on (plugins on the parallel path add latency; misalignment = phasey).

## 3. Settings for the parallel compressor
- Ratio high (8:1 to 20:1 or limiting), **fast attack** (to flatten transients on the parallel path), release fast-medium (timed to groove), **10-20 dB gain reduction**.
- Characterful compressors work well (1176 all-buttons, Distressor, SSL channel comp).
- EQ the parallel return: often boost lows and highs ("smile") or high-pass to avoid low-end build-up.

## 4. Blending
- Start with the parallel fader down, bring it up until the sound thickens; then back off a few dB. Typical: 6-12 dB below the dry level.
- Mute/unmute to check it's adding density, not just level.

## 5. Common uses
- Drums (the classic), lead vocals (body and presence without squashing), bass (consistent level), whole mix (subtle density in mastering or on the mix bus).

## Gotchas
- Phase misalignment if a plugin's latency isn't compensated (side-chained or external processing).
- Too much: ambient noise and room tone come up; cymbals become harsh.

## Verify
- Level-matched comparison: with parallel, the quiet details are more audible and transients unchanged.
- Polarity flip test on the parallel path: if summing gets thinner with polarity flipped, alignment is good.
