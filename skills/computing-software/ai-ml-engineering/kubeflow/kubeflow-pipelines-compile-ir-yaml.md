---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-compile-ir-yaml
name: kubeflow-pipelines-compile-ir-yaml
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [compile, compiler, type-checking, pipelinespec, pipeline-package]
level: practitioner
status: docs-checked
description: "Compile KFP pipelines and components to IR YAML with Compiler().compile: arguments, static type checking, parameter defaults and Kubernetes manifest output."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/compile-a-pipeline.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/core-functions/caching.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines compile ir yaml

Pipelines must be compiled before submission.

```python
from kfp import compiler
compiler.Compiler().compile(my_pipeline, package_path='pipeline.yaml')
```

The output is an Intermediate Representation (IR) YAML, a serialized `PipelineSpec` protobuf, hermetic and not meant to be read, though header comments summarize the pipeline. Components compile too, because components are pipelines: `compile(comp, package_path='component.yaml')`.

`Compiler.compile` arguments:
- `pipeline_func`: pipeline from `@dsl.pipeline` or component from `@dsl.component` (required).
- `package_path`: output YAML path (required).
- `pipeline_name`: overrides the name in `pipelineInfo.name`.
- `pipeline_parameters`: default argument values for pipeline or component parameters.
- `type_check`: enable or disable static type checking.
- `kubernetes_manifest_format`: write a Kubernetes manifest instead of the PipelineSpec IR.
- `kubernetes_manifest_options`: a `KubernetesManifestOptions` (pipeline and version names, display names, `namespace`, `include_pipeline_manifest`), only relevant when `kubernetes_manifest_format=True`. The page says this requires Kubeflow Pipelines in Kubernetes Native API mode (version 2.14.0+) and produces `pipelines.kubeflow.org/v2beta1` Pipeline and PipelineVersion resources.

Static type checking is on by default and verifies, before running, that data passed between components has the expected type: a list goes only to a `typing.List` parameter, a float only to `float`. Artifact types must match, except that `Artifact` is compatible with every artifact type, acting as the any type.

The caching guide shows the CLI form `kfp dsl compile --py my_pipeline.py --output my_pipeline.yaml`.

## Checked

2026-11-08. Confirmed against the Compile a Pipeline page (arguments table, IR description, type checking rules, Kubernetes manifest options) and the caching page (CLI form).
Method: docs-only read of cited pages, 2026-11-08
