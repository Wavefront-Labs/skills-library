---
id: creative-arts.music.mixing-mastering.stereo-widening-and-mid-side-processing
name: stereo-widening-and-mid-side-processing
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, reverb, delay, stereo-widening, mid-side-processing, stereo-image, haas-effect, double-tracking, mono-compatibility, correlation-meter, side-eq, width, imager]
level: practitioner
status: draft
description: "Widen a mix safely: double-tracking and panning, Haas delays, mid/side EQ and compression, imagers and the correlation-meter and mono checks that prevent phase problems."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. Stereo Enhancements", "Bob Katz, Mastering Audio (3rd ed.), mid-side processing", "https://www.soundonsound.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stereo widening and mid/side processing

**Goal:** a wide, immersive mix that still works in mono.

## 1. Width from the source (best)
- **Double-track** guitars, BVs, synth parts (separate performances) and pan hard L/R.
- Stereo-mic'd sources and stereo instruments (pianos, pads) panned appropriately.
- Arrange different parts left and right (complementary rhythms).

## 2. Processing techniques
| Technique | How | Risk |
|---|---|---|
| **Haas effect** | duplicate a mono part, delay one side 10-30 ms, pan L/R | collapses/combs in mono |
| Pitch/chorus doubler | detune copies +/- 5-10 cents, short delay, pan | chorusy, phasey in mono |
| **Mid/side EQ** | boost highs on the side signal, keep lows mono | over-wide hiss |
| Side level / imager | raise the side relative to mid | thin centre, phase issues |
| Stereo reverb/delay returns | width from effects | usually safe |

## 3. Mid/side basics
- **Mid** = L+R (centre content: vocal, kick, bass, snare). **Side** = L-R (stereo differences: wide guitars, reverbs).
- Common moves: high-pass the side below ~100-150 Hz (mono low end), gentle high-shelf boost on side for air, slight mid boost at 2-4 kHz for vocal focus.
- In mastering, M/S compression controls the centre independently.

## 4. Monitoring width
- **Correlation meter**: +1 = mono; 0 = wide; negative = out of phase (cancels in mono). Keep it mostly positive.
- Mono button on the master: vocals and bass must stay solid; widened parts may drop but shouldn't vanish.
- Goniometer/vectorscope shows image shape.

## Gotchas
- Widening the whole mix with an imager: weak centre and mono problems on phones/club systems.
- Stereo low end: keep bass and kick mono.
- Haas on lead vocals: shifts perceived position and combs in mono.

## Verify
- Mono sum: no element disappears entirely; correlation stays above 0 in loud sections.
- Width difference noticeable on headphones and speakers without a hollow centre.
