---
id: computing-software.ai-ml-engineering.seldon-core-2.open-inference-protocol-rest-endpoints
name: open-inference-protocol-rest-endpoints
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, open-inference-protocol, v2-protocol, rest, health-endpoints, model-metadata, kserve]
level: practitioner
status: docs-checked
description: "Open Inference Protocol (V2) REST endpoints Seldon Core 2 servers must serve: v2/health/live and ready, model ready, server and model metadata, and POST infer."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/user-guide/v2/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Open Inference Protocol: REST endpoints

The Open Inference Protocol (formerly the V2 Inference Protocol, based on the KServe original) is endorsed by NVIDIA Triton, TensorFlow Serving and ONNX Runtime Server. A compliant inference server implements the health, metadata and inference APIs over HTTP/REST, gRPC, or both. All strings are case-sensitive.

## URLs
```
GET v2/health/live
GET v2/health/ready
GET v2/models/${MODEL_NAME}[/versions/${MODEL_VERSION}]/ready
GET v2
GET v2/models/${MODEL_NAME}[/versions/${MODEL_VERSION}]
POST v2/models/${MODEL_NAME}[/versions/${MODEL_VERSION}]/infer
```
The version part is optional. If omitted, the server chooses a version by its own policies.

## Health
A health request is an HTTP GET. A 200 status means true and a 4xx means false, with an empty body.
- Server live: the server can receive and respond to metadata and inference requests. It can serve directly as a Kubernetes livenessProbe.
- Server ready: all models are ready for inference. It can serve as a readinessProbe.
- Model ready: a specific model is ready; the name, and optionally version, are in the URL.

## Metadata
`GET v2` returns server metadata. `GET v2/models/${MODEL_NAME}` returns model metadata, including the platform string (such as `onnx_onnxv1` or `pytorch_torchscript`), which is informational only. Failed requests return a JSON error object.

The gRPC API follows the same concepts as the REST API.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/user-guide/v2/README.md (read in full, REST and gRPC sections). Softened a claim that every Seldon server must implement the protocol to the page's "compliant server" wording.
