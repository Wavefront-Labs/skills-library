---
id: computing-software.ai-ml-engineering.mlflow.cross-environment-model-promotion
name: cross-environment-model-promotion
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, model-registry, copy-model-version, model-promotion, model-aliases, champion-challenger, mlops]
level: practitioner
status: docs-checked
description: "Promote MLflow models from dev to staging to prod: aliases vs separate registries, copy_model_version, validation gates, lineage preservation and rollback by alias."
sources:
  - https://mlflow.org/docs/latest/ml/model-registry/
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html#mlflow.client.MlflowClient.copy_model_version
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-environment model promotion

**Goal:** move a validated model version toward production with an auditable trail and a one-step rollback.

## Two patterns
1. **One registry, aliases for environments.** `champion`, `challenger`, `staging` aliases on one registered model; serving loads `models:/churn@champion`. Simple; but dev and prod share one registry and its permissions.
2. **Separate registered models (or catalogs) per environment.** `dev.ml.churn` -> `prod.ml.churn`. Promotion copies the version; prod permissions can be locked to CI service principals.

## Copy a version
```python
from mlflow import MlflowClient
client = MlflowClient()
mv = client.copy_model_version(src_model_uri="models:/dev.ml.churn@candidate", dst_name="prod.ml.churn")
client.set_registered_model_alias("prod.ml.churn", "champion", mv.version)
```
- `src_model_uri` must be a registry URI with the `models:/` scheme; the destination registered model is created if it does not exist, and the copy becomes a new version of it.
- Record the source version in a tag on the new version if you need lineage back to the dev model; do not assume the copy carries it.

## Promotion gate (CI job)
1. Load the candidate (`models:/...@candidate`) and the current champion.
2. Evaluate both on the same fresh holdout; check metric thresholds, slice metrics, latency, signature compatibility.
3. If it passes: copy/alias, tag the version (`client.set_model_version_tag(name, v, "validated_by", run_id)`), record the evaluation report as an artifact.
4. Serving picks up the alias change (reload on alias change, or redeploy).

## Rollback
Move the alias back: `client.set_registered_model_alias(name, "champion", previous_version)`. Keep the previous version's serving container/env reproducible (pinned requirements logged with the model) so rollback is fast.

## Stages are deprecated
Model stages (Staging/Production/Archived, `transition_model_version_stage`) have been deprecated since MLflow 2.9.0 and will be removed in a future major release, in favour of aliases and tags. Migrate stage-based loading (`models:/name/Production`) to aliases. Aliases of the form `v<number>` (for example `v9`) are reserved and cannot be set.

## Verify
- [ ] Prod model version traces back to a run, dataset and code commit.
- [ ] Promotion only possible through the CI identity.
- [ ] Rollback by alias rehearsed.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `copy_model_version(src_model_uri, dst_name)` semantics and the dev-to-prod promotion example with `models:/...@candidate`: docs/classic-ml/model-registry/workflow.mdx and MlflowClient source.
- Stage deprecation (since 2.9.0, removal in a future major release) and the reserved `v<number>` alias rule: workflow.mdx and `set_registered_model_alias` docstring.
- `set_registered_model_alias` and `set_model_version_tag` exist on `MlflowClient`.
- Removed as unconfirmed: lineage preservation on copy, Unity Catalog cross-catalog privilege requirements, and the claim that stages are unsupported in Unity Catalog.

Method: documentation only; no commands were run.
