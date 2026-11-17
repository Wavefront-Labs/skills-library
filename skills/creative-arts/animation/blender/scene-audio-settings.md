---
id: creative-arts.animation.blender.scene-audio-settings
name: scene-audio-settings
category: creative-arts
field: animation
product: blender
tags: [blender, scene-audio, audio-settings, doppler, speaker-objects, audio-scrubbing, sync-mode, mixdown]
level: practitioner
status: docs-checked
description: "Configure sound in a Blender scene: volume, distance model, Doppler speed and factor, and speaker object settings (mono, cache, cones, attenuation)."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html
  - https://docs.blender.org/manual/en/latest/render/output/audio/speaker.html
  - https://docs.blender.org/manual/en/latest/editors/timeline.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# scene-audio-settings

Goal: spatial audio that behaves predictably in a Blender scene with speaker objects.

## Scene Properties > Audio

- **Volume**: volume for the scene.
- **Distance Model**: how attenuation is calculated from distance. Inverse is the most physically correct; linear and exponential falloffs exist. The clamped modes limit volume to 100% (if the distance is below the reference distance the volume stays 100%). The manual refers to the OpenAL documentation for exact definitions.
- **Doppler Speed**: speed of sound for Doppler calculations; typical 343.3 m/s in air, around 1560 m/s in water.
- **Doppler Factor**: strength of the Doppler effect; 1.0 is physically correct, other values exaggerate or attenuate the pitch change.
- **Update Animation Cache**: refreshes the audio animation cache; use it if you notice artifacts in the audio.
- How sound is played back inside Blender (device, buffer and so on) lives in Preferences, System, Sound, not in the scene.

## Speaker objects

Speakers play sound in the 3D Viewport and allow spatial playback.

- **Timing is set in the NLA editor**, not in the speaker properties. New speakers automatically get a sound strip at the current frame; extra strips replay the sound at other times. Playback runs the length of the audio file and ignores the strip length.
- **Sound**: *Cache* decodes the sound into memory (suits short, frequently played effects, not long tracks). *Mono* forces single channel and is required for 3D audio and panning, because multi-channel files assume pre-mixed spatialisation.
- **Mute**, **Volume**, **Pitch** (higher speeds up playback).
- **Distance**: Volume Min and Max clamp the volume; Attenuation sets how fast volume drops (depends on the scene Distance Model); Max Distance is where attenuation stops applying; Distance Reference is where volume is 1.0 and should match the distance the sound was recorded at.
- **Cone**: inner angle keeps full volume, between inner and outer the volume interpolates linearly, outside the outer angle it drops to Outer Cone Volume (lower = more directional). 360 degrees means no directionality.

## Timeline

The Timeline shows keyframes for selected items only unless View, Only Show Selected is off. Use Timecode (Ctrl T) shows time as timestamps; Playback and Keying popovers sit in the header. Default frame range is 1 to 250.

## Gotchas

- Stereo or multi-channel sources will not pan or attenuate spatially; tick Mono.
- Long audio with Cache enabled costs memory.
- Match Distance Reference to the recording distance or the level will be off.

## Checked

Method: 2026-11-09 read the Blender manual source for Scene Properties, Speaker Objects and Timeline; removed unstated claims (sync modes, scrubbing, mixdown, codec and VSE notes).
