---
id: computing-software.ai-ml-engineering.pytorch.torch-compile-modes-and-max-autotune
name: torch-compile-modes-and-max-autotune
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, compile-modes, max-autotune, torch-compile, reduce-overhead, inductor]
level: practitioner
status: docs-checked
description: "Pick torch.compile modes (default, reduce-overhead, max-autotune) and options like dynamic and fullgraph by workload, and measure compile time vs steady-state gain."
sources:
  - https://github.com/pytorch/pytorch/blob/main/torch/__init__.py
  - https://github.com/pytorch/pytorch/blob/main/torch/_inductor/config.py
  - https://github.com/pytorch/pytorch/blob/main/docs/source/torch.compiler_api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# torch.compile modes

```python
model = torch.compile(model, mode="default", dynamic=None, fullgraph=False)
```

## Modes
| Mode | What it does | Use when |
|---|---|---|
| `default` | balance between performance and overhead | start here |
| `reduce-overhead` | CUDA graphs to cut Python overhead; useful for small batches; can use more memory (workspace is cached); not guaranteed to apply (CUDA-only graphs that do not mutate inputs) | small batches, many tiny kernels |
| `max-autotune` | Triton or template-based matmuls and Triton convolutions on supported devices; CUDA graphs on by default on GPU | long-running jobs where extra compile time pays off |
| `max-autotune-no-cudagraphs` | like `max-autotune` without CUDA graphs | when CUDA graphs do not fit |

`torch._inductor.list_mode_options()` shows the exact options each mode sets. Set `TORCH_LOGS=perf_hints` to see why CUDA graphs were skipped.

## Key options
- `dynamic=None` (default): detect dynamism and compile a more dynamic kernel on recompile. `dynamic=False` never generates dynamic kernels (always specialises). `dynamic=True` tries up-front to be as dynamic as possible. Debug over-specialisation with `TORCH_LOGS=dynamic`.
- `fullgraph=True`: require the whole function to be captured in one graph; graph breaks raise an error.
- `options={...}` passes backend options, for example `max_autotune`, `epilogue_fusion` (requires `max_autotune`), `shape_padding`, `triton.cudagraphs`, `fallback_random` (accuracy debugging), `trace.enabled`.
- `backend="inductor"` is the default; `torch._dynamo.list_backends()` lists in-tree backends.

## Costs
- Each frame can be compiled several times after guard failures (`TORCH_LOGS=guards` to debug), up to `torch._dynamo.config.recompile_limit`, which defaults to 8; beyond that it falls back to eager. Per-call override: the `recompile_limit` argument of `torch.compile`.
- Inductor's FX graph cache is controlled by the `fx_graph_cache` config and the `TORCHINDUCTOR_FX_GRAPH_CACHE` environment variable.

## Measuring
```python
for _ in range(3): model(x)            # warmup and compile
torch.cuda.synchronize(); t = time.perf_counter()
for _ in range(50): model(x)
torch.cuda.synchronize(); print((time.perf_counter() - t) / 50)
```
Compare against eager and report compile time separately. Measure training over many steps.

## Checked
2026-11-01. Confirmed in the torch.compile docstring (torch/__init__.py): the four modes and their descriptions, dynamic and fullgraph semantics, options list, recompile_limit default 8 with eager fallback, TORCH_LOGS values, list_mode_options; in torch/_inductor/config.py: fx_graph_cache and its environment variable. Removed (not confirmed): speedup ratios, mark_dynamic, aot_eager bisect advice, cache directory variable, cache-artifact API, input-buffer overwrite claim, assert_close tolerances, repro_after.
Method: documentation only; no commands were run.
