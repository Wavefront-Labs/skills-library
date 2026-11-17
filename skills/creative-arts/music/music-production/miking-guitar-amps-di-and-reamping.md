---
id: creative-arts.music.music-production.miking-guitar-amps-di-and-reamping
name: miking-guitar-amps-di-and-reamping
category: creative-arts
field: music
product: music-production
tags: [music-production, recording, microphone-technique, amp-miking, reamping, di-box, guitar-recording, bass-recording, sm57, ribbon-mic, cone-position, reamp-box, impulse-response, phase-alignment]
level: practitioner
status: draft
description: "Record electric guitar and bass: mic placement on the speaker cone, combining a dynamic and a ribbon, capturing a clean DI, reamping later and phase-aligning multiple sources."
sources: ["https://www.soundonsound.com/techniques/recording-electric-guitar", "https://www.radialeng.com/ (Radial reamping and DI guides)", "https://www.shure.com/en-US/insights/how-to-mic-a-guitar-amp", "Bobby Owsinski, The Recording Engineer's Handbook (Hal Leonard)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Miking guitar amps, DI and reamping

**Goal:** great amp tone on tape, plus a clean DI so the tone can be changed later.

## 1. Mic placement on the speaker
- Start with an **SM57** almost touching the grille (1-3 cm).
- **On-axis at the dust cap** = brightest, most aggressive. **Moving toward the cone edge** = darker, warmer. **Angling off-axis** = softer highs.
- Find the best speaker in a multi-speaker cab first (listen to each at low volume).
- Classic blend: SM57 + **ribbon** (Royer R-121) side by side at equal distance; ribbon adds body and smooth top.
- Room mic 1-2 m away for size (rock).

## 2. Phase
- Two mics at different distances = comb filtering. Align capsules at the same distance from the grille, or nudge the tracks in the DAW (zoom in on transients), or use an alignment plugin.
- Check by summing to mono and flipping polarity on one mic: choose the fuller result.

## 3. DI capture
- Always split the guitar to a **DI box** before the amp (or use the interface Hi-Z input via a splitter/through output). The DI track is insurance and enables reamping or amp sims.
- Bass: record DI **and** amp mic (or DI + amp sim). Blend DI for low-end clarity, amp for grit; align them.

## 4. Reamping
- Send the DI track from an interface line output into a **reamp box** (Radial ProRMP / X-Amp), which converts line level and impedance back to guitar level, then into pedals/amp, then mic as usual.
- Match level so the amp sees the same input as the original guitar (compare against the guitar played live).
- Account for latency: align the reamped track to the DI.

## 5. Gain and tone tips
- Less amp gain than you think: high-gain tones sound smaller recorded; double-track rhythm parts instead (hard pan L/R, separate takes).
- Cab on a stand or tilted to reduce floor coupling (less boom).

## Gotchas
- Amp hum or ground loops through the DI split: use ground lift on the DI.
- Cranking the amp in a small room overloads mic and ears; use attenuators or isolation cabs.
- Single-take "doubled" with a delay is not a double; play it twice.

## Verify
- Solo each mic, then blend: the combination should sound better than either alone with no hollow phase.
- DI track clean, no clipping, recorded at the same time as the amp.
