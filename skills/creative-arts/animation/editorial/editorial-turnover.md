---
id: creative-arts.animation.editorial.editorial-turnover
name: editorial-turnover
category: creative-arts
field: animation
product: editorial
tags: [editorial-turnover, editorial-department, editorial-workflow, turnover-package, layout-handoff, reference-movie, audio-stems, shot-reference]
level: practitioner
status: draft
description: "Prepare editorial turnover packages for layout and animation: per-shot reference movies, audio, frame ranges, notes and naming, so departments start from the cut."
sources:
  - https://ffmpeg.org/ffmpeg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editorial turnover

**Goal:** each downstream artist receives exactly what the cut needs from their shot: timing, audio, framing
intent and notes, without opening the edit.

## Package per shot

| Item | Detail |
|---|---|
| Reference movie | board/animatic for the shot with handles, burn-ins (shot, frame, timecode) |
| Audio | dialogue (and scratch music/SFX if relevant) for the shot range plus handles, WAV 48k 24-bit |
| Context movie | the shot with 2-3 shots either side, so animators see what cuts in and out |
| Frame range | work range (e.g. 1001-1096) and cut range |
| Notes | director's notes from story/editorial, camera intent, continuity points |
| Data | shot entry in the tracker/shot list, EDL/OTIO fragment |

## Making it (ffmpeg, from the locked reel)

```bash
# shot sq020_sh010: cut in at 133.1667 s, 80 frames, 8-frame handles at 24 fps
ffmpeg -ss 132.8333 -i ep104_reel.mov -frames:v 96 -c:v prores_ks -profile:v 0 \
  -vf "drawtext=fontfile=<FONT>:text='sq020_sh010  %{frame_num}':start_number=1001:x=20:y=20:fontcolor=white:box=1:boxcolor=black@0.5" \
  -c:a pcm_s24le turnover/sq020_sh010/sq020_sh010_ref.mov
```
Generate all shots by looping over the shot breakdown CSV. Put the same script in the pipeline so the next
turnover (after recuts) reproduces exactly.

## Process

1. Lock (or partial lock) a sequence; editorial publishes the turnover in one batch, versioned
   (`turnover_v003`).
2. Notify departments via the tracker; tasks link to the package.
3. Any later change goes out as a change list with updated packages for affected shots only.

## Gotchas

- Seeking: put `-ss` before `-i` for speed, but verify frame accuracy on intra-frame sources (ProRes) or
  re-encode; long-GOP sources can start on the wrong frame.
- Frame numbering burn-in must match the work range (1001 start), not the edit timecode, or animators
  misread timings.
- Audio with handles shifts dialogue relative to frame 1001; note the offset in the package.

## Verify

Open a random shot package: frame 1001 + head handle equals the first frame of the cut, dialogue syncs with
the board, and the context movie shows neighbouring shots.
