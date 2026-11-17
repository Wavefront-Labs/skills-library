---
id: creative-arts.animation.encode-delivery.frame-rate-conversion
name: frame-rate-conversion
category: creative-arts
field: animation
product: encode-delivery
tags: [frame-rate-conversion, image-sequence, 23-976, 24fps, 25fps, 29-97, pulldown, telecine, minterpolate, fps-filter, setpts, ffmpeg, audio-speed]
level: advanced
status: verified
description: "Convert animation between 24, 23.976, 25 and 29.97/30 fps without judder or drift: retime vs speed-change, 2:3 pulldown, PAL speed-up, audio handling."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html#fps-1
  - https://ffmpeg.org/ffmpeg-filters.html#telecine
  - https://ffmpeg.org/ffmpeg-filters.html#atempo
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Frame rate conversion

**Goal:** deliver at a different rate without stutter, dropped key poses or audio drift.
Animation is unforgiving: dropping one drawing of a 2s hold is invisible, dropping a contact
frame of a walk is not. Prefer methods that keep every frame.

## Decide the method

| From to | Method | Keeps every frame? |
|---|---|---|
| 24 to 23.976 | re-stamp (0.1% slow), audio resampled | yes |
| 24/23.976 to 25 (PAL) | speed-up 4.1%, audio pitch-corrected or not | yes |
| 23.976 to 29.97 | 2:3 pulldown (telecine) or 3:2 cadence in progressive | yes (repeated fields) |
| 24 to 30 progressive | duplicate every 4th frame (`fps=30`) | yes, slight judder |
| any to any | motion interpolation (`minterpolate`) | no, invents frames; avoid for drawn animation |

## Commands

Re-stamp 24 to 23.976 (same frames, 1000/1001 slower):
```bash
ffmpeg -i in24.mov -vf "setpts=PTS*1001/1000" -r 24000/1001 \
  -af "asetrate=48000*1000/1001,aresample=48000" -c:v prores_ks -profile:v 3 -c:a pcm_s24le out23976.mov
```
For image sequences just reinterpret: `-framerate 24000/1001 -i f_%04d.png`.

PAL speed-up 24 to 25 with pitch kept:
```bash
ffmpeg -i in24.mov -vf "setpts=PTS*24/25" -r 25 -af "atempo=25/24" out25.mov
```
Without `atempo` the audio must be resampled to the new length (`asetrate=48000*25/24,aresample=48000`),
which raises pitch by the same 25/24 ratio (about 0.7 semitone); whether that is acceptable is a delivery-spec question.

2:3 pulldown 23.976p to 29.97i:
```bash
ffmpeg -i in23976.mov -vf "telecine=pattern=23" -flags +ilme+ildct -c:v prores_ks out2997i.mov
```

Simple 24 to 30 frame duplication: `-vf fps=30`.

## Gotchas

- `-r` as an output option asks ffmpeg to conform the frame rate, and the result depends on the sync mode. Measured with ffmpeg 8.0.1 on a 60 s 24 fps MP4: `-r 24000/1001` kept all 1440 frames and stretched the clip to 60.06 s, so it behaves like a re-stamp here but does not touch audio. Do not rely on it for 24 to 23.976: use `setpts` plus `asetrate` as above and compare audio and video durations and the frame count.
- Timecode changes with rate; regenerate it for the new rate.
- Always render animation at the delivery rate when possible; conversion is the fallback.

## Verify

```bash
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=r_frame_rate,nb_read_frames,duration -of default=nw=1 out.mov
```

Frame count equals the source for re-stamp/speed methods; audio and video durations agree to
within one frame.

## Checked

2026-10-28. Confirmed in the ffmpeg-filters manual: `telecine` `pattern` default 23, `fps`, `atempo`, `asetrate`, `setpts`, `minterpolate` exist; codec flags `ilme` and `ildct`; ffprobe `-count_frames` and `nb_read_frames` (ffprobe schema). Ratios are arithmetic: 1000/1001 (0.1%), 25/24 (4.1%, 0.7 semitone), one dropped frame about every 41 s. Removed: the non-drop timecode statement and the broadcaster/music-supervisor acceptance claim.

2026-11-01 run check on a 5 s 24 fps source with audio: the re-stamp command gave 120 frames at 24000/1001 (5.005 s video, 5.005 s audio); the PAL command gave 120 frames at 25 fps (4.8 s) and `atempo=25/24` accepted the fraction; `telecine=pattern=23` gave 150 frames at 30000/1001 with `-flags +ilme+ildct`; `fps=30` gave 150 frames; image-sequence `-framerate 24000/1001` ran. 12 x log2(25/24) = 0.71 semitone, 1000/1001 = 0.1%.

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the ffmpeg manuals for the options above.
