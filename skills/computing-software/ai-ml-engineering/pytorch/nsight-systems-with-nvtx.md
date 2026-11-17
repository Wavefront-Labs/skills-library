---
id: computing-software.ai-ml-engineering.pytorch.nsight-systems-with-nvtx
name: nsight-systems-with-nvtx
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, nsight-systems, nvtx, nsys, gpu-profiling, cuda-profiling, timeline]
level: practitioner
status: gated
description: "Profile PyTorch with Nsight Systems: nsys profile flags, NVTX ranges and emit_nvtx, capture ranges for steady-state steps, and reading CPU/GPU gaps and NCCL overlap."
sources:
  - https://docs.nvidia.com/nsight-systems/UserGuide/index.html
  - https://pytorch.org/docs/stable/autograd.html#torch.autograd.profiler.emit_nvtx
  - https://pytorch.org/docs/stable/cuda.html#nvidia-tools-extension-nvtx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Nsight Systems with NVTX ranges

**Use when:** the PyTorch profiler is too heavy or you need system-wide truth (CPU threads, CUDA API, kernels, memcpy, NCCL, OS runtime) on one timeline.

## Annotate the code
The PyTorch NVTX and cudart calls below are from memory; the PyTorch doc pages cited did not render (gated: unconfirmed, source is paywalled or blocked). Check them against the PyTorch `torch.cuda` and profiler docs.
```python
import torch
for step, batch in enumerate(loader):
    if step == 20: torch.cuda.cudart().cudaProfilerStart()
    torch.cuda.nvtx.range_push(f"step{step}")
    with torch.cuda.nvtx.range("forward"):  out = model(batch)
    with torch.cuda.nvtx.range("backward"): out.loss.backward()
    with torch.cuda.nvtx.range("optim"):    opt.step(); opt.zero_grad()
    torch.cuda.nvtx.range_pop()
    if step == 30: torch.cuda.cudart().cudaProfilerStop(); break
```
`with torch.autograd.profiler.emit_nvtx():` adds a range for every autograd op (verbose, higher overhead; use for short windows).

## Capture
```bash
nsys profile -o run1 --trace=cuda,nvtx,osrt,cudnn,cublas \
  --capture-range=cudaProfilerApi --capture-range-end=stop \
  --cuda-memory-usage=true --force-overwrite=true python train.py
nsys stats run1.nsys-rep            # summary and trace reports from the result file
```
Multi-GPU: profile each rank (the `-o` filename expands `%q{ENV_VAR}` from the environment, so `-o rank%q{RANK}` works when launching nsys per process) and open reports side by side.

## Reading the timeline
| Pattern | Meaning | Action |
|---|---|---|
| Gaps on the GPU row while CPU is busy in Python | launch-bound | CUDA graphs, torch.compile, bigger batch |
| Long `cudaStreamSynchronize` / `cudaMemcpy DtoH` on CPU | hidden sync (`.item()`, printing) | remove syncs |
| NCCL kernels not overlapping compute | poor comm overlap | bucket sizes, FSDP prefetch |
| Memcpy HtoD serialized before compute | unpinned memory | `pin_memory=True`, `non_blocking=True` |

## Tips
- Skip the first steps (warmup, compile, cudnn autotune) using capture ranges.
- Keep captures short (10-20 steps); reports get huge.
- Nsight Compute (`ncu`) is the next step for a single slow kernel (occupancy, memory throughput).

## Verify
- [ ] NVTX step ranges visible and step durations match your logged step time.

## Checked

2026-11-02. Confirmed against the Nsight Systems user guide CLI switch tables: `--trace` values (cuda, nvtx, osrt, cudnn, cublas), `--capture-range` value cudaProfilerApi, `--capture-range-end` value stop, `--cuda-memory-usage true|false`, `--force-overwrite true|false`, `.nsys-rep` result files, `nsys stats`, and `%q{ENV_VAR}` substitution in `-o`. Changed: the multi-GPU line now relies on `%q{ENV_VAR}` per process rather than an unverified torchrun wrapper. Gated: the PyTorch API calls (`torch.cuda.nvtx.*`, `torch.cuda.cudart()`, `emit_nvtx`) because the PyTorch pages cited returned only stubs; the timeline-reading table is practitioner guidance, not a documented claim.

Method: documentation only; no commands were run.
