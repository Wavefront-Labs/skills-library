---
id: computing-software.computer-graphics-engineering.computer-vision.onnx-export-and-model-conversion
name: onnx-export-and-model-conversion
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-deep-learning, onnx-export, onnx, onnxruntime, tensorrt, model-conversion]
level: practitioner
status: gated
description: "Export PyTorch vision models to ONNX and convert onward: torch.onnx.export/dynamo, opsets, dynamic axes, onnxsim, ONNX Runtime checks, then TensorRT/OpenVINO/CoreML/TFLite."
sources: ["https://pytorch.org/docs/stable/onnx.html", "https://onnxruntime.ai/docs/", "https://github.com/daquexian/onnx-simplifier", "https://docs.nvidia.com/deeplearning/tensorrt/latest/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ONNX export and model conversion

## Export
```python
model.eval()
x = torch.randn(1, 3, 640, 640)
torch.onnx.export(model, (x,), "model.onnx", opset_version=17,
                  input_names=["images"], output_names=["out"],
                  dynamic_axes={"images": {0: "batch"}, "out": {0: "batch"}})
# PyTorch 2.14.1 (tested): dynamo=True is the DEFAULT and needs `pip install onnxscript`;
# add dynamo=False for the TorchScript-based exporter used by this call
```
- `model.eval()` first (dropout/BN).
- In PyTorch 2.14.1 the default (dynamo) exporter, given `opset_version=17`, warned and exported opset 18, and wrote the weights to a separate `model.onnx.data` file next to `model.onnx` (copy both); with `dynamo=False` the result was a single opset-17 file. Both loaded and passed `onnx.checker.check_model`.
- Dynamic axes only where needed; static spatial sizes convert more reliably to TensorRT/OpenCV.
- Data-dependent Python control flow is traced for the example input only; check behaviour on
  other inputs.
- Unsupported ops: rewrite them (e.g. avoid in-place index assignment, `torch.where` with
  scalars, custom CUDA ops).

## Simplify and check
```bash
python -m onnxsim model.onnx model.sim.onnx
python -c "import onnx; m=onnx.load('model.sim.onnx'); onnx.checker.check_model(m)"
```
Inspect the graph with Netron.

## Validate numerically
```python
import onnxruntime as ort
s = ort.InferenceSession("model.sim.onnx", providers=["CPUExecutionProvider"])
o = s.run(None, {"images": x.numpy()})[0]
print(np.abs(o - model(x).detach().numpy()).max())   # expect < 1e-4 for FP32 (ResNet-18 measured 3.5e-6)
```
Test several random inputs plus real images.

## Onward conversion
None of the onward tools below were run here (no GPU, TensorRT, OpenVINO, CoreML or TFLite toolchains) (gated: unconfirmed, source is paywalled or blocked).
- TensorRT: `trtexec --onnx=model.onnx --saveEngine=model.engine --fp16` (engines are GPU- and
  TensorRT-version specific).
- OpenVINO: `ovc model.onnx` or `openvino.convert_model`.
- CoreML: `coremltools.convert` from a traced TorchScript/ExportedProgram (ONNX path deprecated).
- TFLite: via `ai-edge-torch` or onnx2tf; check layout (NHWC) and quantisation.

## Gotchas
Preprocessing (resize, normalise) is usually outside the graph: document it or bake it in.

## Checked
PyTorch 2.14.1 CPU, onnx 1.23.2, onnxscript, onnxsim 0.8.1, onnxruntime 1.31.0.
- Run: ResNet-18 export with `opset_version=17, dynamo=False` (single file), with default dynamo (failed without onnxscript, then ran: opset 18, external .data file) and `dynamo=True`; `python -m onnxsim` (returned 0), `onnx.checker.check_model`, ONNX Runtime CPU with batch 1 and batch 4 (dynamic axis worked), max abs difference 3.5e-6.
- Not run: TensorRT, OpenVINO, CoreML, TFLite conversions; gated.
