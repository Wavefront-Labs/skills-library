---
id: computing-software.ai-ml-engineering.pytorch.fsdp2-fully-shard-and-mixed-precision-policy
name: fsdp2-fully-shard-and-mixed-precision-policy
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, fully-shard, fsdp2, mixedprecisionpolicy, dtensor, sharding]
level: practitioner
status: gated
description: "Shard models with FSDP2 fully_shard: per-block wrapping order, MixedPrecisionPolicy, reshard_after_forward, meta-device init, and how it differs from FSDP1."
sources:
  - https://pytorch.org/docs/stable/distributed.fsdp.fully_shard.html
  - https://pytorch.org/tutorials/intermediate/FSDP_tutorial.html
  - https://github.com/pytorch/torchtitan
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSDP2 fully_shard

FSDP2 (`torch.distributed.fsdp.fully_shard`) shards each parameter as a DTensor along dim 0 across ranks, all-gathers before forward/backward of each wrapped unit and reduce-scatters gradients. It replaces FSDP1's `FullyShardedDataParallel` wrapper and flat parameters.

Checked on torch 2.14 with the CPU gloo backend and 2 ranks (`mp.spawn`): this recipe ran with `init_device_mesh("cpu", ...)`, meta-device construction, `to_empty(device="cpu")` and a bf16 `MixedPrecisionPolicy`. GPU memory, NCCL and speed claims were not measured (gated: unconfirmed, source is paywalled or blocked).

## Basic recipe
```python
from torch.distributed.fsdp import fully_shard, MixedPrecisionPolicy
from torch.distributed.device_mesh import init_device_mesh
mesh = init_device_mesh("cuda", (world_size,))
mp = MixedPrecisionPolicy(param_dtype=torch.bfloat16, reduce_dtype=torch.float32)
with torch.device("meta"):
    model = Transformer(cfg)                              # no memory allocated
for block in model.layers:
    fully_shard(block, mesh=mesh, mp_policy=mp)           # inner units first
fully_shard(model, mesh=mesh, mp_policy=mp)               # root last (embeddings, head)
model.to_empty(device="cuda"); model.init_weights()       # materialise shards, then init
opt = torch.optim.AdamW(model.parameters(), lr=3e-4)      # build AFTER sharding
```

## Choices
- **Wrap granularity**: one unit per transformer block. Too coarse = high peak memory (whole model gathered); too fine = many small collectives.
- **reshard_after_forward**: the signature default is `None`, which the docs define as True for non-root modules and False for root modules. `True` frees gathered params after forward and re-gathers in backward (ZeRO-3 like); `False` keeps them (ZeRO-2 like): faster, more memory. The docs say False is usually best for the root because backward starts there immediately (so the default already does it); an `int` reshards to that smaller world size (it must be a non-trivial divisor of the shard mesh size).
- **MixedPrecisionPolicy**: params gathered in bf16, gradients reduced in fp32 for stability; sharded master weights stay fp32. In the run the forward output was bfloat16 while `weight.dtype` stayed float32 after a step. Don't also call `model.to(bf16)`.
- **HSDP**: `init_device_mesh("cuda", (n_nodes, gpus_per_node))` and pass the 2D mesh: replicate across nodes, shard within node.
- **CPU offload**: `offload_policy=CPUOffloadPolicy()` for very large models at a speed cost.

## Differences from FSDP1 that bite
- Parameters keep original names and shapes (as DTensors): `named_parameters()` gave `emb.weight`, `layers.0.l.weight`, ...; an (8, 8) weight reported shape `(8, 8)` with a local shard of `(4, 8)` on each of 2 ranks, so param groups and weight decay filters work normally.
- No `auto_wrap_policy`; you call `fully_shard` explicitly per module.
- Gradient accumulation without sync: `model.set_requires_gradient_sync(False)` on non-final micro-steps (the call exists and returned None; the saved communication was not measured).
- Gradient clipping: `torch.nn.utils.clip_grad_norm_` works on DTensors (it returned a `DTensor`; `.full_tensor().item()` gave a plain float).
- Checkpointing: use `torch.distributed.checkpoint` with `get_model_state_dict`/`get_optimizer_state_dict`, not `model.state_dict()` + `torch.save` on rank 0.

## Pitfalls
- Building the optimizer before `fully_shard` holds references to the old unsharded params: in a run with `SGD(lr=0.5)` created first, `fully_shard` replaced the module's parameters, the optimizer's param was not the module's new `weight`, and a step left the sharded weight unchanged, so training silently does not update (memory also never drops).
- Calling submodules directly (not through the root forward) skips the pre-forward all-gather for units that were not wrapped (not reproduced); `model.unshard()` exists and ran. (gated: unconfirmed, source is paywalled or blocked)
- Activation checkpointing: apply `checkpoint_wrapper` to blocks before `fully_shard` (`checkpoint_wrapper` then `fully_shard` ran, giving an `FSDPCheckpointWrapper`).

## Verify
`torch.cuda.max_memory_allocated()` per rank should drop roughly by world size for parameters + optimizer state compared with DDP (not measured here: no GPU); loss curve should match a DDP run on a small model.
