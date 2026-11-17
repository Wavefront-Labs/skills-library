---
id: computing-software.ai-ml-engineering.pytorch.torch-tensorrt-compilation
name: torch-tensorrt-compilation
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, torch-tensorrt, tensorrt, inference-optimization, int8, fp16, nvidia]
level: practitioner
status: docs-checked
description: "Compile PyTorch models with Torch-TensorRT via torch.compile or ahead-of-time export: precisions, dynamic shapes, fallback ops, saving engines and checking accuracy and speed."
sources:
  - https://pytorch.org/TensorRT/
  - https://pytorch.org/TensorRT/user_guide/torch_compile.html
  - https://pytorch.org/TensorRT/user_guide/saving_models.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Torch-TensorRT compilation

Torch-TensorRT converts supported subgraphs to TensorRT engines and leaves the rest in PyTorch. Install the build matching your torch and CUDA (`pip install torch-tensorrt` from the same index as torch).

## JIT via torch.compile (quickest)
```python
import torch_tensorrt
model = model.eval().cuda()
opt = torch.compile(model, backend="tensorrt", options={"min_block_size": 3})
# the precision option name differs by release (`precision` in the CompilationSettings listing); check the docs for yours
opt(x)   # compilation is triggered by the first call with real inputs
```
Good for experimentation. `min_block_size` defaults to 5 in the documented settings.

## Ahead-of-time (deployment)
```python
inputs = [torch_tensorrt.Input(min_shape=(1, 3, 224, 224), opt_shape=(8, 3, 224, 224),
                               max_shape=(32, 3, 224, 224), dtype=torch.float16)]
trt_gm = torch_tensorrt.compile(model.half(), ir="dynamo", inputs=inputs, workspace_size=1 << 30)  # workspace_size default is 0
torch_tensorrt.save(trt_gm, "model.ep", arg_inputs=[torch.randn(8, 3, 224, 224, device="cuda").half()])  # ExportedProgram
# or output_format="torchscript" with a .ts file for C++ deployment (the docs: ExportedProgram saves are Python-runtime only)
loaded = torch.export.load("model.ep").module()
```
- `opt_shape` is what TensorRT tunes kernels for; set it to the production batch.

## Precision
- The torch.compile guide documents FP16 and FP32 layers and says INT8/quantization support was slated for a future release; check the current docs before planning INT8.
- Always check accuracy against the eager model after lowering precision.

## Fallback and partitioning
- Unsupported ops run in PyTorch; `min_block_size` is the minimum number of operators per TensorRT engine block. `debug=True` prints verbose debugging information.
- `torch_executed_ops` is a sequence of operations to run in Torch regardless of converter coverage (use it when a converter is wrong).

## Verify
```python
with torch.no_grad():
    ref, out = model(x).float(), trt_gm(x.half()).float()
print((ref - out).abs().max(), torch.allclose(ref, out, atol=1e-2, rtol=1e-2))
```
Benchmark with CUDA events after warm-up, at production batch sizes, against plain `torch.compile` (Inductor); keep Torch-TensorRT only if it wins on your model.

## Alternatives
ONNX export into TensorRT directly, or a dedicated LLM serving stack for large language models.

## Checked

2026-11-02. Confirmed against the Torch-TensorRT home, torch.compile backend and saving-models pages: `torch.compile(model, backend="tensorrt")` (and `"torch_tensorrt"`); `ir="dynamo"` compile; `torch_tensorrt.save(..., arg_inputs=...)` with `output_format="torchscript"` for C++ deployment and the ExportedProgram Python-runtime note; `min_block_size` (default 5), `workspace_size` (default 0), `debug`, `torch_executed_ops` meanings; `Input(min_shape, opt_shape, max_shape)`; the note that INT8 support was slated for a future release. Fixed: save keyword `arg_inputs` (not `inputs`); removed `enabled_precisions` (not on the fetched pages; the settings list shows `precision`), the 2-4x speedup, the INT8 calibration/ModelOpt route, the GPU-architecture engine claim, the 'engines rebuild' remark, `trtexec`, `mode="max-autotune"` and the TensorRT-LLM remark.

Method: documentation only; no commands were run.
