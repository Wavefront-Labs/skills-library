---
id: computing-software.ai-ml-engineering.pytorch.finding-hidden-host-device-syncs
name: finding-hidden-host-device-syncs
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, sync-debug-mode, cuda-synchronize, host-device-sync, nonzero-static, performance-debugging]
level: practitioner
status: docs-checked
description: "Find hidden CPU-GPU synchronizations that stall training with torch.cuda.set_sync_debug_mode and replace data-dependent ops such as torch.nonzero with fixed-size ones."
sources:
  - https://github.com/pytorch/pytorch/blob/main/torch/cuda/__init__.py
  - https://github.com/pytorch/pytorch/blob/main/torch/_torch_docs.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Finding hidden host-device syncs

**Why it matters:** the CPU normally queues kernels ahead of the GPU. An op that needs a GPU result on the host blocks until the GPU finishes, leaving the GPU idle.

## Ops documented to sync (CUDA input)
- `torch.nonzero` (the docs say it causes host-device synchronization)
- `torch.normal` when `std` is a CUDA tensor
- `torch.cuda.synchronize()` and `Stream.synchronize()` / `Event.synchronize()` by design (they wait for the work)

## Detect them
```python
torch.cuda.set_sync_debug_mode("warn")     # or "error" to raise at the sync point
train_step(batch)
torch.cuda.set_sync_debug_mode("default")  # 0 turns it off again
```
Modes: `"default"`/0 do nothing, `"warn"`/1 warn on synchronizing operations, `"error"`/2 raise. `torch.cuda.get_sync_debug_mode()` returns the current value.

## Rewrites
| Instead of | Use |
|---|---|
| `torch.nonzero(m)` (output size depends on data) | `torch.nonzero_static(m, size=k)` with `fill_value` (default -1) padding |
| `torch.repeat_interleave(x, repeats)` with a tensor | pass `output_size=` so it avoids stream synchronization |

Some syncs are unavoidable (early stopping checks, data-dependent control flow); keep them out of the inner loop.

## Verify
- [ ] `set_sync_debug_mode("error")` passes for a full steady-state training step.
- [ ] Step time improvement measured.

## Checked
2026-11-01. Confirmed in the PyTorch source docstrings: `set_sync_debug_mode` modes and `get_sync_debug_mode`, `torch.nonzero` host-device synchronization note, `torch.nonzero_static(input, *, size, fill_value=-1)`, `torch.normal` CUDA `std` sync note, `repeat_interleave` `output_size` note. Removed: the list of other syncing ops (`.item()`, `.cpu()`, `print`, `unique`, `masked_select`, `empty_cache`), profiler event names, stack-trace claim and the logging rewrites, none of which were confirmed.
Method: documentation only; no commands were run.
