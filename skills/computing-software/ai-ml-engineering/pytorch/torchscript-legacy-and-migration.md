---
id: computing-software.ai-ml-engineering.pytorch.torchscript-legacy-and-migration
name: torchscript-legacy-and-migration
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, model-export-pytorch, torchscript, torch-jit-trace, torch-jit-script, libtorch, migration]
level: practitioner
status: gated
description: "Maintain or migrate TorchScript models: trace vs script behaviour and pitfalls, freezing, loading in libtorch, and moving to torch.export / AOTInductor."
sources:
  - https://pytorch.org/docs/stable/jit.html
  - https://pytorch.org/docs/stable/export.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TorchScript (legacy) and migration

**Goal:** keep existing TorchScript deployments working and move new work to `torch.export`. On torch 2.14 under Python 3.14, `torch.jit.trace`, `script` and `load` each emit `FutureWarning: ... is not supported in Python 3.14+ and may break. Please switch to torch.compile or torch.export`, and `torch.jit.freeze` emits `FutureWarning: torch.jit.freeze is deprecated. Please use torch.compile instead`.

## trace vs script
```python
traced = torch.jit.trace(model.eval(), example_input)     # records ops for this input
scripted = torch.jit.script(model)                        # compiles Python source (subset)
traced.save("model_traced.pt"); torch.jit.load("model_traced.pt")
```
- **trace** records one execution: Python control flow is frozen to the path taken by the example. A branch on input values or a loop over sequence length silently becomes constant. Measured with `if x.sum()>0: ...`: traced on an all-ones input, the traced module returned -4.27 for an all-negative input where eager returned 8.0, and tracing printed `TracerWarning: Converting a tensor to a Python boolean might cause the trace to be incorrect`. Treat every `TracerWarning` as a potential silent bug.
- **script** keeps control flow but supports only a typed subset of Python; many libraries' models fail with compilation errors and need type annotations or rewrites.
- Mixed: script the control-flow parts, trace the rest (`@torch.jit.script` functions called from a traced module): a traced module calling a scripted function with an `if` still took the right branch on a negative input (16.0, as expected).

## Common pitfalls
- Tracing in `train()` mode bakes in dropout/batchnorm training behaviour (a module traced in train mode gave different outputs on two identical calls) - call `.eval()` first.
- Device is captured: trace on the device you'll run on, or ensure no hard-coded `.cuda()` in forward (not tested: no GPU) (gated: unconfirmed, source is paywalled or blocked).
- `torch.jit.freeze(scripted.eval())` inlines weights and folds constants (the frozen module's `named_parameters()` was empty, so it cannot be fine-tuned); freezing a train-mode module raises `Freezing is currently only implemented for modules in eval mode`. The speedup was not timed here.
- Validate traced output vs eager on inputs of other shapes than the example.

## Loading in C++ (libtorch)
The C++ below was not compiled or run (no C++ toolchain here) (gated: unconfirmed, source is paywalled or blocked); the Python `torch.jit.load` of a saved traced module returned a `RecursiveScriptModule`.
```cpp
torch::jit::script::Module m = torch::jit::load("model_traced.pt");
auto out = m.forward({input_tensor}).toTensor();
```
Keep libtorch and PyTorch versions matched; forward compatibility of saved files is limited (not tested) (gated: unconfirmed, source is paywalled or blocked).

## Migrating
1. Get `torch.export.export(model, example_args, dynamic_shapes=...)` to succeed. A module with `if x.sum()>0` fails with `GuardOnDataDependentSymNode: Could not guard on data-dependent expression`; the same logic written with `torch.cond(pred, true_fn, false_fn, (x,))` exported; `dynamic_shapes={"input": {0: Dim("b")}}` worked on `nn.Linear` (the key is the forward argument name).
2. Deploy with AOTInductor (`torch._inductor.aoti_compile_and_package` exists, but compiling needs a C++ compiler and was not run here) for server C++/Python, ExecuTorch for mobile/edge, or ONNX / TensorRT (not run). `torch.onnx.export(model.eval(), args, dynamo=True)` works on 2.14 (`dynamo=True` is now the default; the result saved and onnxruntime reproduced the torch output exactly on `nn.Linear`; it needs `onnx` and `onnxscript` installed).
3. Compare outputs and latency vs the TorchScript artifact before switching traffic.

## Verify
- [ ] No TracerWarnings unaddressed in existing traced models.
- [ ] Traced/scripted output equals eager across representative shapes.
- [ ] Migration target chosen and parity-tested.
