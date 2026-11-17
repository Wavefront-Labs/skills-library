---
id: creative-arts.animation.encode-delivery.gop-keyframe-placement
name: gop-keyframe-placement
category: creative-arts
field: animation
product: encode-delivery
tags: [gop, rate-control, keyframes, keyint, idr, scene-cut, b-frames, closed-gop, force-key-frames, ffmpeg, libx264]
level: advanced
status: verified
description: "Control GOP length and keyframe placement in ffmpeg: -g, keyint_min, sc_threshold, closed GOP, forced keyframes at shot cuts or segment boundaries."
sources:
  - https://ffmpeg.org/ffmpeg.html#Advanced-Video-options
  - https://ffmpeg.org/ffmpeg-codecs.html#libx264_002c-libx264rgb
  - https://developer.apple.com/documentation/http-live-streaming/hls-authoring-specification-for-apple-devices
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# GOP length and keyframe placement

**Goal:** keyframes where you need them: at regular intervals for seeking and streaming
segments, at shot cuts for quality, and at exact timecodes for chapter marks or editorial
handoff. A GOP (group of pictures) runs from one keyframe (I/IDR frame) to the next.

## Knobs

| Option | Effect |
|---|---|
| `-g 48` | maximum GOP length in frames (2 s at 24 fps) |
| `-keyint_min 48` | minimum distance between keyframes |
| `-sc_threshold 0` | disable extra keyframes on scene cuts (fixed cadence) |
| `-flags +cgop` | closed GOP: no frame refers across a keyframe (the manual describes `-cgop` as disabling closed GOP and enabling open GOP) |
| `-force_key_frames expr` | put IDR frames at chosen times |

## Recipes

Review/web master (seek every ~2 s, keyframes also at cuts):
```bash
ffmpeg -i in.mov -c:v libx264 -crf 18 -g 48 -keyint_min 24 out.mp4
```

Streaming rendition (fixed cadence, identical across all ladder rungs):
```bash
ffmpeg -i in.mov -c:v libx264 -crf 21 -maxrate 5M -bufsize 10M \
  -g 48 -keyint_min 48 -sc_threshold 0 out_1080.mp4
```
Every rendition in an ABR ladder must use the same frame rate and GOP so segments line up.

Forced keyframes at shot boundaries from an EDL or shotlist (seconds):
```bash
ffmpeg -i ep.mov -c:v libx264 -crf 18 -force_key_frames 0,4.25,9.5,17.0 out.mp4
# or periodic: -force_key_frames "expr:gte(t,n_forced*2)"
```

Editing-friendly intermediate: intra-only (every frame a keyframe), use ProRes/DNxHR rather than
`-g 1` H.264.

## Gotchas

- Long GOPs compress static animation well but make scrubbing and seeking sluggish.
- A cut that lands mid-GOP in a stream-copy (`-c copy`) trim starts on a non-keyframe: black or
  smeared frames until the next keyframe. Cut on keyframes or re-encode.
- Open GOP (`-flags -cgop`) can break segmenters and splicers; leave it off for delivery.

## Verify

```bash
ffprobe -v error -select_streams v:0 -skip_frame nokey -show_entries frame=pts_time -of csv=p=0 out.mp4 | head
```

Lists keyframe timestamps only: check the spacing matches `-g` / your forced times.

## Checked

2026-10-28. Confirmed: `-g`, `keyint_min`, `sc_threshold` (scenecut) and `-flags` closed/open GOP in ffmpeg-codecs; `-force_key_frames` with `expr:` and `n_forced` in the ffmpeg manual; `skip_frame` value `nokey`. Removed: `-bf 3`, the x264 default-closed-GOP statement, the open-GOP percentage saving, the platform chapter/thumbnail seek claim.

2026-11-01 run check on a 10 s 24 fps clip: `-g 48` gave keyframes at 0, 2, 4, 6, 8 s (the `-skip_frame nokey` listing from the Verify section); `-force_key_frames 0,4.25,9.5,17.0` gave keyframes at 0, 4.25 and 9.5 s (17.0 is past the end of the clip); `expr:gte(t,n_forced*2)` gave every 2 s; `-flags +cgop`, `-flags -cgop`, `-sc_threshold 0` and the maxrate/bufsize recipe all ran.

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the ffmpeg manuals for the options above.
