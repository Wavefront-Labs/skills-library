---
id: computing-software.ai-ml-engineering.pytorch.choosing-an-optimizer
name: choosing-an-optimizer
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, optimizer-selection, adafactor, adamw, sgd-momentum, lion, torch-optim]
level: practitioner
status: gated
description: "Choose and configure an optimizer: SGD+momentum vs AdamW vs Adafactor vs Lion/Muon, default betas/eps/lr ranges, memory cost per parameter and when to switch."
sources:
  - https://pytorch.org/docs/stable/optim.html
  - https://arxiv.org/abs/1711.05101
  - https://arxiv.org/abs/2302.06675
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing an optimizer

**Goal:** pick a sane optimizer and starting hyperparameters for the model family instead of tuning blind.

## Quick guide
Learning-rate, beta and decay ranges below are rules of thumb from common practice (gated: unconfirmed, source is paywalled or blocked). They were not measured here; sweep them (see Verify).
| Situation | Optimizer | Starting point |
|---|---|---|
| Transformers, LLM fine-tuning, most deep nets | AdamW | lr 1e-4 to 3e-4 (pretrain), 1e-5 to 5e-5 (full fine-tune), 1e-4 to 2e-4 (LoRA); betas (0.9, 0.95) for large LMs, (0.9, 0.999) otherwise; weight_decay 0.01-0.1; eps 1e-8 |
| CNNs on vision with long schedules | SGD momentum=0.9, nesterov=True | lr 0.1 x batch/256, weight_decay 5e-4 to 1e-4, cosine schedule |
| Memory-limited large models | Adafactor (factored second moments) or 8-bit AdamW | `torch.optim.Adafactor` takes an explicit `lr` (default 0.01); the `relative_step` flag belongs to the separate `transformers.Adafactor` |
| Want Adam quality with half the state | Lion | lr 3-10x smaller than AdamW, weight_decay 3-10x larger |
| Small tabular nets | Adam/AdamW | lr 1e-3 |

## Memory per parameter (fp32 states)
- Measured on a 512x256 fp32 parameter after one step (torch 2.14): SGD momentum 4.0 bytes/param, AdamW 8.0, `torch.optim.Muon` 4.0, `torch.optim.Adafactor` about 0.02 (factored row/column statistics). Lion (one momentum buffer) is about 4 and 8-bit Adam about 2 by construction (gated: unconfirmed, source is paywalled or blocked); those two live in third-party libraries and were not run.
- Add master weights (4 bytes) when training in bf16 mixed precision, and gradients (2-4 bytes).

## Configuration rules
- Use **AdamW**, not Adam with `weight_decay` (Adam's L2 is coupled with the adaptive scale and regularizes badly).
- Exclude biases and norm weights from weight decay via parameter groups.
- Always pair with warmup for Adam-family optimizers on transformers (1-5% of steps).
- PyTorch implementations: `torch.optim.AdamW(params, lr, betas, weight_decay, fused=True)` on CUDA for speed; `foreach=None` is the default, which picks the foreach implementation where supported. `fused=True` also ran fine on CPU in torch 2.14.
- `torch.optim.Adafactor` was added in PyTorch 2.5 and `torch.optim.Muon` in 2.9 (release notes); `torch.optim.Lion` does not exist.
- Newer options (Muon for hidden matrices, Schedule-Free AdamW from `schedulefree`) can beat AdamW; benchmark on your task before adopting.

## When to switch
- Loss plateaus early with SGD on a transformer: switch to AdamW.
- AdamW generalizes worse than SGD on a CNN benchmark: try SGD with a longer schedule.
- OOM from optimizer state: 8-bit optimizers, Adafactor, or shard states (ZeRO/FSDP).

## Verify
- [ ] Run a short LR sweep (3-5 values, log-spaced) per optimizer and compare at equal steps.
- [ ] Inspect `opt.state_dict()["state"]` size to confirm memory expectations.
