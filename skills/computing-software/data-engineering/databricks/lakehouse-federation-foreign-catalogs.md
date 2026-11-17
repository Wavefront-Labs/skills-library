---
id: computing-software.data-engineering.databricks.lakehouse-federation-foreign-catalogs
name: lakehouse-federation-foreign-catalogs
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, lakehouse-federation, foreign-catalog, query-federation, uc-connections, predicate-pushdown, catalog-federation, unity-catalog]
level: practitioner
status: docs-checked
description: "Query external databases from Databricks with Lakehouse Federation: UC connections, foreign catalogs, pushdown, catalog federation for Hive/Glue, and when to ingest instead."
sources:
  - https://docs.databricks.com/aws/en/query-federation/
  - https://docs.databricks.com/aws/en/query-federation/postgresql
  - https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-connection
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Lakehouse Federation: connections and foreign catalogs

**Goal:** query operational databases and other warehouses in place, governed by Unity Catalog, for exploration and low-volume joins — without building ingestion first.

## 1. Connection
```sql
CREATE CONNECTION pg_app TYPE postgresql
OPTIONS (host 'app-db.internal', port '5432',
         user secret('federation', 'pg_user'), password secret('federation', 'pg_password'));
```
Creating a connection needs a metastore admin or the `CREATE CONNECTION` privilege on the metastore. Query-federation sources listed by Databricks: MySQL, PostgreSQL, Teradata, Oracle, Amazon Redshift, Salesforce Data 360, Snowflake, SQL Server, Azure Synapse, Google BigQuery and Databricks (check the page for the current list). Compute needs network connectivity to the target database.

## 2. Foreign catalog
```sql
CREATE FOREIGN CATALOG app_pg USING CONNECTION pg_app OPTIONS (database 'appdb');
GRANT USE CATALOG, USE SCHEMA, SELECT ON CATALOG app_pg TO `analysts`;
SELECT o.id, c.segment
FROM app_pg.public.orders o JOIN prod.gold.dim_customer c ON o.customer_id = c.customer_id
WHERE o.created_at >= current_date() - 1;
```
- Creating a foreign catalog needs `CREATE CATALOG` on the metastore plus either ownership of the connection or the `CREATE FOREIGN CATALOG` privilege on it.
- A foreign catalog mirrors a database of the external system in Unity Catalog, with table-level access control.
- Query federation is read-only.

## 3. Pushdown
Databricks Runtime tries to push predicates down to the source. Check with `EXPLAIN FORMATTED`, which shows the query sent to the remote database. A predicate with no source equivalent is evaluated in Databricks after pulling rows. See the federation-query-pushdown-and-performance skill.

## 4. Catalog federation
Catalog federation connects external catalog platforms (legacy Databricks Hive metastore, external Hive metastore, AWS Glue, and others such as Snowflake) so queries read the table files directly in object storage on Databricks compute only, not through JDBC. The documented use cases are migrating to Unity Catalog incrementally or a long-term hybrid model. Setup adds a storage credential and an external location for the table paths. Catalog federation is also read-only.

## 5. When to ingest instead
Databricks lists ad hoc reporting, BI and proof-of-concept access to operational data, with live access and minimal data movement, as the query-federation use case. When a source supports both Lakehouse Federation and Lakeflow Connect, Databricks recommends Lakeflow Connect if performance on higher data volumes and lower latency matter. Every federated query runs against the source database, so limit who can run them.

## Verify
- [ ] `EXPLAIN` shows filters pushed down for common queries.
- [ ] Connection credentials come from secrets, not inline passwords.
- [ ] Heavy recurring federated queries have been replaced by ingestion.

## Checked
2026-11-01. Confirmed against the Databricks pages Connect to external databases and catalogs, Run queries on PostgreSQL (CREATE CONNECTION and CREATE FOREIGN CATALOG privileges and syntax) and Lakehouse Federation performance recommendations (predicate pushdown, EXPLAIN FORMATTED). Removed: GRANT USE CONNECTION, REFRESH FOREIGN SCHEMA, lineage and audit claim, serverless network configuration claim, the federation-versus-ingest table and the read-replica advice.
Method: documentation only; no commands were run.
