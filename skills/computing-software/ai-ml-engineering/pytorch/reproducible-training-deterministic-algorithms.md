---
id: computing-software.ai-ml-engineering.pytorch.reproducible-training-deterministic-algorithms
name: reproducible-training-deterministic-algorithms
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, use-deterministic-algorithms, pytorch-reproducibility, cudnn-deterministic, cublas-workspace-config, seeds]
level: practitioner
status: gated
description: "Make PyTorch runs bit-reproducible on the same hardware: seeds, use_deterministic_algorithms, cuDNN flags, CUBLAS_WORKSPACE_CONFIG and DataLoader generators."
sources:
  - https://pytorch.org/docs/stable/notes/randomness.html
  - https://pytorch.org/docs/stable/generated/torch.use_deterministic_algorithms.html
  - https://docs.nvidia.com/cuda/cublas/index.html#results-reproducibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reproducible PyTorch training

Bitwise reproducibility is only promised for the same PyTorch version, CUDA/cuDNN version, GPU model and process count. Across machines, aim for statistical reproducibility instead.

## Full recipe
```python
import os, random, numpy as np, torch
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"   # before the first CUDA call
def seed_all(seed):
    random.seed(seed); np.random.seed(seed)
    torch.manual_seed(seed)                     # seeds CPU and all CUDA devices
seed_all(0)
torch.use_deterministic_algorithms(True)       # error on known-nondeterministic ops
torch.backends.cudnn.benchmark = False         # autotuner may pick different kernels per run
torch.backends.cudnn.deterministic = True      # PyTorch docs: use_deterministic_algorithms(True) already covers cuDNN convs

def seed_worker(worker_id):
    s = torch.initial_seed() % 2**32
    np.random.seed(s); random.seed(s)
g = torch.Generator(); g.manual_seed(0)
loader = DataLoader(ds, shuffle=True, num_workers=4, worker_init_fn=seed_worker, generator=g)
```

## What each flag fixes
- `cudnn.benchmark=True` times several conv algorithms on first call and caches the fastest; the choice can differ between runs. Turn it off for reproducibility, back on for speed.
- `use_deterministic_algorithms(True)` makes ops that have a deterministic implementation use it and raises `RuntimeError: <op> does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True)'` for ops that do not (the PyTorch randomness note's example is CUDA `index_add_`, and the list in the `use_deterministic_algorithms` docs is authoritative; on this CPU host `torch.Tensor.put_` raised it). Use `warn_only=True` to turn the error into a warning (checked with `put_`). With the flag on, `torch.empty` fills memory with NaN by default (`torch.utils.deterministic.fill_uninitialized_memory`), which can expose reads of uninitialised tensors. Setting the global flag does not flip the `torch.backends.cudnn.deterministic` attribute (it stayed `False`), but the docs say either setting makes CUDA convolution algorithms deterministic.
- `CUBLAS_WORKSPACE_CONFIG=:4096:8` (or `:16:8`, less memory) is required for deterministic cuBLAS on CUDA >= 10.2; without it you get a RuntimeError once determinism is on (gated: unconfirmed, source is paywalled or blocked). The variable's `:[SIZE]:[COUNT]` format is documented in the PyTorch CUDA notes (size in KiB); no GPU was available to test the error.
- DataLoader workers re-seed torch automatically; the PyTorch note still shows `worker_init_fn` seeding NumPy and `random`. On torch 2.14 (Windows, 2 workers) the NumPy draws in the two workers already differed, but without a `generator` and `worker_init_fn` two runs are not repeatable. With both, two runs gave identical NumPy draws, and a seeded `generator` alone fixed the shuffle order (checked).

## Things that still vary
- Changing batch size, number of GPUs or `num_workers` changes reduction order: different floats.
- `torch.compile`/Triton autotuning can pick different kernels; disable autotune or cache it.
- Atomic adds in custom CUDA/Triton kernels.
- Resume from checkpoint: also save and restore `torch.get_rng_state()`, `torch.cuda.get_rng_state_all()`, `np.random.get_state()`, `random.getstate()` and the sampler/generator state, or the resumed run diverges.

## Cost
The docs only say deterministic operations "tend to have worse performance"; measure the cost on your model. Use it to debug and for audited runs; for sweeps, report mean and std over seeds instead.

## Verify
Run 50 steps twice and compare `loss` per step and a parameter hash (`sum(p.double().sum() for p in model.parameters())`). They must match exactly (a 50-step CPU SGD run twice gave identical loss lists and parameter sums). The recipe's CUDA lines (`CUBLAS_WORKSPACE_CONFIG`, cuDNN flags) could not be exercised without a GPU.
