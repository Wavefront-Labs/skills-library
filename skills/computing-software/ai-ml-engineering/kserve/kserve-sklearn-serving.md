---
id: computing-software.ai-ml-engineering.kserve.kserve-sklearn-serving
name: kserve-sklearn-serving
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [sklearn, sklearnserver, kserve-sklearnserver, joblib, protocolversion, mlserver, grpc, h2c, grpcurl]
level: practitioner
status: docs-checked
description: "Serve scikit-learn models: modelFormat sklearn, protocolVersion v1/v2, kserve-sklearnserver vs mlserver runtime, .joblib/.pkl/.pickle files, V2 infer request, gRPC port naming."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/frameworks/sklearn/sklearn.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scikit-learn on KServe

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata: {name: sklearn-iris}
spec:
  predictor:
    model:
      modelFormat: {name: sklearn}
      protocolVersion: v2
      runtime: kserve-sklearnserver
      storageUri: "gs://kfserving-examples/models/sklearn/1.0/model"
```

- By default the v1beta1 API exposes the model through an API compatible with the V1 Dataplane. With `protocolVersion: v2` and no `runtime`, the mlserver runtime is used; set `runtime: kserve-sklearnserver` for the KServe server.
- The server recognises model files ending `.joblib`, `.pkl`, `.pickle`. `storageUri` points at the directory, not the file.
- V2 request: POST `/v2/models/sklearn-iris/infer` with an `inputs` list of objects holding `name`, `shape` (`[2, 4]` in the example), `datatype` (`FP32`) and `data`; send the Host header taken from `.status.url`.

## Local test
`sklearnserver` (from `python/sklearnserver` in the kserve repo, `uv sync`) takes `--model_dir` and optional `--model_name` (default `model`): `python3 sklearnserver --model_dir /path/to/model_dir --model_name sklearn-iris`.

## gRPC
KServe currently exposes either the HTTP or the gRPC port, not both (HTTP by default). Add `ports` to the model spec with `containerPort: 8081`, `protocol: TCP` and the name `h2c` (Knative expects that name for a gRPC port) or, in the second documented variant, a name such as `grpc-port` (KServe requires the format `<protocol>[-<suffix>]`). Test with `grpcurl -plaintext -proto open_inference_grpc.proto -authority <host>` against `inference.GRPCInferenceService.ServerReady` or `ModelInfer`.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website sklearn.md page: manifest, runtime and protocol defaults, accepted model file extensions, local `sklearnserver` arguments, V2 request shape, and the gRPC port rules. Rewrote the V1 path and the Istio and Standard-mode wording to what the page states.
