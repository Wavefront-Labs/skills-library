---
id: computing-software.ai-ml-engineering.seldon-core-2.inference-request-routing-headers-and-paths
name: inference-request-routing-headers-and-paths
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, inference, routing, seldon-model-header, path-routing, pipeline-endpoints, virtual-endpoints]
level: practitioner
status: docs-checked
description: "Route Seldon Core 2 requests to the right model or pipeline with the Seldon-Model header (name or name.pipeline) or with /v2/models and /v2/pipelines path prefixes."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/inference.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Request routing: headers and paths

Models and pipelines can share a name, so Seldon must be told which one a request targets. There are two methods: header-based (preferred) and path-based.

## Header routing
Works for REST (HTTP/1.1) and gRPC (HTTP/2) with the `Seldon-Model` header:
- Model: the model name, for example `Seldon-Model: foo`.
- Pipeline: the pipeline name plus `.pipeline`, for example `Seldon-Model: foo.pipeline`.
- Experiment: the experiment name plus `.experiment`.

```bash
curl -v http://0.0.0.0:9000/v2/models/iris/infer \
   -H "Content-Type: application/json" \
   -H "Seldon-Model: iris" \
   -d @request.json
```

With grpcurl use `-rpc-header seldon-model:iris`; with tritonclient pass `headers={"Seldon-Model": "iris"}` to `client.infer()`. The `seldon` CLI sets these headers itself.

## Path routing
The v2 protocol knows only models, so Seldon adds virtual pipeline endpoints that other v2 components do not understand:
- Models: `/v2/models/{model name}`, normal v2 usage.
- Pipelines: `/v2/pipelines/{pipeline name}`, with no suffix on the name.
- Pipelines, alternatively: `/v2/models/{pipeline name}.pipeline`.

## Checked

Confirmed against the Inference page (Request Routing) and the Experiments page: the Seldon-Model header values for models and pipelines, the .experiment suffix, the grpcurl and tritonclient header forms, and the virtual path forms for pipelines.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb inference.md and kubernetes/resources/experiment.md pages (raw markdown).
