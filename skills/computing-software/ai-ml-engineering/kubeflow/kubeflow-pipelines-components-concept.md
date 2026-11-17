---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-components-concept
name: kubeflow-pipelines-components-concept
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [pipelines, kfp, component, ir-yaml, kfp-overview]
level: intro
status: docs-checked
description: "Kubeflow Pipelines overview and the component concept: Python and YAML based components, what a component consists of, and when to containerize."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/overview.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/concepts/component.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines components concept

Kubeflow Pipelines (KFP) builds portable, scalable ML workflows on Kubernetes. You author components and pipelines with the KFP Python SDK, compile to platform-neutral IR YAML, and submit to the KFP backend (a core Kubeflow component or standalone). A pipeline is a DAG of components; tasks run in parallel where possible and results can be cached.

A component packages code like a function. Its parts:
1. Code: usually a Python function, or another command such as Bash.
2. Dependency support: Python libraries installed at runtime, environment variables, package indices, cluster resources (ConfigMaps, Secrets, PVCs), CPU, memory and GPU requests.
3. Base image: defaults to a generic Python image.
4. I/O specification: components cannot share memory, so use parameters for small values and artifacts for models, datasets and other large data.

Python-based (recommended) uses `@component`:

```python
@component(base_image="python:3.12-slim-bookworm", packages_to_install=["pandas>=2.2.3"])
def process_data(output_data: Output[Dataset]):
    import pandas as pd
    ...
```

Imports go inside the function. For local work call `process_data.execute(output_data=Dataset(uri="data.csv"))`; `python_func` exposes the original function.

YAML-based components have metadata, interface and a container implementation, load with `load_component_from_file`, and run any command on the base image, but lack local-execution support.

To containerize, `kfp component build ... --no-build-image` generates a Dockerfile and `runtime-dependencies.txt`. A one-to-one component-to-image mapping is not recommended because of the maintenance burden; the page suggests a small set of base images supporting many components. The `target_image` parameter must be set in the Python component definition to use the build command.

## Checked

2026-11-08. Confirmed against the KFP overview and Component concept pages: component parts, the @component example, local execution, YAML-based components and the containerize guidance. Nothing needed removal.
Method: docs-only read of cited pages, 2026-11-08
