---
id: creative-arts.film-live-action.davinci-resolve.fairlight-immersive-and-atmos-setup
name: fairlight-immersive-and-atmos-setup
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, fairlight-spatial, fairlight-atmos-setup, immersive-fairlight, dolby-atmos-renderer, 3d-panner, binaural-monitoring, bed-and-objects, adm-bwf]
level: practitioner
status: draft
description: "Mix immersive audio in Fairlight: bus formats (5.1/7.1.4), the 3D panner, the integrated Dolby Atmos renderer with beds and objects, binaural monitoring and ADM BWF export."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Fairlight immersive audio and Dolby Atmos)"
  - "https://professional.dolby.com/content-creation/dolby-atmos/ (Dolby Atmos content creation - beds, objects, ADM BWF)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fairlight immersive and Atmos setup

**Goal:** an immersive mix (surround or Dolby Atmos) built and delivered from Resolve,
with monitoring you can trust.

## 1. Formats and buses
- *Fairlight > Bus Format* (Bus Format dialog): create main buses in the needed format -
  5.1, 7.1, 7.1.4, and others (Ambisonics, Auro, etc. depending on version).
- Tracks can be mono, stereo, 5.1, 7.1, or immersive formats; route to the main bus.
- Set **monitoring** (*Fairlight > Immersive Audio* settings / Monitor setup) to your
  speaker layout or **binaural** for headphones.

## 2. 3D panner
Double-click a track's pan control to open the **3D panner**: X/Y (front-back, left-right),
**Z (height)**, spread/divergence, and rotate. Automate pan moves (flybys) with Fairlight
automation (touch/latch).

## 3. Dolby Atmos (Studio)
- Enable the **Dolby Atmos renderer** (*Project Settings > Fairlight > Immersive audio
  workflow*: Dolby Atmos; choose internal renderer and the monitoring layout - e.g. 7.1.4,
  5.1.4 or binaural).
- **Beds**: a 7.1.2 (or 7.1) bed bus for channel-based elements (ambiences, music
  stems, dialogue anchored centre).
- **Objects**: up to 118 object tracks for elements that move or need precise positioning
  (flybys, rain overhead); assign tracks as objects and pan in 3D.
- Binaural render modes per object (near/mid/far) for headphone delivery.

## 4. Deliverables
- **ADM BWF** master (Atmos master file) exported from the Deliver page/ Fairlight
  export; streaming platforms require it plus a 5.1 and stereo re-render (re-renders
  derived from the renderer - check downmix translation).
- IMF packages can carry the Atmos ADM in supported workflows.
- Check loudness of re-renders against specs (e.g. -27 LKFS dialogue-gated for some
  streamers, -24 broadcast).

## 5. Room and checks
Calibrate speakers to reference level (e.g. 79-85 dB SPL per channel at -20 dBFS pink
noise, per room size); verify layout with test signals; listen to binaural and downmixes.

## Gotchas
- Dialogue as objects drifting off-centre.
- Mixing Atmos only on headphones; translation to speakers fails.
- Downmix fold-down not checked; stereo deliverable thin or phasey.
- Wrong bed format for the deliverable.

## Verify
- [ ] Bus format and monitoring configured for the room or binaural.
- [ ] Beds and objects assigned; dialogue anchored.
- [ ] ADM BWF exported; 5.1/stereo re-renders checked.
- [ ] Loudness of all deliverables measured.
