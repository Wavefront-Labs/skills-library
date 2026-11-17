---
id: creative-arts.music.music-production.buses-auxes-and-send-routing
name: buses-auxes-and-send-routing
category: creative-arts
field: music
product: music-production
tags: [music-production, logic-pro, pro-tools, daw, aux-sends, bus-routing, aux-track, summing-stack, vca-fader, cue-mix, headphone-mix, pre-fader-send, internal-bus, routing-folder]
level: practitioner
status: draft
description: "Route Logic Pro or Pro Tools sessions: aux tracks and buses for effects and submixes, pre/post-fader cue sends, summing stacks, VCAs and bus naming."
sources: ["https://support.apple.com/guide/logicpro/ (Use send effects; Summing track stacks; VCA faders)", "https://www.avid.com/pro-tools (Pro Tools Reference Guide - I/O Setup, buses, sends, VCA masters)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Buses, auxes and send routing (Logic, Pro Tools)

**Goal:** clean routing for effects, submixes and cue mixes in any DAW.

## 1. Concepts
- **Bus**: a virtual cable. **Aux track** (aux input): a channel that receives a bus, processes it, and outputs it.
- **Send**: copies part of a track's signal to a bus (for effects or cue mixes). **Output routing**: moves the whole track to a bus (for submixes).

## 2. Send effects
- Logic: click a Send slot > choose a bus; Logic creates an aux automatically. Name it (e.g. "Plate Vox"). Pro Tools: Send slot > New Track or choose a named bus; create a stereo aux with input = that bus.
- Effect on the aux 100% wet; send level per track.

## 3. Submixes / group buses
- Logic: select tracks > Track > Create Track Stack > **Summing Stack** (creates a bus + aux). Pro Tools: set track outputs to a named bus (e.g. "DRUMS"), create an aux with that input.
- Process the aux (bus compression, EQ) and route it to the mix bus.

## 4. Pre vs post-fader sends (cue mixes)
- Post-fader (default for effects): follows the track fader.
- **Pre-fader** for headphone/cue mixes: performer's mix independent of your control-room mix. Pro Tools: send "PRE" button; Logic: send mode Pre Fader. Route cue buses to interface outputs feeding headphone amps.

## 5. VCAs
- **VCA faders** control the levels of assigned tracks without summing audio (Logic VCA; Pro Tools VCA Master). Use for overall section rides without changing bus processing input.

## 6. Organisation
- Name buses in I/O setup (Pro Tools Setup > I/O > Bus) or Logic's bus labels; colour aux tracks; keep effects returns together.

## Gotchas
- Feedback loops: a track sending to a bus that feeds back to itself.
- Mixing sends to a bus that also receives outputs: confusing levels.
- Pro Tools mono/stereo mismatch on sends and auxes (stereo send to a mono aux).

## Verify
- Solo-safe the aux returns so soloing a track still lets you hear its effects.
- Signal flow check: each track's path to the mix bus is clear and passes through only intended buses.
