---
id: computing-software.ai-ml-engineering.mlflow.loading-models-by-uri
name: loading-models-by-uri
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, model-uri, pyfunc, load-model, model-registry, model-aliases, mlflow-models]
level: practitioner
status: gated
description: "Load MLflow models with the right URI scheme: runs:/, models:/name/version, models:/name@alias, file and cloud paths, pyfunc vs native flavor loading and dependency checks."
sources:
  - https://mlflow.org/docs/latest/ml/model/
  - https://mlflow.org/docs/latest/ml/model-registry/
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Loading models by URI

## URI schemes
| URI | Resolves to |
|---|---|
| `runs:/<run_id>/model` | artifact path logged in a run |
| `models:/<name>/<version>` | a specific registry version |
| `models:/<name>@<alias>` | version currently pointed to by an alias (e.g. `@champion`) |
| `models:/<name>/latest` | newest version; resolves in MLflow 3.17 (tested), but avoid in production |
| `s3://bucket/path`, `gs://...`, `file:///...` | a saved model directory (cloud schemes not run here (gated: unconfirmed, source is paywalled or blocked)) |
| `models:/m-<model_id>` | MLflow 3 LoggedModel id |
Unity Catalog: `models:/catalog.schema.model@champion` with `mlflow.set_registry_uri("databricks-uc")` (gated: unconfirmed, source is paywalled or blocked).

## Loading
```python
import mlflow
model = mlflow.pyfunc.load_model("models:/fraud@champion")   # generic predict(DataFrame) interface
preds = model.predict(df)
sk = mlflow.sklearn.load_model("models:/fraud@champion")      # native object (predict_proba etc.)
```
- pyfunc gives a uniform interface for serving and batch scoring; native flavors expose framework methods.
- `model.metadata.get_input_schema()` and `model.metadata.run_id` for validation and lineage.
- Download only: `mlflow.artifacts.download_artifacts("models:/fraud/7", dst_path="./m")` returns the local directory (tested).
- `runs:/<run_id>/model` still loads in MLflow 3 even though the model is stored as a LoggedModel (tested on 3.17.1).

## Environment mismatches
MLflow warns when the current environment differs from the logged `requirements.txt`. Install exact deps with `mlflow.pyfunc.get_model_dependencies("models:/fraud@champion")` → pip install the returned file, or let `mlflow models serve`/`build-docker` create the environment. `get_model_dependencies` returns the path of the model's `requirements.txt` (tested).

## Practices
- Production services resolve an **alias** (`@champion`) at start-up and log the resolved version; promotion = moving the alias.
- Cache the downloaded model locally in serving containers; resolve at deploy time for immutable images if you want strict reproducibility.
- Credentials: loading from the registry needs tracking server access plus artifact store access (unless artifacts are proxied).

## Verify
- [ ] `mlflow.models.get_model_info(uri).signature` matches what the service sends.
- [ ] Resolved version logged at service start.
