---
id: computing-software.ai-ml-engineering.model-training.normalization-layer-choice
name: normalization-layer-choice
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, layernorm, rmsnorm, batchnorm, groupnorm, pre-norm, normalization-layers]
level: practitioner
status: draft
description: "Choose normalization layers: BatchNorm for CNNs with large batches, GroupNorm for small batches, LayerNorm/RMSNorm for transformers, pre-norm vs post-norm, and failure modes."
sources:
  - https://pytorch.org/docs/stable/nn.html#normalization-layers
  - https://arxiv.org/abs/1910.07467
  - https://arxiv.org/abs/2002.04745
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Normalization layer choice

## Options
| Layer | Normalizes over | Best for | Watch out |
|---|---|---|---|
| BatchNorm | batch (+ spatial) per channel | CNNs with batch >= ~16 per device | train/eval discrepancy, small batches, distributed (SyncBatchNorm), sequence padding |
| GroupNorm | channel groups per sample | detection/segmentation with tiny batches | slightly slower; tune num_groups (32) |
| LayerNorm | features per token/sample | transformers, RNNs | none major; costs a mean and variance |
| RMSNorm | features (no mean centering, no bias) | modern LLMs (Llama, etc.) | cheaper than LayerNorm, similar quality |
| InstanceNorm | spatial per sample-channel | style transfer | removes contrast information |

## Transformers: pre-norm vs post-norm
- Post-norm (original Transformer: `x = LN(x + f(x))`) needs warmup and is unstable when deep.
- Pre-norm (`x = x + f(LN(x))`) trains stably at depth; standard in GPT/Llama. Add a final norm before the output head.
- Extra stabilizers for large models: QK-norm (normalize queries/keys), and keeping norm computation in fp32.

## BatchNorm pitfalls
- Forgetting `model.eval()` at inference uses batch statistics: predictions change with batch composition.
- Fine-tuning with small batches: freeze BN statistics (keep BN layers in eval mode) or replace with GroupNorm.
- Multi-GPU with small per-GPU batches: `nn.SyncBatchNorm.convert_sync_batchnorm(model)`.
- Running stats drift when train and inference distributions differ; recalibrate stats on target data if needed.

## Weight decay
Exclude norm weights and biases from weight decay (parameter groups).

## Verify
- [ ] For BN models: eval-mode accuracy on validation equals what you expect and is independent of batch size.
- [ ] For deep transformers: loss curve without spikes in the first thousand steps with pre-norm.
