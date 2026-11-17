---
id: computing-software.ai-ml-engineering.mlflow.mlflow-scoring-server-tuning
name: mlflow-scoring-server-tuning
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-serve-workers, mlflow-models-serve, mlserver, gunicorn, uvicorn, inference-performance]
level: practitioner
status: docs-checked
description: "Tune MLflow model serving: uvicorn workers, request timeout (MLFLOW_SCORING_SERVER_REQUEST_TIMEOUT), the removed MLServer backend, input formats and health endpoints."
sources:
  - https://mlflow.org/docs/latest/ml/deployment/deploy-model-locally/
  - https://github.com/mlflow/mlflow/blob/master/mlflow/models/cli.py
  - https://github.com/mlflow/mlflow/blob/master/CHANGELOG.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scoring server tuning (workers, timeouts, MLServer)

## Default server
`mlflow models serve -m models:/fraud@champion -p 5001 --env-manager local` starts a uvicorn-based server exposing `/invocations`, `/ping`, `/health` (same as `/ping`) and `/version`. Options include `--host`, `--port`, `--workers`, `--timeout` and `--env-manager` (default virtualenv).

## Concurrency
- `--workers N` / `-w` (or `MLFLOW_MODELS_WORKERS`): number of uvicorn workers, default 1. Workers are separate processes, so memory grows with N; size N against CPU cores and model memory, and measure for GPU models.
- Request timeout: `--timeout` / `-t` or `MLFLOW_SCORING_SERVER_REQUEST_TIMEOUT`, in seconds, default 60; raise it for slow models.

## MLServer backend (removed)
The MLServer pyfunc backend, and with it `--enable-mlserver`, parallel inference workers and adaptive batching through MLflow, was removed in MLflow 3.13.0 (it was deprecated before that): `mlflow models serve` and `build-docker` always use the built-in scoring server. If you need request batching or the Open Inference Protocol, serve the model through a platform that provides them, for example KServe (see the SageMaker and KServe deployment skill).
## Request format
`/invocations` takes JSON (`dataframe_split`, `dataframe_records`, `instances`, `inputs`) with `Content-Type: application/json`, or CSV with `application/csv`. For very large payloads consider batch scoring instead of HTTP.

## Health and readiness
Use `/ping` (or its alias `/health`) for liveness/readiness probes; warm the model at start-up (send a sample request) before marking ready, especially with lazy-loaded frameworks.

## Verify
- [ ] Load test at expected concurrency: p50/p99 latency and memory per worker recorded for several `--workers` values.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `serve` options (`--port`, `--host`, `--timeout`/`-t` with env `MLFLOW_SCORING_SERVER_REQUEST_TIMEOUT` default 60, `--workers`/`-w` with env `MLFLOW_MODELS_WORKERS` default 1, uvicorn workers, `--env-manager` default virtualenv; no `--enable-mlserver`): mlflow/models/cli.py, mlflow/utils/cli_args.py and mlflow/environment_variables.py.
- Endpoints and input formats: docs/classic-ml/deployment/deploy-model-locally/index.mdx.
- MLServer removed in 3.13.0 (previously deprecated): CHANGELOG.md.
- Removed as unconfirmed: the MLServer `model-settings.json` batching keys and env vars (the backend no longer exists), the one-worker-per-GPU rule, and the `dataframe_split` efficiency claim. The old MLServer docs link was dropped.

Method: documentation only; no commands were run.
