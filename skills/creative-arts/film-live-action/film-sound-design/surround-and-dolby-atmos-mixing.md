---
id: creative-arts.film-live-action.film-sound-design.surround-and-dolby-atmos-mixing
name: surround-and-dolby-atmos-mixing
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, post-production-sound, re-recording-mixer, surround, surround-mixing, 5-1, 7-1, atmos, dolby-atmos, immersive-audio, immersive, beds, objects, dolby-atmos-renderer, dolby-atmos-production-suite, atmos-mastering-suite, adm-bwf, binaural-render, re-renders, object-panner, pro-tools-atmos, nuendo-atmos, resolve-atmos, fairlight-atmos, home-atmos, theatrical-atmos, 7-1-4, 9-1-6, overheads, height-channels, surround-panning, divergence, lfe-management, bass-management, centre-channel, exit-sign-effect, surround-monitoring, room-calibration, downmix-compatibility, trim-and-downmix-metadata, dts-x, auro-3d, mpeg-h, atmos-renderer-setup, renderer-routing, beds-and-objects, object-panning, atmos-room, atmos-calibration, adm-bwf-delivery, atmos-master, binaural-render-use, downmix-check, surround-panning-rules, centre-channel-use]
level: practitioner
status: draft
description: "Mix in surround and Dolby Atmos: 5.1/7.1 placement rules, LFE and the centre channel, Atmos beds vs objects, the Renderer and monitoring layouts, trim/downmix metadata, binaural, the ADM master."
sources:
  - "https://professional.dolby.com/content-creation/dolby-atmos-for-content-creators/ (Dolby Atmos production guidelines and Renderer documentation)"
  - "https://cinemaaudiosociety.org/ (Cinema Audio Society - surround mixing craft)"
  - "https://www.avid.com/pro-tools (Pro Tools - Dolby Atmos integration)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Surround and Dolby Atmos mixing

**Goal:** an immersive mix that translates - envelops in a theatre, collapses cleanly
to a soundbar, and still has the dialogue in the right place when heard on a phone.

## 1. Surround fundamentals (5.1 / 7.1)
- **Centre** carries dialogue and on-screen anchors; L/R the width of music and
  effects; **surrounds** ambience, reverb returns and occasional discrete events;
  **LFE** (0.1, band-limited 20-120 Hz) is an *effects* channel, not the sub - most
  bass should live in the main channels with bass management in the playback system.
- **Front-back balance**: audiences sit everywhere; surround content that's too
  specific (a car passing only in Ls) reads as a fault for half the room. Spread diffuse
  sounds, keep discrete surround events motivated by picture (the "exit sign effect" -
  a sudden surround cue makes people turn around - is a tool, use rarely).
- **Divergence/spread** on panners keeps movement smooth across speakers; hard point-
  source pans across the front image can tear on cuts.
- 7.1 adds side vs rear surround separation for more precise placement; mix 7.1 with
  a 5.1 fold-down check.
- Monitor at the calibrated reference in a room with correct speaker angles (ITU-R
  BS.775); theatrical vs near-field (home) targets differ - decide which version is
  the master and derive the other.

## 2. Dolby Atmos concepts
- A **bed** is a channel-based layer (7.1.2 typically): ambiences, music beds, anything
  diffuse. **Objects** (up to 118) are mono/stereo sounds with 3D position metadata
  rendered to whatever speakers exist - dialogue off-screen, fly-overs, specific
  effects, music elements you want overhead or precise.
- The **Dolby Atmos Renderer** (Production Suite/Mastering Suite, or integrated in
  Pro Tools/Nuendo/Resolve-Fairlight) receives 128 inputs from the DAW, renders to the
  monitoring layout (7.1.4, 9.1.6, 5.1.4, 2.0, binaural) and records the **master**
  (ADM BWF / .atmos). DAW track outputs route to Renderer inputs; object panners
  (Pro Tools' 3D panner) send position metadata.
- **Home vs theatrical** Atmos: theatrical masters are for cinema (full object count,
  larger rooms, 85 dB); home deliverables are typically from a **7.1.4 near-field
  mix** with **trim and downmix metadata** set in the Renderer for 5.1/2.0/binaural.

## 3. Mixing Atmos
- Dialogue stays as a centre-anchored object or in the bed centre; don't fly it.
- Put **ambience and reverb** in the bed including the heights (`.2` or `.4`); the
  overheads are for weather, interiors with ceilings, flying things - sparingly.
- Make objects for sounds that move or need placement precision; keep the number
  manageable (each object costs rendering and attention); group static sounds into the
  bed.
- **Size/spread** on objects to avoid pinpoint sources that collapse badly to stereo.
- Check **binaural** (headphone) render settings per object (near/mid/far/off) - the
  streaming audience largely hears Atmos as binaural on AirPods/phones.
- **Loudness**: measure on the 5.1 re-render (or as the spec says - Netflix measures
  the 5.1 re-render dialogue-gated); true peak on all re-renders.

## 4. Monitoring layouts and calibration
Home Atmos room: 7.1.4 minimum (9.1.4 better) with overheads at ~45° elevation,
calibrated to 79-82 dB C per channel (-20 dBFS), bass managed subs; theatrical stages
use Dolby's room specs and 85 dB. Switch monitoring layouts in the Renderer to audition
5.1, stereo, binaural - do this constantly.

## 5. Deliverables
- **ADM BWF** master (48 kHz 24-bit, includes beds/objects/metadata, up to 2 h) per
  reel or programme; **IAB** for DCP; **Dolby Atmos re-renders**: 7.1, 5.1, 2.0,
  binaural; plus the legacy printmasters (see the loudness and stems skill).
- Trim/downmix metadata: set in the Renderer *before* exporting; the ADM carries it.
- QC: play the ADM back through the Renderer, check the binaural and 2.0 re-renders
  on headphones/speakers, confirm frame rate and start timecode.

## Gotchas
- Everything as objects; the mix is fragile and the stereo fold-down is a mess.
- Dialogue panned into the heights for "fun"; intelligibility drops on soundbars.
- LFE used as the bass of the music; bass-managed home systems double it.
- Mixing only on the 7.1.4 layout; the binaural render was never heard.
- Theatrical Atmos master delivered to a streamer; levels and room assumptions wrong.

## Verify
- [ ] Dialogue centred, surrounds motivated, LFE reserved for effects; 5.1 fold-down checked.
- [ ] Beds for diffuse content, objects only for placed/moving sounds; binaural settings per object.
- [ ] Renderer monitoring switched across 7.1.4/5.1/2.0/binaural during the mix; trim/downmix metadata set.
- [ ] ADM BWF (or IAB) plus re-renders exported, played back and loudness-measured per spec.
