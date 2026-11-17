---
id: computing-software.ai-ml-engineering.mlflow.unity-catalog-model-registry
name: unity-catalog-model-registry
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, model-registry, unity-catalog-registry, databricks, three-level-namespace, model-signature, governance]
level: practitioner
status: draft
description: "Use the MLflow Model Registry in Databricks Unity Catalog: databricks-uc registry URI, three-level names, required signatures, aliases, privileges and migrating old models."
sources:
  - https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/
  - https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/upgrade-workflows
  - https://mlflow.org/docs/latest/ml/model-registry/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unity Catalog model registry

**Goal:** register and govern models in Unity Catalog so access control, lineage and cross-workspace sharing work like they do for tables.

## Register
```python
import mlflow
mlflow.set_registry_uri("databricks-uc")      # default in newer Databricks runtimes/MLflow versions
with mlflow.start_run():
    mlflow.sklearn.log_model(model, name="model", input_example=X_sample,     # older MLflow: artifact_path=
                             registered_model_name="ml_prod.churn.churn_classifier")
```
- Names are `catalog.schema.model`.
- A **signature is required** (from `input_example` or `infer_signature`); logging without one fails at registration.
- Aliases instead of stages: `MlflowClient().set_registered_model_alias("ml_prod.churn.churn_classifier", "champion", 3)`; load with `models:/ml_prod.churn.churn_classifier@champion`.

## Privileges
- Create models: `USE CATALOG`, `USE SCHEMA`, `CREATE MODEL` on the schema.
- Load/serve a model: `EXECUTE` on the model (plus `USE CATALOG`/`USE SCHEMA`).
- Owners (or `MANAGE`) can edit aliases and permissions.
Grant to groups/service principals, not individuals, e.g. `GRANT EXECUTE ON MODEL ml_prod.churn.churn_classifier TO \`ml-serving-sp\`` (or via Catalog Explorer).

## Lineage
Log training inputs as datasets from UC tables (`mlflow.log_input(mlflow.data.load_delta(table_name="ml_prod.churn.features"), context="training")`) so the model's lineage graph shows source tables.

## Cross-workspace
Any workspace attached to the metastore can load the model given privileges - no need to export/import between dev and prod workspaces. Use separate catalogs (`ml_dev`, `ml_prod`) as environments.

## Migrating from the workspace registry
`copy_model_version(src_model_uri="models:/old_name/5", dst_name="ml_prod.churn.churn_classifier")` - versions without signatures must be re-logged with one first. Update loaders from `models:/name/Production` to alias URIs.

## Verify
- [ ] Model registered with signature and visible in Catalog Explorer with lineage.
- [ ] Serving principal has EXECUTE and nothing more.
- [ ] Loaders use alias URIs.
