---
id: creative-arts.animation.editorial.editorial-track-layout
name: editorial-track-layout
category: creative-arts
field: animation
product: editorial
tags: [track-layout, editorial-sound, audio-turnover, dialogue-tracks, sfx-tracks, music-tracks, checkerboarding, nle-audio, temp-tracks]
level: practitioner
status: draft
description: "Organise the cut's audio tracks by type (dialogue, temp SFX, temp music) and checkerboard dialogue by character so sound turnover and temp mixes are clean."
sources:
  - https://www.routledge.com/Dialogue-Editing-for-Motion-Pictures/Purcell/p/book/9781138242418
  - https://www.avid.com/learn-and-support
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Editorial audio track layout

**Goal:** an edit whose audio tracks are already organised the way sound post expects, so the AAF turnover
is usable, temp mixes are quick, and nobody hunts for which track holds which line.

## Standard layout (adapt to the show)

| Tracks | Content |
|---|---|
| A1-A4 | dialogue, checkerboarded by character or by take source (mono) |
| A5-A6 | scratch/temp VO, guide tracks (to be replaced) |
| A7-A10 | temp SFX (stereo pairs) |
| A11-A12 | temp ambience |
| A13-A16 | temp music (stereo pairs, alternating cues to allow overlaps) |
Keep the same layout across every sequence and episode; templates make this automatic.

## Checkerboarding dialogue

Alternate lines between tracks (A1, A2, A1, A2...) or assign one track per main character. Overlapping lines
then sit on different tracks, fades are possible, and the dialogue editor can treat each character's voice
consistently.

## Rules

- Mono dialogue on mono tracks; don't let NLEs turn mono lines into dual-mono stereo clips.
- Name tracks (DIA 1, DIA 2, SFX 1...) where the NLE allows; names carry into AAF.
- No audio effects baked in the NLE beyond simple gain and fades; sound post rebuilds them.
- Keep temp material clearly separate from production audio (final dialogue recordings).

## Gotchas

- Merged/linked clips with multiple channels expand differently in AAF; check one export early in the project.
- Levels: normalise dialogue roughly (clip gain) for screenings, but don't compress or limit on clips.

## Verify

Export a test AAF (`creative-arts.animation.editorial.aaf-audio-turnover`), open in the DAW: tracks arrive in
the same order and names, dialogue on mono tracks, nothing missing.
