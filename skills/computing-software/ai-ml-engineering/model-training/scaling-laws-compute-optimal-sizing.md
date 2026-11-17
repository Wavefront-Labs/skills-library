---
id: computing-software.ai-ml-engineering.model-training.scaling-laws-compute-optimal-sizing
name: scaling-laws-compute-optimal-sizing
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, scaling-laws, compute-optimal, chinchilla, training-budget, flops-estimation]
level: practitioner
status: draft
description: "Size models and data from compute budgets: training FLOPs about 6ND, Chinchilla tokens-per-parameter, fitting small-scale scaling curves, and inference-aware over-training."
sources:
  - https://arxiv.org/abs/2203.15556
  - https://arxiv.org/abs/2001.08361
  - https://arxiv.org/abs/2401.00448
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Scaling laws and compute-optimal model sizing

## Core arithmetic
- Training compute for dense transformers: `C ≈ 6 N D` FLOPs (N parameters, D training tokens).
- Wall-clock: `time ≈ C / (num_gpus x peak_flops x MFU)`. With H100 bf16 dense peak ~ 1e15 FLOP/s and MFU 40%, a 7B model on 1T tokens (4.2e22 FLOPs) needs about 1.2e8 GPU-seconds / 3.3e4 ≈ 29k GPU-hours.

## Chinchilla result
For a fixed compute budget, loss is minimized with parameters and tokens scaled roughly equally: about **20 tokens per parameter** (e.g. 7B params -> ~140B tokens). Earlier (Kaplan) laws favored bigger models with fewer tokens; Chinchilla corrected this.

## Inference-aware sizing
If the model will serve many requests, train a smaller model on far more tokens than compute-optimal (Llama-style 100-2000+ tokens/param). Higher training cost, much cheaper inference. Choose by total lifecycle cost.

## Fit your own curve before a big run
1. Train 5-8 small models (e.g. 10M to 500M params) at compute-optimal token counts with the same data mix and recipe.
2. Fit `L(C) = a C^(-b) + L_inf` (or `L(N, D) = E + A/N^α + B/D^β`) to final validation losses.
3. Extrapolate to the target budget; check one intermediate size before committing.
Keep hyperparameters scaled sensibly (learning rate decreases with width; muP makes them transfer across widths).

## Data constraints
Repeating data up to ~4 epochs costs little; beyond that, returns diminish sharply. Data quality filtering can shift curves more than model size.

## Fine-tuning context
Scaling laws for fine-tuning are task-specific; for most applied work, the question is whether a larger base model beats more fine-tuning data. Run small pilots across 2-3 model sizes and 2-3 data sizes.

## Verify
- [ ] Budget sheet: N, D, C, expected GPU-hours at measured MFU, and the extrapolated loss with its fit uncertainty.
