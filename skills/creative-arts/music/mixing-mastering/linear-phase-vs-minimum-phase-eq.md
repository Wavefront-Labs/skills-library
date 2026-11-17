---
id: creative-arts.music.mixing-mastering.linear-phase-vs-minimum-phase-eq
name: linear-phase-vs-minimum-phase-eq
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, eq, equalisation, linear-phase-eq, minimum-phase-eq, natural-phase, pre-ringing, latency, phase-shift, parallel-processing, mastering-eq, multi-mic-sources]
level: advanced
status: draft
description: "Choose between minimum-phase, linear-phase and natural-phase EQ modes: what phase shift and pre-ringing do, where each is safe (multi-mic, parallel, mastering), and latency costs."
sources: ["Bob Katz, Mastering Audio (3rd ed.), ch. on equalisation and filter types", "https://www.fabfilter.com/help/pro-q", "https://www.soundonsound.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linear-phase vs minimum-phase EQ

**Goal:** pick the EQ processing mode that avoids side effects for the job at hand.

## 1. What differs
| Mode | Phase behaviour | Side effects | Latency |
|---|---|---|---|
| **Minimum phase** (normal analogue-style EQ) | phase shift around each band, more for steep/narrow filters | slight smearing near the boosted/cut band; sounds natural, transient-friendly | ~0 |
| **Linear phase** | no phase shift between frequencies (all delayed equally) | **pre-ringing** (energy before transients) with steep low-frequency filters; can sound "soft" | high (tens to thousands of samples) |
| Natural phase (FabFilter) | approximates analogue phase response | compromise | moderate |

## 2. When phase matters
- **Multi-miked or parallel sources** (kick in/out, snare top/bottom, DI + amp, parallel compression): EQ on one path shifts its phase relative to the other and can cause comb filtering. Linear phase keeps them aligned (or EQ them together on a bus).
- **Mastering / stem EQ** with steep low cuts or large broad moves: linear phase keeps the stereo image and transients intact for mid/side moves... but watch pre-ringing on low-end boosts.
- **Mid/side EQ**: linear phase avoids phase differences between mid and side that alter the image.

## 3. When minimum phase is better
- Most single-track mix EQ: lower latency, no pre-ringing, sounds "musical".
- Low-frequency boosts on drums: pre-ringing in linear phase blurs the attack.
- Tracking/live use (latency).

## 4. Practical tips
- Linear-phase EQ adds big latency; the DAW compensates, but avoid it on record-enabled or live-monitored tracks.
- Use higher-quality/lower-resolution settings deliberately (FabFilter "low/medium/high/very high/maximum" latency vs low-frequency accuracy).

## Gotchas
- Assuming linear phase is always "better": it trades phase shift for pre-ringing.
- Comparing at different levels; match loudness before judging.

## Verify
- On a kick or snare, compare modes with a 6 dB low boost: listen for softened or smeared attack (pre-ringing).
- On parallel paths, sum both with the EQ in each mode: linear phase should not change the summed tone except as EQ'd.
