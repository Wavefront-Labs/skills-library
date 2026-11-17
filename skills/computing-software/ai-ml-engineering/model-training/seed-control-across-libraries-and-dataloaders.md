---
id: computing-software.ai-ml-engineering.model-training.seed-control-across-libraries-and-dataloaders
name: seed-control-across-libraries-and-dataloaders
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, random-seeds, reproducibility, seed-everything, rng-state, dataloader-seeding]
level: practitioner
status: draft
description: "Control randomness across Python, NumPy, PyTorch, TensorFlow, JAX and data loaders: one seeding function, per-worker and per-rank seeds, and saving RNG state for resume."
sources:
  - https://pytorch.org/docs/stable/notes/randomness.html
  - https://www.tensorflow.org/api_docs/python/tf/keras/utils/set_random_seed
  - https://numpy.org/doc/stable/reference/random/generator.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Seed control across libraries and dataloaders

Seeds make runs repeatable for debugging and fair for comparisons. They don't make results trustworthy by themselves: you still need multiple seeds to measure variance.

## One function, called first
```python
import os, random, numpy as np
def seed_everything(seed: int):
    os.environ["PYTHONHASHSEED"] = str(seed)       # only affects subprocesses; set in the shell for the main one
    random.seed(seed)
    np.random.seed(seed)                            # legacy global RNG (many libs still use it)
    try:
        import torch; torch.manual_seed(seed)       # CPU + all CUDA devices
    except ImportError: pass
    try:
        import tensorflow as tf; tf.keras.utils.set_random_seed(seed)   # python, numpy, tf at once
    except ImportError: pass
```
Lightning: `lightning.seed_everything(seed, workers=True)`. HF: `transformers.set_seed(seed)`. JAX has no global state: pass `jax.random.PRNGKey(seed)` explicitly and split it.

## Prefer explicit generators
```python
rng = np.random.default_rng(seed)                   # pass rng to functions instead of using np.random.*
g = torch.Generator().manual_seed(seed)
idx = torch.randperm(n, generator=g)
train_test_split(X, y, random_state=seed)           # sklearn: pass random_state everywhere
```
Explicit generators keep one component's randomness from shifting when another component draws extra numbers.

## Data loaders
- PyTorch workers: torch seed is `base_seed + worker_id` automatically; seed NumPy/random per worker in `worker_init_fn` from `torch.initial_seed()`. Pass `generator=` to the DataLoader for a fixed shuffle order.
- tf.data: `shuffle(buffer, seed=s)`, `tf.random.set_seed`; stateless random ops (`tf.random.stateless_uniform`) for augmentation reproducibility under parallel map.
- Distributed: same seed for model init on all ranks (DDP broadcasts weights anyway), different seeds for per-rank augmentation (seed + rank); DistributedSampler uses `seed` + `set_epoch(epoch)`.

## Resume exactly
Checkpoint RNG states with the model:
```python
state = {"py": random.getstate(), "np": np.random.get_state(), "torch": torch.get_rng_state(),
         "cuda": torch.cuda.get_rng_state_all(), "sampler_epoch": epoch, "step": step}
```
Restore all before continuing; also skip already-seen batches in the epoch.

## What seeds don't fix
GPU nondeterministic kernels, different hardware or library versions, thread scheduling and `cudnn.benchmark`. See the GPU nondeterminism and deterministic-algorithms skills.

## Verify
Run the same seed twice for N steps: per-step losses equal (CPU or deterministic GPU mode). Run two different seeds: losses differ, confirming the seed is actually wired in.
