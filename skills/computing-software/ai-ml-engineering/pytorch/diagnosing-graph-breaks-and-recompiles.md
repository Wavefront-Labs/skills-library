---
id: computing-software.ai-ml-engineering.pytorch.diagnosing-graph-breaks-and-recompiles
name: diagnosing-graph-breaks-and-recompiles
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, graph-breaks, torch-logs, tlparse, recompiles, dynamo-explain]
level: practitioner
status: verified
description: "Find and fix torch.compile graph breaks and recompilations with TORCH_LOGS, torch._dynamo.explain, tlparse and fullgraph, and know the usual Python causes."
sources:
  - https://pytorch.org/docs/stable/torch.compiler_troubleshooting.html
  - https://github.com/pytorch/tlparse
  - https://pytorch.org/docs/stable/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing graph breaks and recompiles

A graph break splits the model into several graphs with eager Python in between: less fusion, more overhead. A recompile re-traces because a guard failed (new shape, dtype, Python value). Both silently eat the speedup.

## Find graph breaks
```bash
TORCH_LOGS="graph_breaks" python train.py        # each break with reason and source line (run: it printed "Graph break from `Tensor.item()` ... consider setting capture_scalar_outputs = True" with the user line)
TORCH_LOGS="recompiles" python train.py          # which guard failed and why
TORCH_LOGS="+dynamo" python train.py             # very verbose
```
```python
exp = torch._dynamo.explain(model)(x)
print(exp.graph_count, exp.graph_break_count)
for b in exp.break_reasons: print(b)
```
Run on torch 2.14 with the default backend settings (using `backend="eager"` since Inductor needs a C++ compiler the test host lacks): `explain` gave 2 graphs and 1 break for `x * x.sum().item()` (reason "Unsupported Tensor.item() call with capture_scalar_outputs=False"), for `if x.sum() > 0:` (reason `generic_jump TensorVariable()`) and for `x[x > 0]` ("Dynamic shape operator ... aten.nonzero.default"), and 1 graph with 0 breaks for plain tensor math. The result object has `graph_count`, `graph_break_count`, `break_reasons`, `op_count`, `ops_per_graph`, `out_guards`, `compile_times`, `graphs`.
`torch.compile(model, fullgraph=True)` turns the first break into an exception with a stack trace (run: `Unsupported ... Data-dependent branching` for the `if` example).

## tlparse for whole-run reports
```bash
TORCH_TRACE=/tmp/trace python train.py
pip install tlparse && tlparse /tmp/trace -o report/   # HTML: graphs, breaks, recompiles, guards, compile times
```
Checked on Windows: `pip install tlparse` installs a `tlparse.exe`; `tlparse <trace log file> -o <new dir>` wrote `index.html`, `compile_directory.json` and per-compile folders (the output directory must not already exist, otherwise pass `--overwrite`). Per-rank logs for distributed jobs were not tried.

## Common causes and fixes
| Cause | Fix |
|---|---|
| `.item()` | keep values as tensors; or `torch._dynamo.config.capture_scalar_outputs = True` (run: 1 break became 0). `print(tensor)` did not break the graph on torch 2.14 (0 breaks) |
| Data-dependent `if x.sum() > 0:` | `torch.where`, or `torch.cond` |
| `x.nonzero()`, boolean mask indexing | `capture_dynamic_output_shape_ops = True` (run: 1 break became 0), or restructure with masks |
| Calling unsupported C extensions on tensors (simple NumPy calls such as `np.sin` were traced without a break on 2.14) | wrap as `torch.library.custom_op`, or `torch.compiler.disable` that function (run: a disabled helper in the middle of a function gave 1 graph break) |
| Logging, tqdm, wandb calls inside forward | move out of the compiled region |
| Changing shapes each batch (variable seq length) | pad to buckets / multiples; `mark_dynamic`. On 2.14 the first size change logged one recompile (`tensor 'x' size mismatch at index 0. expected 4, actual 5`) and later sizes then reused a dynamic-shape graph |
| Python int attributes that change (`self.step += 1` used in forward) | pass as tensor, or keep out of forward |
| Toggling `model.train()/eval()` or `no_grad` | expected: separate graph per mode, compiled once each (run: the `training` flag appears as a guard failure in the `recompiles` log) |

## Recompile limit
After the recompile limit (default 8: `torch._dynamo.config.cache_size_limit`, also exposed as `recompile_limit`) recompiles for a frame, Dynamo falls back to eager with a warning. On torch 2.14 the text is "torch._dynamo hit config.recompile_limit (8)" followed by the function, the last guard failure reason and a pointer to the recompilation docs (older releases said `config.cache_size_limit`). Reproduced by turning `automatic_dynamic_shapes` off and feeding 12 different sizes. Treat it as a bug to fix rather than raising the limit.

## Selectively exclude code
```python
@torch.compiler.disable
def debug_stats(x): ...
```
Better than letting a break land in the middle of a hot block. `TORCH_LOGS="recompiles"` printed `Recompiling function ... triggered by the following guard failure(s)` lines for a size change and a train/eval toggle.

## Verify
Target: `graph_break_count == 0` for the forward (or a small, understood number), and no "recompiles" log lines after the first few steps of training.
