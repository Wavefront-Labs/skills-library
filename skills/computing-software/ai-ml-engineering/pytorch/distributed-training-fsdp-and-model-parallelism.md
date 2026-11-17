---
id: computing-software.ai-ml-engineering.pytorch.distributed-training-fsdp-and-model-parallelism
name: distributed-training-fsdp-and-model-parallelism
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, fsdp, fully-sharded-data-parallel, model-parallelism, tensor-parallelism, pipeline-parallelism, deepspeed, zero, activation-checkpointing, mixed-precision, large-models, distributed-training, sharding, torch-distributed]
level: advanced
status: draft
description: "Train models too large for one GPU with PyTorch FSDP: sharding policy, mixed precision, activation checkpointing, and when to reach for tensor/pipeline parallelism instead."
sources:
  - https://pytorch.org/docs/stable/fsdp.html
  - https://pytorch.org/tutorials/intermediate/FSDP_tutorial.html
  - https://www.deepspeed.ai/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FSDP and model parallelism — when DDP stops fitting

**Goal:** know which parallelism strategy a model's size and hardware actually need, and set up FSDP without the config mistakes that silently retrain on garbage or OOM anyway.

## 1. Pick the strategy by what doesn't fit
- Model (+ optimizer states + gradients + activations) fits on one GPU → plain **DDP** (see computing-software.ai-ml-engineering.pytorch.training-loop). Each GPU holds a full copy; only gradients sync.
- Model fits but Adam's two extra fp32 moment buffers plus gradients don't → **FSDP** (PyTorch) or **DeepSpeed ZeRO** stage 2/3. These shard optimizer state, gradients, and (ZeRO-3/FSDP full-shard) parameters across GPUs, gathering each layer's full weights only for the instant it runs.
- A single layer (huge embedding, huge MLP) doesn't fit on one GPU even unsharded → **tensor parallelism** (Megatron-style, split the matrix multiply itself across GPUs) — rarely hand-rolled; use DeepSpeed, Megatron-LM, or framework-native TP (`torch.distributed.tensor.parallel`) rather than writing custom all-gather logic.
- The model is many sequential stages and inter-GPU bandwidth is the bottleneck → **pipeline parallelism**, splitting layers across GPUs by depth and streaming micro-batches through; adds "bubble" idle time that shrinks as micro-batch count grows.
- Most real large-model jobs combine all of the above (3D parallelism) — don't hand-build this; use a framework (DeepSpeed, Megatron-LM, FSDP2 with device_mesh) that has solved the communication scheduling.

## 2. FSDP setup (the parts people get wrong)
```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
model = FSDP(model, auto_wrap_policy=my_policy, mixed_precision=mp_policy,
             sharding_strategy=ShardingStrategy.FULL_SHARD,
             device_id=torch.cuda.current_device())
```
- **Wrap policy matters more than the top-level call.** Wrapping only the outer module shards almost nothing (one giant all-gather of the whole model per step). Use `transformer_auto_wrap_policy` (wraps each transformer block) or size-based wrapping so each shard-unshard unit is a reasonably sized chunk — this is where most of the memory savings live.
- **Mixed precision policy** is separate from autocast: FSDP's `MixedPrecision(param_dtype=bf16, reduce_dtype=bf16, buffer_dtype=bf16)` controls what dtype parameters are gathered/communicated in, independent of the forward pass's autocast. Mismatching these causes either silent fp32 communication (slow) or precision loss you didn't intend.
- **Checkpointing an FSDP model is not `state_dict()` as usual.** Use `FSDP.state_dict_type` context (`FULL_STATE_DICT` to gather a normal checkpoint on rank 0, `SHARDED_STATE_DICT` to save per-shard and avoid ever materializing a full copy — required once the full model doesn't fit on one GPU even for saving). Loading a full checkpoint into a freshly-sharded model needs the same context on load.
- Activation checkpointing (`torch.utils.checkpoint`) composes with FSDP and is usually mandatory at this scale — apply per transformer block, not to the whole model (checkpointing the whole model forces full recompute and defeats pipelining of comms and compute).
- Gotcha: optimizer must be constructed **after** wrapping in FSDP (it needs the sharded parameters), and the LR/weight-decay groups must be built from `model.parameters()` post-wrap, not a reference saved before wrapping.
- Communication overlap: FSDP overlaps the next layer's all-gather with the current layer's compute automatically, but only if `limit_all_gathers` and `backward_prefetch` are left at sane defaults — manually disabling them "to save memory" usually costs more in stalled GPUs than it saves.

## 3. Sizing and failure modes
- Estimate memory before launching: params × (2 for bf16/fp16 weights + 2 for grad + 8–12 for Adam fp32 moments+master weights) ÷ num_gpus for full sharding, plus activations (depends on batch×seq×hidden, not shardable without checkpointing).
- A job that OOMs only during checkpoint save (not training) is almost always `FULL_STATE_DICT` materializing the whole model on rank 0 — switch to `SHARDED_STATE_DICT` or stream to CPU offload.
- NCCL timeout on a large job is usually one straggler rank (slow disk read, imbalanced shard) — set `NCCL_DEBUG=INFO` and look for which rank entered the collective late, not a comms bug.
- Loss diverges only at larger world size: check the **effective batch size** and LR together — scaling GPUs without scaling warmup/LR is the most common "worked on 8 GPUs, diverged on 64" bug, not a framework bug.

## Verify
- [ ] Wrap policy confirmed to shard at the transformer-block level (check `model` repr or FSDP's `summon_full_params` memory before/after), not just the top module.
- [ ] Memory estimate (params/grads/optimizer/activations) done before the job was launched; actual peak memory checked against it.
- [ ] Checkpoint save/load tested at the target world size, not just locally — `SHARDED_STATE_DICT` used if the full model doesn't fit ungathered.
- [ ] Optimizer built after FSDP wrapping.
- [ ] LR/warmup revisited when world size (and therefore effective batch) changed.
