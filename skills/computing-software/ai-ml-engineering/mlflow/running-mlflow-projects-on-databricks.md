---
id: computing-software.ai-ml-engineering.mlflow.running-mlflow-projects-on-databricks
name: running-mlflow-projects-on-databricks
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-databricks-backend, mlflow-projects, databricks-jobs, cluster-spec, mlproject]
level: practitioner
status: docs-checked
description: "Execute MLflow Projects on Databricks clusters with the databricks backend: cluster spec JSON, experiment paths, git sources, and when to switch to Jobs or Asset Bundles."
sources:
  - https://docs.databricks.com/aws/en/mlflow/projects
  - https://mlflow.org/docs/latest/ml/projects/#run-an-mlflow-project-on-databricks
  - https://docs.databricks.com/aws/en/dev-tools/bundles/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running MLflow Projects on Databricks

**Goal:** a project developed locally runs on a Databricks job cluster with one command and logs to the workspace tracking server.

## Setup
```bash
pip install mlflow
# authenticate to the workspace first, as described in the Databricks docs
```
Pass the target experiment with `--experiment-id <experiment-id>`.

## Cluster spec
`cluster-spec.json` describes a new job cluster:
```json
{
  "new_cluster": {
    "spark_version": "<runtime version>",
    "node_type_id": "i3.xlarge",
    "num_workers": 2
  }
}
```
The Databricks page describes a JSON document containing a `new_cluster` structure; MLflow's page nests it under `cluster_spec`. Check both for your MLflow version.

## Run
```bash
mlflow run https://github.com/acme/churn-train#training --version v1.4.0 \
  -b databricks --backend-config cluster-spec.json \
  --experiment-id <experiment-id> -P alpha=0.3
```
- `--version` selects a git commit or branch; Tracking records the git commit and parameters.
- The Databricks page's example output shows the project being uploaded to a DBFS path before the entry point runs.

## Limits and modern alternatives
For recurring or production jobs use Databricks Jobs (see the Databricks bundles docs for defining them as code), and keep the MLproject entry points as the code those tasks call so local and remote runs stay identical.

## Gotchas
- To install libraries on workers, use the cluster specification format; Python wheels must be uploaded to DBFS and listed as pypi dependencies.

## Verify
- [ ] The run appears in the workspace experiment with the git commit and parameters.
- [ ] Confirm in the workspace that no cluster is left running after the run.

## Checked
Date: 2026-10-28.
- Confirmed in the Databricks MLflow Projects page and the MLflow Projects page: `mlflow run <uri> -b databricks --backend-config`, `new_cluster` structure, `--experiment-id`, `i3.xlarge`, `num_workers`, DBFS upload, worker libraries via cluster spec and DBFS wheels, `--version` for commits and branches, git commit and parameters recorded.
- Removed as unconfirmed: `databricks auth login` and `databricks-sdk` setup, `MLFLOW_TRACKING_URI` values, `--experiment-name`, `-v` (documented as verbose in MLflow's troubleshooting), the runtime string, `spark_env_vars`, Workflows and `--run-id` claims, bundle commands, policy and tracking-URI gotchas.
Method: documentation only; no commands were run.
