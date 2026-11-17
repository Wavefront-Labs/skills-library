---
id: computing-software.computer-graphics-engineering.computer-vision.self-supervised-pretraining-for-vision
name: self-supervised-pretraining-for-vision
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-deep-learning, self-supervised-learning, contrastive-learning, dino, mae, domain-adaptation]
level: advanced
status: draft
description: "Use self-supervised pretraining for vision: when it pays off, SimCLR/MoCo vs DINO/iBOT vs MAE, continued domain pretraining, linear-probe and kNN evaluation."
sources: ["https://arxiv.org/abs/2002.05709", "https://arxiv.org/abs/2304.07193", "https://arxiv.org/abs/2111.06377", "https://docs.lightly.ai/self-supervised-learning/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Self-supervised and contrastive pretraining

## When it is worth it
- Many unlabelled images, few labels, and a domain far from ImageNet (medical, satellite,
  microscopy, industrial). For natural images, off-the-shelf DINOv2/CLIP weights are usually
  already better than anything you can pretrain.

## Method families
| Family | Examples | Notes |
|---|---|---|
| Contrastive | SimCLR, MoCo v3 | Needs large batch/queue and strong augmentations |
| Self-distillation | DINO, DINOv2, iBOT | Excellent frozen features, kNN-friendly |
| Masked image modelling | MAE, SimMIM | ViT-friendly, cheap per step, needs fine-tuning |

## Practical recipe
1. Start from a general checkpoint (DINOv2 or MAE ImageNet weights) and **continue pretraining** on
   domain images rather than starting from scratch: far cheaper.
2. Augmentations encode invariances: colour jitter is wrong if colour is the signal (histology
   stains need stain augmentation instead); crops must keep the object of interest.
3. Train with libraries that get details right (lightly, solo-learn, official DINOv2 repo).
4. Monitor collapse: embedding standard deviation per dimension and kNN accuracy on a small
   labelled set during training.

## Evaluation
- Linear probe and kNN accuracy on a labelled validation set (frozen features).
- Low-shot fine-tuning with 1/10 percent labels against an ImageNet-initialised baseline. Report
  both; SSL only matters if it beats the baseline here.

## Gotchas
Duplicate and near-duplicate images inflate kNN results; deduplicate (perceptual hashing or
embedding similarity) before splitting.
