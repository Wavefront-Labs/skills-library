---
id: computing-software.ai-ml-engineering.model-training.double-descent-and-overparameterization
name: double-descent-and-overparameterization
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, double-descent, overparameterization, interpolation-threshold, bias-variance, model-size, regularization]
level: practitioner
status: draft
description: "Recognise double descent in model size, epochs and data size, why test error can peak at the interpolation threshold, and practical rules for sizing and early stopping."
sources:
  - https://arxiv.org/abs/1912.02292
  - https://www.pnas.org/doi/10.1073/pnas.1903070116
  - https://openai.com/index/deep-double-descent/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Double descent and overparameterized models

Classical bias-variance says test error is U-shaped in model complexity. Modern models show **double descent**: error falls, rises to a peak around the **interpolation threshold** (where the model can just fit the training set exactly, including noise), then falls again as the model grows further (Belkin et al. 2019; Nakkiran et al. 2019).

## Three forms (Nakkiran et al.)
- **Model-wise**: vary width/parameters at fixed data and epochs. Peak near where parameters ~ effective number of training examples.
- **Epoch-wise**: test error falls, rises, then falls again with longer training for mid-sized models. Early stopping at the first minimum may not be optimal.
- **Sample-wise**: near the threshold, *more data can hurt* temporarily, because it shifts the threshold to larger models.

## Why the peak
At the threshold there is essentially one way to fit all points, and it uses extreme weights to fit noise. Larger models have many interpolating solutions, and gradient descent's implicit bias picks smooth (low norm) ones.

## What makes the peak worse or disappear
- **Label noise** amplifies the peak strongly. Clean labels shrink it.
- **Regularisation** (weight decay, tuned properly), data augmentation and optimal early stopping can largely remove the peak.
- Optimal ridge regularisation removes double descent in linear models.

## Practical implications
- If a model is slightly bigger than the data can support and validation error is poor, the answer may be a **much bigger** model (with regularisation) or a smaller one, not small tweaks around the current size.
- When sweeping model size, sweep widely (log scale over orders of magnitude) and plot test error; do not conclude "bigger is worse" from points near the peak.
- For epoch-wise behaviour: keep checkpoints and evaluate the whole curve; a rising validation loss in the middle of training may recover. Combine with LR schedules (cosine decay often smooths it).
- Large pretrained models plus fine-tuning sit far right of the threshold, one reason they generalise well despite huge parameter counts.

## Reproduce to build intuition
Random features regression: fit `Ridge(alpha=1e-8)` on `n` samples with `p` random ReLU features, sweep `p` from 0.1n to 10n; test error spikes at p ~ n and falls after. Add `alpha` to see the peak vanish.

## Do not over-apply
Most production tuning happens far from the threshold; standard validation-driven early stopping and regularisation remain the right tools. Double descent explains surprising curves; it does not license skipping regularisation.
