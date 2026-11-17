---
id: computing-software.ai-ml-engineering.seldon-core-2.test-installation-iris-model-and-pipeline
name: test-installation-iris-model-and-pipeline
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, installation, test-installation, smoke-test, iris, host-header, seldon-model-header, pipeline-suffix, kubectl-wait]
level: practitioner
status: docs-checked
description: "Verify a Seldon Core 2 install: deploy the iris Model and a Pipeline in seldon-mesh, wait for readiness, and curl inference with Host and Seldon-Model headers."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/installation/test-installation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Test an installation with iris

After installing Core 2, Kafka and the service mesh, deploy a sample model and infer.

## Deploy the model
Apply a Model named `iris` in namespace `seldon-mesh` with `storageUri: "gs://seldon-models/scv2/samples/mlserver_1.3.5/iris-sklearn"` and `requirements: [sklearn]`. Check readiness:
```bash
kubectl wait --for condition=ready --timeout=300s model --all -n seldon-mesh
```

## Deploy a pipeline
Apply a Pipeline `irispipeline` with `steps: [{name: iris}]` and `output.steps: [iris]`, then wait the same way with `pipeline --all`. The pipeline name must not equal any step name in it: that gives the Kubernetes validation error `pipeline iris must not have a step name with the same name as pipeline name`.

## Infer through the ingress
POST to `http://<INGRESS_IP>:80/v2/models/iris/infer` with a JSON body holding one input named `predict`, shape `[1, 4]`, datatype `FP32`, data `[[1, 2, 3, 4]]`. Headers:
- `Host: seldon-mesh.inference.seldon`, matching the virtual host in your service mesh.
- `Content-Type: application/json`.
- `Seldon-Model: iris`, the model name.

For the pipeline use `/v2/models/irispipeline/infer` and header `Seldon-Model: irispipeline.pipeline`. The `.pipeline` suffix distinguishes a pipeline from a model sharing its base name.

Expected: the model returns outputs with `predict` datatype INT64 and data `[2]`; the pipeline returns the same output with an empty `model_name`.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/installation/test-installation.md (read in full).
