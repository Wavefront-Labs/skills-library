---
id: computing-software.ai-ml-engineering.mlflow.experiment-tracking-and-model-registry
name: experiment-tracking-and-model-registry
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, experiment-tracking, tracking-uri, set-tracking-uri, autolog, log-param, log-metric, log-artifact, model-signature, infer-signature, input-example, model-registry, registered-model, model-aliases, champion-challenger, model-stages, mlflow-models-serve, pyfunc, reproducibility, mlops, model-versioning]
level: practitioner
status: gated
description: "Track ML experiments in MLflow (tracking URI, autolog, params/metrics/artifacts), log models with signatures, promote versions with registry aliases, and serve with mlflow models serve."
sources:
  - https://mlflow.org/docs/latest/index.html
  - https://mlflow.org/docs/latest/tracking.html
  - https://mlflow.org/docs/latest/model-registry.html
  - https://mlflow.org/docs/latest/models.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MLflow Experiment Tracking and Model Registry — every run reproducible, every deploy traceable

**Goal:** record each training run so any result can be reproduced, and move models to production through the registry by alias so serving code never hard-codes a version.

## 1. Point at a tracking server
```python
import mlflow
mlflow.set_tracking_uri("http://mlflow.internal:5000")   # or env MLFLOW_TRACKING_URI
mlflow.set_experiment("churn-model")
```
- With no URI, MLflow 3.17.1 defaulted to a local SQLite database, `sqlite:///<cwd>/mlflow.db` (`mlflow.get_tracking_uri()`, tested); older releases wrote a `./mlruns` file store (model artifacts are still written under `./mlruns`). Fine for a laptop, invisible to the team.
- A shared server: `mlflow server --backend-store-uri postgresql://... --artifacts-destination s3://<BUCKET>/mlflow --host 0.0.0.0 --port 5000`. The backend store holds params/metrics; artifacts (models, plots) live in object storage. The registry needs a database backend in older releases; the Postgres/S3 server command was not run here (gated: unconfirmed, source is paywalled or blocked); `mlflow server --help` lists `--backend-store-uri`, `--registry-store-uri` and `--artifacts-destination`.
- The open-source server has no authentication by default; put it behind a proxy or enable the basic-auth app before exposing it (gated: unconfirmed, source is paywalled or blocked).

## 2. Log a run
```python
with mlflow.start_run(run_name="lgbm-depth8") as run:
    mlflow.log_params({"max_depth": 8, "lr": 0.05, "features": "v3"})
    for step, auc in enumerate(val_aucs):
        mlflow.log_metric("val_auc", auc, step=step)
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.set_tags({"git_sha": GIT_SHA, "data_version": DATA_HASH})
```
- `mlflow.autolog()` (or `mlflow.sklearn.autolog()`, `mlflow.pytorch.autolog()`, ...) captures params, metrics and the model for supported libraries. Call it **before** `fit`. It logs a lot; turn off pieces with arguments like `log_models=False` if you log models yourself.
- Params are immutable per run and stringified (tested: `get_run(...).data.params['a']` is `str`); logging the same key again with the same value is accepted, with a different value raises `Changing param values is not allowed` (also via `log_params`).
- Always tag the git commit and a data version/hash — metrics without the data they came from cannot be reproduced.
- Use nested runs (`start_run(nested=True)`) for hyperparameter searches so the parent groups trials.

## 3. Log the model with a signature
```python
from mlflow.models import infer_signature
sig = infer_signature(X_val.head(100), model.predict(X_val.head(100)))
mlflow.sklearn.log_model(model, name="model", signature=sig,
                         input_example=X_val.head(3),
                         registered_model_name="churn")
```
- The signature records input columns and types; serving rejects or warns on mismatched payloads instead of silently mis-predicting. An integer column with missing values at inference may need to be logged as float.
- MLflow 3 renamed the `artifact_path` argument of `log_model` to `name`; `artifact_path=` still works on 3.17.1 but logs a deprecation warning (tested); 2.x code uses `artifact_path="model"`.
- The logged model directory includes `requirements.txt`/`conda.yaml` with library versions — check they are pinned correctly; mismatched scikit-learn versions break unpickling (see computing-software.ai-ml-engineering.scikit-learn.pipelines-and-cross-validation).

## 4. Promote with aliases, not stages
Stages (`Staging`/`Production`/`Archived`) are deprecated since MLflow 2.9 in favour of **aliases** and tags.
```python
from mlflow import MlflowClient
c = MlflowClient()
c.set_registered_model_alias("churn", "champion", version=7)   # raises if version 7 does not exist (tested)
c.set_model_version_tag("churn", "7", "validation_status", "approved")
model = mlflow.pyfunc.load_model("models:/churn@champion")
```
- An alias points to exactly one version; moving it is the deployment, and moving it back is the rollback.
- Use a `challenger` alias for the candidate under shadow or canary evaluation (see computing-software.ai-ml-engineering.mlops.production-model-monitoring).
- Gate promotion in CI: compare the candidate's metrics on the same frozen evaluation set as the champion before calling `set_registered_model_alias`.

## 5. Serve
```bash
mlflow models serve -m "models:/churn@champion" -p 5001 --env-manager local
curl -X POST localhost:5001/invocations -H "Content-Type: application/json" \
  -d '{"dataframe_split": {"columns": ["age","plan"], "data": [[42,"pro"]]}}'
```
- `--env-manager` takes `local`, `virtualenv`, `uv` or `conda` (per `mlflow models serve --help`); `local` reuses the current environment (faster, less isolated), and with it the `uvicorn` executable must be on PATH (tested: serving `models:/churn@champion` returned `{"predictions": [1]}`). The default-manager behaviour was not confirmed (gated: unconfirmed, source is paywalled or blocked).
- `mlflow models build-docker -m ... -n churn-img` packages a container for Kubernetes or other platforms (Docker not available here (gated: unconfirmed, source is paywalled or blocked)).
- The process loads the version the alias pointed to at startup; moving the alias needs a restart or reload.

## Verify
- [ ] Runs appear on the shared server (not a local `mlruns`) with git SHA and data version tags.
- [ ] Re-running training from a run's logged params and data version reproduces its metrics within noise.
- [ ] The logged model has a signature and input example; a malformed payload is rejected.
- [ ] Serving code loads `models:/<name>@champion`, never a hard-coded version number.
- [ ] Moving the alias back to the previous version and restarting restores the old predictions.
