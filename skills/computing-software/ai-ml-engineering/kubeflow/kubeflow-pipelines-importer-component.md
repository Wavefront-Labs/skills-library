---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-importer-component
name: kubeflow-pipelines-importer-component
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [importer, dsl-importer, modelcar, reimport, artifact-uri]
level: practitioner
status: docs-checked
description: "Load an existing artifact into a pipeline with dsl.importer: artifact_uri, artifact_class, reimport, metadata, OCI modelcar images and download_to_workspace."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/components/importer-component.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines importer component

`dsl.importer` is a pre-built component for artifacts not produced by a task in the current pipeline. Import it from `dsl`; do not write one.

```python
importer_task = dsl.importer(
    artifact_uri='gs://ml-pipeline-playground/shakespeare1.txt',
    artifact_class=dsl.Dataset,
    reimport=True,
    metadata={'date': task.output})
other_component(dataset=importer_task.output)
```

- `artifact_uri` and `artifact_class` are required.
- `metadata` may include outputs of upstream tasks.
- `reimport`: if `False`, KFP checks whether the artifact is already in ML Metadata and reuses it.

Modelcar images (KFP 2.5 and later): pass an OCI URI such as `oci://quay.io/my-org/my-model:v1`. When a component consumes it, the modelcar runs as a sidecar and the model `path` points to `/models` in that container. Both containers must run as the same user ID or reading `path` fails with a permission error. This needs no action on distributions that assign random UIDs (such as OpenShift). Otherwise build the modelcar with your component's UID, or set `PIPELINE_RUN_AS_USER` to a non-root UID on the KFP API server deployment.

Version 2.15.0 and later: `download_to_workspace=True` downloads the imported artifact directly into the Pipeline Run Workspace.

## Checked

2026-11-09: confirmed every claim against the Kubeflow website page "Special Case: Importer Components" (content/en/docs/components/pipelines/user-guides/components/importer-component.md, read in full). Nothing removed.

Method: docs-checked 2026-11-09 against the Kubeflow website importer-component page (raw markdown, read in full).
