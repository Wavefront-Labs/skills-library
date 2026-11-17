---
id: computing-software.game-programming.game-engine-architecture.spatial-3d-audio-attenuation
name: spatial-3d-audio-attenuation
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, spatial-audio, 3d-audio, attenuation-curves, occlusion, hrtf, doppler, listener-position, game-programming]
level: advanced
status: draft
description: "Implement 3D game audio: listener placement, attenuation curves and min/max distance, panning vs HRTF, occlusion/obstruction raycasts, doppler and reverb zones."
sources: ["https://valvesoftware.github.io/steam-audio/", "https://docs.unity3d.com/Manual/class-AudioSource.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spatial 3D audio and attenuation

**Goal:** players can locate sounds and judge distance, and the mix stays clean as hundreds of
emitters come and go (Gregory ch. 14).

## Listener placement
Third-person games: put the listener between camera and character (or at the character with camera
orientation), otherwise sounds near the player pan oddly as the camera orbits. First-person: at the
head, oriented with the camera. Split screen needs one listener per player (engine support varies).

## Attenuation
- **Min distance** (full volume radius) and **max distance** (inaudible or floor volume).
- Curve shape: inverse (`gain = min / (min + rolloff*(d − min))`, physically plausible, long tails),
  linear or custom curves (designer-friendly, predictable cut-off). Most games use custom curves per
  category (gunshots audible 200 m; footsteps 20 m).
- Distance also drives a **low-pass filter** (air absorption), reverb send and spread, not only volume.
- Cull/virtualise beyond max distance (see `audio-mixing-buses-and-voice-management`).

## Panning and HRTF
- Speaker panning (VBAP/equal-power) for stereo/5.1/7.1.
- **HRTF** binaural rendering for headphones gives elevation and front/back cues (Steam Audio,
  Microsoft Spatial Sound, Sony Tempest 3D, Unreal binaural plugins, Resonance). Offer a headphone
  mode option.
- **Spread** for large sources (rivers, crowds): widen the image as the listener gets close; or use
  multiple emitters / line and area emitters.

## Occlusion and obstruction
Raycast (or multi-ray) from listener to emitter against a simplified audio collision layer:
- Blocked: apply low-pass and volume reduction (occlusion).
- Throttle: a few rays per frame round-robin across emitters; smooth results over ~100 ms to avoid
  chatter.
- Better: propagation via portals/rooms (Wwise Spatial Audio rooms & portals, Steam Audio baked
  propagation) so sound comes around corners from the doorway.

## Doppler and reverb
Doppler from relative velocity (pitch factor `(c + v_listener) / (c − v_source)` along the line);
clamp and scale it down (full physical doppler sounds wrong on fast vehicles). Reverb zones / rooms
set environment reverb per area; emitters send to the listener's room reverb.

## Engine mapping
Unity AudioSource Spatial Blend, 3D Sound Settings (rolloff, min/max, spread, doppler) and Audio
Spatializer plugins; Unreal Sound Attenuation assets (falloff, spatialization method, occlusion,
reverb send, focus); Godot AudioStreamPlayer3D (`unit_size`, `max_distance`, attenuation model,
`Area3D` reverb bus).

## Verify
- [ ] Blindfold test: testers point to sound sources with headphones (HRTF on vs off).
- [ ] Sounds behind a wall are muffled; opening the door un-muffles smoothly.
- [ ] Orbiting the camera around the character does not swing nearby sounds left/right wildly.
