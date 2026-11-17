---
id: computing-software.ai-ml-engineering.mlflow.archiving-and-deleting-registered-model-versions
name: archiving-and-deleting-registered-model-versions
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, model-version-retention, model-registry, mlflow-gc, aliases, lifecycle]
level: practitioner
status: gated
description: "Retire MLflow registry versions safely: alias and tag based archiving, deleting versions and models, purging run artifacts with mlflow gc, and Unity Catalog differences."
sources:
  - https://mlflow.org/docs/latest/ml/model-registry/
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html
  - https://mlflow.org/docs/latest/api_reference/cli.html#mlflow-gc
  - https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Archiving and deleting model versions

**Goal:** the registry lists only versions someone might deploy or audit, storage does not grow forever, and nothing serving traffic is deleted.

## Stages are deprecated; archive with aliases and tags
Since MLflow 2.9.0, stages (Staging/Production/Archived) are deprecated in favour of aliases and tags (MLflow model registry workflow docs and RFC issue 10336); Unity Catalog never had them (gated: unconfirmed, source is paywalled or blocked). Use:
- aliases for what is live (`champion`, `challenger`),
- a tag for lifecycle state: `client.set_model_version_tag("churn", "12", "lifecycle", "archived")`.
(`version` is an `int` and alias values are `int` on MLflow 3.17.1 with SQLite, `str` in some older releases and APIs, hence the `int()` casts; the loop above ran as written.) An archived version keeps its lineage (run, metrics, data) for audit but is filtered out of tooling:
```python
from mlflow import MlflowClient
c = MlflowClient()
live = {int(v) for v in c.get_registered_model("churn").aliases.values()}
versions = c.search_model_versions("name='churn'", order_by=["version_number DESC"])
newest = int(versions[0].version)
for mv in versions:
    if int(mv.version) not in live and int(mv.version) < newest - 10:
        c.set_model_version_tag("churn", mv.version, "lifecycle", "archived")
```

## Retention policy
Write it down per model class, for example: keep all aliased versions; keep the last N unaliased versions; keep regulated models' versions for the record-retention period (often years) even if archived; delete everything else after 90 days archived.

## Deleting
- `c.delete_model_version("churn", "3")` removes the registry entry. Deleting a version that an alias points to succeeded and silently removed the alias on the SQLite backend (tested: `get_model_version_by_alias` then raised `Registered model alias champion not found`); other backends were not tested (gated: unconfirmed, source is paywalled or blocked). Reassign the alias first either way.
- `c.delete_registered_model("churn")` deletes all versions; serving endpoints that load `models:/churn@champion` break immediately.
- Registry deletion does not delete the run artifacts the version came from. To reclaim storage, delete the runs (`client.delete_run`) and then purge: `mlflow gc --backend-store-uri <db-uri> --older-than 30d` (permanently removes runs in the deleted state and their artifacts; the age is `#d#h#m#s`; with a tracking server that proxies artifacts set `MLFLOW_TRACKING_URI` first, per `mlflow gc --help`). In MLflow 3 a model logged with `log_model` is a LoggedModel stored under `<experiment>/models/m-<id>`: after `delete_run` and `gc` that directory was still on disk (tested), and `client.delete_logged_model(model_id)` only hid it from `search_logged_models`; confirm how your store purges logged models before relying on `gc` to free model storage.

## Unity Catalog
Unity Catalog behaviour was not run here (no Databricks account) (gated: unconfirmed, source is paywalled or blocked): check the Databricks docs for `delete_model_version`, `DROP MODEL`, the privileges required, the retention window for dropped models, and whether `UNDROP` applies to models.

## Safety checks before deletion
1. No alias points to the version.
2. No serving endpoint, batch job or pipeline config references the version number (grep deployment configs).
3. Not under legal or regulatory hold.
4. Export model card, metrics and lineage to the audit store if required.

## Verify
- [ ] Deleting a version used by an endpoint is blocked by the check script.
- [ ] Storage of the artifact bucket drops after `mlflow gc`.
- [ ] Archived versions are excluded from promotion tooling but still queryable for audit.
