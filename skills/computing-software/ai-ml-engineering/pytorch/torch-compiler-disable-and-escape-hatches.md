---
id: computing-software.ai-ml-engineering.pytorch.torch-compiler-disable-and-escape-hatches
name: torch-compiler-disable-and-escape-hatches
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, compiler-disable, allow-in-graph, torch-compile, graph-breaks, substitute-in-graph, dynamo]
level: practitioner
status: gated
description: "Use torch.compile escape hatches: torch.compiler.disable, allow_in_graph, is_compiling, assume_constant_result and custom ops to keep unsupported code out of capture."
sources:
  - https://pytorch.org/docs/stable/torch.compiler_fine_grain_apis.html
  - https://pytorch.org/docs/stable/generated/torch.compiler.disable.html
  - https://pytorch.org/docs/stable/generated/torch.compiler.allow_in_graph.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# torch.compile escape hatches

When part of a model cannot or should not be traced, mark it explicitly instead of letting Dynamo guess.

## torch.compiler.disable
```python
@torch.compiler.disable
def log_stats(t):                # runs eagerly; Dynamo breaks the graph around the call
    wandb.log({"mean": t.mean().item()})
@torch.compiler.disable(recursive=False)
def outer(x): return inner(x)    # skip only this frame; inner() is still compiled
```
- Each disabled call is a graph break: compiled code before and after it runs as separate graphs (measured: 2 graphs for a function with one disabled call). Put disabled calls at block boundaries, not inside hot inner loops.
- Works on modules too: `torch.compiler.disable(module.forward)` or decorate the method.
- Not allowed with `fullgraph=True` on the path that calls it (raises `Unsupported: Skip calling torch.compiler.disable()d function`).

## torch.compiler.allow_in_graph
```python
torch.compiler.allow_in_graph(my_fn)
```
`torch.compiler.allow_in_graph` exists on 2.14 (not exercised here: needs an inductor/AOT run to prove the claims below) (gated: unconfirmed, source is paywalled or blocked). Dynamo inserts `my_fn` as a single opaque node without tracing inside it. The function must be traceable by AOTAutograd (pure tensor ops, no side effects, no data-dependent Python control flow on tensor values). It is a sharp tool: guards are not installed on its internals, so behaviour changes inside it are not detected. Prefer `torch.library.custom_op` (with `register_fake`; both exist on 2.14) for real opaque kernels (C extensions, NumPy, Triton launchers): it gets a fake (meta) implementation and works with export (not run here). (gated: unconfirmed, source is paywalled or blocked)

## torch.compiler.is_compiling
```python
if not torch.compiler.is_compiling():
    check_invariants(x)          # skipped while tracing, no graph break
```
Measured: a function returning `x+1` under `is_compiling()` and `x` otherwise gave `x` in eager and `x+1` under `torch.compile(backend="eager")`.
Use for asserts, logging and debug paths.

## Other fine-grain APIs
- `torch.compiler.assume_constant_result(fn)`: Dynamo calls it once and bakes the result in (configuration lookups). Wrong if the value changes. (The function exists on 2.14; the baking behaviour was not run.) (gated: unconfirmed, source is paywalled or blocked)
- `torch._dynamo.config.capture_scalar_outputs = True`: lets `.item()` stay in graph as a symbolic value instead of breaking (2 graphs became 1 in a run).
- `torch.compiler.substitute_in_graph(original_fn)(replacement)`: provide a traceable Python version of a C function Dynamo cannot read (exists on 2.14; usage not run). (gated: unconfirmed, source is paywalled or blocked)
- `torch._dynamo.mark_dynamic(x, dim)` and `mark_static`: control shape specialisation per input dim.
- `torch.compiler.set_stance("force_eager")` (first release not checked; present in 2.14, and the backend was never called inside it): disable compilation globally at runtime, e.g. for a debug run, without editing call sites.

## Choosing
| Situation | Hatch |
|---|---|
| Logging, metrics, Python side effects | `disable` or `is_compiling` guard |
| Third-party C/NumPy code on tensors | `torch.library.custom_op` + `register_fake` |
| Pure torch function Dynamo traces badly | `allow_in_graph` |
| Whole model temporarily eager | `set_stance("force_eager")` |

## Verify
`TORCH_LOGS=graph_breaks python train.py` should list only the breaks you introduced deliberately. `torch._dynamo.explain(fn)(x)` also reports `graph_break_count`.
