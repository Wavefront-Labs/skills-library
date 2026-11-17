---
id: creative-arts.film-live-action.cinematography.led-fixtures-practicals-and-dmx-control
name: led-fixtures-practicals-and-dmx-control
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, led-tubes, led-panel-control, led-colour-control, dmx-control, lighting-console, wireless-lighting-control, practicals-in-frame, dimming-practicals, practical-rigging, crmx, sacn]
level: practitioner
status: draft
description: "Use LED panels and tubes, rig and dim practicals in frame, and control it all over DMX: modes, addressing, wireless CRMX, consoles and apps, and cueing lighting changes."
sources:
  - "https://www.esta.org (ANSI E1.11 DMX512-A and E1.31 sACN standards - ESTA)"
  - "https://www.lumenradio.com (LumenRadio CRMX - wireless DMX)"
  - "Harry C. Box, Set Lighting Technician's Handbook (dimmers, practicals and control)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LED fixtures, practicals and DMX control

**Goal:** every light, including the lamps in shot, under precise remote control - so
colour and level can be changed in seconds and cued during takes.

## 1. LED panels and tubes
- **Panels** (e.g. SkyPanel, Litemat, Creamsource): soft, tunable CCT (2700-10000 K),
  +/- green, RGB(W) effects. **Tubes** (Astera, Quasar, Nanlux): hide in frame, line
  sources, battery-powered with built-in wireless.
- Modes: **CCT** (Kelvin + green), **HSI** (hue/saturation/intensity), **RGBW**, **xy
  coordinates**, **gel emulation** (pick a Lee/Rosco gel), **effects** (fire, TV, lightning,
  police). Choose the fixture's **DMX mode** (a channel profile) - "CCT 8-bit", "HSI
  16-bit" etc. - from the manual.
- Quality: check TLCI/SSI; mixing brands requires metering (see colour meter skill).
- Dimming curves and PWM frequency: some LEDs flicker at high frame rates - test.

## 2. DMX addressing
- DMX512: one **universe** = 512 channels. Each fixture occupies N channels from its
  **start address**. Make a **patch sheet**: fixture, mode, universe, address, channels,
  position.
- Wired: 5-pin XLR, daisy-chained, terminated at the end of the line.
- Wireless: **CRMX** (LumenRadio) receivers built into many fixtures; pair them to a
  transmitter; or **sACN/Art-Net** over Ethernet/Wi-Fi to nodes.

## 3. Control surfaces
- **Consoles**: grandMA, ETC Ion/Eos, or compact boards; a dedicated **dimmer board
  operator** on larger sets.
- **Apps**: Luminair, Blackout, manufacturer apps (Aputure Sidus, Astera app) for small
  sets; tablet + wireless node.
- Record **presets/cues**: "Day", "Dusk", "Lights off", "TV flicker" - cue during takes
  on the operator's go.

## 4. Practicals in frame
- Choose bulbs: tunable LED bulbs (e.g. Astera NYX, wireless DMX) or dimmable tungsten on
  a dimmer. Match colour to the scene (2700-3200 K warm).
- **Exposure**: practicals usually read 1-3 stops over key on the shade; too bright
  clips and looks "lit". Dim, use ND/diffusion inside the shade, or lower-wattage bulbs.
- **Rigging**: hide a dimmer (in-line or DMX) at the lamp; tape cables along legs; use
  hidden LED tape inside shades to throw light onto faces.
- Use them as **sources**: place practicals where the key motivation should be.

## Gotchas
- Two fixtures on overlapping addresses responding together.
- DMX mode on the fixture not matching the console profile.
- Wireless dropouts with metal and distance - keep a wired backup.
- Practicals clipping or flickering on camera at off-speed.

## Verify
- [ ] Patch sheet with modes, universes and addresses; no overlaps.
- [ ] Wireless paired and range-tested; wired fallback available.
- [ ] Cues recorded and rehearsed with the operator.
- [ ] Practicals dimmed to the intended level and tested at the shooting frame rate.
