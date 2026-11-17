---
id: computing-software.ai-ml-engineering.pytorch.memory-efficient-optimizers-8bit-and-zero
name: memory-efficient-optimizers-8bit-and-zero
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, 8bit-optimizers, zeroredundancyoptimizer, bitsandbytes, optimizer-state-sharding, paged-optimizers]
level: practitioner
status: gated
description: "Cut optimizer memory with bitsandbytes 8-bit/paged AdamW and ZeroRedundancyOptimizer state sharding: setup, stability tips, checkpointing and when FSDP is better."
sources:
  - https://huggingface.co/docs/bitsandbytes/main/en/optimizers
  - https://pytorch.org/docs/stable/distributed.optim.html
  - https://pytorch.org/tutorials/recipes/zero_redundancy_optimizer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Memory-efficient optimizers (8-bit Adam, ZeroRedundancyOptimizer)

**Goal:** fit a bigger model or batch by shrinking the 8 bytes/param of AdamW state.

## bitsandbytes 8-bit optimizers
Block-wise quantized m and v (2 bytes/param total) with near-identical convergence for most fine-tuning (convergence claim not measured here (gated: unconfirmed, source is paywalled or blocked)). Run on bitsandbytes 0.50.2 with a CPU-only torch 2.14: `AdamW8bit` stepped on CPU, and its state for a 8192-element weight was `state1`/`state2` as `torch.uint8` plus float32 `qmap` and `absmax` tensors, so about 2 bytes/param plus small tables.
```python
import bitsandbytes as bnb
opt = bnb.optim.AdamW8bit(model.parameters(), lr=2e-5, betas=(0.9, 0.999), weight_decay=0.01)
# paged variant spills state to CPU under memory pressure instead of OOM
opt = bnb.optim.PagedAdamW8bit(model.parameters(), lr=2e-5)
```
- Keep embeddings in 32-bit state for stability: `bnb.optim.GlobalOptimManager.get_instance().register_module_override(model.embed, "weight", {"optim_bits": 32})` (call `register_parameters(model.parameters())` first and build the optimizer before the override; in a run that gave float32 `state1`/`state2` for a 5000x8 embedding), or use `bnb.nn.StableEmbedding` (exists).
- Tensors with fewer than 4096 elements stay 32-bit by default: `min_8bit_size=4096` in the signature, and in a run a 64-element bias had float32 state while the 8192-element weight had uint8 state.
- In HF Trainer: `optim="adamw_bnb_8bit"` or `"paged_adamw_8bit"` (both names are in `transformers/training_args.py` of transformers 5.20.2; `adamw_8bit` is an alias for the first). `PagedAdamW8bit` constructs on CPU; the paging to CPU under GPU memory pressure was not exercised (gated: unconfirmed, source is paywalled or blocked).

## ZeroRedundancyOptimizer (ZeRO stage 1 in core PyTorch)
Shards optimizer state across DDP ranks; each rank updates its shard and broadcasts parameters.
```python
from torch.distributed.optim import ZeroRedundancyOptimizer
model = DDP(model.cuda(), device_ids=[local_rank])   # CPU/gloo: DDP(model) worked the same way
opt = ZeroRedundancyOptimizer(model.parameters(), optimizer_class=torch.optim.AdamW, lr=1e-4)
```
- State memory drops by roughly world_size; params and grads are still replicated. Measured on 2 gloo CPU ranks with a 4-layer MLP: each rank held 16644 state elements against 33288 for a full AdamW, exactly half, and the parameters stayed identical on both ranks.
- Checkpoint: call `opt.consolidate_state_dict(to=0)` on all ranks, then save `opt.state_dict()` on rank 0 only (calling `state_dict()` before consolidating raised `RuntimeError: Optimizer state has not been consolidated on this rank`; afterwards rank 0 got keys `state` and `param_groups`).
- `overlap_with_ddp=True` with a DDP comm hook overlaps the update with backward (advanced; the argument exists in the signature, the overlap was not run) (gated: unconfirmed, source is paywalled or blocked).

## When to use what
| Need | Choice |
|---|---|
| Single GPU, fine-tuning | 8-bit or paged 8-bit AdamW |
| Multi-GPU DDP, model fits, state does not | ZeroRedundancyOptimizer or DeepSpeed ZeRO-1 |
| Params+grads also too big | FSDP2 / DeepSpeed ZeRO-3 (shards everything) |
| Extreme memory limits | Adafactor or GaLore/LoRA (fewer trainable params; not run here) |

## Gotchas
- 8-bit optimizers were historically CUDA-only; 0.50.2 ran `AdamW8bit` on CPU here, so check the backend support table for your hardware and version.
- Loading a 32-bit optimizer checkpoint into an 8-bit optimizer is not supported; restart optimizer state or keep the same class (not tried (gated: unconfirmed, source is paywalled or blocked)).
- Gradient clipping and GradScaler still work; clip before `opt.step()` as usual.

## Verify
- [ ] Compare `torch.cuda.max_memory_allocated()` (GPU) or the state-element count above (CPU) and the first 500 steps' loss curve against standard AdamW.
