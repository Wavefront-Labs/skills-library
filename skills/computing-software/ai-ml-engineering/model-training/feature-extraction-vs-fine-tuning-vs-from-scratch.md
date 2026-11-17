---
id: computing-software.ai-ml-engineering.model-training.feature-extraction-vs-fine-tuning-vs-from-scratch
name: feature-extraction-vs-fine-tuning-vs-from-scratch
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, transfer-learning, feature-extraction-vs-fine-tuning, linear-probe, pretrained-models]
level: practitioner
status: draft
description: "Decide between frozen feature extraction, partial or full fine-tuning, parameter-efficient tuning and training from scratch, by data size, domain distance and compute budget."
sources:
  - https://cs231n.github.io/transfer-learning/
  - https://arxiv.org/abs/1411.1792
  - https://arxiv.org/abs/2202.10054
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Feature extraction vs fine-tuning vs training from scratch

## Decision table
| Your labelled data | Domain vs pretraining | Do this |
|---|---|---|
| Small (hundreds to low thousands) | similar | frozen features + linear/logistic head (linear probe) |
| Small | different | linear probe on earlier layers' features, or light fine-tuning with strong regularisation; consider PEFT |
| Medium to large | similar | full fine-tuning at low LR (or LoRA for big models) |
| Large | different | full fine-tuning; consider continued pretraining on unlabelled domain data first |
| Huge, and no suitable pretrained model exists (new modality, sensor data) | | train from scratch |
Pretrained initialisation almost always beats scratch at equal compute, even for fairly different domains (medical images from ImageNet, code from text). Scratch wins mainly when the input format is foreign to every available model or data is enormous.

## Practical ladder
1. **Zero-shot / prompt** a foundation model (LLM, CLIP) to get a baseline with no training.
2. **Linear probe**: extract embeddings once, cache them, train logistic regression/GBM. Minutes, very robust, great for small data and many tasks.
3. **PEFT** (LoRA, adapters, prompt tuning): most of full fine-tuning's gain with 0.1-1% trainable params; small checkpoints per task.
4. **Full fine-tuning**: best accuracy with enough data; highest memory, risk of forgetting and overfitting.
5. **LP-FT**: linear probe first, then fine-tune all layers starting from the trained head. Reduces feature distortion and improves out-of-distribution robustness (Kumar et al., 2022).

## What to check before choosing
- **Licence and provenance** of the pretrained model.
- **Input match**: resolution, tokenizer/vocabulary, normalisation statistics.
- **Latency/size constraints**: a smaller pretrained model fully tuned may beat a large one linearly probed under a latency budget.
- **Label budget**: plot accuracy vs number of labelled examples for probe and fine-tune; the crossover tells you which to use and whether labelling more pays.

## Gotchas
- Fine-tuning with a high LR (scratch-level, e.g. 1e-3 for a transformer) destroys pretrained features. Typical: 1e-5 to 5e-5 for transformers, 1e-4 to 1e-3 for CNN heads with lower LR for the backbone.
- Small data plus full fine-tuning: high variance across seeds; run several seeds and report mean/std.
- BatchNorm statistics with tiny batches during fine-tuning: freeze BN.

## Verify
Run the linear probe and one fine-tuning config on the same splits with 3 seeds; pick the cheapest option within noise of the best.
