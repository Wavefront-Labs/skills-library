---
id: computing-software.ai-ml-engineering.pytorch.torch-export-and-exportedprogram
name: torch-export-and-exportedprogram
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, torch-export, model-export-pytorch, exportedprogram, dynamic-shapes, aoti, torch-cond]
level: practitioner
status: gated
description: "Capture a PyTorch model as a full graph with torch.export: example inputs, Dim-based dynamic shapes, graph-break fixes with torch.cond, saving .pt2, and AOTInductor packaging."
sources:
  - https://pytorch.org/docs/stable/export.html
  - https://pytorch.org/tutorials/intermediate/torch_export_tutorial.html
  - https://pytorch.org/docs/stable/torch.compiler_aot_inductor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# torch.export and ExportedProgram

**Goal:** a sound, Python-free graph of the model for deployment runtimes (AOTInductor, ExecuTorch, TensorRT, ONNX), with explicit dynamic dimensions.

## Export
```python
import torch
from torch.export import export, Dim
model = MyModel().eval()
x = torch.randn(4, 3, 224, 224)
batch = Dim("batch", min=1, max=64)
ep = export(model, (x,), dynamic_shapes={"x": {0: batch}})
print(ep.graph_module.code)           # inspect the captured ATen-level graph
torch.export.save(ep, "model.pt2")
ep2 = torch.export.load("model.pt2")
out = ep2.module()(torch.randn(8, 3, 224, 224))
```
- Unlike `torch.compile`, export does **not** fall back to Python on unsupported code: it errors, telling you exactly what to fix.
- Without `dynamic_shapes`, every dimension is specialised to the example's size; a different batch size then fails at runtime (`AssertionError: Guard failed: x.size()[0] == 4`). With `Dim("batch", min=1, max=64)` a batch of 65 fails with `Guard failed: x.size()[0] <= 64`.
- `export` defaults to `strict=False` in torch 2.14 (checked from the signature): non-strict traces with Python semantics; strict mode uses TorchDynamo and is more conservative.

## Fixing export errors
- **Data-dependent control flow** (`if x.sum() > 0:` raises `GuardOnDataDependentSymNode: Could not guard on data-dependent expression`): replace with `torch.cond(pred, true_fn, false_fn, (x,))`, or move the branch outside the model.
- **Shape constraints violated** ("specialized to a constant"): your code forces a dimension (e.g. reshape with a hard-coded batch); rewrite with `-1` or relate dims (`Dim` arithmetic like `2 * batch`).
- **Unsupported Python** (logging, NumPy calls, `.item()` driving shapes): remove from `forward` or guard with `torch.compiler.is_exporting()`.
- `torch.export.draft_export(model, args)` (exists in 2.14; ran on a data-dependent `if` model and returned an `ExportedProgram`) records the issues instead of stopping at the first one.

## Running it: AOTInductor
This snippet needs a C++ compiler and a CUDA device and could not be run on the CPU-only Windows test host, so treat it as unconfirmed beyond the API names (`torch._inductor.aoti_compile_and_package` and `aoti_load_package` exist in 2.14) (gated: unconfirmed, source is paywalled or blocked).
```python
path = torch._inductor.aoti_compile_and_package(ep, package_path="model_aoti.pt2")
runner = torch._inductor.aoti_load_package(path)
y = runner(torch.randn(8, 3, 224, 224).cuda())
```
Compiles to a shared library loadable from Python or C++ without the Python model code (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Exported program's outputs match eager on several input shapes within tolerance.
- [ ] Dynamic dims declared for every axis that varies in production.
- [ ] `.pt2` loads in a fresh process without the model's Python source.
