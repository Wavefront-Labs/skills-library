---
id: creative-arts.animation.sound-design.pull-up-pull-down
name: pull-up-pull-down
category: creative-arts
field: animation
product: sound-design
tags: [pull-down, audio-sync, pull-up, 0-1-percent, 23-976, 25fps-speedup, pal-speedup, pitch-correction, timecode, audio-drift]
level: advanced
status: draft
description: "Keep audio in sync when picture frame rates change: 0.1% pull-down/up between 24 and 23.976, 4% PAL speed-up to 25, and pitch-corrected vs uncorrected versions."
sources:
  - https://sox.sourceforge.net/sox.html
  - https://ffmpeg.org/ffmpeg-filters.html#atempo
  - https://www.avid.com/learn-and-support
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pull-up and pull-down

**Goal:** audio stays in sync after picture changes speed for a different frame rate, without surprise pitch
changes that music and dialogue supervisors notice.

## The common cases

| Picture change | Speed ratio | Audio operation |
|---|---|---|
| 24 to 23.976 | x 1000/1001 (0.1% slower) | pull-down: resample/varispeed by 0.999 |
| 23.976 to 24 | x 1001/1000 | pull-up |
| 24 to 25 (PAL) | x 25/24 (4.17% faster) | speed-up; pitch rises ~0.7 semitone unless corrected |
| 23.976 to 25 | x 25025/24000 | same as above, with the 0.1% |

## Commands

0.1% pull-down (no pitch correction; 0.1% is inaudible, about 1.7 cents):
```bash
sox in.wav out.wav speed 0.999000999    # 1000/1001; changes duration and pitch together
ffmpeg -i in.wav -af "asetrate=48000*1000/1001,aresample=48000" out.wav
```
PAL speed-up, pitch-corrected:
```bash
ffmpeg -i mix24.wav -af "atempo=25/24" mix25.wav            # duration shorter, pitch kept
```
PAL speed-up, natural (pitch rises):
```bash
ffmpeg -i mix24.wav -af "asetrate=48000*25/24,aresample=48000" mix25_natural.wav
```

## Choosing pitch correction

- Broadcasters accept both; music with sustained tones sounds noticeably sharp at +4% uncorrected, and
  time-stretch processing can add artefacts on transients. Decide per show and document it; render both for
  the music supervisor to approve on the first episode.
- 0.1% changes: no correction needed.

## Timecode

After a speed change, timecode at the new rate is regenerated; a 22:00:00 programme at 24 becomes 21:07:12 at
25 (speed-up). Re-spot any TC-based cue lists.

## Gotchas

- Doing pull-down twice (once in the DAW, once in the NLE) is the classic drift bug; one owner per conversion.
- Varispeed in a DAW at session level vs per-file: know which the session uses.

## Verify

Lay the converted mix against the converted picture: 2-pop and last sync point (a hard consonant near the end)
both line up within a frame.
