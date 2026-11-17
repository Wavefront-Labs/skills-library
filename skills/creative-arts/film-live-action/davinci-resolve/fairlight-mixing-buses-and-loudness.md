---
id: creative-arts.film-live-action.davinci-resolve.fairlight-mixing-buses-and-loudness
name: fairlight-mixing-buses-and-loudness
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, fairlight, fairlight-page, fairlight-mixing, mixing, bus-layout, buses, main-bus, sub-bus, aux-bus, track-types, mono, stereo, 5-1, 7-1, atmos, fairlight-fx, dialogue-processor, de-esser, noise-reduction, voice-isolation, dialogue-leveler, eq, compressor, limiter, loudness-meter, lufs, lkfs, true-peak, ebu-r128, atsc-a85, netflix-loudness, automation, fader-automation, clip-gain, normalize, track-normalisation, audio-track-layout, adr-recording, foley-sampler, bus-export, stems-export, deliver-audio, fairlight-audio-editor, fairlight-tracks, fairlight-patching, fairlight-mixer, voice-isolation-use, fairlight-dialogue, dialogue-leveler-use, fairlight-automation, automation-modes, fader-automation-use, fairlight-loudness, loudness-metering, normalise-to-loudness, fairlight-export, bus-export-use, stems-from-fairlight]
level: practitioner
status: draft
description: "Mix a film in Fairlight: DX/MX/FX sub buses to a main, clip gain vs faders vs automation, Fairlight FX for dialogue cleanup, loudness metering to R128/A85/streamer specs, and exporting stems."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Definitive Guide to DaVinci Resolve - Fairlight chapters; Fairlight Audio Guide)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Fairlight section)"
  - "https://tech.ebu.ch/publications/r128 (EBU R128 loudness)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fairlight: mixing, buses and loudness

**Goal:** a mix built on a bus structure that makes stems, loudness compliance and
revisions trivial - dialogue first, music and effects around it - without leaving Resolve.

## 1. Track and bus layout
Fairlight page > `Fairlight > Bus Format`:
- **Main 1** (stereo or 5.1) is the mix. Add **Sub buses**: `DX` (dialogue), `MX`
  (music), `FX` (effects/ambience), optionally `VO`. Route tracks to subs, subs to Main.
  Subs carry the bus processing and become the **stems**.
- Track types (right-click track header > *Change Track Type*): mono for dialogue ISOs,
  stereo for music, 5.1 for pre-mixed beds. Mismatched types (a mono file on a stereo
  track) play fine but confuse routing.
- Name tracks (`DX Marta`, `DX Boom`, `FX Amb`, `MX Score`) and colour them; use the
  **Track Index** to show/hide groups and the **Mixer** (`Ctrl/Cmd+Shift+M`) for faders.
- **Aux buses** for shared reverb (send dialogue to a room verb) so all ADR sits in one space.

## 2. Gain staging: clip gain, faders, automation
1. **Clip gain** (Inspector or `Alt`+drag the clip's gain line) to level each clip near
   -20 dBFS RMS / dialogue peaks around -12; *Normalize Audio Levels* on a selection for
   a rough start (set Target: -23 LUFS or peak -1 dB for sample peaks).
2. **Fades** on every edit (drag the clip corners); crossfades on dialogue cuts in the
   same take (right-click > *Add Crossfade*).
3. **Faders** for balance between tracks; **bus faders** for the overall DX/MX/FX relationship.
4. **Automation** (`Automation` toolbar: Touch/Latch/Write, parameters: volume, pan,
   plugin params) for moves over time; draw with the pencil in the track's automation
   lane for precision. Clip gain for static problems, automation for dynamic ones.

## 3. Processing (Fairlight FX)
Per track or bus via the Mixer's effect slots:
- **Dialogue**: *Noise Reduction* (learn a noise profile from room tone), *Voice
  Isolation* (AI; use sparingly, listen for artefacts), *De-Esser*, *Dialogue Processor*
  (one-stop EQ/comp/de-ess), *Vocal Channel*, a high-pass at 80-100 Hz, gentle
  compression (3:1, -18 threshold, slow attack) and **Dialogue Leveler** on the DX bus.
- **Music**: EQ dip 2-4 kHz under dialogue; ducking via automation or a sidechained
  compressor on the MX bus keyed from DX (Compressor > Sidechain).
- **FX**: reverb (*Reverb*, *Chamber*), *Foley Sampler* for quick footsteps, *Stereo
  Width*, *Pitch*.
- **Main bus**: a *Limiter* at -1 dBTP as a safety, not as the loudness tool.
Order matters: NR > EQ > de-ess > compression > level.

## 4. Loudness
Open the **Loudness meter** (Mixer right side; `Fairlight > Loudness`), choose the
standard in `Project Settings > Fairlight > Loudness`: **EBU R128** (-23 LUFS integrated,
-1 dBTP, broadcast EU/UK), **ATSC A/85** (-24 LKFS, -2 dBTP, US broadcast), streamer specs
(Netflix: -27 LKFS dialogue-gated average, -2 dBTP; YouTube/web often -14 to -16 LUFS
integrated). Reset, play the whole program, read *Integrated*, *Short-term max*,
*Range (LRA)*, *True Peak*. Hit the target by adjusting bus/main faders, not by the
limiter. For dialogue-gated specs use the dialogue-only measurement (solo DX). Theatrical
mixes are not loudness-normalised; they're mixed at 85 dB C reference in a calibrated room.

## 5. Monitoring
Calibrate the room/headphones; use *Fairlight > Monitoring* for downmix checks (5.1 ->
stereo, mono) because broadcast listens in every format. `Ctrl/Cmd+Shift+D` dim.
Reference the mix on consumer speakers before delivery.

## 6. Export
- Deliver page > *Audio*: export the Main (stereo/5.1) with the picture; render
  **bus outputs** separately (`Render > Audio > Output Tracks: Bus 1..n`) for stems
  (DX/MX/FX) - *Export per bus* as separate WAV files, 48 kHz 24-bit.
- `Fairlight > Export > ... ` AAF/OMF of the Fairlight timeline for a Pro Tools mix if the
  show goes out of house; include handles.
- Burn the loudness report (Deliver page can add a loudness measurement log in some versions).

## Gotchas
- All tracks routed straight to Main; no stems, no bus processing, no easy fix later.
- Loudness hit with a brick-wall limiter; the mix pumps.
- Normalizing clips to -23 LUFS *individually* then wondering why quiet lines are loud.
- Reverb inserted per track instead of an aux; every line sounds like a different room.
- Delivering 44.1 kHz or 16-bit stems by leaving the project default.

## Verify
- [ ] DX/MX/FX sub buses to Main; tracks named, typed and routed.
- [ ] Clip gain for levels, automation for moves, fades on every cut.
- [ ] Loudness report meets the delivery spec (integrated and true peak); downmix checked.
- [ ] Stems exported per bus at 48 kHz/24-bit with the final mix.
