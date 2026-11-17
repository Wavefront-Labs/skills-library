---
id: creative-arts.film-live-action.production-sound.ifb-camera-hops-and-digital-wireless
name: ifb-camera-hops-and-digital-wireless
category: creative-arts
field: film-live-action
product: production-sound
tags: [production-sound, film-live-action, ifb-setup, comms-setup, camera-hop-setup, digital-wireless, wireless-latency, digital-systems, comtek, iem, encryption, wisycom, lectrosonics-dbu]
level: practitioner
status: draft
description: "Set up IFB feeds and camera hops for the set, and work with digital wireless systems: latency budgets, encryption, timecode in transmitters and mixing analog and digital links."
sources:
  - "https://www.lectrosonics.com (Lectrosonics - digital wireless (D Squared, DCHT) and IFB)"
  - "https://www.wisycom.com (Wisycom - wireless systems and camera hops)"
  - "https://www.zaxcom.com (Zaxcom - digital wireless with recording transmitters)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IFB, camera hops and digital wireless

**Goal:** everyone who needs to hear the dialogue hears it; cameras get the mix; and the
wireless system adds no audible delay or sync problems.

## 1. IFB (interruptible foldback) feeds
- Transmit the **mix** to director, script supervisor, producers, video assist, client
  via IFB/IEM transmitters to belt receivers with earpieces (Comtek, Lectrosonics IFB,
  Sennheiser IEM, Wisycom). Count receivers in prep; label and charge them.
- Optionally a **talkback** channel (sound mixer to boom op/ director).
- Use a separate frequency block from talent mics (RF plan).

## 2. Camera hops
- A transmitter from the mixer's outputs to a receiver on each camera (stereo or
  dual-channel) recording the **mix on the camera's audio tracks**: editorial gets synced
  sound in dailies even before full sync; also a backup.
- Set line-level output into the camera; adjust camera input gain; check levels and the
  channel mapping on a recorded clip (see camera-audio skill).
- Some systems also send **timecode** to the camera.

## 3. Digital wireless
- Examples: Lectrosonics D Squared/DCHT, Zaxcom (digital with **recording transmitters**
  - local backup recording in the transmitter), Wisycom (analog/ hybrid), Shure Axient Digital.
- **Latency**: digital links add ~1-4 ms per hop depending on system and mode. Mixing a
  digital lav with an analog boom (or a different digital system) creates time offsets ->
  comb filtering. Keep all talent mics on the **same system/ latency**, or delay the boom
  input to match (recorder input delay).
- Camera hops/IFB add latency too - fine for monitoring but note it for lip-sync with
  camera scratch tracks.
- **Encryption** (AES-256 on many digital systems) for confidential productions.
- **Recording transmitters** (Zaxcom, Deity TC-1, Tentacle Track E style) are a dropout
  backup - jam timecode to them and collect the files daily.

## 4. RF planning
Coordinate all frequencies (talent, hops, IFB, boom, comms) in one plan with intermod-free
spacing; scan the location; re-scan when moving. See wireless and RF coordination skill.

## Gotchas
- Mixed latency systems summed in the mix - phasey dialogue.
- Hops left at mic level into a line input.
- IFB receivers dead at 2pm because nobody charged them.
- Recording transmitters not jammed - files can't be synced.

## Verify
- [ ] IFB count, frequencies and charging plan.
- [ ] Camera hops recording the mix at correct levels and channels.
- [ ] Wireless latency matched or compensated; encryption as required.
- [ ] Recording transmitters jammed and harvested daily.
