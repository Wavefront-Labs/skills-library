---
id: computing-software.ai-ml-engineering.pytorch.aotinductor-packaging
name: aotinductor-packaging
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, aotinductor, aoti-compile-and-package, torch-export, inference-deployment]
level: practitioner
status: docs-checked
description: "Ahead-of-time compile an exported PyTorch model into a .pt2 package with aoti_compile_and_package and load it back with aoti_load_package."
sources:
  - https://github.com/pytorch/pytorch/blob/main/torch/_inductor/__init__.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AOTInductor packaging

**Goal:** ship a pre-compiled model artifact so start-up does not pay a JIT compile.

## Flow: export, compile, package, load
```python
import torch

ep = torch.export.export(model, example_inputs)      # an ExportedProgram
path = torch._inductor.aoti_compile_and_package(ep, package_path="model.pt2")
runner = torch._inductor.aoti_load_package("model.pt2")
out = runner(*example_inputs)
```
- `aoti_compile_and_package(..., package_path=None, inductor_configs=None)`: `package_path` is a file ending in `.pt2`, `None`, or a writable seekable buffer; any other value is rejected.
- `inductor_configs` is an optional dict of Inductor configs for the compile.
- The docstring says you no longer need to pass args/kwargs to it; pass the `ExportedProgram`.
- These live in the private `torch._inductor` namespace, so check the signature on each PyTorch upgrade.

## Verify
- [ ] Output of the loaded package equals eager output within tolerance for the input shapes you serve.
- [ ] Rebuild and retest the package after every PyTorch upgrade.

## Checked
2026-11-01. Confirmed in `torch/_inductor/__init__.py` docstrings and code: `aoti_compile_and_package` and `aoti_load_package`, the `package_path` and `inductor_configs` parameters, the `.pt2` requirement. Removed: dynamic-shape `Dim` example, C++ loader call, what is baked into the artifact, pitfalls list and `max_autotune` option, which were not confirmed from the source.
Method: documentation only; no commands were run.
