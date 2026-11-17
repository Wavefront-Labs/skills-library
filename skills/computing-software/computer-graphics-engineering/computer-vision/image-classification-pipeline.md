---
id: computing-software.computer-graphics-engineering.computer-vision.image-classification-pipeline
name: image-classification-pipeline
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, recognition, image-classification, timm, torchvision, class-imbalance, calibration]
level: practitioner
status: draft
description: "Build an image classifier end to end: label set and data audit, pretrained backbone choice with timm/torchvision, augmentation, imbalance, calibration and per-class metrics."
sources: ["https://huggingface.co/docs/timm/index", "https://pytorch.org/vision/stable/models.html", "https://arxiv.org/abs/1706.04599"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Image classification

## 1. Define the task
- Single-label (softmax) vs multi-label (sigmoid per class, BCE loss). Do not force multi-label
  problems into softmax.
- Write labelling guidelines with edge cases; measure label agreement on a sample (two annotators).

## 2. Backbone
```python
import timm
model = timm.create_model("convnext_tiny.fb_in22k", pretrained=True, num_classes=len(classes))
cfg = timm.data.resolve_data_config({}, model=model)        # correct mean/std/size
tf_train = timm.data.create_transform(**cfg, is_training=True, auto_augment="rand-m9-mstd0.5")
```
Small data: start from strong pretrained weights (ConvNeXt, EfficientNetV2, ViT/DINOv2 features
with a linear head). Edge: MobileNetV3/EfficientNet-Lite.

## 3. Train
- AdamW, lr about 1e-4 to 5e-4 for fine-tuning, cosine schedule with warm-up, label smoothing 0.1,
  mixed precision.
- Imbalance: class-balanced sampling or loss weights; report macro metrics.
- Augmentations matched to the domain (no horizontal flips for text/digits/left-right classes).

## 4. Evaluate
- Per-class precision/recall, confusion matrix, macro-F1; top-1/top-5 only for many classes.
- Calibration: reliability diagram, ECE; fix with temperature scaling on a validation set.
- Check splits for leakage (same object/patient/session across splits).

## 5. Deploy
- Preprocessing must match training exactly (resize mode, crop, mean/std, RGB order).
- Threshold/abstain: low max-probability -> "unknown"/human review.

## Verify
Hold-out test set untouched until the end; error analysis on the top confused pairs before
collecting more data.
