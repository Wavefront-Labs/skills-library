---
id: computing-software.ai-ml-engineering.mlflow.multistep-workflows-mlflow-run
name: multistep-workflows-mlflow-run
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, multistep-workflow, mlflow-run, mlflow-projects, pipeline, nested-runs, run-caching]
level: practitioner
status: docs-checked
description: "Chain MLflow Projects entry points into a multistep workflow: driver script with mlflow.run, passing artifact URIs between steps, nested runs, and reusing finished steps."
sources:
  - https://mlflow.org/docs/latest/ml/projects/
  - https://github.com/mlflow/mlflow/tree/master/examples/multistep_workflow
  - https://github.com/mlflow/mlflow/blob/master/mlflow/projects/__init__.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multistep workflows chaining mlflow.run

**Use when:** a lightweight pipeline (download -> preprocess -> train -> evaluate) should be reproducible and tracked without adopting a full orchestrator.

## MLproject with several entry points
```yaml
name: churn
python_env: python_env.yaml
entry_points:
  load_raw:   {parameters: {snapshot: string}, command: "python load.py --snapshot {snapshot}"}
  featurize:  {parameters: {raw_uri: uri}, command: "python featurize.py --raw-uri {raw_uri}"}
  train:      {parameters: {features_uri: uri, lr: {type: float, default: 0.05}},
               command: "python train.py --features-uri {features_uri} --lr {lr}"}
  main:       {parameters: {snapshot: string}, command: "python main.py --snapshot {snapshot}"}
```

## Driver (main.py)
```python
import mlflow
from mlflow.tracking import MlflowClient

def run_step(entry, params):
    sub = mlflow.run(".", entry_point=entry, parameters=params, env_manager="local")
    return MlflowClient().get_run(sub.run_id)

with mlflow.start_run(run_name="pipeline") as parent:
    raw = run_step("load_raw", {"snapshot": snapshot})
    raw_uri = f"{raw.info.artifact_uri}/raw"
    feats = run_step("featurize", {"raw_uri": raw_uri})
    run_step("train", {"features_uri": f"{feats.info.artifact_uri}/features"})
```
Each step logs its outputs as artifacts; the next step receives an artifact URI, not a local path, so steps can run on different machines/backends.

## Reusing completed steps
The official example (`examples/multistep_workflow/main.py`) searches the experiment with `MlflowClient().search_runs`, looks for a run of the same entry point and parameters whose status is FINISHED and whose `mlflow.source.git.commit` tag matches, and reuses it instead of re-running. Implement the same check to make reruns cheap. A `mlflow.run` call made inside an active run tags the new run with `mlflow.parentRunId`.

## Limits
This pattern is a driver script, not an orchestrator. When you need scheduling, retries or fan-out, move the steps into a workflow engine and keep MLflow for tracking.

## Verify
- [ ] Parent run shows child runs for each step; re-running with identical params skips cached steps.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- Parameter types `string`, `float`, `int`, `path`, `uri` (so `str` was invalid): docs/classic-ml/projects/index.mdx; example MLproject in examples/multistep_workflow.
- `mlflow.run` returns a `SubmittedRun` with `run_id` and `wait()`; parent run tag set when an active run exists: mlflow/projects/__init__.py and utils.py; result-caching logic (`_already_ran`, FINISHED status, git commit tag): examples/multistep_workflow/main.py.
- Removed as unconfirmed: the list of missing orchestrator features and the Airflow/Kubeflow/Prefect names.

Method: documentation only; no commands were run.
