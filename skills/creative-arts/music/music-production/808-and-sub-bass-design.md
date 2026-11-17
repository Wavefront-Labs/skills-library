---
id: creative-arts.music.music-production.808-and-sub-bass-design
name: 808-and-sub-bass-design
category: creative-arts
field: music
product: music-production
tags: [music-production, beatmaking, sound-design, 808, sub-bass, tr-808, glide, portamento, saturation, kick-and-808, sidechain, mono-bass, trap, drill, low-end, tuning-the-808]
level: practitioner
status: draft
description: "Design and mix 808s and sub-bass: tuning to the key, glides, saturation for small speakers, managing kick and 808 overlap, and keeping the low end mono and controlled."
sources: ["https://www.ableton.com/en/live-manual/12/live-instrument-reference/ (Simpler/Operator for sub bass)", "Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), low-end chapters"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 808 and sub-bass design

**Goal:** a powerful low end that is in tune, audible on phones, and doesn't fight the kick.

## 1. Source
- **808**: a long-decay sine-ish kick sample (TR-808 bass drum with long decay) played melodically in a sampler, or a synthesised sine with pitch envelope.
- **Sub-bass**: pure sine or triangle from a synth (Operator, Serum), usually sustained notes under a separate kick.

## 2. Tuning
- Find the 808 sample's root note (tuner plugin on a long note) and set the sampler's root key accordingly. Play bass lines in the song's key; most hits land on roots.
- Keep most notes between about **E1 and G1-ish (40-50 Hz)** fundamentals for trap/drill; very low notes (<35 Hz) disappear on most systems.

## 3. Glides and envelopes
- **Mono mode with legato glide** (portamento ~50-150 ms) for slides between notes; overlap MIDI notes to trigger the glide.
- Amp envelope: attack 0, decay/sustain to taste, release short so notes don't smear; choke group with the kick if they overlap badly.

## 4. Saturation for translation
- Phones and laptops can't reproduce 40 Hz: add **saturation/distortion** (soft clip, tape, Decapitator, Saturator) to create harmonics at 80-200 Hz+ so the bass line is heard. Blend in parallel to keep the clean sub.
- Check on small speakers frequently.

## 5. Kick vs 808
- Decide who owns the sub: often **808 owns the sub**, kick provides the click/punch (high-pass the kick or choose a short kick).
- Avoid kick and 808 hitting together with clashing pitch: tune the kick to the key or to the 808 note, or offset slightly.
- **Sidechain** the 808 to the kick (fast duck, 2-4 dB) or use volume shaping, so the transient comes through.
- Keep everything below ~120 Hz **mono** (utility/bass mono tool).

## Gotchas
- 808 notes in a different octave each bar wreck the energy; keep the range tight.
- Long-decay 808 under fast notes = mud; shorten decay for busy lines.
- Over-saturating destroys the sub; meter the low end with a spectrum analyser.

## Verify
- Spectrum: one clear fundamental per note, no buildup between kick and 808.
- Phone speaker check: the bass line is still recognisable.
- Mono check: low end stays full.
