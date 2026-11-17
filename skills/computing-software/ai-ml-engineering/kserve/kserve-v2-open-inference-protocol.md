---
id: computing-software.ai-ml-engineering.kserve.kserve-v2-open-inference-protocol
name: kserve-v2-open-inference-protocol
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [v2-protocol, open-inference-protocol, v2models, infer, datatype, fp32, model-metadata, health-ready, health-live, modelinfer, grpcinferenceservice]
level: practitioner
status: docs-checked
description: "Open Inference (V2) protocol: REST and gRPC endpoints, inference request/response JSON, tensor datatypes, metadata and health probes, platforms."
sources: ["https://github.com/kserve/website/blob/main/docs/concepts/architecture/data-plane/v2-protocol/v2-protocol.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Open Inference Protocol (V2)

A compliant server implements health, metadata and inference APIs over HTTP/REST and/or gRPC. No `:explain`. Strings are case-sensitive; extensions are part of the API.

| API | REST |
|---|---|
| Inference | POST v2/models/NAME[/versions/VER]/infer |
| Model metadata | GET v2/models/NAME[/versions/VER] |
| Model ready | GET v2/models/NAME[/versions/VER]/ready |
| Server ready / live / metadata | GET v2/health/ready, v2/health/live, v2 |

gRPC service `GRPCInferenceService`: ServerLive, ServerReady, ModelReady, ServerMetadata, ModelMetadata, ModelInfer. Server ready/live map directly to Kubernetes readiness/liveness probes.

```json
{"id": "42",
 "inputs": [{"name": "input0", "shape": [2, 2], "datatype": "UINT32", "data": [1, 2, 3, 4]}],
 "outputs": [{"name": "output0"}]}
```

Response carries `model_name`, optional `model_version`, `id` (echoed), `outputs[]` with `name`, `shape`, `datatype`, `data`. Errors are `{"error": "..."}` with HTTP status (typically 400). `parameters` objects are free-form, server-defined.

Datatypes: BOOL, UINT8/16/32/64, INT8/16/32/64, FP16, FP32, FP64, BYTES. Data is flattened row-major with no stride or padding; JSON may be nested or flat. Metadata shapes use -1 for variable dimensions. Platforms use `<project>_<format>` such as `pytorch_torchscript`, `tensorflow_savedmodel`, `onnx_onnxv1`, `tensorrt_plan`.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited KServe V2 protocol page in full; every claim matches it. No content removed.
