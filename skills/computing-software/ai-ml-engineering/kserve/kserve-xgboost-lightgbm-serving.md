---
id: computing-software.ai-ml-engineering.kserve.kserve-xgboost-lightgbm-serving
name: kserve-xgboost-lightgbm-serving
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [xgboost, lightgbm, xgbserver, lgbserver, kserve-xgbserver, kserve-lgbserver, modelbst, nthread, ubj]
level: practitioner
status: docs-checked
description: "Deploy XGBoost and LightGBM: modelFormat, runtimes kserve-xgbserver and kserve-lgbserver, accepted model extensions, --nthread server flag, V1 vs V2 payloads, gRPC port setup."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/frameworks/xgboost/xgboost.md", "https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/frameworks/lightgbm/lightgbm.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# XGBoost and LightGBM on KServe

```yaml
spec:
  predictor:
    model:
      modelFormat: {name: xgboost}          # or lightgbm
      protocolVersion: v2
      runtime: kserve-xgbserver             # kserve-lgbserver for LightGBM
      storageUri: "gs://kfserving-examples/models/xgboost/iris"
```

- XGBoost server recognises `.bst`, `.json`, `.ubj` files. The LightGBM example saves `model.bst`. `storageUri` points at the directory.
- For V2 with no `runtime`, `mlserver` is used. The default (no `protocolVersion`) is V1.
- LightGBM V1 example: `modelFormat.name: lightgbm`, input `{"inputs":[{"sepal_length_(cm)":[5.1], ...}]}` to `/v1/models/lightgbm-iris:predict`. V2: POST `/v2/models/NAME/infer`.

## Local servers (python/xgbserver, python/lgbserver, `uv sync`)
Flags: `--model_dir`, `--model_name` (optional, default `model`), `--nthread` (threads used by the library, default 1).

## gRPC
Either HTTP or gRPC is exposed, not both. Add `ports: [{name: h2c, protocol: TCP, containerPort: 8081}]` on Knative, or `name: grpc-port` when Istio needs the port name (format `<protocol>[-<suffix>]`). Test with `grpcurl -plaintext` and the Open Inference Protocol `open_inference_grpc.proto`; check readiness first with the ServerReady RPC.

## Checked
Confirmed against KServe's XGBoost and LightGBM pages: `.bst`/`.json`/`.ubj` extensions, `kserve-xgbserver` and `kserve-lgbserver` runtimes, `mlserver` default for V2 without `runtime`, local server flags (`--model_dir`, `--model_name` default `model`, `--nthread` default 1), HTTP or gRPC but not both, `h2c` and `grpc-port` port names, `grpcurl` testing with the Open Inference Protocol proto.
Method: docs-only read of cited pages, 2026-11-08
