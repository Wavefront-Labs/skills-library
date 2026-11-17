---
id: computing-software.ai-ml-engineering.mlops.edge-deployment-sagemaker-neo-and-on-device
name: edge-deployment-sagemaker-neo-and-on-device
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, sagemaker-neo, edge-deployment, on-device-inference, tflite, model-compilation]
level: practitioner
status: draft
description: "Deploy models to edge devices: compile with SageMaker Neo or export to LiteRT, Core ML, ONNX Runtime or ExecuTorch, quantize, benchmark on hardware, and roll out OTA updates."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/neo.html
  - https://ai.google.dev/edge/litert
  - https://pytorch.org/executorch/stable/index.html
  - https://docs.aws.amazon.com/greengrass/v2/developerguide/what-is-iot-greengrass.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Edge deployment (SageMaker Neo and on-device)

**Goal:** a trained model runs on cameras, phones or gateways within latency, memory and power budgets, and the fleet can be updated and rolled back.

## Choose the runtime
| Target | Path |
|---|---|
| Android / embedded Linux / MCU | LiteRT (TFLite) |
| iOS / macOS | Core ML via `coremltools` |
| Cross-platform, many accelerators | ONNX Runtime (Mobile) |
| PyTorch-native on device | ExecuTorch (`torch.export` -> `.pte`) |
| NVIDIA Jetson | TensorRT |
| Many edge targets, AWS workflow | SageMaker Neo compile + DLR runtime |

## SageMaker Neo
```python
sm.create_compilation_job(
    CompilationJobName="detector-jetson-v3", RoleArn=ROLE,
    InputConfig={"S3Uri": "s3://ml/models/detector/model.tar.gz",
                 "DataInputConfig": '{"input0": [1, 3, 640, 640]}', "Framework": "PYTORCH",
                 "FrameworkVersion": "2.0"},
    OutputConfig={"S3OutputLocation": "s3://ml/compiled/", "TargetDevice": "jetson_xavier"},
    StoppingCondition={"MaxRuntimeInSeconds": 1800})
```
Input shapes must be fixed and exact. Use `TargetPlatform` (`Os`, `Arch`, `Accelerator`) when no named device matches. SageMaker Edge Manager was discontinued in 2024; deploy and manage fleets with AWS IoT Greengrass v2 components (or your MDM) instead.

## Make it fit
- Quantize: int8 post-training quantization with a representative calibration set (hundreds of real samples), or QAT if accuracy drops more than tolerated.
- Prune/distil to a smaller architecture before compiling; compilers cannot rescue a model 10x too big.
- Check operator support for the target delegate (GPU/NNAPI/Core ML/NPU); unsupported ops fall back to CPU and destroy latency.

## Benchmark on real hardware
Measure p50/p95 latency, peak memory, model load time, and power/thermals under sustained load (throttling shows after minutes). Compare accuracy of the compiled/quantized model to the original on the same eval set - export bugs and quantization often cost more than expected.

## Fleet rollout
- Version every artifact (model + preprocessing + runtime version) and keep the previous one on device.
- Staged OTA: canary devices, then percentages; automatic rollback on crash rate or health-check failure.
- Telemetry: inference latency, errors, confidence distributions; sample inputs only with consent and privacy review.
- Sign artifacts and verify on device.

## Verify
- [ ] On-device accuracy within the agreed delta of the server model.
- [ ] Latency and memory budgets met at sustained load.
- [ ] Rollback to the previous model tested on a canary device.
