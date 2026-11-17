---
id: computing-software.ai-ml-engineering.pytorch.distributed-checkpoint-dcp
name: distributed-checkpoint-dcp
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, distributed-checkpoint, dcp, torch-distributed-checkpoint, sharded-checkpoint, resharding]
level: practitioner
status: gated
description: "Save and load sharded PyTorch training state with torch.distributed.checkpoint: state_dict helpers, async save, resharding to a new world size and converting to a single file."
sources:
  - https://pytorch.org/docs/stable/distributed.checkpoint.html
  - https://pytorch.org/tutorials/recipes/distributed_checkpoint_recipe.html
  - https://pytorch.org/tutorials/recipes/distributed_async_checkpoint_recipe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed checkpoint (DCP)

`torch.distributed.checkpoint` writes each rank's shards in parallel plus a metadata file, and can load into a different parallelism layout (resharding). Use it for FSDP/TP/HSDP; `torch.save` from rank 0 needs a full gather and does not scale.

## Save and load
Run on torch 2.14 CPU build with the gloo backend, 2 ranks (via `mp.spawn` and a file init method: `torchrun` failed on this Windows wheel, see the torchrun skill), with `fully_shard` on a two-layer MLP. Rank 0's checkpoint folder held `.metadata`, `__0_0.distcp`, `__1_0.distcp` (one data file per rank); the saved and re-loaded parameters compared equal.
```python
import torch.distributed.checkpoint as dcp
from torch.distributed.checkpoint.state_dict import get_state_dict, set_state_dict
def save(step):
    model_sd, optim_sd = get_state_dict(model, opt)
    state = {"model": model_sd, "optim": optim_sd, "step": step, "sched": sched.state_dict()}
    dcp.save(state, checkpoint_id=f"ckpt/step_{step}")       # every rank calls this
def load(path):
    model_sd, optim_sd = get_state_dict(model, opt)          # templates with the right sharding
    state = {"model": model_sd, "optim": optim_sd, "step": 0, "sched": sched.state_dict()}
    dcp.load(state, checkpoint_id=path)                      # in-place into the templates
    set_state_dict(model, opt, model_state_dict=state["model"], optim_state_dict=state["optim"])
    sched.load_state_dict(state["sched"]); return state["step"]
```
`get_state_dict` handles FSDP1/FSDP2/DDP differences and fully qualified names: `DDP(...).state_dict()` keys start `module.0.weight` and a `torch.compile` wrapper's start `_orig_mod.0.weight`, but `get_state_dict` returned `0.weight` for both, and `DTensor` values for the FSDP2 model.

## Async save
```python
fut = dcp.async_save(state, checkpoint_id=path)   # copies to CPU, writes in background
...
fut.result()                                       # before the next save
```
`async_save` ran on CPU and its `fut.result()` completed (the returned object printed as `Future`; the 2.14 docs describe `AsyncSaveResponse` with `staging_completion` and `upload_completion` futures too, so check what your version returns). The claimed stall reduction from minutes to a GPU-to-CPU copy, the CPU RAM need and the gloo coordination group were not measured (gated: unconfirmed, source is paywalled or blocked).

## Resharding
Resharding works: a checkpoint saved by 2 FSDP2 ranks loaded into an unsharded single-process model with `get_state_dict` templates and `dcp.load` (step restored to 7). The 64-to-8 GPU and TP+FSDP cases were not run (gated: unconfirmed, source is paywalled or blocked).

## Convert for inference / HF
```python
from torch.distributed.checkpoint.format_utils import dcp_to_torch_save, torch_save_to_dcp
dcp_to_torch_save("ckpt/step_1000", "model_full.pt")     # single-process, no GPU needed
```
The saved file keeps the whole `state` structure (keys `model`, `optim`, `step`, `sched` in the test), so take `sd["model"]`. The CLI modes are `dcp_to_torch` and `torch_to_dcp` (not `dcp_to_torch_save`, which argparse rejects): `python -m torch.distributed.checkpoint.format_utils dcp_to_torch ckpt/step_1000 full.pt` worked. Then load into an unsharded model and save as safetensors (not run).

## Operational tips
- Write to a temp dir and rename (or write a `COMPLETE` marker) so a crash mid-save doesn't leave a "latest" checkpoint that's corrupt (sound practice, not exercised here).
- Keep the last N checkpoints; object storage via `fsspec` (`FsspecWriter` and `FsspecReader` import from `torch.distributed.checkpoint._fsspec_filesystem`, a private module, not from `torch.distributed.checkpoint`; S3/GCS not tested (gated: unconfirmed, source is paywalled or blocked)).
- Include dataloader/sampler state and RNG states for exact resume.

## Verify
Save at step N, load into a fresh process (ideally a different world size), run one step, and compare the loss with the original run's step N+1.
