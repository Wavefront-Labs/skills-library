---
id: computing-software.ai-ml-engineering.model-training.dropout-weight-decay-and-augmentation
name: dropout-weight-decay-and-augmentation
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, regularization, dropout, weight-decay, adamw, label-smoothing, data-augmentation, mixup, overfitting]
level: practitioner
status: draft
description: "Choose and tune neural-net regularizers: decoupled weight decay with AdamW, dropout rates and placement, label smoothing, augmentation and mixup, and how they interact."
sources:
  - https://arxiv.org/abs/1711.05101
  - https://jmlr.org/papers/v15/srivastava14a.html
  - https://arxiv.org/abs/1710.09412
  - https://pytorch.org/docs/stable/generated/torch.optim.AdamW.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dropout, weight decay and augmentation

**Goal:** close a train/validation gap with the right regularizer and sane default strengths.

## Diagnose first
Regularise only when the learning curves show overfitting (train loss keeps falling, val loss bottoms out and rises). If both are poor, regularisation makes it worse; add capacity or fix data.

## Weight decay
- Use **decoupled** weight decay (AdamW, Loshchilov & Hutter). With plain Adam, `weight_decay` is L2 added to the gradient and gets rescaled by the adaptive denominator, which makes it much weaker for parameters with large gradient variance.
- Typical values: 0.01-0.1 for AdamW on transformers/CNNs; 1e-4-5e-4 for SGD with momentum on ImageNet-style CNNs.
- Exclude biases and normalisation weights (LayerNorm/BatchNorm gamma/beta) and often embeddings from decay via parameter groups.
- Weight decay interacts with learning rate: the effective shrinkage per step is `lr * wd`. When you change LR a lot, retune WD.

## Dropout
- Fully connected heads: 0.2-0.5. Transformers: 0.1 on attention and residual outputs (large pretrained models often fine-tune with 0.0-0.1).
- Avoid dropout directly before BatchNorm (variance shift between train and eval); place it after the last norm / before the classifier.
- CNNs benefit more from spatial dropout, DropBlock or stochastic depth (drop path, 0.1-0.2 for deep ResNets/ViTs) than element-wise dropout on conv maps.
- Dropout slows convergence; you will need more epochs.

## Label smoothing
`CrossEntropyLoss(label_smoothing=0.1)` prevents over-confident logits and often improves accuracy for classification with many classes. It hurts calibration-sensitive uses less than you'd expect but harms knowledge distillation teachers (smoothed teachers transfer less).

## Data augmentation
Often the strongest regulariser. Images: random resized crop + flip as baseline; RandAugment/TrivialAugment for more. Mixup/CutMix (alpha 0.2-1.0) for classification - incompatible with some losses and metrics (soft targets). Text: back-translation, token dropout. Tabular: usually none; regularise the model instead.

## Interactions
- Heavy augmentation + strong dropout + high WD at once usually underfits; add one at a time, measure val loss.
- Mixup/label smoothing change the training loss scale, so train loss is no longer comparable to val loss.
- Early stopping is a regulariser too; with good early stopping, extra regularisation buys less.

## Verify
- [ ] Learning curves show the gap narrowed without raising val loss floor.
- [ ] Biases/norm weights excluded from decay.
- [ ] Each regulariser's contribution measured by ablation (one on/off at a time).
