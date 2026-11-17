---
id: computing-software.ai-ml-engineering.pytorch.torch-export-dynamic-dims-and-failure-triage
name: torch-export-dynamic-dims-and-failure-triage
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, export-dynamic-dims, torch-export, dynamic-shapes, draft-export, guards, data-dependent]
level: practitioner
status: verified
description: "Mark dynamic dimensions in torch.export with Dim and Dim.AUTO, read constraint violations and data-dependent errors, and triage export failures with draft_export and strict=False."
sources:
  - https://pytorch.org/docs/stable/export.html
  - https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/export/programming_model.html
  - https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/export/draft_export.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dynamic dims in torch.export and failure triage

By default `torch.export.export(model, args)` specialises every dimension to the example input's sizes. Serving with any other batch size then fails.

## Declaring dynamic dims
```python
from torch.export import export, Dim
batch = Dim("batch", min=1, max=1024)
seq = Dim("seq", min=1, max=4096)
ep = export(model, (ids, mask), dynamic_shapes={"ids": {0: batch, 1: seq}, "mask": {0: batch, 1: seq}})
print(ep.range_constraints)
```
- `dynamic_shapes` mirrors the forward signature (dict by arg name, or tuple by position); nested inputs use nested structures.
- Shared `Dim` objects assert equality between dims.
- `Dim.AUTO` lets export infer whether each dim is dynamic and what relations hold; `Dim.STATIC` forces specialisation. AUTO is the easiest start, then read `ep.range_constraints`.
- Example inputs of size 0 or 1 get specialised (0/1 specialisation); use example batch >= 2. Run here: an example batch of 1 with `Dim("batch", min=1, ...)` raised `Constraints violated (batch)! ... You marked batch as dynamic but your code specialized it to be a constant (1)`, while `Dim.AUTO` on the same input just left that dim static and exported.
- Measured on torch 2.14: `Dim("batch", min=1, max=1024)` gives `ep.range_constraints` `{s23: VR[1, 1024], ...}`; `Dim.AUTO` on both dims gave `VR[2, int_oo]` for each; `Dim.STATIC` on dim 1 left only dim 0 symbolic. A nested input (dict holding a tuple) takes a matching nested `dynamic_shapes` structure.

## Reading errors
- **Constraint violation** (`UserError: Constraints violated (batch)!`): the message says either "You marked batch as dynamic but your code specialized it to be a constant (1)" or, for two separate `Dim`s on dims that must match, "The values of b ... and a ... must always be equal. Suggested fixes: b = a" (both reproduced on 2.14). It usually means a hidden assumption in the model or inputs. Apply the suggested fix (share one `Dim`), use a larger example, or remove the assumption. Other suggestions you may see in the message, such as `Dim(..., min=2)` or `2*_seq` relations, were not reproduced here.
- **Data-dependent error** (`GuardOnDataDependentSymNode: Could not guard on data-dependent expression Eq(u0, 1)`): reproduced by `if x.sum() > 0:`. In 2.14 slicing with `n.item()` exported without error (it creates unbacked symbols `u0`, `u1` with runtime asserts), so `.item()` alone is not always fatal. Fixes: `torch._check(k >= 0)` hints (accepted and exported here), `torch.cond` for branching on values, or move the logic out of the exported region.
- **Unsupported Python** (strict mode): try `export(..., strict=False)` (default in recent versions), which traces with Python running normally and is far more permissive.

## Triage workflow
1. `strict=False` first.
2. `torch.export.draft_export(model, args)` returns an `ExportedProgram` even when it cannot soundly produce a graph and logs `WARNING: 1 issue(s) found ...`; inspect `print(ep._report)` or run `tlparse <log id> --export` for an HTML report (both named in the warning text). Fix the issues one by one.
3. `TORCH_LOGS="+dynamic"` shows where each guard on a symbol was added (the error message itself tells you to set it).
4. Custom ops without fake kernels fail under fake tensors: add `register_fake` (run: `RuntimeError: There was no fake impl registered for <CustomOpDef(mylib::nofake)> ...`).

## Validate
```python
for b, s in [(1, 7), (33, 512), (1024, 4096)]:
    torch.testing.assert_close(ep.module()(*make(b, s)), model(*make(b, s)))
```
Test boundary values of every Dim range, not just the example size.
