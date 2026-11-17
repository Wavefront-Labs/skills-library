---
id: computing-software.computer-graphics-engineering.computer-vision.optical-flow-and-motion-estimation
name: optical-flow-and-motion-estimation
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-vision, optical-flow, motion-estimation, lucas-kanade, klt, farneback, raft, dense-flow, sparse-flow, motion-vectors, video-codec, pyramid, aperture-problem]
level: advanced
status: gated
description: "Choose and tune sparse (Lucas-Kanade/KLT) vs dense (Farneback, RAFT) optical flow, and avoid the aperture-problem, occlusion and large-motion pitfalls that break it."
sources: ["https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html", "https://arxiv.org/abs/2003.12039"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optical flow and motion estimation

**Goal:** estimate per-pixel or per-feature 2D motion between frames correctly —
picking sparse vs dense, handling the cases where brightness-constancy breaks, and
knowing when flow is lying to you.

## The core assumption (and when it breaks)
Optical flow assumes **brightness constancy**: a point's intensity doesn't change
between frames, only its position. This breaks under:
- Specular highlights / reflections moving independently of the surface.
- Lighting changes, shadows sweeping across the scene.
- Large, fast motion where the linearised (Taylor-expansion) flow equation no longer
  holds — solved by image pyramids (coarse-to-fine), not by the base algorithm.
- **The aperture problem**: a small patch with motion only along an edge (e.g. a
  diagonal line) cannot distinguish component motion along the edge — only the
  perpendicular component is observable. Corners/textured regions resolve it;
  featureless or 1D-structured regions don't.

## Sparse: Lucas-Kanade / KLT
```python
pts1 = cv2.goodFeaturesToTrack(gray0, maxCorners=200, qualityLevel=0.01, minDistance=7)
pts2, status, err = cv2.calcOpticalFlowPyrLK(gray0, gray1, pts1, None,
                     winSize=(21,21), maxLevel=3,
                     criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT, 30, 0.01))
good1, good2 = pts1[status==1], pts2[status==1]
```
- Track good **corner** features (`goodFeaturesToTrack`, Shi-Tomasi) — flat regions
  give an ill-conditioned normal-equations matrix and unreliable flow.
- `maxLevel` sets pyramid depth: each level doubles the motion range it can track.
  Fast motion with `maxLevel=0` silently fails (no error — just wrong vectors). Tested on a
  photo shifted horizontally with 200 Shi-Tomasi corners and `winSize=(21,21)`: at a 30 px shift
  `maxLevel=0` returned status 1 for 178 points of which only 13% were within 1 px of the truth
  (0.41 correct at level 1, 0.91 at level 2, 0.98 at level 3); at 12 px level 0 gave 0.63 and
  level 2 0.98; at 4 px every level gave 0.97 or better.
- Drop/re-detect tracked points periodically; points drift off features over many
  frames (`err` output flags bad tracks — filter on it, don't ignore it: in the 30 px, level-0 test the
  wrong tracks had median `err` 46.9 against 0.0 for the correct ones).

## Dense: Farneback / RAFT
- `cv2.calcOpticalFlowFarneback` — classical, fast, CPU-friendly, polynomial expansion.
  Good for coarse motion fields (e.g. motion blur direction, rough scene flow) but
  blurs sharp motion boundaries.
- **RAFT** and other learned dense-flow networks (torchvision, or ONNX export) give
  far sharper boundaries and handle larger displacements, at GPU inference cost (gated: unconfirmed, source is paywalled or blocked). Not run here (no GPU, no model weights downloaded).
- Dense flow at object boundaries is inherently ambiguous (foreground/background
  disagree) — don't trust flow magnitude right at silhouette edges.

## Occlusion and validity
- A point visible in frame 1 but occluded in frame 2 has **no correct flow vector**
  — any algorithm still outputs *something*. Use forward-backward consistency
  (compute flow A→B and B→A, warp B→A by A→B and add; large residual = unreliable/occluded) to
  mask it out. Tested with Farneback on a textured square moving 20 px over a textured
  background: mean residual 0.39 px in the uncovered strip and 0.35 px in the newly covered strip
  against 6e-6 px in the static background.
- Flow at image borders is unreliable (nothing to match against outside frame) —
  mask a border margin before using flow for anything downstream (stabilisation,
  frame interpolation).

## Verify
- [ ] Forward-backward consistency check run and large-error pixels/points masked
      before downstream use.
- [ ] Pyramid levels sufficient for the actual motion magnitude observed (measure
      max pixel displacement, pick `maxLevel` so the reach covers it; measured reach with a
      21 px window was roughly `winSize/2 * 2^maxLevel`, not `winSize * 2^maxLevel`: a 30 px
      shift needed level 3, not level 1).
- [ ] Flow visualised (HSV wheel: hue=direction, value=magnitude) and sanity-checked
      against known camera/object motion before trusting it numerically.
- [ ] Sparse tracks re-seeded periodically rather than tracked indefinitely.
