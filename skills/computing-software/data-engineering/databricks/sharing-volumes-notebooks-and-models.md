---
id: computing-software.data-engineering.databricks.sharing-volumes-notebooks-and-models
name: sharing-volumes-notebooks-and-models
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, share-volumes, delta-sharing, model-sharing, notebook-sharing]
level: advanced
status: docs-checked
description: "Share more than tables with Databricks-to-Databricks sharing: volumes, notebooks, AI models and views, required privileges and recipient setup."
sources:
  - https://docs.databricks.com/aws/en/delta-sharing/create-share
  - https://docs.databricks.com/aws/en/delta-sharing/share-data-databricks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing volumes, notebooks and models

**Goal:** give a partner or another workspace files, code and ML models, governed by Unity Catalog, alongside tables. The docs now call the feature OpenSharing (the Delta Sharing URLs redirect to it).

## Add assets to a share
```sql
CREATE SHARE IF NOT EXISTS <share-name>;
ALTER SHARE <share-name> ADD TABLE <catalog>.<schema>.<table> WITH HISTORY;
ALTER SHARE <share-name> ADD VOLUME <catalog>.<schema>.<volume> AS <alias>;
ALTER SHARE <share-name> ADD MODEL <catalog>.<schema>.<model> AS <alias>;
ALTER SHARE <share-name> ADD VIEW <catalog>.<schema>.<view>;
```
- A share can hold tables, streaming tables, views (including dynamic views), materialized views, metric views, volumes, Python UDFs, notebooks, AI models, FeatureSpecs and more, from one Unity Catalog metastore only. Assets can be added or removed at any time.
- Notebooks: Catalog Explorer wizard, Add notebooks tab (Share data > Add notebooks); you need CAN READ on the notebook and must be the share owner.
- `AS <alias>` gives the name the recipient must use; the real name is then not usable by them.
- Sharing a whole schema shares all its tables, views, models and volumes now and added later; aliases and partitions are removed in that case.
- Python UDFs and FeatureSpecs are added with `ADD MODEL` too, with the object type MODEL in the CLI.

## Privileges (share owner)
- Create a share: `CREATE SHARE` on the metastore, in a workspace attached to that metastore. Databricks recommends a group as share owner.
- Volume: `USE CATALOG`, `USE SCHEMA` and `READ VOLUME`. Keep `READ VOLUME`, or the recipient loses access.
- Model: `USE CATALOG`, `USE SCHEMA` and `EXECUTE` on the model.
- Table or view: `USE CATALOG`, `USE SCHEMA`, `SELECT`.
- Schema share via SQL needs a SQL warehouse or compute on Databricks Runtime 13.3 LTS or above.

## Recipient side (Databricks-to-Databricks)
- Provider creates a share, creates a recipient object (invite by email or use the recipient metastore's sharing identifier), and grants the recipient access to the share.
- The share appears in the recipient's workspace. A metastore admin or privileged user must create a catalog from the share; others are then granted access to that catalog. Objects in catalogs created from shares are read-only.
- Shared notebooks live at catalog level and anyone with `USE CATALOG` on the catalog can access them.
- Sharing with Azure Government environments is not supported.

## Gotchas
- Cloud-token (direct file) access applies to Delta tables shared with history and no partition filter; views, volumes, notebooks, Python UDFs and AI models do not use it.
- History sharing: `WITH HISTORY` is the default for tables on Databricks Runtime 16.2 and above (otherwise `WITHOUT HISTORY`); a schema share always includes history. Enable change data feed before sharing if recipients need `table_changes()`.
- Volumes cannot be filtered: share a view for rows or columns, and separate files by audience in different volumes.

## Verify
Recipient creates the catalog from the share and can list the volume, read the notebook and see the model; removing an asset from the share removes access.

## Checked
2026-11-09: read the Create shares and Databricks-to-Databricks pages (create-share read for the asset list, requirements, ALTER SHARE syntax, tables, schemas and cloud tokens sections; remaining sections skimmed by search). Removed unconfirmed claims: open-sharing recipient support matrix by asset type, `GRANT SELECT ON SHARE` syntax, recipient `CREATE CATALOG ... USING SHARE` and MLflow loading code, cross-region egress costs.
Method: documentation only; no commands were run.
