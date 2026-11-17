---
id: computing-software.ai-ml-engineering.pytorch.executorch-on-device-deployment
name: executorch-on-device-deployment
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, model-export-pytorch, executorch, on-device, xnnpack, pte, mobile-inference, edge-ai]
level: practitioner
status: docs-checked
description: "Deploy PyTorch models to mobile and edge with ExecuTorch: export, lowering to backends (XNNPACK, Core ML, Qualcomm) via partitioners, .pte files and host-side validation."
sources:
  - https://pytorch.org/executorch/stable/index.html
  - https://pytorch.org/executorch/stable/getting-started.html
  - https://pytorch.org/executorch/stable/backends-xnnpack.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-device deployment with ExecuTorch

**Goal:** run a PyTorch model on Android/iOS/embedded devices with a small runtime and hardware acceleration.

## Export and lower
```python
import torch
from torch.export import export
from executorch.exir import to_edge_transform_and_lower
from executorch.backends.xnnpack.partition.xnnpack_partitioner import XnnpackPartitioner

model = MyModel().eval()
example = (torch.randn(1, 3, 224, 224),)
ep = export(model, example)
prog = to_edge_transform_and_lower(ep, partitioner=[XnnpackPartitioner()]).to_executorch()
with open("model.pte", "wb") as f:
    f.write(prog.buffer)
```
- The backend is chosen by the `partitioner` argument of `to_edge_transform_and_lower`. The backends overview lists XNNPACK (CPU, all platforms, general-purpose and the fallback), Core ML (iOS, macOS), Vulkan (Android GPU), Qualcomm (Android NPU) and Arm Ethos-U (embedded NPU), among others.
- Operators the delegate does not support run on the portable CPU fallback, giving partial acceleration; you can list several partitioners in priority order.
- To support several platforms, generate a dedicated `.pte` file per backend.
- Getting started suggests XNNPACK for Android and Core ML or XNNPACK for iOS as a first step.

## Quantize
The XNNPACK delegate can run symmetrically quantized models (8-bit); see the XNNPACK Quantization page of the ExecuTorch docs for schemes and APIs. Measure accuracy on the lowered model, not just in PyTorch.

## Run
- Host check: the ExecuTorch Python runtime APIs (`runtime.load_program("model.pte")`) validate a `.pte` before you go on-device and can be used to evaluate accuracy.
- Android: the runtime is published to Maven Central (`org.pytorch:executorch-android`); iOS ships via a Swift Package Manager package (with Core ML and XNNPACK acceleration). Load the `.pte` with the `Module` API.
- The XNNPACK delegate is included by default in the published Android, iOS and pip packages; building from source needs `-DEXECUTORCH_BUILD_XNNPACK=ON`.

## Verify
- [ ] `.pte` outputs match eager within tolerance on test inputs.
- [ ] The hot ops are delegated to the intended backend.
- [ ] On-device latency, memory and app size measured on the target device.

## Checked
2026-11-01. Confirmed in the ExecuTorch docs source (docs/source: getting-started.md, backends-overview.md, backends/xnnpack/xnnpack-overview.md).
Removed: the MPS backend claim, the static-shape advice, PT2E and per-channel quantizer specifics, LLM export-flow claims, and the version-match, binary-size and thermal-throttling gotchas.
Method: documentation only; no commands were run.
