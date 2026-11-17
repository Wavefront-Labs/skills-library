---
id: engineering-technology.automotive-vehicle-engineering.nvh.psychoacoustic-metrics
name: psychoacoustic-metrics
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [psychoacoustics, loudness, sharpness, roughness, fluctuation-strength, tonality, sound-quality-metrics]
level: practitioner
status: gated
description: "Apply psychoacoustic metrics (loudness, sharpness, roughness, fluctuation strength, tonality) to vehicle noise, with standards references and limits of the metrics."
sources:
  - "Zwicker and Fastl, Psychoacoustics: Facts and Models"
  - "https://ecma-international.org/publications-and-standards/standards/ecma-418/"
  - "ISO 532-1 (Zwicker loudness) and ISO 532-2 (Moore-Glasberg); confirm editions on iso.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Loudness and psychoacoustic metrics

1. A-weighted SPL (dB(A)) approximates human sensitivity for moderate levels; does not capture tonal or time-varying features.
2. **Loudness** in sone (Zwicker method standardised in ISO 532-1; Moore-Glasberg method in ISO 532-2; both designations (gated: unconfirmed, source is paywalled or blocked), iso.org returned 403): accounts for critical-band masking; 1 sone = 40 phon and loudness doubles per +10 phon above that (N = 2^((P-40)/10), computed).
3. **Sharpness** (acum): high-frequency emphasis; high sharpness sounds harsh.
4. **Roughness** (asper): peaks near 70 Hz for steady sounds; ECMA-418-2 covers about 20-300 Hz; **fluctuation strength** (vacil): slow modulation (ECMA-418-2 covers about 0.25-20 Hz; peak near 4 Hz (gated: unconfirmed, source is paywalled or blocked)); relevant for beating engine orders and motor whine.
5. **Tonality:** prominence of tones; ECMA-418-2 (Sottek Hearing Model; 4th edition, June 2025, per ecma-international.org) and the older DIN 45681 (gated: unconfirmed, source is paywalled or blocked); important for EV motor and gear tones.
6. Workflow: record binaural, compute metrics in a tool, compare with jury ratings (see sound-quality jury testing) to see which metrics predict preference.
7. Limits: metrics are developed for steady sounds; interpret time-varying signals with specific loudness over time; ensure calibrated recordings.
8. Report with the exact method and standard edition.

**Gotchas:** using uncalibrated recordings; applying stationary methods to short transients.

## Verify
- [ ] Reference signal (calibrated tone or noise) produces the expected loudness value.
- [ ] Metric version and parameters stated in the report.
