---
id: computing-software.ai-ml-engineering.mlflow.mlproject-file-entry-points-and-environments
name: mlproject-file-entry-points-and-environments
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-projects, mlproject, mlproject-file, entry-points, python-env, reproducible-runs, mlproject-parameters]
level: practitioner
status: docs-checked
description: "Package training code as an MLflow Project: MLproject entry points, typed parameters, python_env/conda/docker environments, and running locally or on Databricks/Kubernetes."
sources:
  - https://mlflow.org/docs/latest/ml/projects/
  - https://github.com/mlflow/mlflow/blob/master/mlflow/projects/__init__.py
  - https://github.com/mlflow/mlflow/blob/master/mlflow/cli/__init__.py
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# MLproject file: entry points and environments

**Goal:** anyone can run your training with one command and get the same environment and parameters recorded in MLflow.

## MLproject
```yaml
name: churn-model
python_env: python_env.yaml          # or conda_env: conda.yaml, or docker_env (see Docker skill)
entry_points:
  main:
    parameters:
      data: {type: uri, default: "s3://ml/data/churn/2026-10-01/"}
      alpha: {type: float, default: 0.5}
      max_depth: {type: int, default: 6}
    command: "python train.py --data {data} --alpha {alpha} --max-depth {max_depth}"
  evaluate:
    parameters:
      model_uri: {type: string}
    command: "python evaluate.py --model-uri {model_uri}"
```
`python_env.yaml`:
```yaml
python: "3.11"
build_dependencies: [pip]
dependencies: ["scikit-learn==1.5.2", "pandas==2.2.3"]
```
- Parameter types: `string`, `float`, `int`, `path` (remote URIs such as `s3://` are downloaded to local files before the command runs) and `uri` (relative paths are made absolute; remote URIs are passed through as is).
- Declare every parameter the command uses.

## Run
```bash
mlflow run . -e main -P alpha=0.3 -P max_depth=8 --experiment-name churn --env-manager virtualenv
mlflow run . -e evaluate -P model_uri=runs:/<id>/model
```
`--env-manager local` skips environment creation (fast, but not reproducible); `virtualenv` (venv, with pyenv for Python versions), `uv` or `conda` builds the declared environment. If you do not pass it, MLflow picks the manager from the project (a `python_env` key means virtualenv).

From Python: `mlflow.projects.run(uri=".", entry_point="main", parameters={"alpha": 0.3}, backend="local")`. Backends: `databricks` (runs as a job, needs a cluster spec JSON) and `kubernetes` (needs `docker_env` plus a job template and kube context).

## Inside train.py
Use `mlflow.start_run()` normally; when launched by `mlflow run`, the run is already created and your code attaches to it through the injected `MLFLOW_RUN_ID` (together with `MLFLOW_TRACKING_URI` and `MLFLOW_EXPERIMENT_ID`).

## Verify
- [ ] Fresh clone + `mlflow run .` works on a clean machine.
- [ ] Run page shows the source tags, including the git commit when run from a git checkout.
- [ ] Environment file pins versions (requirements with `==`).

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- MLproject keys, parameter types (string, float, int, path, uri) and their handling, `python_env.yaml` keys (`python`, `build_dependencies`, `dependencies`), env manager choices and default selection: docs/classic-ml/projects/index.mdx and `--env-manager` help in mlflow/utils/cli_args.py.
- `mlflow.projects.run(uri, entry_point, version, parameters, docker_args, experiment_name, backend, backend_config, synchronous, env_manager, build_image, docker_auth, ...)`: mlflow/projects/__init__.py; injected `MLFLOW_RUN_ID`, `MLFLOW_TRACKING_URI`, `MLFLOW_EXPERIMENT_ID`: mlflow/projects/utils.py; git tags `mlflow.source.git.commit` etc.: mlflow/utils/mlflow_tags.py.
- Databricks backend takes a cluster spec JSON via `--backend-config`: projects docs. Kubernetes needs `docker_env`: `validate_docker_env` in mlflow/projects/__init__.py.
- Removed as unconfirmed: the pass-through-of-undeclared-parameters rule, `-r requirements.txt` inside `python_env.yaml` dependencies (the docs list packages), and the claim that parameters are recorded automatically by attaching.

Method: documentation only; no commands were run.
