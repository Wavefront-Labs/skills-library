---
id: computing-software.ai-ml-engineering.pytorch.diagnosing-input-bound-training
name: diagnosing-input-bound-training
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, dataloader-bottleneck, dataloader, gpu-utilization, input-pipeline, data-loading-performance]
level: practitioner
status: gated
description: "Prove whether training is starved by the DataLoader and fix it: timing data vs compute, profiler gaps, workers, decode cost, storage throughput and GPU-side augmentation."
sources:
  - https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html
  - https://pytorch.org/docs/stable/data.html
  - https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Diagnosing input-bound training

**Symptom:** GPU utilization saw-tooths or sits at 30-60%, step time does not improve with a faster GPU or smaller model.

## Step 1: measure data wait vs compute
```python
import time, torch
t0 = time.perf_counter()
for i, batch in enumerate(loader):
    t1 = time.perf_counter()                       # time spent waiting for data
    batch = [b.cuda(non_blocking=True) for b in batch]
    loss = step(batch); torch.cuda.synchronize()
    t2 = time.perf_counter()
    if i % 50 == 0: print(f"data {t1-t0:.3f}s  compute {t2-t1:.3f}s")
    t0 = t2
```
If `data` is a large fraction of `compute`, you are input bound. With `.cuda(...)` and `torch.cuda.synchronize()` removed, this loop ran on CPU against a dataset whose `__getitem__` sleeps 4 ms: it printed data 0.071 s against compute 0.0003 s per batch of 16, an obvious input-bound signature (the CUDA lines themselves were not run: no GPU) (gated: unconfirmed, source is paywalled or blocked). Also iterate the loader alone (no model) to get its max throughput in samples/s and compare with the model's samples/s.

## Step 2: locate the cost
- Profile one worker in-process: `num_workers=0` and `cProfile` / `py-spy record -o prof.svg -- python train.py` to see decode (PIL, JPEG), tokenization or augmentation hot spots (`py-spy` was not installed or run (gated: unconfirmed, source is paywalled or blocked)).
- In `torch.profiler` traces, gaps between GPU kernels with `enumerate(DataLoader)` on the CPU track confirm loader stalls.
- Check storage: `iostat -x 1` / cloud disk throughput; many small files on network storage is a classic cause (Linux tool and storage claim, not run) (gated: unconfirmed, source is paywalled or blocked).

## Fixes, cheapest first
1. `num_workers` = CPU cores per GPU (try 4-16; a starting heuristic, tune by measuring), `persistent_workers=True`, `prefetch_factor=2-4`, `pin_memory=True`. Constraints measured on torch 2.14: `persistent_workers=True` with `num_workers=0` raises `ValueError: persistent_workers option needs num_workers > 0`, and `prefetch_factor` with `num_workers=0` raises `ValueError: prefetch_factor option could only be specified in multiprocessing`; `pin_memory=True` on a CPU-only build ran without error (a warning at most). On Windows (spawn start method) `worker_init_fn` and the dataset class must be importable top-level objects, otherwise workers die with `AttributeError: module '__mp_main__' has no attribute 'init'`, and in a 256-sample test with 4 ms per item the throughput was 226 samples/s with 0 workers versus 99 and 118 with 2 and 4 workers because worker start-up dominated a short epoch, so measure over a realistic length.
2. Move augmentation to GPU (torchvision.transforms.v2 on CUDA tensors, NVIDIA DALI; `torchvision.transforms.v2` imports in torchvision 0.29.1, DALI not checked) and decode with `torchvision.io.decode_jpeg(device="cuda")` (the `device` parameter exists in the 0.29.1 signature, GPU decode not run) (gated: unconfirmed, source is paywalled or blocked).
3. Pre-process once offline (resize, tokenize) and store compact formats: WebDataset tar shards, MosaicML Streaming MDS, Arrow, or uint8 numpy memmaps (suggestions; none benchmarked here).
4. Pack small files into shards (100MB-1GB is a rule of thumb, not measured) for object storage; stage to local NVMe.
5. Avoid per-sample Python overhead: batch-level collate work, vectorized transforms, `torch.from_numpy` instead of list conversions.
6. Watch CPU oversubscription: set `torch.set_num_threads(1)` in workers (`worker_init_fn`, which ran), `OMP_NUM_THREADS`.

## Verify
- [ ] Loader-only throughput is at least 1.3x the model's consumption rate (a suggested margin, not a standard).
- [ ] `nvidia-smi dmon -s u` shows steady SM utilization (not run: no GPU); data time per step under 5% of compute (suggested threshold).
