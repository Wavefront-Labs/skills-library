---
id: computing-software.ai-ml-engineering.kserve.kserve-tensorflow-serving
name: kserve-tensorflow-serving
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [tensorflow, tensorflow-serving, grpc, h2c, grpc-port, containerport, savedmodel, signature-name, serving-default]
level: practitioner
status: docs-checked
description: "Deploy TensorFlow SavedModels via the tensorflow modelFormat: V1 REST predict, gRPC on containerPort 9000 with port name h2c (Knative) or grpc-port, TF Serving API Python client."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/frameworks/tensorflow/tensorflow.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TensorFlow on KServe

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata: {name: flower-sample}
spec:
  predictor:
    model:
      modelFormat: {name: tensorflow}
      storageUri: "gs://kfserving-examples/models/tensorflow/flowers"
      resources:
        requests: {cpu: "100m", memory: 256Mi}
        limits: {cpu: "1", memory: 1Gi}
```

REST: `POST /v1/models/$MODEL_NAME:predict` with `Host` set from `.status.url`; response is a `predictions` list (here `scores`, `prediction`, `key`).

## gRPC
Add a port to the model spec. The page's example uses container port 9000:

```yaml
      ports:
        - containerPort: 9000
          name: h2c          # Knative requires h2c
          protocol: TCP
```

The page gives a second variant that names the port `grpc-port`; KServe requires the name format `<protocol>[-<suffix>]`.

Client: `tensorflow-serving-api` (the doc script uses TF 1.x, `tensorflow-serving-api>=1.14.0,<2.0.0`) builds a `PredictRequest` with `model_spec.name`, `model_spec.signature_name` (default `serving_default`) and `make_tensor_proto` inputs, using `grpc.insecure_channel` to the ingress host and port; pass the service hostname through `grpc.ssl_target_name_override`. Response includes a `model_spec` with name, version and signature name.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website tensorflow.md page: manifest, V1 REST path and response fields, gRPC port block, client package pin and calls. Removed the claim that TF Serving listens on 9000 and the Standard-mode label, which the page does not state.
