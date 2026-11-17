---
id: creative-arts.theatre.theatre-sound-design.speaker-placement-and-system-tuning
name: speaker-placement-and-system-tuning
category: creative-arts
field: theatre
product: theatre-sound-design
tags: [theatre, theatre-sound-design, reinforcement-design, pa-design, delay-speakers, speaker-placement, system-tuning, smaart, time-alignment, eq, haas-effect, foldback, front-fills]
level: practitioner
status: draft
description: "Design and tune a theatre reinforcement system: main, fill and delay speaker placement, time alignment to the stage image, measurement with Smaart, and foldback."
sources:
  - "https://www.rationalacoustics.com/pages/smaart-v9"
  - "https://meyersound.com/"
  - "https://www.dbaudio.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Speaker placement and system tuning

## Design goals
Even coverage of every seat, intelligibility, and **localisation** — the audience
should hear the sound coming from the actor, not the speaker.

## Placement
1. **Mains**: proscenium-mounted left/right and/or centre cluster/arrays covering
   the bulk of seats; aim using prediction software (Meyer MAPP 3D, d&b
   ArrayCalc, L-Acoustics Soundvision).
2. **Front fills**: small speakers along the stage lip for the first rows
   (often below the mains' coverage) — help localise to the stage.
3. **Under-balcony and over-balcony delays**: for seats shadowed by balconies;
   fed with delayed signal.
4. **Surround/effects speakers** for immersive effects positioned by design.
5. **Subwoofers** placement (ground-stacked, flown, cardioid arrays) for low-end.
Record everything on a **speaker plot** and block diagram.

## Time alignment
- Delay each fill/delay speaker so its sound arrives **slightly after** (roughly
  5-15 ms) the reference (the actor's acoustic voice or the main system) —
  the precedence (Haas) effect makes the ear localise to the first arrival.
- Measure distances/arrival times; set delay in the DSP/console.

## Tuning with measurement (e.g. Smaart)
1. Calibrated measurement mic at representative seats.
2. Dual-channel **transfer function** (reference = signal sent; measurement =
   mic) shows magnitude, phase and coherence.
3. Align each element (delay finder), then EQ to correct broad tonal problems —
   cut more than boost; use high-coherence data only.
4. Check summing between mains and fills at crossover zones.
5. Final listen with known material and voice.

## Foldback (monitors)
Actors need to hear the band/tracks and sometimes themselves: wedges, side-fills,
in-ear monitors (rare in plays, common in musicals for some performers); keep
foldback low to avoid feedback with radio mics.

## Gotchas
- Delays set by tape measure only — verify by measurement.
- Over-EQing at one seat.
- Speakers visible in sightlines without design agreement.

## Verify
- [ ] Prediction shows coverage at all seats.
- [ ] Delays and EQ set from measurement and listening.
- [ ] Speaker plot and block diagram current.
