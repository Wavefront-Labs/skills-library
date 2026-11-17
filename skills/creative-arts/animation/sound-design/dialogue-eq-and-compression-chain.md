---
id: creative-arts.animation.sound-design.dialogue-eq-and-compression-chain
name: dialogue-eq-and-compression-chain
category: creative-arts
field: animation
product: sound-design
tags: [dialogue-eq, dialogue-compression, dialogue-mix, de-esser, high-pass, voice-processing]
level: advanced
status: draft
description: "Build a dialogue processing chain for animation mixes: clean-up EQ, subtractive then tonal EQ, compression stages, de-essing and a signal-flow order that holds up."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Dialogue EQ and compression chain

A dialogue chain makes recorded voices sit consistently in the mix. Set it up per character on a dialogue bus or track, after dialogue editing and clean-up (`dialogue-declick.md`, `dialogue-denoise.md`) and before the final mix level (`dialogue-mix-master.md`).

## Signal-flow order (a common starting point)
1. **Clip gain / levelling**: even out whole-line differences first (see `clip-gain-levelling.md`) so the compressor is not doing the work.
2. **High-pass filter**: typically 60-100 Hz, 12 dB/oct or more; removes rumble and mic-stand thumps. Raise the cutoff for thin character voices, lower for deep ones.
3. **Subtractive EQ**: narrow cuts for problems: boxy 200-400 Hz build-up, nasal 800 Hz-1 kHz, harsh 2-4 kHz. Sweep a narrow boost, find the offending resonance, then cut.
4. **De-esser**: reduce sibilance in the 5-9 kHz region. Cut sparingly. Over-de-essing makes lisping.
5. **Compression**: transparent dynamic control. Typical starting point: ratio 2:1 to 4:1, attack 5-30 ms (slow enough to let consonants through), release 50-150 ms, 3-6 dB of gain reduction on peaks.
6. **Tonal EQ**: gentle boosts for presence (2-5 kHz) and air (above 10 kHz) and low-body warmth (100-200 Hz). Do this after the compressor so the boost does not drive it.
7. **Optional second compressor or limiter** to catch peaks, only if the mix needs it.

## Ranges are starting points
Voices differ. Every number above is a starting point, adjusted by ear and by loudness consequences. Do not copy a chain between characters without listening.

## Animation-specific notes
- Stylised voices (small creatures, robots, shouty characters) may require a more aggressive chain or creative processing; keep the processed and dry versions available.
- Always A/B the chain bypassed at the same loudness. It is easy to prefer the louder version.
- Keep the chain identical for a character across episodes. Save presets by character.

## Gotchas
- Compression before clean-up amplifies noise.
- Using the compressor's make-up gain without level matching biases the A/B.
- Dialogue that was heavily noise-reduced may exhibit new artefacts when boosted at high frequencies.

## Verify
- [ ] Chain bypass/engage A/B at matched loudness shows a real improvement.
- [ ] 3-6 dB gain reduction at peaks; no pumping on sustained vowels.
- [ ] Sibilance is controlled without lisping on solo playback.
