---
id: computing-software.ai-ml-engineering.mlflow.mlflow-models-build-docker
name: mlflow-models-build-docker
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-serve, mlflow-deployment, build-docker, invocations, model-serving-container, generate-dockerfile]
level: practitioner
status: docs-checked
description: "Package an MLflow model as a Docker serving image with build-docker: env managers, /invocations payload formats, health endpoints, Dockerfile generation and image-size control."
sources:
  - https://mlflow.org/docs/latest/ml/deployment/deploy-model-locally/
  - https://github.com/mlflow/mlflow/blob/master/mlflow/models/cli.py
  - https://github.com/mlflow/mlflow/blob/master/CHANGELOG.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# mlflow models build-docker

**Goal:** a self-contained container that serves any MLflow model via a standard REST API.

## Build and run
```bash
mlflow models build-docker -m "models:/churn@champion" -n churn-serving:1.4.0
docker run --rm -p 8080:8080 churn-serving:1.4.0
```
- `-m` accepts `runs:/<run_id>/model`, `models:/name/version`, `models:/name@alias`, or a local path. Resolve aliases at build time and tag the image with the concrete version for traceability.
- The image's default entrypoint serves the model at port 8080 with MLflow's built-in scoring server; `--enable-mlserver` (MLServer backend) was removed in MLflow 3.13.0. Without `-n` the image is named `mlflow-pyfunc-servable`.
- `--env-manager local|virtualenv|uv|conda` controls how the model's dependencies (`requirements.txt`, `python_env.yaml`, `conda.yaml` logged with the model) are installed; the default is virtualenv.

## Call it
```bash
curl -s localhost:8080/ping                         # health check (/health is the same)
curl -s -X POST localhost:8080/invocations -H "Content-Type: application/json" -d '{
  "dataframe_split": {"columns": ["age", "plan", "tenure"], "data": [[42, "pro", 13]]}}'
```
Accepted JSON keys: `dataframe_split`, `dataframe_records`, `instances` and `inputs` (tensor-style input), plus `params` for models that take inference params. CSV is accepted with `Content-Type: application/csv`; the header must be `application/json` or `application/csv`.

## Customising
`mlflow models generate-dockerfile -m <uri> -d build_dir/` writes a Dockerfile (equivalent to the one `build-docker` produces; the output directory defaults to `mlflow-dockerfile`) so you can add OS packages, a non-root user, or a different base image, then build with your normal tooling.

Before building, smoke-test the model's environment offline: `mlflow models predict -m <uri> -i sample.json -t json --env-manager virtualenv` (or `uv`) recreates the logged environment and scores the file (`-t` takes `json` or `csv`), catching missing dependencies before the image exists. Use `--env-manager local` only to debug in the current interpreter.

## Production concerns
- Image size: the generated image installs the model's environment, so keep the logged requirements minimal; the Python version comes from the model's logged `python_env.yaml`.
- Workers and timeouts: see the scoring-server tuning skill (`--workers`, `--timeout`, `MLFLOW_SCORING_SERVER_REQUEST_TIMEOUT`, default 60 s).
- Run as non-root (via `generate-dockerfile`) and scan the image like any other service.

## Verify
- [ ] `/invocations` returns predictions identical to `mlflow.pyfunc.load_model(...).predict` on the same rows.
- [ ] Image tagged with model name + version.
- [ ] Health and request-timeout behaviour tested under load.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `build-docker` options (`-m`, `-n` default `mlflow-pyfunc-servable`, `--env-manager`, `--install-mlflow`, `--mlflow-home`, `--install-java`) and `generate-dockerfile -d` default `mlflow-dockerfile`; no `--enable-mlserver` option: mlflow/models/cli.py and mlflow/utils/cli_args.py (env manager default virtualenv; options local, virtualenv, uv, conda).
- MLServer removal in 3.13.0: CHANGELOG.md. Endpoints `/invocations`, `/ping`, `/health`, `/version`, JSON keys `dataframe_split`/`dataframe_records`/`instances`/`inputs`, `application/csv`: docs/classic-ml/deployment/deploy-model-locally/index.mdx.
- `mlflow models predict` flags `-i`, `-t json|csv`, `--env-manager`: mlflow/models/cli.py. Logged `conda.yaml`, `python_env.yaml`, `requirements.txt`: docs/classic-ml/model/index.mdx.
- Removed as unconfirmed: gunicorn worker environment variables for the image and the claims about conda image size relative to virtualenv.

Method: documentation only; no commands were run.
