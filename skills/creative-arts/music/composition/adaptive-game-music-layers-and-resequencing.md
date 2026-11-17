---
id: creative-arts.music.composition.adaptive-game-music-layers-and-resequencing
name: adaptive-game-music-layers-and-resequencing
category: creative-arts
field: music
product: composition
tags: [composition, media-composition, game-audio, adaptive-music, horizontal-resequencing, vertical-layering, fmod, wwise, interactive-music]
level: advanced
status: draft
description: "Compose and implement adaptive game music with vertical layering and horizontal resequencing, transition rules and stingers in FMOD or Wwise."
sources: ["https://www.audiokinetic.com/en/library/edge/?source=WwiseFundamentalApproach&id=interactive_music", "https://www.fmod.com/docs/2.02/studio/welcome-to-fmod-studio.html", "Winifred Phillips, A Composer's Guide to Game Music (MIT Press, 2014)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adaptive game music: layers and resequencing

**Goal:** music that follows gameplay state (explore, tension, combat, victory) without
audible seams.

## 1. Choose the technique per situation
- **Vertical layering (re-orchestration):** several stems of the same piece play in
  sync; game parameters fade layers in and out (e.g. percussion layer on when enemies
  are near). Smooth and fast to react; harmony and tempo cannot change.
- **Horizontal resequencing:** the piece is cut into segments; the engine chooses what
  plays next at a legal transition point. Can change key, tempo and mood; reaction time
  is limited by segment length.
- Most scores combine both: horizontal sections with vertical layers inside each.

## 2. Writing for layers
- All layers share tempo, length and harmony; each must sound complete alone and with
  any combination. Write the full mix first, then split it.
- Leave headroom: four layers at full level must not clip. Export each stem from the
  same start with identical length, including reverb tails rendered in.

## 3. Writing for resequencing
- Segments end on bar lines; write **transition segments** (or stingers) between moods.
- Define **exit cues** (next bar, next beat, end of segment) per transition.
- Reverb tails: export a pre-entry/post-exit region or the "tail" so cuts are not dry.

## 4. Implementing
- **Wwise:** Music Switch Container driven by a State or Switch; Music Playlist
  Containers for sequences; Transitions matrix sets source exit point, destination
  entry and fade; Stingers attach to Triggers. RTPCs drive layer volumes.
- **FMOD Studio:** a music event with a timeline, loop regions, **transition markers**
  and transition timeline regions, and parameters (e.g. `Intensity` 0-1) automating
  track volumes. Use quantisation on transitions (bar or beat).
- Test with the game build, not only in the authoring tool.

## Gotchas
- Loop points with a non-zero-crossing or missing tail click; render loops with the tail
  wrapped to the start.
- Combat that flips on and off every few seconds needs hysteresis (minimum time in state).
- Memory budget: streamed music vs in-memory; agree format (Vorbis/Opus quality) early.

## Verify
- [ ] Every state change in the test level produces a musical transition, not a cut.
- [ ] All layer combinations are mix-tested at full gain without clipping.
- [ ] Loops are seamless over at least ten iterations.
