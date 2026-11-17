---
id: computing-software.ai-ml-engineering.pytorch.correct-gpu-timing-with-benchmark-and-cuda-events
name: correct-gpu-timing-with-benchmark-and-cuda-events
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, torch-benchmark, cuda-events, benchmarking, timing, warmup]
level: practitioner
status: docs-checked
description: "Time PyTorch GPU code correctly with torch.utils.benchmark or CUDA events: synchronisation, warmup, thread settings, and reading medians instead of single runs."
sources:
  - https://github.com/pytorch/pytorch/blob/main/torch/utils/benchmark/utils/timer.py
  - https://github.com/pytorch/pytorch/blob/main/docs/source/notes/cuda.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Correct GPU timing

GPU operations are asynchronous by default, so timing a CUDA call with a host clock without synchronising measures queueing, not execution. PyTorch's CUDA notes say to call `torch.cuda.synchronize()` before measuring, or use `torch.cuda.Event`.

## torch.utils.benchmark (preferred)
```python
import torch.utils.benchmark as benchmark
t = benchmark.Timer(stmt="f(x)", globals={"f": model, "x": x}, label="fwd", sub_label="bs=32",
                    description="eager", num_threads=torch.get_num_threads())
m = t.blocked_autorange(min_run_time=2.0)
print(m)
```
- With an accelerator present, `Timer`'s default timer synchronises accelerators before reading the clock.
- `num_threads` defaults to 1; set it to match production.
- `blocked_autorange` runs blocks until `min_run_time` seconds (default 0.2) have elapsed and returns a `Measurement` (labels `label`, `sub_label`, `description` group results when printing).

## CUDA events (parts of a step)
```python
start = torch.cuda.Event(enable_timing=True); end = torch.cuda.Event(enable_timing=True)
start.record(); f(x); end.record()
torch.cuda.synchronize()          # wait for the events to be recorded
ms = start.elapsed_time(end)
```
Repeat after some warmup calls and report the median of many runs.

## Rules
- Warm up first: initialisation, autotuning and compilation happen on early calls.
- Synchronise before reading the clock.
- Report median and spread, not one run.
- Use the same inputs, shapes and dtypes as production.
- Exclude data loading unless you are benchmarking it.

## Checked
2026-11-01. Confirmed in torch/utils/benchmark/utils/timer.py (Timer arguments, num_threads default 1, accelerator synchronisation by the default timer, blocked_autorange and its min_run_time default) and the PyTorch CUDA notes (asynchronous execution, Event timing example with synchronize). Removed (not confirmed): Compare usage, clock-locking advice, L2 flush and Triton do_bench, MFU formula, run-to-run agreement threshold.
Method: documentation only; no commands were run.
