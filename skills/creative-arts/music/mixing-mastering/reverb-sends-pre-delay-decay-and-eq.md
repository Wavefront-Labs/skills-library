---
id: creative-arts.music.mixing-mastering.reverb-sends-pre-delay-decay-and-eq
name: reverb-sends-pre-delay-decay-and-eq
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, reverb, delay, reverb-send, pre-delay, decay-time, plate-reverb, hall-reverb, room-reverb, reverb-eq, early-reflections, tempo-synced-pre-delay, ducked-reverb, depth]
level: practitioner
status: draft
description: "Set up reverb sends for depth: room, plate and hall roles, pre-delay and decay tied to tempo, EQ on the return, ducking, and several reverbs without mud."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. Mixing with Reverb", "https://www.valhalladsp.com/ (Valhalla reverb manuals)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reverb sends: pre-delay, decay and EQ

**Goal:** depth and space that make the mix three-dimensional but not washy.

## 1. Use sends, 100% wet
- Put reverbs on aux returns (100% wet) and send to them. Several sources share a space (cohesion) and you can EQ/compress the reverb itself.

## 2. A standard set of reverbs
| Return | Type | Decay | Use |
|---|---|---|---|
| Short room/ambience | room, early reflections | 0.3-0.8 s | glue, natural space for drums/guitars without obvious tail |
| Plate | plate | 1.2-2 s | vocals, snare: bright, dense |
| Hall/long | hall/chamber | 2-3.5 s | ballads, pads, special moments |
- Mixing Secrets suggests distinguishing "blend" reverbs (subtle, short) from "size/sustain" reverbs (audible tails).

## 3. Pre-delay
- Delay before the reverb starts; keeps the dry signal clear (the ear hears the source first).
- 20-80 ms typical on vocals; tempo-related (e.g. a 1/64 or 1/32 note) helps it groove. Longer pre-delay = closer-sounding source in a bigger room.

## 4. Decay time to tempo
- Let tails end before the next important beat or phrase. Rough tempo link: quarter note = 60000 / bpm ms; decays of 1-2 bars for long reverbs on slow songs; shorter for fast songs.

## 5. EQ the return
- **High-pass 200-500 Hz** to keep low-end clean; **low-pass 6-10 kHz** to avoid sibilant splashes and make it sit behind.
- De-ess before the reverb send for vocals.

## 6. Ducking
- Sidechain-compress the reverb return from the dry vocal: reverb dips while the singer sings, blooms in the gaps.

## Gotchas
- Too many different reverb types: incoherent space. 2-3 is usually plenty.
- Reverb on bass and kick: mud (use very short or none).
- Judging reverb level solo; always in context at the loudest section, then check quiet sections.

## Verify
- Mute the reverb returns: the mix should lose depth noticeably but not change balance drastically.
- Low-end check: reverb returns contribute nothing below ~200 Hz on the analyser.
