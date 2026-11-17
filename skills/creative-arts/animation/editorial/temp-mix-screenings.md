---
id: creative-arts.animation.editorial.temp-mix-screenings
name: temp-mix-screenings
category: creative-arts
field: animation
product: editorial
tags: [temp-mix, editorial-sound, audio-turnover, screening-mix, loudness, dialogue-intelligibility, nle-mixing, temp-music]
level: practitioner
status: draft
description: "Build a quick temp mix in the NLE for screenings: dialogue first, music and effects under it, consistent loudness, and a stereo export that plays well in a room."
sources:
  - https://tech.ebu.ch/publications/r128
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Temp mix for screenings

**Goal:** a screening where the audience hears every line and the cut is judged on story, not on jumpy levels
and buried dialogue. Not a final mix; a fast, consistent one.

## Order of work

1. **Dialogue**: clip-gain every line to a consistent level (meter around -24 to -20 LUFS short-term for
   speech in a -24 integrated mix); fix obvious clicks; cross-fade edits (2-4 frames).
2. **Music**: under dialogue by ~10-15 dB during lines, up in gaps and transitions. Use keyframes or the NLE's
   auto-ducking (Premiere Essential Sound "Ducking", Resolve Fairlight sidechain).
3. **Effects and ambience**: only what the story needs; ambience low and continuous across cuts to hide
   dialogue edits.
4. **Master bus**: a limiter at -1 dBTP; check integrated loudness of the whole cut.

## Loudness target

For a screening room or TV, about -24 LUFS integrated is comfortable; for laptops/online review copies, about
-16 to -14 LUFS. Measure in the NLE's loudness meter or:
```bash
ffmpeg -i screening.mov -af ebur128=peak=true -f null - 2>&1 | tail -12
```

## Export

Stereo 48 kHz 24-bit PCM in the screening file (or AAC 320 kbps for online review). Listen to the export once on
the room's system before the audience arrives.

## Gotchas

- Temp music cleared for internal use only: screenings outside the company may need licences; label temp.
- Over-processed temp mixes set expectations the real mix must then match; keep it neutral.
- Mono-summed rooms: check the mix in mono so panned dialogue doesn't vanish.

## Verify

Play the first act in the screening room at the planned level: every line intelligible from the back row,
no music cue jumping out, integrated loudness within 1 LU of the target.
