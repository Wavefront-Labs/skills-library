---
id: computing-software.ai-ml-engineering.model-training.diagnosing-loss-curves-and-convergence
name: diagnosing-loss-curves-and-convergence
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, error-analysis, loss-curves, training-convergence, learning-rate, divergence, plateau, training-diagnostics]
level: practitioner
status: draft
description: "Read training and validation loss curves to diagnose LR too high or low, divergence, plateaus, noisy loss, overfitting onset, data-order problems and broken evaluation."
sources:
  - https://developers.google.com/machine-learning/testing-debugging/metrics/interpretic
  - https://github.com/google-research/tuning_playbook
  - https://karpathy.github.io/2019/04/25/recipe/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diagnosing loss curves and convergence

**Goal:** turn the shape of the loss curves into a specific next action.

## Log the right things
Per step: training loss (raw + smoothed EMA), learning rate, gradient norm. Per eval: validation loss and the main metric. Plot loss on a log y-axis; early dynamics vanish on a linear one.

## Patterns
| Curve shape | Likely cause | Action |
|---|---|---|
| Flat from step 0 | LR far too low, frozen params, bug (labels not connected, loss detached) | overfit-one-batch test, check grads, LR range test |
| Drops then explodes / NaN | LR too high, no warmup, fp16 overflow | lower LR, add warmup, clip grads, bf16 |
| Periodic spikes, recovers | bad batches/outliers, LR at edge of stability | inspect spike batches, clip, slightly lower LR |
| Very noisy, slow downward trend | batch too small or LR high for batch size | larger batch / accumulation, lower LR |
| Plateau, then sudden drop | normal for some tasks; or LR decay kicked in | be patient; check schedule |
| Train falls, val rises | overfitting | regularisation, more data, early stopping |
| Val below train | dropout/augmentation active only in train; val easier or leaked | check eval mode, check split |
| Val loss falls but metric flat | loss and metric misaligned (calibration, threshold) | evaluate the metric you care about directly |
| Step-change at epoch boundaries | data not shuffled; ordered data | shuffle, check sampler |

## Tuning playbook habits
- Compare runs at equal **steps/examples**, not wall-clock.
- Change one thing at a time; seed variance can be larger than the effect you're chasing - run 2-3 seeds for close calls.
- Check that "converged" really means converged: extend a run 2x and see if the metric still improves.

## Gradient norm as an early warning
Rising grad norm before a loss spike points to instability (LR, precision). Steadily shrinking to ~0 with high loss means vanishing gradients or saturated units.

## Verify
- [ ] Loss, LR and grad norm logged per step for every run.
- [ ] Diagnosed pattern and action recorded in the experiment notes.
- [ ] Close comparisons backed by multiple seeds.
