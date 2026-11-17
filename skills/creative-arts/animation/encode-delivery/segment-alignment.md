---
id: creative-arts.animation.encode-delivery.segment-alignment
name: segment-alignment
category: creative-arts
field: animation
product: encode-delivery
tags: [segment-alignment, adaptive-streaming, segment-duration, keyframe-alignment, target-duration, hls, dash, cmaf, ffprobe]
level: advanced
status: docs-checked
description: "Choose segment duration and prove keyframe/segment alignment across ABR renditions so HLS/DASH players switch without stalls or jumps."
sources:
  - https://developer.apple.com/documentation/http-live-streaming/hls-authoring-specification-for-apple-devices
  - https://ffmpeg.org/ffmpeg-formats.html#hls-2
  - https://dashif.org/guidelines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Segment duration and alignment

**Goal:** every rendition's segment N covers exactly the same media time and starts with an
IDR frame, so a player can switch between renditions at any boundary.

## Choose the numbers

- Segment duration must be a whole multiple of the GOP. At 24 fps: GOP 48 (2 s), segments 6 s
  = 3 GOPs. At 23.976 fps the same frame counts give 6.006 s segments; that is fine, keep frame
  counts, not seconds, identical.
- VOD: 6 s is what Apple's HLS authoring specification recommends (target durations should be 6 seconds).
- Audio codec frames cover a fixed number of samples, so audio segment edges usually do not land exactly on video edges; packagers handle this, but it is why tiny duration differences can show between audio and video playlists.

## Encode settings that guarantee alignment

```bash
# every rung
-r 24 -g 48 -keyint_min 48 -sc_threshold 0
# or force exact times regardless of encoder decisions
-force_key_frames "expr:gte(t,n_forced*2)"
```

With scene-cut detection on (`sc_threshold` default), the encoder can add extra keyframes at different
places per rung; extra keyframes are harmless only if the GOP cadence is still enforced at the
segment boundaries. Disabling it is simplest.

## Check alignment

```bash
for f in v1080.mp4 v720.mp4 v480.mp4; do
  ffprobe -v error -select_streams v:0 -skip_frame nokey -show_entries frame=pts_time -of csv=p=0 $f | md5sum
done
```
Identical hashes = identical keyframe timelines. For packaged HLS, compare the `#EXTINF`
durations between variant playlists: they should match line for line.

## Failure symptoms

| Symptom | Likely cause |
|---|---|
| Picture jumps back or forward at a quality switch | segment boundaries differ between rungs |
| Stall at switch, then resume | segment does not start with an IDR (open GOP) |
| Playlist `#EXT-X-TARGETDURATION` larger than expected | a long GOP made one segment overrun |

## Verify

Play with a network throttle that forces repeated up and down switches through an action
sequence; watch for jumps and listen for audio glitches at switch points.

## Checked

2026-10-28. Confirmed: Apple HLS authoring specification (target durations should be 6 seconds; segment durations nominally 6 seconds, 6.006 s for 29.97); RFC 8216 `#EXTINF` and `#EXT-X-TARGETDURATION`; ffmpeg `-force_key_frames expr:` with `n_forced`, `sc_threshold`. Removed: the AAC 1024-sample and 21.33 ms figures, the low-latency 1-2 s statement, the x264-specific scene-cut wording.

Method: documentation only; no commands were run.
