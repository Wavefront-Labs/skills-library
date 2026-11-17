---
id: computing-software.ai-ml-engineering.pytorch.torch-profiler-traces-with-schedule
name: torch-profiler-traces-with-schedule
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, profiler-trace, chrome-trace, torch-profiler, perfetto, tensorboard-trace-handler]
level: practitioner
status: gated
description: "Capture PyTorch profiler traces with a wait/warmup/active schedule, export to Perfetto or TensorBoard, and read GPU idle gaps, top kernels and CPU overhead."
sources:
  - https://pytorch.org/docs/stable/profiler.html
  - https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiler traces with a schedule

## Capture a few steps of training
```python
from torch.profiler import profile, schedule, ProfilerActivity, tensorboard_trace_handler
prof = profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    schedule=schedule(wait=5, warmup=2, active=3, repeat=1),   # skip compile/warmup steps
    on_trace_ready=tensorboard_trace_handler("./tb_prof"),      # or lambda p: p.export_chrome_trace("t.json")
    record_shapes=True, profile_memory=True, with_stack=False)
with prof:
    for step, batch in enumerate(loader):
        train_step(batch)
        prof.step()                                             # advance the schedule
        if step >= 12: break
print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=20))
```
The block ran on a CPU-only torch 2.14 build with a `Linear` (listing `ProfilerActivity.CUDA` there is accepted, `tensorboard_trace_handler` wrote one `<host>_<pid>.<ts>.pt.trace.json` file, the handler fired once for `schedule(wait=1, warmup=1, active=2, repeat=1)` over 6 steps, and `sort_by="cuda_time_total"` raised nothing). `schedule` takes keyword-only `wait, warmup, active, repeat=0, skip_first=0, skip_first_wait=0`. GPU columns and kernel names were not seen (gated: unconfirmed, source is paywalled or blocked).
- `wait` skips startup noise, `warmup` runs the profiler but discards data (profiler overhead settles), `active` records.
- `with_stack=True` adds Python source lines; useful but slows capture and inflates files.
- Label regions: `with torch.profiler.record_function("data_to_gpu"):`.

## View
- **Perfetto** (ui.perfetto.dev) or `chrome://tracing`: drag the exported JSON in (`export_chrome_trace("t.json")` wrote a non-empty file). Not opened in a viewer here (gated: unconfirmed, source is paywalled or blocked).
- **TensorBoard**: `tensorboard --logdir tb_prof` with the `torch-tb-profiler` plugin (last PyPI release 0.4.3, October 2023, and the `tb_plugin` folder is no longer in the pytorch/kineto repo root listing, so treat it as unmaintained; not run here). HTA (Holistic Trace Analysis) for multi-rank traces.

## What to look for
(Items 1-5 below describe GPU traces and were not reproduced on this CPU-only machine (gated: unconfirmed, source is paywalled or blocked).)
1. **GPU stream row has gaps**: GPU idle. Look at the CPU row at that time: data loading (`enumerate(DataLoader)`), `cudaStreamSynchronize` from `.item()`, Python overhead between many tiny kernels.
2. **Top kernels by CUDA time**: GEMMs (`sm90_xmma`, `ampere_*gemm`, `cutlass`) should dominate in a healthy transformer. If elementwise kernels (`vectorized_elementwise_kernel`) are a large share, fuse with `torch.compile`.
3. **Many short kernels with launch gaps**: launch-bound; try CUDA graphs or larger batches.
4. **Memcpy HtoD on the compute stream** without overlap: pin memory and `non_blocking=True`.
5. **NCCL kernels** not overlapping with compute in DDP/FSDP: bucket sizes, prefetch settings.

## Gotchas
- Profiling the first steps captures compilation and cuDNN autotuning; the schedule's `wait` avoids that.
- Traces of many active steps reach GBs; 2-5 active steps is enough.
- Distributed: profile all ranks with per-rank filenames (the handler adds worker names); a slow rank stalls everyone.
- `key_averages(group_by_input_shape=True)` only fills the shape column when the profile was captured with `record_shapes=True` (without it nothing raised on 2.14; with it, `aten::linear` rows carried `input_shapes`).

## Verify
After an optimisation, re-capture with the same schedule and compare step time and GPU busy percentage in the same viewer.
