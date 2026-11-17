---
id: computing-software.ai-ml-engineering.pytorch.cuda-memory-snapshots
name: cuda-memory-snapshots
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, memory-snapshot, record-memory-history, cuda-memory, memory-viz, oom-debugging]
level: practitioner
status: docs-checked
description: "Record PyTorch CUDA memory snapshots with _record_memory_history and _dump_snapshot, view them in memory_viz, and use the allocator counters to find what fills GPU memory."
sources:
  - https://github.com/pytorch/pytorch/blob/main/torch/cuda/memory.py
  - https://github.com/pytorch/pytorch/blob/main/torch/cuda/_memory_viz.py
  - https://github.com/pytorch/pytorch/blob/main/docs/source/torch_cuda_memory.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CUDA memory snapshots

## Record
```python
torch.cuda.memory._record_memory_history(max_entries=100_000)
for step in range(5):
    train_step(next(it))
torch.cuda.memory._dump_snapshot("snap.pickle")
torch.cuda.memory._record_memory_history(enabled=None)    # stop recording
```
`max_entries` keeps at most that many trace entries; when full, new entries overwrite the oldest, so long runs keep only the last ones. `enabled` takes `None`, `"state"` or `"all"`. These are private (underscore) APIs.

## View
Open pytorch.org/memory_viz and drag in the pickle. Views include **Active Memory Timeline** and **Allocator State History** (segments, useful for fragmentation).
Offline: `python -m torch.cuda._memory_viz trace_plot snap.pickle -o snap.html` (`-o/--output` defaults to `output.html`; `-d/--device` picks a device).

## Quick numbers without a snapshot
```python
torch.cuda.memory_allocated(), torch.cuda.max_memory_allocated()
torch.cuda.memory_reserved()
print(torch.cuda.memory_summary(abbreviated=True))
torch.cuda.reset_peak_memory_stats()
```

## Fragmentation
Setting `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` is the allocator option the PyTorch source names; test it against your peak reserved memory.

## Verify
After a fix, dump a new snapshot for the same steps; the peak in the timeline and `max_memory_allocated` should both drop.

## Checked
2026-11-01. Confirmed in the PyTorch source and `docs/source/torch_cuda_memory.md`: `_record_memory_history` (`max_entries`, `enabled` values, overwrite behaviour), `_dump_snapshot`, the memory_viz view names, `trace_plot` CLI with `-o`/`-d`, the memory counter functions, `expandable_segments:True`. Removed: OOM-catch snippet, the "healthy step" reading guide, optimizer-state and checkpointing advice, empty_cache and context-size remarks, which were not confirmed.
Method: documentation only; no commands were run.
