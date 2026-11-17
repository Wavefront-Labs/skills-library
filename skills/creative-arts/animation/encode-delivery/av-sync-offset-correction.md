---
id: creative-arts.animation.encode-delivery.av-sync-offset-correction
name: av-sync-offset-correction
category: creative-arts
field: animation
product: encode-delivery
tags: [av-sync, audio-mux, muxing, itsoffset, adelay, sync-offset, lip-sync-drift, ffmpeg, start-time]
level: advanced
status: verified
description: "Measure and correct audio/video sync offsets and drift in muxed files: 2-pop checks, -itsoffset, adelay/atrim, start_time and edit-list problems."
sources:
  - https://ffmpeg.org/ffmpeg.html#Main-options
  - https://ffmpeg.org/ffmpeg-filters.html#adelay
  - https://ffmpeg.org/ffmpeg-formats.html#mov_002c-mp4_002c-ismv
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# A/V sync offsets and drift

**Goal:** dialogue lands on the mouth shapes in every deliverable. Distinguish two faults:
- **Constant offset**: audio early or late by the same amount everywhere. Fix by shifting.
- **Drift**: in sync at the start, off by the end. Caused by a rate mismatch (23.976 vs 24,
  44.1k vs 48k). Fix the rate, not the offset.

## Measure

1. Use the 2-pop (a 1-frame tone two seconds before first frame of action, aligned with a
   single white frame on the leader). Find the audio peak and the video flash:
```bash
ffmpeg -i ep.mov -af "silencedetect=n=-40dB:d=0.02" -vn -f null - 2>&1 | grep silence_end | head -2
ffmpeg -i ep.mov -vf "blackdetect=d=0:pix_th=0.1" -an -f null - 2>&1 | grep black_end | head -2
```
2. Compare start times the container claims:
```bash
ffprobe -v error -show_entries stream=index,codec_type,start_time,duration -of compact ep.mov
```
A non-zero audio `start_time` (for example from codec priming or an edit list) is a common
hidden offset.

## Shift without re-encoding video

Audio late by 3 frames at 24 fps (0.125 s) - move audio earlier:
```bash
ffmpeg -i ep.mov -itsoffset -0.125 -i ep.mov -map 0:v -map 1:a -c copy fixed.mov
```
Audio early - delay it:
```bash
ffmpeg -i ep.mov -af "adelay=125:all=1" -c:v copy -c:a pcm_s24le fixed.mov
```

## Drift

Duration ratio tells you: video 1320.0 s, audio 1321.32 s = ratio 1.001 = a 23.976/24 mismatch.
Conform the audio rate (`asetrate`/`aresample`, see
`creative-arts.animation.encode-delivery.frame-rate-conversion`), do not slice in offsets.

## Gotchas

- MP4 edit lists: players may treat them differently, so a file "in sync" in one player can be
  off in another. Re-muxing without an edit list (`-use_editlist 0`, a mov/mp4 muxer option) can give consistent results.
- Variable frame rate video drifts against constant audio; re-encode to CFR first.
- Animation lip sync is judged harshly; aim for zero offset.

## Verify

Re-measure the 2-pop: flash frame and pop within the same frame. Spot-check a hard consonant
(b, p, m closure) mid-episode and in the final minute.

## Checked

2026-10-28. Confirmed in the ffmpeg manuals: `adelay` (`delays` in milliseconds, `all`), `silencedetect`, `blackdetect`, `-itsoffset` input option, `use_editlist` mov/mp4 muxer option. The 3-frame example is 3/24 = 0.125 s. Removed: the 0.021 s priming figure, `-avoid_negative_ts make_zero` (value not found in the fetched manual), and the BT.1359 45 ms / 125 ms thresholds (standard not readable).

2026-11-01 run check: `silencedetect` printed `silence_end` after a 2 s silent lead and `blackdetect` printed `black_end` after 2 s of black on a synthetic file; the `ffprobe` start_time/duration query ran; `-itsoffset -0.125` with a second input left video 5.000 s and shortened audio to 4.875 s; `adelay=125:all=1` lengthened audio to 5.125 s; `-use_editlist 0` worked as an output option after `-i` (it is rejected as an input option).

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the ffmpeg manuals for the options above.
