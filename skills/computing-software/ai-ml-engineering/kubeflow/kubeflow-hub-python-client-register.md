---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-hub-python-client-register
name: kubeflow-hub-python-client-register
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [python-client, register-model, modelregistry-client, model-version, model-artifact]
level: practitioner
status: docs-checked
description: "Register and retrieve models with the Model Registry Python client: connect, register_model, and the get_registered_model, get_model_version, get_model_artifact calls."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/hub/getting-started.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hub python client register

Install the client in a notebook: `pip install model-registry`. A Hub client also exists in the Kubeflow SDK at `kubeflow.hub.ModelRegistryClient`; this page uses the standalone `model_registry` client. Pydantic version conflicts with other packages are possible.

Connect:

```python
from model_registry import ModelRegistry
registry = ModelRegistry(
    server_address="http://model-registry-service.kubeflow.svc.cluster.local",
    port=8080, author="your name", is_secure=False)
```

Register a model and its artifact metadata:

```python
rm = registry.register_model(
    "iris",
    "gs://kfserving-examples/models/sklearn/1.0/model",
    model_format_name="sklearn", model_format_version="1",
    version="v1", description="Iris scikit-learn model",
    metadata={"accuracy": 3.14, "license": "BSD 3-Clause License"})
```

Retrieve:

```python
model = registry.get_registered_model("iris")
version = registry.get_model_version("iris", "v1")
art = registry.get_model_artifact("iris", "v1")
```

Each returns an object with an `id`, and these calls assume the earlier registration step used the same model name `iris` and version `v1`. The retrieved objects can then be used to create a KServe inference endpoint. The same data is available through the REST API, and the examples can be reproduced with the REST APIs or your own SDK. The Model Registry UI (reached from the Central Dashboard) can also register, view, update and delete models.

## Checked

Confirmed the pip install, the ModelRegistry constructor arguments, the register_model example, the three get_ calls and the UI actions against the Hub getting-started page. Nothing removed.

Method: docs-checked 2026-11-09 against the raw kubeflow/website Hub getting-started.md page, read in full.
