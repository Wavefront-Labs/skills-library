---
id: computing-software.ai-ml-engineering.pytorch.async-checkpointing
name: async-checkpointing
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, async-checkpointing, distributed-checkpoint, dcp, checkpoint-stall, training-throughput]
level: practitioner
status: gated
description: "Hide checkpoint save time with torch.distributed.checkpoint.async_save: staging to CPU, waiting on the previous future, pinned memory and failure handling."
sources:
  - https://pytorch.org/tutorials/recipes/distributed_async_checkpoint_recipe.html
  - https://pytorch.org/docs/stable/distributed.checkpoint.html
  - https://pytorch.org/blog/reducing-checkpointing-times/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Asynchronous checkpointing

**Problem:** saving a large sharded checkpoint blocks training for tens of seconds to minutes; frequent checkpoints (needed for preemptible capacity) eat throughput.

## How async save works
1. **Staging (blocking, short):** copy GPU state to CPU memory.
2. **Persist (background):** a thread/process writes the CPU copy to storage while training continues.

```python
import torch.distributed.checkpoint as dcp
from torch.distributed.checkpoint.state_dict import get_state_dict

ckpt_future = None
for step, batch in enumerate(loader):
    train_step(batch)
    if step % save_every == 0:
        if ckpt_future is not None:
            ckpt_future.result()                  # never have two saves in flight (starting a second save before the first finished made the first `result()` fail with a gloo `Timed out waiting 40000ms for send operation` on both ranks)
        model_sd, optim_sd = get_state_dict(model, optimizer)
        state = {"model": model_sd, "optim": optim_sd, "step": step}
        ckpt_future = dcp.async_save(state, checkpoint_id=f"{ckpt_dir}/step-{step}")
if ckpt_future is not None:
    ckpt_future.result()                          # flush before exit
```
Run on torch 2.14 CPU with gloo and 2 ranks: the loop's `async_save` returned a `Future` and `result()` completed. Collectives are used, so every rank must call it and a process group must be initialised (the `"cuda:nccl,cpu:gloo"` backend string is the GPU form; NCCL is not available here, so it was not run (gated: unconfirmed, source is paywalled or blocked)). `async_save`'s signature on 2.14 includes `async_checkpointer_type` (`AsyncCheckpointerType.THREAD` default, or `PROCESS`), `async_stager`, `process_group`, `no_dist` and `use_collectives`, and returns a `Future` or `AsyncSaveResponse`.

## Tuning
- Use pinned-memory staging: `from torch.distributed.checkpoint.staging import DefaultStager, StagingOptions` (not exported from `torch.distributed.checkpoint` itself); `StagingOptions(use_pinned_memory=True, use_shared_memory=True, use_async_staging=True, use_non_blocking_copy=True)` are the 2.14 defaults and the docs say pinned memory requires CUDA. Pass the stager as `async_stager=`. Speed was not measured (gated: unconfirmed, source is paywalled or blocked).
- Host RAM must hold a full copy of the local shard; check node memory before enabling (reasoned, not measured).
- Write to fast local NVMe then upload asynchronously to object storage if the filesystem is slow (not tested).

## Failure semantics
- A checkpoint is only valid once the future completes; write a marker (e.g. `latest` pointer file) after `result()` returns, and resume only from marked checkpoints.
- Exceptions in the background save surface on `result()` (the gloo timeout above appeared there, not at the `async_save` call); call it before the next save and at exit so failures are not silent.

## Verify
- [ ] Training step time around save steps is close to normal (measure blocking time = staging only).
- [ ] A resume from an async checkpoint reproduces the loss at that step.
