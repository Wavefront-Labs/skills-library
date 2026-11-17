---
id: computing-software.ai-ml-engineering.mlops.azure-ml-pipelines-and-components
name: azure-ml-pipelines-and-components
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, azure-ml-pipelines, azure-machine-learning, components, azure-ai-ml, ml-pipelines]
level: practitioner
status: draft
description: "Build Azure Machine Learning pipelines with SDK v2 or CLI: command components in YAML, the @pipeline DSL, compute and data inputs, output reuse, and registering components."
sources:
  - https://learn.microsoft.com/en-us/azure/machine-learning/concept-ml-pipelines
  - https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-component-pipeline-python
  - https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-component-pipelines-cli
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Azure ML pipelines and components

**Goal:** a reusable multi-step training pipeline in Azure ML where each step is a versioned component, steps reuse outputs when nothing changed, and CI can submit it.

## Component (YAML)
```yaml
$schema: https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json
name: prep_data
version: 3
type: command
inputs:
  raw_data: {type: uri_folder}
  test_size: {type: number, default: 0.2}
outputs:
  prepared: {type: uri_folder}
code: ./src/prep
environment: azureml:sklearn-env:7
command: >-
  python prep.py --raw ${{inputs.raw_data}} --test-size ${{inputs.test_size}} --out ${{outputs.prepared}}
```
Pin environment versions; `@latest` makes reruns non-reproducible.

## Pipeline (Python SDK v2)
```python
from azure.ai.ml import MLClient, Input, load_component
from azure.ai.ml.dsl import pipeline
from azure.identity import DefaultAzureCredential

ml = MLClient.from_config(DefaultAzureCredential())
prep = load_component(source="components/prep.yml")
train = load_component(source="components/train.yml")

@pipeline(default_compute="cpu-cluster")
def churn_pipeline(raw: Input, lr: float = 0.05):
    p = prep(raw_data=raw)
    t = train(training_data=p.outputs.prepared, learning_rate=lr)
    t.compute = "gpu-cluster"                 # per-step override
    return {"model": t.outputs.model}

job = churn_pipeline(raw=Input(type="uri_folder", path="azureml:churn-raw:12"))
job.settings.default_datastore = "workspaceblobstore"
submitted = ml.jobs.create_or_update(job, experiment_name="churn")
ml.jobs.stream(submitted.name)
```
CLI equivalent: a pipeline YAML with `type: pipeline` and `jobs:` referencing component files, submitted with `az ml job create -f pipeline.yml`.

## Reuse and determinism
Azure ML reuses a step's previous output when component, inputs, parameters and environment are unchanged (`is_deterministic: true`, the default). Set `job.settings.force_rerun = True` for a clean run, and mark steps that read external moving data as non-deterministic or pass a date parameter.

## Sharing
Register components to the workspace (`ml.components.create_or_update(prep)`) or to an Azure ML registry for cross-workspace reuse; pipelines then reference `azureml:prep_data:3`. Version components on every change.

## Gotchas
- Compute clusters scale from zero; first step start can take minutes. Set `min_instances` for latency-sensitive dev loops.
- Data inputs referenced as `azureml:<asset>:<version>` give lineage; raw URLs do not.
- Managed identity on the compute needs access to datastores and the key vault.

## Verify
- [ ] Resubmitting unchanged reuses all steps (shown as reused in studio).
- [ ] Component and environment versions are pinned in the submitted job.
- [ ] Output model is registered with the pipeline job as its lineage source.
