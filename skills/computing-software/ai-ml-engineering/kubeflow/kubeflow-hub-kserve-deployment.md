---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-hub-kserve-deployment
name: kubeflow-hub-kserve-deployment
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [kserve, inferenceservice, model-registry-csi, storage-uri]
level: advanced
status: docs-checked
description: "Deploy a KServe InferenceService from Model Registry metadata, using registry labels and the model-registry:// custom storage initializer URI."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/hub/getting-started.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/hub/installation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hub kserve deployment

Registry metadata removes error-prone manual copying of deployment details. Using the objects from `get_registered_model`, `get_model_version` and `get_model_artifact`, build an InferenceService:

Option 1, pass artifact metadata: label the service `modelregistry/registered-model-id: <model.id>` and `modelregistry/model-version-id: <version.id>`, set `storage_uri=art.uri` and `model_format` from `art.model_format_name` and `art.model_format_version`, then create it with `kserve.KServeClient().create(isvc)`. The labels keep references to the original registry entities.

Option 2, the Model Registry custom storage initializer (CSI): set `storageUri: "model-registry://iris/v1"`, protocol `model-registry://{modelName}/{modelVersion}`. The CSI fetches the latest artifact data for that model version from the registry and downloads the model from its URI.

Equivalent YAML:

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: iris-model
  labels:
    modelregistry/registered-model-id: "MODEL_ID"
    modelregistry/model-version-id: "VERSION_ID"
spec:
  predictor:
    model:
      storageUri: "model-registry://iris/v1"
      modelFormat: {name: "sklearn", version: "1"}
```

Prerequisites: the registry is installed, and for Option 2 the cluster-scoped `CustomStorageContainer` from `options/csi` is applied. The example pins `kserve==0.13` for the Python SDK.

## Checked

Confirmed the label names, the artifact-metadata and model-registry:// storage URI options, the YAML shape, the options/csi CustomStorageContainer prerequisite and the kserve 0.13 pin. Nothing removed.

Method: docs-checked 2026-11-09 against the raw kubeflow/website Hub getting-started.md and installation.md pages, read in full.
