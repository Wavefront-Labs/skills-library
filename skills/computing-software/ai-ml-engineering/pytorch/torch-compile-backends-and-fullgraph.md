---
id: computing-software.ai-ml-engineering.pytorch.torch-compile-backends-and-fullgraph
name: torch-compile-backends-and-fullgraph
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, compile-backends, fullgraph, torch-compile, inductor, aot-eager, custom-backend]
level: practitioner
status: gated
description: "Choose torch.compile backends (inductor, cudagraphs, aot_eager, eager, tensorrt), bisect bugs by backend, write a debug backend and use fullgraph=True to enforce capture."
sources:
  - https://pytorch.org/docs/stable/torch.compiler.html
  - https://pytorch.org/docs/stable/torch.compiler_custom_backends.html
  - https://pytorch.org/docs/stable/generated/torch.compile.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compiler backends and fullgraph=True

`torch.compile(model, backend=..., fullgraph=..., mode=...)`. Dynamo captures FX graphs from Python bytecode; the **backend** turns each graph into runnable code.

## Backends
```python
import torch._dynamo as dynamo
print(dynamo.list_backends())                # stable ones; list_backends(None) includes experimental
# torch 2.14 CPU build: ['cudagraphs', 'inductor', 'openxla', 'tvm']; list_backends(None) adds eager, aot_eager,
# aot_eager_decomp_partition, ts, aot_ts, pre_dispatch_eager, invoke_subgraph, eager_debug and TESTING_ONLY/minifier backends
```
| Backend | What it does | Use |
|---|---|---|
| `inductor` (default) | TorchInductor codegen; the docs page lists it as the default backend (Triton on GPU and C++ on CPU is not run here: no GPU and no C++ compiler on this machine) (gated: unconfirmed, source is paywalled or blocked) | production speed |
| `cudagraphs` | "CUDA graphs with AOT Autograd" (docs); needs a GPU, not run (gated: unconfirmed, source is paywalled or blocked) | launch-bound inference, small batches |
| `aot_eager` | AOTAutograd tracing, eager kernels | debugging: isolates AOT/functionalization |
| `eager` | Dynamo capture only, run original ops | debugging: isolates Dynamo |
| `tensorrt` | Torch-TensorRT; the docs say it requires `import torch_tensorrt` in the calling script to register the backend (not run) (gated: unconfirmed, source is paywalled or blocked) | NVIDIA inference |
| `openxla`, `tvm` | external compilers, listed by `list_backends()`; the docs list `ipex` for CPU too (not run) (gated: unconfirmed, source is paywalled or blocked) | specific hardware |

`backend="onnxrt"` is not a backend on torch 2.14: `torch.compile(m, backend="onnxrt")` raises `Invalid backend: 'onnxrt'`.

`torch._inductor.list_mode_options()` on 2.14: `reduce-overhead` = `{'triton.cudagraphs': True}`; `max-autotune` = `{'max_autotune': True, 'triton.cudagraphs': True, 'coordinate_descent_tuning': True}`; `max-autotune-no-cudagraphs` = the same without cudagraphs. The docs add that reduce-overhead only helps CUDA-only graphs that do not mutate inputs.

## Bisecting a compile bug by backend
Run the failing case with `eager`, then `aot_eager`, then `aot_eager_decomp_partition`, then `inductor`. The first backend that fails names the culprit layer (`aot_eager_decomp_partition` is in `list_backends(None)`): Dynamo, AOTAutograd, decompositions, or Inductor codegen. Report bugs with that information (and the minifier output).

## Custom debug backend
```python
def inspect_backend(gm: torch.fx.GraphModule, example_inputs):
    gm.graph.print_tabular()               # see exactly what Dynamo captured (needs `pip install tabulate`, otherwise compilation fails with ModuleNotFoundError)
    return gm.forward                      # run it unchanged
opt = torch.compile(model, backend=inspect_backend)
```
Counting how many times this is called equals the number of graphs (graph breaks + recompiles): a function with one `@torch.compiler.disable` call compiled as 2 graphs.

## fullgraph=True
- Default `fullgraph=False`: on unsupported Python, Dynamo breaks the graph, runs that bit in Python, and resumes. Silent and correct but slower.
- `fullgraph=True`: any graph break raises with the reason and location. Use it:
  - while optimising a model to prove the forward is one graph,
  - for `torch.export`-style requirements and CUDA graphs (breaks defeat them),
  - in CI to stop regressions that introduce breaks.
- Measured on torch 2.14 with `fullgraph=True`: `print(...)` raises `Unsupported: Failed to trace builtin operator`; `if y.sum() > 0:` raises `Unsupported: Data-dependent branching`; a call to a `torch.compiler.disable`d function raises `Unsupported: Skip calling torch.compiler.disable()d function`. But `.item()` compiled in one graph and a generator inside the function compiled too (both were breaks in older advice); without `fullgraph`, `.item()` gave 2 graphs unless `torch._dynamo.config.capture_scalar_outputs = True` (then 1). `torch.cuda.synchronize` was not tried (no GPU). Fix breaks or isolate them with `torch.compiler.disable` (then fullgraph must be off for that region).

## Options worth knowing
- `dynamic=None` (default) recompiles once with dynamic shapes after seeing a size change (sizes 2, 3, 4 gave 2 compiles); `dynamic=False` specialises always (3 compiles).
- `options={"triton.cudagraphs": True, "max_autotune": True}` for fine control (both are Inductor config names); `torch._inductor.list_options()` returned 644 names.
- `torch.compiler.reset()` clears caches between experiments in one process.

## Verify
`torch._dynamo.explain(model)(x)` returns an object with `graph_count`, `graph_break_count` and `break_reasons` (a function with one `print` gave 2 graphs, 1 break, 1 reason).
