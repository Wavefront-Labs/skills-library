---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-artifacts-parameters
name: kubeflow-pipelines-artifacts-parameters
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [artifacts, parameters, input-output-artifacts, artifact-path, dsl-artifact]
level: practitioner
status: docs-checked
description: "KFP data passing: parameters (small JSON-serialized values) versus artifacts (Input/Output Dataset, Model with path, uri, metadata), and the Python type mapping."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/data-handling/artifacts.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/data-handling/parameters.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines artifacts parameters

Use **parameters** for small values that are not ML artifacts; use **artifacts** for models, datasets, metrics and similar data.

Parameter types map to ML Metadata: `str` is string, `int` and `float` are number, `bool` is boolean, `list` and `dict` (also `typing.List`, `typing.Dict`) are object. Defaults are ordinary Python defaults. KFP serializes parameters as JSON; Python components handle this transparently, and container components receive deserialized inputs but must write outputs themselves.

Artifacts are annotated with `dsl.Input[...]` and `dsl.Output[...]` of types such as `Dataset` and `Model`:

```python
@dsl.component
def training_component(dataset: Input[Dataset], model: Output[Model]):
    with open(dataset.path) as f:
        contents = f.read()
    tf_model.save(model.path)
    model.metadata['framework'] = 'tensorflow'
```

Four properties on an artifact:
- `name`: artifact name (cannot be overwritten on Vertex Pipelines).
- `uri`: object location. Inputs: where it lives; outputs: where it will be written.
- `metadata`: key-value pairs.
- `path`: a local filesystem path for the `uri`. Writing the artifact content to `path` makes the backend upload it to object storage; reading it for inputs gives the downloaded content.

Artifact annotations also enable type checking and special UI rendering for some artifact types.

## Checked

Confirmed the parameter type table, JSON serialization behaviour, the training_component example, the four artifact properties and the path-to-uri upload behaviour. Nothing removed.

Method: docs-checked 2026-11-09 against the raw kubeflow/website pipelines data-handling artifacts.md and parameters.md pages, read in full.
