---
id: computing-software.computer-graphics-engineering.computer-vision.few-shot-and-fine-grained-recognition
name: few-shot-and-fine-grained-recognition
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, recognition, few-shot-recognition, fine-grained-recognition, clip, dinov2, metric-learning]
level: advanced
status: draft
description: "Recognise fine-grained or rare classes from few examples: CLIP/DINOv2 embeddings with prototypes or kNN, linear probes, metric learning, high-res crops and open-set rejection."
sources: ["https://github.com/openai/CLIP", "https://github.com/facebookresearch/dinov2", "https://arxiv.org/abs/1703.05175"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fine-grained recognition and few-shot

## Embedding + prototypes (start here)
```python
feats = normalize(backbone(images))                  # DINOv2 CLS or CLIP image embeddings
protos = {c: normalize(feats[labels == c].mean(0)) for c in classes}
pred = max(protos, key=lambda c: q @ protos[c])     # cosine similarity
```
- DINOv2 features are best for visual similarity (species, parts, products); CLIP adds zero-shot
  text prompts ("a photo of a {class}, a type of bird").
- With 5 to 50 examples per class, a logistic-regression **linear probe** on frozen features usually
  beats prototypes; with more data, fine-tune.
- kNN over all support embeddings handles multi-modal classes (front/back views) better than a
  single mean.

## Fine-grained specifics
- Differences are small and local: use higher input resolution (448 to 518 px) or crop the object
  first (detector), then classify.
- Augmentations must not destroy the discriminative cue (colour jitter for colour-defined classes,
  flips for handedness).
- Metric learning losses (ArcFace, supervised contrastive) when fine-tuning on many identities
  (re-identification, product SKUs).

## Open-set
New items not in the gallery must be rejected: threshold the top similarity (and the margin over the
second) chosen on a validation set containing unknowns.

## Gallery management
Store embeddings in a vector index (FAISS); adding a class = adding embeddings, no retraining.
Re-embed everything if the backbone changes.

## Verify
N-way K-shot episodes on held-out classes (e.g. 5-way 5-shot accuracy), and open-set AUROC.
