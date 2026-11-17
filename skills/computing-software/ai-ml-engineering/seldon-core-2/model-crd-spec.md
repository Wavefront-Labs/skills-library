---
id: computing-software.ai-ml-engineering.seldon-core-2.model-crd-spec
name: model-crd-spec
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, model, crd, storageuri, requirements, memory, mlops-seldon-io]
level: practitioner
status: docs-checked
description: "Write a Seldon Core 2 Model resource: apiVersion, storageUri, requirements tags and memory, with the iris sklearn example."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/resources/model.md", "https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/resources/server.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Model custom resource

A Model is the atomic building block in Seldon Core 2. It points to a machine learning artifact that will be loaded onto a running Server. It can be a TensorFlow, PyTorch or SKLearn model, a transformation such as a custom Python component, a drift or outlier detector, or an Alibi-Explain explainer.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Model
metadata:
  name: iris
spec:
  storageUri: "gs://seldon-models/scv2/samples/mlserver_1.5.0/iris-sklearn"
  requirements:
  - sklearn
  memory: 100Ki
```

## Core fields
- `storageUri`: location of the artifact; any rclone URI specification works.
- `requirements`: tags that the Server must advertise as capabilities. The default install ships Servers covering a range of artifact types.
- `server`: optionally name a specific Server to target, for example a custom one (the Server page shows `server: mlserver-134`).
- `memory`: appears in the example (`100Ki`); the page does not describe it further.

## Checked
2026-11-09. Confirmed against docs-gb/kubernetes/resources/model.md and server.md (Seldon Core v2 branch): the description of a Model as the atomic building block and the artifact types listed; the sklearn iris example verbatim; `storageUri` as any rclone URI; `requirements` as tags matched by the Server; the default Servers covering a range of artifact types; the `server` field naming a Server. Removed as not stated in the sources fetched: the `memory` scheduling explanation, `secretName`, `minReplicas` partial scheduling, the Scheduler gRPC `LoadModel` call with port 9004 and its fields, and the kubectl apply and get commands.
Method: documentation only; no commands were run.
