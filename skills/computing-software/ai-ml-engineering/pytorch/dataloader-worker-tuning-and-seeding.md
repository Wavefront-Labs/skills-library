---
id: computing-software.ai-ml-engineering.pytorch.dataloader-worker-tuning-and-seeding
name: dataloader-worker-tuning-and-seeding
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, persistent-workers, worker-init-fn, num-workers, prefetch-factor, dataloader-performance]
level: practitioner
status: gated
description: "Tune PyTorch DataLoader num_workers, persistent_workers, prefetch_factor and pin_memory, seed workers properly, and diagnose input-bound training."
sources:
  - https://pytorch.org/docs/stable/data.html#multi-process-data-loading
  - https://pytorch.org/docs/stable/notes/randomness.html#dataloader
  - https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DataLoader worker tuning and seeding

## Settings and what they do
| Arg | Effect | Starting point |
|---|---|---|
| `num_workers` | worker processes running `__getitem__` + collate | CPU cores per GPU, often 4-8 (rule of thumb, tune by benchmark) |
| `persistent_workers=True` | keep workers alive between epochs (needs `num_workers > 0`, else `ValueError`) | on whenever num_workers > 0 |
| `prefetch_factor` | batches each worker loads ahead (default `None`, which means 2 when `num_workers > 0`; setting it with `num_workers=0` raises `ValueError`) | 2-4; raise for bursty I/O |
| `pin_memory=True` | page-locked host memory for faster, async H2D | on for GPU training |
| `multiprocessing_context` | fork / spawn / forkserver | default per OS |
Without `persistent_workers`, every epoch restarts the workers and re-runs dataset setup, causing a stall at each epoch start, very visible with short epochs and validation loaders. Measured with 2 workers and a `worker_init_fn` that logged each call over 3 epochs: 5 logged calls (6 expected; one append was lost) without persistence and 2 with it.

## Is training input-bound?
- `nvidia-smi dmon` or the profiler: GPU utilisation dipping to 0 periodically while CPU workers are at 100% (no GPU on the test host; not run).
- Time `next(iter)` in the loop vs the step time. If data wait > ~5% of step time, tune.
- Quick test: replace the loader with a cached fixed batch. If throughput jumps, the loader is the bottleneck.
Fixes in order: more workers; move decode/augment to GPU (DALI, torchvision v2 on GPU); pre-resize images; pack small files into shards; cache decoded data.

## Seeding workers
Each worker's torch seed is `base_seed + worker_id`, set automatically (checked: two workers reported `torch.initial_seed()` values differing by 1). Older patterns did not reseed NumPy, so NumPy augmentations could repeat across workers; on torch 2.14 the NumPy draws in two workers already differed, but seeding NumPy and `random` yourself is still what the PyTorch reproducibility note shows and is needed for reproducible runs:
```python
def seed_worker(worker_id):
    s = torch.initial_seed() % 2**32
    np.random.seed(s); random.seed(s)
g = torch.Generator(); g.manual_seed(42)
DataLoader(ds, num_workers=8, worker_init_fn=seed_worker, generator=g, persistent_workers=True)
```
Use `worker_init_fn` also for per-worker setup: opening file handles, DB connections, setting `torch.set_num_threads(1)`.

## Gotchas
- **Memory growth with many workers**: Python lists of objects in the dataset get copied on access (refcount writes break copy-on-write). Store metadata as NumPy arrays or Arrow, not lists of dicts or Python strings (fork-based behaviour; not reproducible on Windows spawn) (gated: unconfirmed, source is paywalled or blocked).
- **Too many workers**: oversubscription, each worker spawning OpenMP threads. Set `OMP_NUM_THREADS=1` or call `torch.set_num_threads(1)` in workers (not measured) (gated: unconfirmed, source is paywalled or blocked).
- **Windows/macOS spawn**: dataset and collate must be picklable and the script needs `if __name__ == "__main__":` (on Windows the default start method is `spawn`; a dataset class defined inside the `__main__` block made the workers exit unexpectedly in a test).
- **`/dev/shm` too small in Docker**: "bus error" or "DataLoader worker killed". Run with `--shm-size=8g` or `--ipc=host` (Docker was not available; not run) (gated: unconfirmed, source is paywalled or blocked).
- **Hangs with DDP**: make sure all ranks iterate the same number of batches (uneven shard lengths hang the next all-reduce).

## Verify
Benchmark loader throughput alone (`for b in loader: pass` over 200 batches) for num_workers in [2, 4, 8, 16] and pick the knee.
