---
id: creative-arts.music.ableton-live.drum-rack-pads-choke-groups-and-sends
name: drum-rack-pads-choke-groups-and-sends
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, drum-rack, instrument-rack, drum-rack-pads, choke-groups, rack-returns, receive-note, pad-layering, hi-hat-choke, drum-programming]
level: practitioner
status: docs-checked
description: "Build Drum Racks in Live: loading and layering pads, choke groups, Receive and Play note mapping, and return chains fed by per-chain send sliders."
sources:
  - https://www.ableton.com/en/live-manual/12/instrument-drum-and-effect-racks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Drum Rack pads, choke groups and sends (Live)

**Goal:** a playable, well-organised drum kit in one device.

## 1. Loading pads
- Each pad represents one of the 128 MIDI notes; the pad overview shifts the visible set in
  groups of 16.
- Dropping a multi-selection of samples onto a pad maps new Simplers and chains upwards
  chromatically from that pad, replacing samples on those pads but leaving effects alone.
- **Layering:** Alt (Windows) or Cmd (Mac) dragging a multi-selection onto one pad layers all
  the samples on that pad in a nested Instrument Rack.

## 2. Choke groups
- In the Input/Output section, the **Choke** chooser sets a chain to one of sixteen choke
  groups. Chains in the same group cut each other off (for example open and closed hi-hats).

## 3. Note mapping
- **Receive** chooser: the incoming MIDI note the drum chain responds to.
- **Play** slider: the outgoing MIDI note sent to the devices in the chain.

## 4. Return chains and sends
- Up to six return chains of audio effects can be added in the Drum Rack; they are fed by
  send sliders in each of the drum chains. This keeps effects inside the rack.

## Verify
- Play one hat in a choke group then the other: the first stops.
- Send sliders feed the return chains audibly.

## Checked
2026-11-01. Confirmed in the Live 12 manual chapter "Instrument, Drum and Effect Racks": 128 notes and groups of 16, multi-sample drop behaviour, Alt/Cmd layering into a nested Instrument Rack, sixteen choke groups in the Input/Output section, Receive chooser and Play slider, up to six return chains with send sliders. Removed (not on that page): Cmd/Ctrl-only layering wording, per-pad "knob" wording, the "R" button, mixer-expansion steps, saving and Collect All notes, Simpler mode gotchas.
Method: documentation only; no commands were run.
