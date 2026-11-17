---
id: creative-arts.music.mixing-mastering.mix-balance-eq-compression-and-loudness-delivery
name: mix-balance-eq-compression-and-loudness-delivery
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, mixing, mastering, mix-engineer, static-mix, gain-staging, eq, equalisation, high-pass-filter, subtractive-eq, compression, ratio, attack, release, threshold, bus-compression, reverb, delay, panning, stereo-image, mono-compatibility, lufs, true-peak, loudness-normalisation, limiter, reference-track, dither, spotify, apple-music]
level: practitioner
status: draft
description: "A practical mix-to-master workflow: static balance, subtractive EQ, compression settings by purpose, space with reverb/delay, mono checks, and mastering to LUFS and true-peak targets for streaming."
sources: ["Mike Senior, Mixing Secrets for the Small Studio", "Bob Katz, Mastering Audio", "AES TD1004 streaming loudness recommendation", "Platform loudness targets change; check current specs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mix balance, EQ, compression and loudness delivery

**Goal:** turn multitracks into a balanced, translating stereo mix, then a master that
sounds right on streaming platforms without being crushed.

## 1. Set up
- Import consolidated stems; **gain-stage** each so peaks sit around −10 to −6 dBFS
  pre-fader. Plugins modelled on analog behave best near nominal level.
- Load 2–3 **reference tracks** on a separate bus, level-matched (by ear or LUFS) to
  your mix. Comparing at different loudness lies to you — louder sounds better.
- Monitor at a moderate, consistent level (many engineers aim around 75–85 dB SPL in
  a small room; quieter checks are useful too).

## 2. Static mix first (faders and pan only)
- Start with the most important element (usually vocal or kick+bass), then add parts
  in order of importance. Get 80% of the mix from faders before any plugin.
- **Pan** for space: kick, snare, bass, lead vocal centre; doubles, guitars and keys
  spread. Use LCR panning as a starting point.

## 3. EQ
- **High-pass** everything that doesn't need lows (vocals ~80–120 Hz, guitars,
  keys) — clears mud. Don't over-do it on full-range instruments; listen in context.
- **Subtractive first:** cut problem resonances with narrow bands (sweep a boosted
  band to find the ugly frequency, then cut it) rather than boosting everything else.
- Common zones: 200–500 Hz mud/boxiness; 2–5 kHz presence and harshness; 5–9 kHz
  sibilance; 10 kHz+ air.
- EQ **in the mix, not solo** — a sound that's thin solo may sit perfectly in context.

## 4. Compression by purpose
| Purpose | Ratio | Attack | Release | Gain reduction |
|---|---|---|---|---|
| Vocal levelling | 3:1–4:1 | medium (5–15 ms) | auto/medium | 3–6 dB |
| Drum punch | 4:1 | slow (20–30 ms) lets transient through | fast, to the groove | 3–6 dB |
| Bass consistency | 4:1 | medium | medium | 3–6 dB |
| Mix bus glue | 2:1 | slow (10–30 ms) | auto | 1–2 dB |
Starting points, not rules. Always **level-match** bypass comparisons.

## 5. Space and depth
- Use **send** reverbs/delays (2–3 shared spaces) rather than one per track.
- Short room for cohesion, plate for vocals, longer hall or delay for depth.
- High-pass and low-pass reverb returns to keep them out of the vocal's way.
- Front = drier, brighter, louder; back = wetter, darker, quieter.

## 6. Checks
- **Mono check:** collapse to mono; elements that vanish have phase problems.
- Small speaker / earbuds / car.
- Take breaks; ears fatigue in about 45–60 minutes of focused listening.

## 7. Mastering and delivery
- Separate session; light EQ, gentle compression, then a **limiter** with true-peak
  ceiling around **−1.0 dBTP** (more headroom, e.g. −2 dBTP, for very loud masters to
  survive lossy encoding).
- Streaming services normalise loudness; many target about **−14 LUFS integrated**
  (some use −16 or offer different modes). Mastering much louder buys nothing on those
  platforms and costs dynamics. Check each platform's current spec.
- Deliver WAV at the session sample rate (24-bit), plus 16-bit/44.1 kHz with **dither**
  when required; name files with title, version, date.

## Gotchas
- Soloing and tweaking for hours — check every change in full mix.
- Bus compression added at the end changes the balance; add it early and mix into it.
- Uncertain: platform loudness targets change over time; verify before delivery.

## Verify
- [ ] Level-matched against references at the same LUFS.
- [ ] Mix survives mono, earbuds and a car.
- [ ] Master integrated LUFS and true peak measured and logged.
- [ ] No clipping or inter-sample overs (true-peak meter).
- [ ] Delivery files correctly named, formatted and dithered where needed.
