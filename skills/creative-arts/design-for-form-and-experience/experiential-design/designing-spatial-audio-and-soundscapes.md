---
id: creative-arts.design-for-form-and-experience.experiential-design.designing-spatial-audio-and-soundscapes
name: designing-spatial-audio-and-soundscapes
category: creative-arts
field: design-for-form-and-experience
product: experiential-design
tags: [spatial-audio, soundscape, installation-audio, ambisonics, multichannel-audio, sound-design-installations, immersive-installations]
level: advanced
status: draft
description: "Design spatial audio for installations: speaker layout, zones, delay alignment, ambisonic or object-based spatialisation, levels and neighbours, with commissioning tests."
sources:
  - "Audinate Dante documentation (audinate.com)"
  - "IEM Plug-in Suite (plugins.iem.at)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Spatial audio and soundscapes

Sound sets mood and directs attention in immersive spaces. Spatial design decides where sounds come from and how they behave around visitors.

## Design the soundscape
1. **Intent:** what the sound does (ambience, narrative, cues, interaction feedback); keep layers: bed, events, accents.
2. **Zones and levels:** separate areas so sound from one does not wash into another; measure the room's noise floor and aim for a margin for the content; agree peak and average levels with the venue (also for neighbours and hearing safety).
3. **Content approach:** stereo, multichannel beds with sounds placed on specific speakers, ambisonics (sound field encoded then decoded to the speaker array), or object-based systems from audio manufacturers.

## Speakers and system
- **Layout:** decide height layers and coverage; directional speakers (including parametric or beam-type devices) to create sound pockets without spill; subwoofers for body feel; consider acoustic treatment against reverberation that blurs spatial cues.
- **Network and processing:** audio over IP (Dante, AES67 or similar) with a DSP for routing, EQ and limiting; the DSP also holds delays per speaker.
- **Time alignment:** sound travels at about 343 metres per second, which is about 2.9 ms per metre; delay nearer speakers so sounds from the array arrive consistently.

## Tools
Digital audio workstations (such as Reaper) with ambisonic plug-ins (for example the free IEM Plug-in Suite), Max or Pure Data for interactive sound, and QLab for playback (see `...experiential-design.programming-show-control`).

## Commission
Walk the space with pink noise and test content; check coverage, levels, intelligibility and phase; save presets; test the idle and failure behaviour.

## Verify
- [ ] Levels were measured and agreed with the venue.
- [ ] Spatial effects work across the visitor area, not just at the sweet spot.
- [ ] Speakers are time-aligned and protected by limiters.
