---
id: computing-software.ai-ml-engineering.mlflow.custom-pyfunc-models-and-serving
name: custom-pyfunc-models-and-serving
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, pyfunc, custom-model, mlflow-models, model-serving, conda-env, pip-requirements, signature, input-example, mlflow-serve, model-flavor, preprocessing-bundling]
level: advanced
status: verified
description: "Package non-standard models (custom preprocessing, ensembles, non-sklearn frameworks) as MLflow pyfunc models with a correct signature and environment so serving matches training exactly."
sources:
  - https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html
  - https://mlflow.org/docs/latest/models.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MLflow custom `pyfunc` models — packaging what the built-in flavors don't

**Goal:** wrap a model (or a model plus preprocessing, or an ensemble of several models) that doesn't fit MLflow's built-in framework flavors into a `pyfunc` that serves identically to how it was tested, with no "works when I load it, breaks when MLflow serves it" surprise.

## 1. When you need `pyfunc` instead of a built-in flavor
Built-in flavors (`mlflow.sklearn`, `mlflow.pytorch`, `mlflow.transformers`, etc.) handle the common case: one model object, standard predict signature. Reach for `mlflow.pyfunc.PythonModel` when:
- Prediction requires **preprocessing/postprocessing bundled with the model** (a tokenizer, a custom scaler fit on training data, business-rule thresholding on raw scores) — if this logic lives in separate application code instead of the model artifact, it drifts from the model over time and training/serving skew creeps in silently.
- You're serving an **ensemble or pipeline of multiple model objects** (a ranker plus a re-ranker, a classifier plus a calibration layer) that no single built-in flavor represents as one unit.
- You're using a framework MLflow has no native flavor for — `pyfunc`'s `predict(context, model_input)` contract is framework-agnostic.

```python
class MyModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.tokenizer = joblib.load(context.artifacts["tokenizer"])
        self.model = load_my_model(context.artifacts["weights"])

    def predict(self, context, model_input, params=None):
        features = self.tokenizer.transform(model_input)
        return self.model.predict(features)

mlflow.pyfunc.save_model(path="model", python_model=MyModel(),
                          artifacts={"tokenizer": "tok.joblib", "weights": "weights.pt"},
                          pip_requirements=["torch==2.3.0", "joblib==1.4.0"],
                          signature=signature, input_example=example_df)
```

## 2. The three things that cause "works locally, fails when served"
- **Environment under-specification**: `pip_requirements` (or a full `conda.yaml`) must list every package `predict` actually imports, pinned to the versions used when the model was validated — an unpinned or incomplete list means the serving environment MLflow builds (or that a downstream deployer builds from the logged `conda.yaml`) can silently resolve different versions, changing numeric behavior or breaking on an API change. Use `mlflow.models.infer_pip_requirements(model_uri, flavor)` as a starting point (on a saved sklearn-based pyfunc it returned `numpy`, `pandas`, `psutil`, `scikit-learn`, `scipy`, all pinned; it also adds packages you may not want, so review it), then verify by hand against what `load_context`/`predict` actually touch — inference misses implicit imports inside conditional branches.
- **Missing or wrong signature**: `signature` (input/output schema, inferred via `mlflow.models.infer_signature(input_example, output)`) is what lets MLflow validate incoming requests at serving time and lets other tools (model registry UI, serving frameworks) know the expected shape. A model saved without a signature serves anything you throw at it with no validation — a type mismatch becomes a confusing runtime error inside `predict` instead of a clear 400 at the boundary (tested: with a signature, `mlflow models serve` answered HTTP 400 `BAD_REQUEST ... Data is not compatible with model signature`; the same bad input to a model saved without one failed inside `predict` with `ValueError: could not convert string to float`).
- **`load_context` referencing artifacts by the wrong key or absolute path**: artifacts dict keys in `context.artifacts` must match exactly what was passed to `artifacts={...}` at save time, and paths inside `load_context` must be relative to what MLflow reconstructs at load time (it copies artifacts into a new directory on load) — a hardcoded absolute path from the training machine breaks the moment the model is loaded anywhere else, including the serving container.

## 3. Testing before you trust it in production
- `mlflow.pyfunc.load_model(path).predict(input_example)` **in a fresh environment** (a new venv/container, not the one you trained in) is the real test — loading in the same process/environment you saved from hides every missing-dependency bug.
- `mlflow models serve -m <uri>` locally (MLflow 3.17.1 starts `uvicorn` for it, which must be on PATH when you use `--env-manager local`; `/ping` returned 200 and `/invocations` took `{"dataframe_split": {...}}` and returned `{"predictions": [...]}`), then send a real HTTP request matching the signature, before deploying to the actual serving infrastructure — this exercises the same code path (environment build, signature validation, `pyfunc` wrapper) that production serving will use.
- If `predict` depends on GPU availability, test the CPU-only fallback path too unless you're certain the serving environment always has a GPU — a model that assumes `.cuda()` in `load_context` with no device check fails outright on a CPU-only serving replica.

## Verify
- [ ] `pip_requirements`/`conda.yaml` lists every package actually imported by `load_context`/`predict`, with pinned versions matching what was validated.
- [ ] Model has an explicit `signature` inferred from a real input/output example, not omitted.
- [ ] `load_context` uses only the artifact keys/relative paths MLflow provides, no hardcoded absolute paths.
- [ ] Model loads and predicts correctly in a fresh environment (new venv or container), not just the training environment.
- [ ] `mlflow models serve` tested locally with a real request before deploying to production serving infra.
- [ ] Device assumptions (GPU vs CPU) in `predict` are explicit and tested on the actual serving hardware.
