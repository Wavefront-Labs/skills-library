---
id: computing-software.computer-graphics-engineering.computer-vision.visual-place-recognition
name: visual-place-recognition
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, sfm-slam, place-recognition, loop-closure, netvlad, dbow2, visual-localization]
level: advanced
status: draft
description: "Recognise previously visited places for loop closure and localisation: DBoW2, NetVLAD, MixVPR/SALAD/AnyLoc global descriptors, hloc pipelines, and recall@N evaluation."
sources: ["https://github.com/dorian3d/DBoW2", "https://github.com/cvg/Hierarchical-Localization", "https://arxiv.org/abs/1511.07247", "https://github.com/gmberton/VPR-methods-evaluation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Visual place recognition

Retrieval problem: given a query image, find database images of the same place despite viewpoint,
lighting, season and dynamic objects.

## Approaches
| Approach | Use |
|---|---|
| BoW on binary features (DBoW2/3) | ORB-SLAM loop closure, embedded, fast |
| NetVLAD | Classic learned global descriptor |
| MixVPR, EigenPlaces, SALAD, BoQ | Current strong global descriptors |
| AnyLoc (DINOv2 + VLAD) | Zero-shot across domains (underwater, aerial, indoor) |

## Two-stage pipeline (hloc)
```bash
python -m hloc.extract_features --conf netvlad ...     # global descriptors
python -m hloc.pairs_from_retrieval --num_matched 20 ...
python -m hloc.extract_features --conf superpoint_aachen ...
python -m hloc.match_features --conf superglue ...     # or lightglue
python -m hloc.localize_sfm ...                         # PnP against SfM model
```
Global retrieval for top-K candidates, then local feature matching + geometric verification
(RANSAC on F/H or PnP). Verification is essential: retrieval alone produces false positives
in repetitive environments (corridors, parking garages).

## SLAM loop closure specifics
- Exclude recent frames (temporal window) from candidates.
- Require temporal consistency (consecutive keyframes agreeing) before accepting a loop.
- Feed accepted loops into pose-graph optimisation with robust kernels.

## Evaluation
Recall@1/5/10 with a distance threshold (e.g. 25 m for city-scale); precision-recall for loop
closure (precision must be near 100 percent).

## Gotchas
Database and query from different cameras/FOV need descriptor robustness; resize consistently.
