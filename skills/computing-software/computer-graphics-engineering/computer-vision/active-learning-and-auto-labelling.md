---
id: computing-software.computer-graphics-engineering.computer-vision.active-learning-and-auto-labelling
name: active-learning-and-auto-labelling
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-data-evaluation, active-learning, auto-labeling, pre-labeling, uncertainty-sampling, annotation]
level: practitioner
status: draft
description: "Cut labelling cost: model-assisted pre-labelling in CVAT/Label Studio, uncertainty and diversity sampling, auto-labelling with foundation models, and QA loops for model labels."
sources: ["https://docs.cvat.ai/docs/annotation/auto-annotation/", "https://labelstud.io/guide/ml", "https://docs.voxel51.com/", "https://arxiv.org/abs/1708.00489"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Active learning and auto-labelling

## Pre-labelling (biggest win)
Run the current model (or a foundation model: Grounding DINO/OWLv2 for boxes, SAM 2 for masks) on
unlabelled data, import predictions as editable annotations, and let annotators correct them.
Correction is typically 3 to 10x faster than drawing from scratch.
- CVAT: serverless functions (Nuclio) or "auto annotation" with your model.
- Label Studio: ML backend serving predictions per task.

## Selecting what to label
| Strategy | Signal |
|---|---|
| Uncertainty | Low max-prob, small margin, high entropy; for detection, mean/min box confidence near threshold |
| Disagreement | Ensembles / MC dropout / TTA variance |
| Diversity | Core-set (k-centre on embeddings), clustering, dedup |
| Error-driven | Slices where the model fails (from error analysis) |
Combine: take uncertain samples, then pick diverse ones among them to avoid near-duplicates.

## Loop
1. Label a random seed set (also keep a random **test set** that active learning never touches).
2. Train, predict on the pool, select a batch (a few hundred to few thousand), label, retrain.
3. Stop when validation metric gains per batch flatten.

## Auto-labelling without review
Only accept model labels above a high confidence where measured precision on an audit sample is
sufficient; audit a random slice every round. Label noise from auto-labels compounds over iterations.

## Gotchas
- Pure uncertainty sampling picks outliers and garbage frames: filter blurred/corrupt images first.
- Video: sample frames sparsely (scene change detection) to avoid duplicates.

## Verify
Plot metric vs number of labelled images for active selection vs random selection on the same
budget: active learning should reach the same accuracy with fewer labels.
