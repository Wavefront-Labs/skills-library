---
id: computing-software.computer-graphics-engineering.computer-vision.long-term-point-tracking
name: long-term-point-tracking
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, motion-estimation, point-tracking, cotracker, tapir, video-tracking, tap-vid]
level: advanced
status: draft
description: "Track arbitrary points through long videos with CoTracker, TAPIR/BootsTAPIR: query formats, occlusion/visibility outputs, grid vs sparse queries, memory limits and evaluation."
sources: ["https://github.com/facebookresearch/co-tracker", "https://github.com/google-deepmind/tapnet", "https://arxiv.org/abs/2307.07635"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Long-term point tracking (CoTracker)

Optical flow links adjacent frames and drifts; Lucas-Kanade loses points on occlusion. Track-any-point
(TAP) models output per-point trajectories plus **visibility** over the whole clip.

## CoTracker
```python
import torch
cotracker = torch.hub.load("facebookresearch/co-tracker", "cotracker3_offline").cuda()
video = torch.from_numpy(frames).permute(0, 3, 1, 2)[None].float().cuda()   # B,T,C,H,W in 0..255
queries = torch.tensor([[0., 400., 350.], [10., 600., 500.]]).cuda()[None]  # (t, x, y)
tracks, vis = cotracker(video, queries=queries)          # tracks B,T,N,2 ; vis B,T,N
# or a grid: cotracker(video, grid_size=30)
```
- Online variant (`cotracker3_online`) processes sliding windows for streaming.
- Joint tracking of many points improves each track (points support each other); add a sparse grid
  of support points even when you care about a few.
- Memory grows with T x H x W: downscale to the training resolution (about 384x512) and chunk long
  videos.

## TAPIR / BootsTAPIR (tapnet)
Per-point matching + refinement; strong occlusion handling, online variant for robotics.

## Uses
Video editing (sticker/tattoo attachment), deformable object tracking, robotics manipulation
keypoints, 4D reconstruction initialisation, motion analysis in biology/sports.

## Evaluation
TAP-Vid metrics: average Jaccard (AJ), position accuracy (fraction within 1 to 16 px thresholds),
occlusion accuracy. On your data, label a few trajectories by hand at keyframes.

## Gotchas
- Queries are (frame index, x, y) in pixel coordinates of the input resolution.
- Visibility is a prediction: threshold it, and do not use positions while invisible for
  measurement.
