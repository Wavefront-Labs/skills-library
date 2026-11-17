---
id: creative-arts.animation.encode-delivery.abr-ladder-design
name: abr-ladder-design
category: creative-arts
field: animation
product: encode-delivery
tags: [abr-ladder, adaptive-streaming, bitrate-ladder, per-title-encoding, convex-hull, vmaf, renditions, streaming]
level: advanced
status: draft
description: "Design an adaptive bitrate ladder for animation: rung resolutions and bitrates, per-title tuning with VMAF, and aligning segments so players switch cleanly."
sources:
  - https://netflixtechblog.com/per-title-encode-optimization-7e99442b62a2
  - https://developer.apple.com/documentation/http-live-streaming/hls-authoring-specification-for-apple-devices
  - https://github.com/Netflix/vmaf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ABR ladder design

**Goal:** the fewest renditions that give every viewer the best picture their bandwidth allows.
Animation is easy content: flat colour and holds compress far better than live action, so a
generic ladder wastes bandwidth on top rungs.

## Starting ladder (H.264, 24 fps, from Apple's authoring spec scale)

| Rung | Resolution | Video kbps (generic) | Animation, flat style |
|---|---|---|---|
| 1 | 416x234 | 145 | 120 |
| 2 | 640x360 | 365 | 300 |
| 3 | 768x432 | 730 | 550 |
| 4 | 960x540 | 2000 | 1200 |
| 5 | 1280x720 | 3000 | 2000 |
| 6 | 1920x1080 | 6000 | 3500-4500 |

Adjacent rungs should differ by about 1.5-2x in bitrate; too-close rungs waste encode time,
too-far rungs cause visible quality jumps.

## Per-title tuning (the Netflix convex hull idea, simplified)

1. Encode a representative 2-3 minute excerpt at each resolution across a range of bitrates
   (or CRFs).
2. Score each against the source upscaled to display size with VMAF
   (`creative-arts.animation.encode-delivery.vmaf-scoring`).
3. For each bitrate, keep the resolution with the highest VMAF; that envelope is the hull.
4. Pick rungs along the hull at roughly equal VMAF steps (e.g. 60, 70, 80, 88, 93, 96) and cap
   the top at the bitrate where VMAF stops rising (often 93-96 for animation).

## Alignment rules (non-negotiable)

- Same frame rate on every rung (do not drop to 12 fps low rungs for 24 fps animation unless
  the player is known to handle it).
- Identical GOP and keyframe positions (`-g`, `-keyint_min`, `-sc_threshold 0`, or forced
  keyframes) and identical segment duration, so segment N starts at the same time everywhere.
- Audio: one or two shared audio renditions (e.g. AAC 128k stereo, 64k for the low rungs).

## Gotchas

- Upscaled 1080p is not worth shipping if the source is 720p renders.
- Line art at very low resolutions aliases: use `scale=...:flags=lanczos` and consider a
  slight blur before downscale for the bottom rungs.
- Set `BANDWIDTH` from measured peak (VBV maxrate), not the average.

## Verify

Plot VMAF against bitrate for the chosen rungs; it should rise monotonically. Then confirm
alignment: keyframe timestamps listed per rung (`ffprobe -skip_frame nokey ...`) are identical.
