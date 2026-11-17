---
id: computing-software.ai-ml-engineering.mlflow.registering-models-and-version-lineage
name: registering-models-and-version-lineage
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, register-model, model-registry, model-version, model-lineage, registered-model]
level: practitioner
status: verified
description: "Register MLflow models with lineage: registered_model_name at log time vs register_model, version descriptions and tags, linking versions to runs/data and naming conventions."
sources:
  - https://mlflow.org/docs/latest/ml/model-registry/
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.register_model
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Registering models and version lineage

## Two ways to register
```python
# 1. at log time (creates the registered model if missing, adds a new version)
mlflow.sklearn.log_model(model, name="model", registered_model_name="fraud-detector",
                         input_example=X.head(), signature=sig)

# 2. later, from any model URI (e.g. after evaluation gates pass)
mv = mlflow.register_model(model_uri=f"runs:/{run_id}/model", name="fraud-detector",
                           tags={"git_sha": sha, "data_version": "2026-10-01"})
```
Option 2 is better for CI pipelines: train and evaluate first, register only candidates that pass.

## Describe the version
```python
from mlflow import MlflowClient
c = MlflowClient()
c.update_model_version("fraud-detector", mv.version,
                       description="LightGBM, 2025-01..2026-09 data, AUC 0.931 on Oct holdout")
c.set_model_version_tag("fraud-detector", mv.version, "validation_status", "passed")
c.update_registered_model("fraud-detector", description="Card-not-present fraud scoring. Owner: risk-ml")
```

## Lineage
- Each version stores `run_id` and `source` (in MLflow 3 the source of a version logged with `registered_model_name` is a `models:/m-<id>` LoggedModel URI; tested); the run holds params, metrics, code version (`mlflow.source.git.commit` tag) and logged datasets (`mlflow.log_input`).
- Add explicit tags for training data snapshot, feature set version and pipeline run id so you can answer "what data trained the model in production?".

## Naming and structure
- One registered model per prediction task and target, not per algorithm (versions can change algorithms).
- Separate registries or name prefixes per environment only if you cannot use aliases plus permissions; prefer copying versions across environments (`copy_model_version`).
- Registration can be asynchronous (`PENDING_REGISTRATION` is a valid `ModelVersionStatus`): wait until `status == "READY"` before setting aliases. On the SQLite backend of MLflow 3.17.1 both routes returned `READY` immediately (tested). `ModelVersion.version` is an `int` there, so compare and key by that type, not `"4"`.

## Verify
- [ ] From the registry UI, a version links to its run, and the run shows dataset and git commit.
