---
id: media-communication.broadcasting.broadcast-audio.mic-balance-mix-minus-and-loudness-compliance
name: mic-balance-mix-minus-and-loudness-compliance
category: media-communication
field: broadcasting
product: broadcast-audio
tags: [broadcast-audio, sound-supervisor, audio-mixing, broadcast-console, calrec, lawo, wheatstone, studer, yamaha, mixing-desk, mic-balance, gain-structure, mix-minus, n-1, clean-feed, ifb, talkback, loudness, lufs, lkfs, ebu-r128, atsc-a85, true-peak, ppm, ob, outside-broadcast, live-sound, lavalier, broadcasting]
level: practitioner
status: draft
description: "Mix live broadcast sound on a studio or OB console: gain structure, balancing mics, building mix-minus (N-1) feeds for remote contributors, and hitting EBU R128 or ATSC A/85 loudness."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mic balance, mix-minus and loudness compliance

**Goal:** clear, consistent speech on air, every remote contributor hearing the programme
without their own voice echoing back, and output that passes the broadcaster's loudness spec.

## 1. Gain structure first
- Set **input gain (trim)** with the talent speaking at performance level, not saying
  "one two" quietly. Aim for healthy level with headroom; set faders near their marked
  unity/0 position so you have travel both ways.
- Consoles differ (Calrec, Lawo, Wheatstone, Studer, Yamaha and others) but all reward the
  same habit: trim at the input, mix with the fader.
- Use the **high-pass filter** on every voice mic (around 80-100 Hz).
- Light **compression** on voices evens out level; heavy compression raises noise and room.

## 2. Mic balance
- **One open mic per speaker when they speak.** Every open mic adds room noise and
  comb-filtering (phasey sound) when two mics hear the same voice. Ride faders down on
  silent speakers or use an automixer if the console has one.
- Lavaliers: position mid-chest, away from clothing rustle; tape a loop for strain relief.
  Check for jewellery clicks.
- **PFL** (pre-fade listen) every source before opening it.
- Balance by ear on good monitors at a consistent volume, confirmed by meters.

## 3. Mix-minus (N-1, clean feed)
A remote contributor (phone line, codec, video call, OB) needs to hear the programme
**minus their own voice** — otherwise they hear themselves delayed and the line may
feed back.
- On broadcast consoles: assign the contributor's channel to its own **mix-minus/N-1
  output**. Most consoles generate it automatically per channel ("N-1" or "clean feed").
- On small mixers without automatic N-1: use an aux send with **every source except the
  contributor**, pre-fade or post-fade as needed, and route that aux to the codec/phone.
- Add **talkback** into the N-1 so the producer can speak to the contributor off-air.
- **Test** each N-1 in rehearsal: ask the contributor whether they hear themselves
  (they shouldn't) and the presenter (they should).

## 4. Loudness compliance
Broadcast delivery is measured by **integrated loudness** over the programme:
| Standard | Region (typical) | Target | Max true peak |
|---|---|---|---|
| EBU R128 | Europe and many others | -23 LUFS | -1 dBTP |
| ATSC A/85 (CALM Act) | United States | -24 LKFS | -2 dBTP |
Some broadcasters set tighter house specs; streaming platforms often target louder levels
(around -14 to -16 LUFS) — *confirm the delivery spec for each outlet*.

Practice:
- Use a **loudness meter** (momentary, short-term, integrated) on the output, not only PPM.
- Mix speech to sit consistently near target short-term; music and effects follow speech.
- Control peaks with a limiter on the main output set below the true-peak limit.
- Watch loudness range — very quiet passages followed by loud stings annoy viewers and
  can fail QC.

## 5. OB specifics
- Clearly label every line and channel; tie lines get swapped.
- Record a backup multitrack where possible.
- Keep communications (talkback, comms) on separate, clearly labelled paths from programme.
- Confirm line-up tone and level with the receiving end (e.g. -18 dBFS EBU line-up — check
  your broadcaster's line-up level).

## Verify
- [ ] Each mic trimmed at performance level; HPF on.
- [ ] Only active speakers' mics open; no comb filtering.
- [ ] Each remote contributor confirms clean N-1 (no self-echo) and talkback works.
- [ ] Integrated loudness and true peak within spec on the programme output.
- [ ] Line-up tone and level agreed with the destination.
