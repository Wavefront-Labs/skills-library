---
id: computing-software.ai-ml-engineering.mlflow.reproducing-a-past-run
name: reproducing-a-past-run
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-projects, run-reproduction, reproducibility, git-commit-tag, download-artifacts, lineage]
level: practitioner
status: docs-checked
description: "Reproduce a past MLflow run: read source commit, params, environment and dataset inputs from the run, download its artifacts, re-execute, and compare metrics within tolerance."
sources:
  - https://mlflow.org/docs/latest/ml/tracking/
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.artifacts.html
  - https://mlflow.org/docs/latest/ml/dataset/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reproducing a past run

**Goal:** given a run ID (often of a production model), rebuild the same model or explain why it can't be rebuilt.

## 1. Collect what the run recorded
```python
from mlflow import MlflowClient
c = MlflowClient(); r = c.get_run(run_id)
r.data.params                                         # hyperparameters
r.data.tags["mlflow.source.git.commit"]               # code version (if run from a git checkout)
r.data.tags.get("mlflow.source.name")                 # entry script / notebook
[i.dataset for i in r.inputs.dataset_inputs]          # logged datasets: name, digest, source
```
Model environment: the logged model directory contains `requirements.txt`, `python_env.yaml`/`conda.yaml`:
```python
import mlflow
local = mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path="model")
```
Gaps you'll often find: no git commit (run from an uncommitted notebook), data path recorded but not a version, unpinned requirements. Fix those in the training template so the next run is reproducible.

## 2. Re-execute
- Check out the commit; create the environment from the logged requirements (`mlflow models` env or `pip install -r requirements.txt`).
- Fetch the exact data version (table version, lakeFS commit, snapshot path) referenced by the dataset input digest/source.
- Run with the same params and seeds; if it was an MLflow Project: `mlflow run <repo> --version <commit> -P ...`.

## 3. Compare
- Metrics within tolerance (GPU nondeterminism makes exact equality unrealistic for deep learning).
- Predictions of old vs new model on a fixed sample: correlation, max absolute difference.
- If they differ beyond tolerance: diff library versions first, then data row counts/digests, then hardware (GPU type, number of workers).

## Make it routine
Training template logs: git commit (refuse to run with a dirty tree in CI), full pinned environment, dataset inputs with versions/digests, random seeds, hardware info. Periodically run a reproduction check on the current production model.

## Verify
- [ ] Reproduction succeeded or the missing ingredient is documented.
- [ ] Metric and prediction differences reported with tolerance.
- [ ] Template updated to close any gaps found.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- Tags `mlflow.source.git.commit`, `mlflow.source.name`: mlflow/utils/mlflow_tags.py; `RunInputs.dataset_inputs` and `DatasetInput.dataset` with `name`, `digest`, `source`: mlflow/entities; `mlflow.artifacts.download_artifacts(run_id=, artifact_path=)`: mlflow/artifacts/__init__.py.
- Models log `requirements.txt`, `python_env.yaml` and `conda.yaml` automatically: docs/classic-ml/model/index.mdx. `mlflow run <repo> --version <commit>`: docs/classic-ml/projects/index.mdx.
- Removed as unconfirmed: the claim that fixed-seed tree models are often exactly reproducible.

Method: documentation only; no commands were run.
