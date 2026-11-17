---
id: computing-software.ai-ml-engineering.mlops.ml-metadata-and-artifact-lineage
name: ml-metadata-and-artifact-lineage
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-governance, ml-lineage, ml-metadata, artifact-lineage, mlmd, openlineage, sagemaker-lineage]
level: practitioner
status: draft
description: "Track ML lineage so you can answer what data and code produced a model and which models used a dataset: MLMD, Vertex ML Metadata, SageMaker lineage, MLflow inputs, OpenLineage."
sources:
  - https://www.tensorflow.org/tfx/guide/mlmd
  - https://cloud.google.com/vertex-ai/docs/ml-metadata/introduction
  - https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html
  - https://openlineage.io/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ML metadata and artifact lineage

**Goal:** answer audit and debugging questions in minutes: "Which data, code and parameters produced model v12?" and "Which models were trained on the dataset we must delete?"

## The model
Most systems share one shape:
- **Artifacts:** datasets, features, models, evaluation reports (with URI + version/digest).
- **Executions:** runs of pipeline steps (with parameters, code version, environment).
- **Events/associations:** execution consumed artifact A, produced artifact B.
- **Contexts:** groupings (pipeline run, experiment).

## Systems
- **ML Metadata (MLMD):** backs TFX and Kubeflow Pipelines; records every component's inputs/outputs automatically.
- **Vertex ML Metadata:** same model, populated by Vertex Pipelines; lineage graph in the console.
- **SageMaker ML Lineage Tracking:** artifacts, actions, contexts and associations, auto-created for SageMaker jobs/pipelines/model packages; queryable with `LineageQuery`.
- **MLflow:** run params, source commit, `mlflow.log_input(dataset)` for data inputs, logged models linked to runs; registry versions link to runs.
- **OpenLineage (+ Marquez/DataHub/OpenMetadata):** data pipeline lineage from Airflow/Spark/dbt; connects upstream tables to the features your models use.

## Make it complete
Lineage breaks at hand-offs. Common holes:
- Training reads "latest" data without recording the version -> log table version/snapshot ID or a content digest.
- Features built outside the pipeline (notebook exports) -> forbid for production models.
- Model copied between registries without carrying the source run reference.
Join data lineage (OpenLineage/catalog) with ML lineage (registry/MLMD) via shared dataset identifiers.

## Use cases to test it against
- Data deletion/correction request: find all models (and their deployments) trained on affected data.
- Incident: a bad upstream table load - which models/predictions were affected, from when.
- Audit: reproduce the evidence behind a production model's approval.

## Verify
- [ ] For the current production model, lineage reaches source tables/versions and code commit without manual digging.
- [ ] Reverse query (dataset -> models) works.
- [ ] Hand-off points (registry copies, feature exports) carry identifiers.
