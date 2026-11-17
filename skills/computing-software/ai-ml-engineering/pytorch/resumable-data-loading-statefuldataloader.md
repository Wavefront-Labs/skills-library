---
id: computing-software.ai-ml-engineering.pytorch.resumable-data-loading-statefuldataloader
name: resumable-data-loading-statefuldataloader
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, statefuldataloader, torchdata, resume-training, mid-epoch-resume, dataloader]
level: practitioner
status: verified
description: "Resume training mid-epoch without repeating or skipping samples using torchdata StatefulDataLoader state_dict, stateful datasets/samplers and distributed caveats."
sources:
  - https://pytorch.org/data/beta/torchdata.stateful_dataloader.html
  - https://github.com/pytorch/data/tree/main/torchdata/stateful_dataloader
  - https://pytorch.org/docs/stable/data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Resumable data loading with StatefulDataLoader

**Goal:** after a preemption at step 37,000 of a 50,000-step epoch, continue from sample 37,001, not from the start of the epoch.

## Why plain DataLoader is not enough
`torch.utils.data.DataLoader` has no state. Common hacks (skip N batches) re-read and re-decode all skipped data and break with shuffling unless the sampler seed is fixed.

## StatefulDataLoader (torchdata)
Drop-in replacement with `state_dict()` / `load_state_dict()`.
```python
from torchdata.stateful_dataloader import StatefulDataLoader
loader = StatefulDataLoader(ds, batch_size=32, shuffle=True, num_workers=8, persistent_workers=True)

# save, together with model/optimizer
ckpt = {"model": model.state_dict(), "optim": opt.state_dict(),
        "loader": loader.state_dict(), "step": step}
torch.save(ckpt, path)

# resume (must construct with identical args before loading)
loader = StatefulDataLoader(ds, batch_size=32, shuffle=True, num_workers=8)
loader.load_state_dict(torch.load(path)["loader"])   # a plain-dict state loaded with the default weights_only=True in the run here
for batch in loader:   # continues mid-epoch
    ...
```
- Map-style datasets: by default the state holds the number of batches yielded and fast-forwards the sampler (torchdata docs); `RandomSampler` shuffling resumed exactly. Run with torchdata 0.11.0 on torch 2.14 (Windows): after 10 of 50 batches, `state_dict()` into a fresh `StatefulDataLoader(..., shuffle=True)` reproduced the remaining batches of the original iteration, with `num_workers=0` and no seed, and with `num_workers=2` plus a seeded `generator` (the full 50-batch sequence matched an uninterrupted run).
- Iterable datasets: without dataset state the loader only fast-forwards by the count of batches yielded (torchdata docs); implement `state_dict()`/`load_state_dict()` on the dataset (e.g. file index + offset) to avoid re-reading, and the loader aggregates the state across worker processes (but not across ranks). Run here with `num_workers=0`: a stream dataset with `state_dict`/`load_state_dict` resumed at the right item (next batch `[12, 13, 14, 15]` after 3 batches of 4).
- Custom samplers: implement the same two methods.

## Distributed
- Each rank saves its own loader state (different shards); store per rank, e.g. in a DCP checkpoint keyed by rank, or `f"loader_rank{rank}.pt"`.
- Resuming with a different world size or `num_workers` invalidates the state (loading a `num_workers=2` state into `num_workers=0` or `4` loaders raised `AssertionError`); document the constraint or re-shard and accept approximate resume.
- With `DistributedSampler`, still call `set_epoch(epoch)` at each epoch start.

## Gotchas
- Snapshot frequency: worker states are snapshotted every `snapshot_every_n_steps` (default 1, from the 0.11.0 signature); larger values cut overhead but mean slightly less precise resume (a trade-off described by the parameter name; not benchmarked).
- The loader state reflects batches yielded to the main process, including prefetched ones not yet trained on if you checkpoint mid-loop; checkpoint right after an optimizer step.
- Hugging Face `datasets` `IterableDataset` defines `state_dict()`/`load_state_dict()` and Accelerate's `DataLoaderConfiguration` has `use_stateful_dataloader` (default `False`); both confirmed in their source (the combination itself is not exercised in this review).

## Verify
- [ ] Log sample ids: a run interrupted and resumed sees exactly the same id sequence as an uninterrupted run with the same seed.
