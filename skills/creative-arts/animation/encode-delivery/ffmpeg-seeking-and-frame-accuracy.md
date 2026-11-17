---
id: creative-arts.animation.encode-delivery.ffmpeg-seeking-and-frame-accuracy
name: ffmpeg-seeking-and-frame-accuracy
category: creative-arts
field: animation
product: encode-delivery
tags: [ffmpeg-seeking, seeking, frame-accuracy, ss, trim, stream-copy, keyframes]
level: advanced
status: verified
description: "Cut and extract frames with ffmpeg accurately: -ss before versus after -i, keyframe snapping with stream copy, -t versus -to, single-frame grabs, and verification."
sources:
  - https://ffmpeg.org/ffmpeg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Input vs output seeking and frame accuracy

## Where -ss goes
- **Input seeking** (`-ss` before `-i`): jumps near the position using the container's index, fast. With re-encoding, FFmpeg then decodes from the preceding keyframe and discards frames up to the exact time, so the cut is frame-accurate in current versions.
- **Output seeking** (`-ss` after `-i`): decodes and discards from the start, slow on long files; the result is the same accuracy but takes much longer. Use it only when you need filters that depend on earlier frames, or old behaviours.
- `-accurate_seek` is on by default; `-noaccurate_seek` disables the discard step.

## Stream copy
- With `-c copy` there is no decoding, so the cut starts at a **keyframe**: the output may begin earlier than requested (or with a few undecodable frames) when the requested start is not a keyframe. For frame-accurate cuts, re-encode, or cut at known keyframes (`gop-keyframe-placement.md`).

## Duration
- `-t 10` sets a duration; `-to 00:01:10` sets an end time. With input seeking, timestamps restart at zero after the seek, so `-to` can be misread. Prefer `-t` with input seeking, or compute the duration.

## Examples
```bash
# Accurate 5 s clip, re-encoded
ffmpeg -ss 00:01:23.000 -i in.mov -t 5 -c:v libx264 -crf 16 -c:a aac clip.mp4

# Fast clip at keyframe boundaries (no re-encode)
ffmpeg -ss 00:01:23 -i in.mov -t 5 -c copy clip.mov

# One frame as PNG
ffmpeg -ss 00:00:10 -i in.mov -frames:v 1 frame.png

# A frame by number (frame 240) with the select filter
ffmpeg -i in.mov -vf "select=eq(n\,240)" -vframes 1 frame240.png
```

## Frame numbers and timecode
- Time = frame / fps, so at 24 fps frame 240 is 10.000 s; for 23.976 use the exact rational rate (24000/1001).
- Source timecode is not used by `-ss`; it is time from the start of the file. Add the start timecode offset manually when cutting from a timecoded file.

## Gotchas
- Variable frame rate sources shift frame counting; convert to constant frame rate first (`frame-rate-conversion.md`).

## Checked
Run with FFmpeg 8.0.1 on 2026-10-18 using a synthetic clip whose red value encodes the frame number: input `-ss` and output `-ss` with re-encoding both produced a first frame equal to the requested frame (frame 50 at 25 fps, 2 s); `-ss 2 -c copy` started at the preceding keyframe (frame 0 with a 100-frame GOP); `-ss 2 -i ... -to 3` produced a 3.0 s output (the `-to` value is relative to the reset timestamps, hence the advice to use `-t`); `-noaccurate_seek` is accepted; `select=eq(n\,100)` extracted frame 100.

## Verify
- [ ] Check the first and last frame of the cut by extracting them, or with `ffprobe -show_frames`.
- [ ] Duration matches the request.
