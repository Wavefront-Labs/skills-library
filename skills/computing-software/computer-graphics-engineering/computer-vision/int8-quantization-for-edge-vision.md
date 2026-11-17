---
id: computing-software.computer-graphics-engineering.computer-vision.int8-quantization-for-edge-vision
name: int8-quantization-for-edge-vision
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, vision-deep-learning, int8-quantization, edge-inference, post-training-quantization, calibration-dataset, tensorrt, onnxruntime-quantization, qat, jetson]
level: advanced
status: gated
description: "Deploy vision models on edge devices with INT8: post-training quantisation with a representative calibration set, per-channel weights, sensitive layers, QAT fallback."
sources: ["https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html", "https://docs.nvidia.com/deeplearning/tensorrt/developer-guide/index.html#working-with-int8", "https://arxiv.org/abs/1712.05877", "https://ai.google.dev/edge/litert/models/post_training_quantization"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# INT8 quantisation for edge vision

**Goal:** 2–4x faster, 4x smaller detection/segmentation models on Jetson, mobile NPUs,
Intel CPUs or microcontrollers with < 1% accuracy loss.

## 1. Post-training static quantisation (start here)
Weights and activations to int8 using scales computed from a **calibration set**.
```python
from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantFormat, QuantType
class Reader(CalibrationDataReader):
    def __init__(self, images): self.it = iter([{"images": preprocess(i)} for i in images])
    def get_next(self): return next(self.it, None)
quantize_static("model_fp32.onnx", "model_int8.onnx", Reader(calib_images),
                quant_format=QuantFormat.QDQ, per_channel=True,
                activation_type=QuantType.QInt8, weight_type=QuantType.QInt8)
```
The block ran in ONNX Runtime 1.31.0 on a ResNet-18 (8 random calibration images, input named `images`): output 11.8 MB vs 46.7 MB for FP32, but CPU latency was 8.7 ms vs 8.5 ms (no speed-up on this CPU), a reminder to check the int8 kernels are used.
TensorRT: build with `--int8` and a calibrator (entropy calibration) or from a QDQ ONNX (`--int8` appears in the trtexec README);
TFLite: `converter.optimizations = [tf.lite.Optimize.DEFAULT]` + `representative_dataset` (not run: no TensorRT, GPU or TensorFlow here) (gated: unconfirmed, source is paywalled or blocked).

## 2. Calibration data
200–1000 images **from the deployment distribution** (same cameras, lighting, resolution,
preprocessing). Random internet images or the training set with heavy augmentation give
wrong activation ranges → accuracy collapse at night/edge cases.

## 3. Sensitive layers
- First conv and final detection head/regression outputs are often sensitive: keep them in
  FP16/FP32 (mixed precision) — ORT `nodes_to_exclude` (a `quantize_static` parameter, confirmed from its signature), TensorRT per-layer precision (not run) (gated: unconfirmed, source is paywalled or blocked).
- Ops that quantise poorly: softmax/sigmoid-heavy heads, depthwise convs with wide ranges,
  concatenations with mismatched scales (YOLO necks).
- Per-channel weight quantisation is almost always worth it.

## 4. Quantisation-aware training (if PTQ loses too much)
Insert fake-quant nodes and fine-tune a few epochs (PyTorch `torch.ao.quantization`, which exposes `prepare_qat`; NVIDIA
`pytorch-quantization`/ModelOpt not checked) (gated: unconfirmed, source is paywalled or blocked), export QDQ ONNX → TensorRT. Recovers most of the loss.

## 5. Evaluate properly
- Accuracy: full validation metric (mAP, mIoU), not a few images; check per-class and hard
  slices (small objects, low light).
- Latency: on the **target device**, after warm-up, at the deployment batch size, including
  pre/post-processing; check the int8 kernels are actually used (TensorRT layer info, NPU
  delegate logs — unsupported ops fall back to CPU silently and can be slower than FP16).

## Gotchas
- Accuracy drop concentrated on small objects/low contrast — mAP@0.5 may hide it; look at AP_small.
- INT8 on GPUs without int8 tensor cores may not be faster than FP16.
- Calibration cache files are tied to the engine/version; regenerate after model changes.

## Verify
- [ ] Accuracy delta vs FP32 reported on the full validation set and hard slices.
- [ ] On-device latency (p50/p99) and memory measured end to end.
- [ ] Delegate/engine logs confirm int8 execution for the bulk of layers.

## Checked
onnxruntime 1.31.0, onnx 1.23.2, PyTorch 2.14.1 CPU.
- Run: `quantize_static` with `CalibrationDataReader`, `QuantFormat.QDQ`, `per_channel=True`, `QInt8` for activations and weights on a ResNet-18 ONNX; compared file size and CPU latency; printed the full `quantize_static` signature (includes `nodes_to_exclude`, `calibrate_method`); `torch.ao.quantization.prepare_qat` exists.
- Fetched: TensorRT trtexec README (`--int8`, `--best`).
- Not run: TensorRT, TFLite, NPU delegates, QAT export (no GPU/devices); gated.
