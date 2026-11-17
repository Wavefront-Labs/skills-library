---
id: computing-software.ai-ml-engineering.kserve.kserve-custom-transformer
name: kserve-custom-transformer
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [transformer, predictor-host, preprocess, postprocess, grpc-v2, protocol, image-transformer, pre-post-processing, kserve-tritonserver]
level: practitioner
status: docs-checked
description: "Write a KServe transformer deriving from kserve.Model with preprocess and postprocess handlers, ModelServer start with predictor_host, and deploy it beside a predictor."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/transformers/custom-transformer/custom-transformer.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom transformer

A transformer is an InferenceService component doing pre/post processing next to the model. Derive from `kserve.Model` and override `preprocess` and `postprocess`; `predict` calls the predictor at `predictor_host`, which KServe fills in automatically. Default is REST; pass `--protocol grpc-v2` for gRPC to the predictor. For V2 use `InferRequest` / `InferInput` / `InferResponse`.

```python
class ImageTransformer(kserve.Model):
    def __init__(self, name, predictor_host=None, protocol=None):
        super().__init__(name, return_response_headers=True)
        self.ready = True
    def preprocess(self, payload, headers=None): ...
    def postprocess(self, outputs, headers=None, response_headers=None): ...
ModelServer().start(models=[ImageTransformer(args.model_name, predictor_host=args.predictor_host, protocol=args.protocol)])
```

Several models can share one transformer instance type: loop over model names and register one transformer each.

## Deploy
```yaml
spec:
  predictor:
    model:
      modelFormat: {name: pytorch}
      storageUri: gs://kfserving-examples/models/torchserve/image_classifier/v1
  transformer:
    containers:
      - name: kserve-container
        image: kserve/image-transformer:latest
        command: ["python", "-m", "model"]
        args: [--model_name, mnist]
```

`STORAGE_URI` env on a custom container works like `storageUri`; files land in `/mnt/models`.

## gRPC to the predictor
Override the PyTorch default runtime (TorchServe) with `runtime: kserve-tritonserver`, `runtimeVersion: 20.10-py3`, a port named `h2c` on containerPort 9000, and give the transformer `--protocol grpc-v2`. The page says gRPC is faster than REST because of tight Protocol Buffer packing and HTTP/2, which helps most when large tensors move between transformer and predictor.

If a transformer overrides `predict()` or makes its own HTTP calls to the predictor, it must forward the `Authorization` header itself: accept the `headers` parameter and include the header in the request to the predictor.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website custom-transformer page: base class and handlers, `predictor_host` auto-fill, REST default and `--protocol grpc-v2`, per-model registration loop, `STORAGE_URI` and `/mnt/models`, and the Triton gRPC override with `runtimeVersion: 20.10-py3` and the `h2c` port. Added the Authorization forwarding note from the same page.
