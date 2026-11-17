---
id: computing-software.ai-ml-engineering.mlflow.search-runs-and-mlflowclient
name: search-runs-and-mlflowclient
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, experiment-tracking, search-runs, mlflowclient, filter-string, metric-history, run-comparison]
level: practitioner
status: verified
description: "Query MLflow runs programmatically: mlflow.search_runs filter syntax, ordering and paging with MlflowClient, metric history, and building leaderboards and cleanup scripts."
sources:
  - https://mlflow.org/docs/latest/search-runs.html
  - https://mlflow.org/docs/latest/python_api/mlflow.client.html
  - https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.search_runs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Querying runs with search_runs and MlflowClient

## pandas leaderboard
```python
import mlflow
df = mlflow.search_runs(
    experiment_names=["churn"],
    filter_string="metrics.val_auc > 0.80 and params.model_type = 'xgboost' "
                  "and attributes.status = 'FINISHED' and tags.dataset_version = 'v12'",
    order_by=["metrics.val_auc DESC"], max_results=20,
)
df[["run_id", "metrics.val_auc", "params.max_depth", "start_time"]]
```
Filter grammar: `metrics.`, `params.`, `tags.`, `attributes.` (status, run_name, start_time, end_time, artifact_uri), `datasets.` (name, digest, context); operators: metrics take `= != < <= > >=`; params, tags and string attributes take `= != LIKE ILIKE` (params and tags also `IS NULL` / `IS NOT NULL`); numeric attributes such as `start_time` take the numeric comparators; `IN` works only for `attributes.run_id` and `datasets.name/digest/context` (`attributes.status IN (...)` is rejected, tested on 3.17.1); join with `and` only (`or` raises `Invalid clause(s) in filter string`). Quote names with special characters using backticks or double quotes: `tags."mlflow.runName" LIKE 'baseline%'`.

**Params are strings.** `params.max_depth > 5` raises `Expected a quoted string value`, and `> '5'` raises `Invalid comparator '>'`; params only support `=`, `!=`, `LIKE`, `ILIKE`, `IS [NOT] NULL` (tested; matches the search docs). Quote numeric values (`params.batch_size = '2'`), filter ranges in pandas after fetching (cast with `astype(float)`), or log the value additionally as a metric.

## Paging with the client
```python
from mlflow import MlflowClient
from mlflow.entities import ViewType
client = MlflowClient()
exp = client.get_experiment_by_name("churn")
token = None
while True:
    page = client.search_runs([exp.experiment_id], filter_string="attributes.status = 'FAILED'",
                              run_view_type=ViewType.ACTIVE_ONLY, max_results=500, page_token=token)
    for r in page:
        client.delete_run(r.info.run_id)          # soft delete; `mlflow gc` purges later
    token = page.token
    if not token:
        break
```
`mlflow.search_runs` returns a DataFrame of at most `max_results` rows (default 100,000); `MlflowClient.search_runs` defaults to `max_results=1000` and accepts at most 50,000 per page (`SEARCH_MAX_RESULTS_THRESHOLD = 50000`); `page.token` is `None` on the last page (tested with page size 2).

## Metric history and comparisons
```python
hist = client.get_metric_history(run_id, "val_loss")   # list of Metric(step, value, timestamp)
best = df.iloc[0]; model_uri = f"runs:/{best.run_id}/model"
```
`run.data.metrics` holds only the **latest** value per key (tested: step 2 value after steps 0-2); use history for curves.

MLflow 3 adds `mlflow.search_logged_models(experiment_ids=[...])` to query LoggedModel entities (ran and returned the logged models) - prefer it when models are logged as first-class objects.

## Verify
- [ ] Leaderboard query matches the UI sort for the same filter.
- [ ] Cleanup script dry-run prints the run ids before deleting.
