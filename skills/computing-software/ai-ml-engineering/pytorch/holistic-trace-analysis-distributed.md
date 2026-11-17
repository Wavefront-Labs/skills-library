---
id: computing-software.ai-ml-engineering.pytorch.holistic-trace-analysis-distributed
name: holistic-trace-analysis-distributed
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, holistic-trace-analysis, hta, distributed-profiling, kineto-traces, comm-compute-overlap, straggler]
level: practitioner
status: docs-checked
description: "Analyse multi-rank PyTorch profiler traces with Holistic Trace Analysis: temporal breakdown, idle time, comm-compute overlap, kernel stats and queue length."
sources:
  - https://hta.readthedocs.io/en/latest/
  - https://pytorch.org/tutorials/beginner/hta_intro_tutorial.html
  - https://github.com/facebookresearch/HolisticTraceAnalysis
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Holistic Trace Analysis (HTA)

Viewing one rank's trace in Perfetto works for a single GPU. With many ranks you need aggregate answers: which rank is slow, how much GPU time is idle, whether communication overlaps compute. HTA reads the traces of all ranks and computes them.

## Collect
```python
from torch.profiler import profile, schedule, ProfilerActivity, tensorboard_trace_handler
with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
             schedule=schedule(wait=5, warmup=2, active=3, repeat=1),
             on_trace_ready=tensorboard_trace_handler("traces/"),
             record_shapes=True, with_stack=False) as p:
    for step, batch in enumerate(loader):
        train_step(batch); p.step()
        if step > 12: break
```
Profile the same steps on every rank and put every rank's trace file in one directory.

## Analyse
```python
from hta.trace_analysis import TraceAnalysis
ta = TraceAnalysis(trace_dir="traces/")
ta.get_temporal_breakdown()                 # per rank: idle, compute and non-compute time
ta.get_idle_time_breakdown()                # idle split into host wait, kernel wait, other
ta.get_comm_comp_overlap()                  # communication/computation overlap percentage per rank
ta.get_gpu_kernel_breakdown()               # top kernels by time
ta.get_queue_length_summary(ranks=[0])      # outstanding CUDA ops per stream
ta.get_cuda_kernel_launch_stats()           # kernel launch statistics
ta.get_memory_bw_summary()                  # memcpy / memset bandwidth
```
Each returns pandas DataFrames (some return tuples or per-rank dicts) and has a `visualize` option that is on by default.

## Reading results
- Temporal breakdown: non-compute time is time the GPU is not executing a compute op, such as data transfers, memory copies and communication collectives.
- Idle time (GPU idle = no kernel running). **Host wait**: the CPU thread has not enqueued enough kernels to keep the GPU busy. **Kernel wait**: gaps between consecutive kernels below `consecutive_kernel_delay`, an overhead of launching many small kernels. **Other**: unknown cause, for example a compute kernel waiting on a CUDA event from a communication kernel. `get_idle_time_breakdown` analyses rank 0 only unless you pass `ranks`.
- Queue length is the number of outstanding CUDA operations on a stream; a queue near empty alongside host wait points at a CPU or input-pipeline bottleneck.
- Compare per-rank overlap and idle numbers to find a rank that differs from the others, then investigate that rank (data imbalance, a bad node) with other tools.

## Trace diff
`from hta.trace_diff import TraceDiff` provides `TraceDiff.compare_traces(control, test, ...)` to compare two runs (before and after a change).

## Gotchas
- Large traces: keep `active` small and `with_stack=False`.
- Do not compare absolute timestamps between hosts.

## Checked
2026-11-01. Confirmed in the HolisticTraceAnalysis repository source (hta/trace_analysis.py docstrings and signatures, hta/trace_diff.py, hta/analyzers).
Removed: the overlap threshold figure, FSDP/DDP tuning parameter names, the Kineto file-extension claim, the clock-alignment claim, and the straggler heuristics about NCCL kernel durations and thermal throttling.
Method: documentation only; no commands were run.
