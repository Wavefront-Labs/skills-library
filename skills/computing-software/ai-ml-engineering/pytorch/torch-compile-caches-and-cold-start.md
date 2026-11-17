---
id: computing-software.ai-ml-engineering.pytorch.torch-compile-caches-and-cold-start
name: torch-compile-caches-and-cold-start
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, torch-compile, compile-cache, fx-graph-cache, mega-cache, cold-start, inductor]
level: practitioner
status: gated
description: "Cut torch.compile cold-start time with FX graph / AOTAutograd / autotune caches, mega-cache save_cache_artifacts, cache directories in containers and warmup strategy."
sources:
  - https://pytorch.org/tutorials/recipes/torch_compile_caching_tutorial.html
  - https://pytorch.org/tutorials/recipes/torch_compile_caching_configuration_tutorial.html
  - https://pytorch.org/docs/stable/torch.compiler_troubleshooting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# torch.compile caches and cold-start time

**Problem:** compiling a large model takes minutes on every pod start or job restart, and `max-autotune` takes longer still.

## Caches that exist (read from torch 2.14 source and config; compile runs need a C++/Triton toolchain this machine lacks, so hit/miss behaviour was not run) (gated: unconfirmed, source is paywalled or blocked)
| Cache | What it stores | Control |
|---|---|---|
| FX graph cache (Inductor) | compiled Inductor output per graph | `TORCHINDUCTOR_FX_GRAPH_CACHE=1` (`torch._inductor.config.fx_graph_cache` read True on 2.14) |
| AOTAutograd cache | joint forward/backward graphs | `TORCHINDUCTOR_AUTOGRAD_CACHE=1` (`torch._functorch.config.enable_autograd_cache` read True on 2.14) |
| Triton kernel / autotune cache | compiled kernels and best configs | under the cache dir |
| Remote caches | same, shared via Redis | `TORCHINDUCTOR_FX_GRAPH_REMOTE_CACHE=1`, `TORCHINDUCTOR_REDIS_HOST` (also `TORCHINDUCTOR_REDIS_PORT`, default 6379, and `TORCHINDUCTOR_REDIS_URL`) |

Location: `TORCHINDUCTOR_CACHE_DIR`; the default is `tempfile.gettempdir()/torchinductor_<user>` (read in `torch/_inductor/runtime/cache_dir_utils.py`; `/tmp/torchinductor_<user>` on Linux, under `%TEMP%` on Windows). In containers `/tmp` is ephemeral, so mount a persistent volume and point the env var there.

## Mega-cache: portable artifacts
```python
compiled = torch.compile(model, mode="max-autotune")
compiled(example)                                   # compile and warm
artifact_bytes, info = torch.compiler.save_cache_artifacts()
open("compile_cache.bin", "wb").write(artifact_bytes)

# on a new machine before compiling
torch.compiler.load_cache_artifacts(open("compile_cache.bin", "rb").read())
```
Bake this file into the image or download it at start-up. `torch.compiler.save_cache_artifacts` and `load_cache_artifacts` exist on 2.14; `save_cache_artifacts()` returned `None` when nothing had been compiled with inductor, so guard for that. Cache hits require the same PyTorch/Triton version, GPU arch, model code and input shapes/dtypes (and dynamic-shape settings).

## Reduce what needs compiling
- Regional compilation: compile the repeated transformer block once, not the whole model.
- Mark dynamic dimensions (`torch._dynamo.mark_dynamic`) to avoid a recompile per sequence length; or pad to a few buckets.
- Use `mode="max-autotune-no-cudagraphs"` or default mode in dev; reserve autotune for production builds with cached results (all four mode names are documented in the `torch.compile` page).

## Warmup in serving
Run representative shapes (each batch-size bucket) at start-up before marking the pod ready; tie the readiness probe to warmup completion.

## Verify
- [ ] `TORCH_LOGS=+inductor` or `torch._dynamo.utils.counters["inductor"]` shows fxgraph cache hits on the second start.
- [ ] Measure time-to-first-step before/after with a cold container.
