---
id: computing-software.data-engineering.databricks.unity-catalog-governance
name: unity-catalog-governance
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, unity-catalog, metastore, three-level-namespace, external-location, storage-credential, catalog-grants, data-lineage, delta-sharing, workspace-binding, system-tables, uc-migration]
status: docs-checked
level: practitioner
description: "Set up Unity Catalog's three-level namespace, grants, and lineage so Databricks governance doesn't collapse into workspace-local hacks."
sources:
  - https://docs.databricks.com/en/data-governance/unity-catalog/index.html
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/best-practices
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage
  - https://docs.databricks.com/aws/en/admin/system-tables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unity Catalog — governance that spans workspaces, not just one

**Goal:** stop re-solving access control per workspace and get one account-level governance layer, lineage, and cross-workspace data sharing.

## 1. The three-level namespace and why it exists
Data and AI assets such as tables, views, volumes, functions and models follow the `catalog.schema.object` namespace. Storage credentials, external locations, connections and shares sit directly under the **metastore**. You can have only one metastore per region, and all workspaces in that region share it. Metastores give regional isolation but are not meant as the default unit of data isolation: isolation typically begins at the catalog level, and Databricks suggests catalogs that reflect an environment scope, team, business unit or a mix (for example a `prod` catalog bound to production workspaces). Workspaces can be bound to specific catalogs and external locations.
- Unity Catalog is automatically enabled for workspaces created after November 8, 2023. Older workspaces need the "Upgrade a Databricks workspace to Unity Catalog" procedure, which is a project rather than a flag flip; follow the current Databricks upgrade guide for your runtime instead of assuming it is automatic.
- Do not register frequently accessed tables as external tables in more than one metastore: schema and metadata changes made through one metastore will not register in the other. Share between metastores or regions with Databricks' open sharing protocol instead.

## 2. Storage credentials and external locations
An external location combines a storage credential with a storage path and gives control and auditability of storage access. Tables and volumes can be managed (Unity Catalog governs both access and file lifecycle) or external (governance only). An external table must be created on a path under a defined external location.
- Limit the number of users with direct access to any bucket registered as an external location, since direct access bypasses Unity Catalog access control, auditing and lineage.
- Do not grant general READ FILES or WRITE FILES on external locations to end users; use volumes for path-based access to non-tabular data. Grant ability to create external locations only to administrators or trusted data engineers.
- Do not mount storage to DBFS if it is also an external location. Databricks recommends one external location per schema for external tables.

## 3. Grants — inheritance direction
Securable objects are hierarchical and privileges are inherited downward, so a privilege granted on a catalog applies to the schemas and tables beneath it. That is useful for broad access, but a grant set too high silently covers new objects created later. Grant at the narrowest level that meets the need, and audit catalog- and schema-level grants specifically. Do not carry permissive "just in case" grants over from an old setup into the account-wide system.

## 4. Lineage and system tables
Unity Catalog captures lineage automatically for queries run on Databricks, down to the column level, aggregated across all workspaces attached to the metastore. View it in Catalog Explorer or query the lineage system tables `system.access.table_lineage` and `system.access.column_lineage`. Lineage is retained in the UI indefinitely for data captured after September 1, 2024 (default view is 1 year), and the lineage system tables keep a rolling 395-day window by default. Upstream sources (such as Salesforce or MySQL) and downstream tools (such as Tableau or Power BI) can be registered as external assets in Unity Catalog and linked, so end-to-end lineage needs that explicit registration. UDF lineage is captured at table level only.
- **System tables** are queryable platform data, for example `system.billing.usage` for billing, and an audit log system table for access and activity. Check them before building custom cost or audit pipelines.

## 5. Sharing across organisations
Unity Catalog supports sharing live data and AI assets across organisations and clouds through an open sharing protocol (the docs now call it OpenSharing; it was previously Delta Sharing). Evaluate it before building a custom export job for a partner.

## Verify
- [ ] No workspace has broad cloud-storage access outside what is mediated by a storage credential and external location.
- [ ] Catalog- and schema-level grants were reviewed individually, none inherited broadly by accident.
- [ ] Lineage for a sample critical table shows the expected upstream/downstream objects in Catalog Explorer.
- [ ] A cross-org data-sharing need was evaluated against Unity Catalog sharing before building an export job.

## Checked
Date: 2026-11-09. Confirmed against the Databricks pages in sources: What is Unity Catalog (object model, enablement date), Unity Catalog best practices (one metastore per region, catalog isolation, inheritance, external location advice, multi-metastore warning), Data lineage (column-level, retention windows, external assets, UDF limit, lineage system tables) and System tables (system.billing.usage). Removed: SYNC command and spark.databricks.acl.* migration details, the claim that old clusters with instance profiles bypass grants, the system.lineage.* and system.access.audit table names. Not read: the migration guide and the sharing protocol pages.
Method: documentation only; no commands were run.
