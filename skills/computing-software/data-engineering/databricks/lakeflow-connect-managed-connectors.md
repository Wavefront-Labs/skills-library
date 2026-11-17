---
id: computing-software.data-engineering.databricks.lakeflow-connect-managed-connectors
name: lakeflow-connect-managed-connectors
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, lakeflow-connect, managed-connectors, ingestion-gateway, salesforce-ingestion, sql-server-cdc, saas-ingestion, unity-catalog-connections]
level: practitioner
status: docs-checked
description: "Ingest SaaS apps and databases with Lakeflow Connect: UC connections, ingestion pipelines vs gateways, SQL Server requirements, SCD options, scheduling."
sources:
  - https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/
  - https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/sql-server-pipeline
  - https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/scd
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lakeflow Connect managed connectors

**Goal:** land SaaS and database sources into Unity Catalog streaming tables with incremental sync, without writing or hosting extraction code.

## 1. Components
| Piece | What it is |
|---|---|
| UC connection | Unity Catalog securable that stores authentication details for the source; needs `CREATE CONNECTION` to create, `USE CONNECTION` to use |
| Ingestion pipeline | pipeline on serverless compute that writes streaming tables to destination tables |
| Ingestion gateway (database connectors) | continuous pipeline on classic compute that extracts snapshot and change data and stages it in a Unity Catalog volume |
- Connector types: database (CDC; MySQL, PostgreSQL, SQL Server), SaaS (Salesforce, HubSpot, Jira, Workday and more), file, query-based (no CDC needed, no gateway), streaming, plus community and custom connectors.
- SaaS and file connectors use connection + ingestion pipeline + destination tables. Database connectors add the gateway and staging storage.
- Connectors are in various release states; check the connector's own page.

## 2. SQL Server
- Supports Azure SQL Database, Azure SQL Managed Instance and Amazon RDS SQL, SQL Server on Azure VMs and EC2, and on-premises via Azure ExpressRoute or AWS Direct Connect.
- Requirements: Unity Catalog and serverless compute enabled; `USE CATALOG` on the target; `USE SCHEMA`, `CREATE TABLE` and `CREATE VOLUME` on a schema (or `CREATE SCHEMA` on the catalog); a primary instance (change tracking and CDC are not supported on read replicas or secondaries).
- Source setup (change tracking or CDC) follows "Configure Microsoft SQL Server for ingestion into Databricks"; the wizard's Validate step reports missing configuration.
- Do not manually stop the gateway: it must run continuously to capture changes before source change logs are truncated. A stopped gateway can lose changes, which needs a full refresh of affected tables.
- Gateway driver node: minimum 8 cores. Databricks recommends the smallest worker nodes for gateways.
- The staging catalog can equal the destination catalog but cannot be a foreign catalog.

## 3. Create the pipeline
UI: Data Ingestion > Databricks connectors > pick the source. Or Declarative Automation Bundles, notebook, or Terraform. SQL Server bundle shape (from the docs):
```yaml
resources:
  pipelines:
    gw_pipeline:
      name: <gateway-name>
      continuous: true
      catalog: <staging-catalog>
      schema: <staging-schema>
      gateway_definition:
        connection_name: <connection-name>
        gateway_storage_catalog: <staging-catalog>
        gateway_storage_schema: <staging-schema>
    mi_pipeline:
      name: <ingestion-name>
      continuous: false
      serverless: true
      catalog: <dest-catalog>
      schema: <dest-schema>
      ingestion_definition:
        ingestion_gateway_id: ${resources.pipelines.gw_pipeline.id}
        objects:
          - schema:
              source_catalog: <source-database>
              source_schema: <source-schema>
              destination_catalog: <dest-catalog>
              destination_schema: <dest-schema>
```
- The gateway must be continuous; continuous mode is not supported for the ingestion pipeline, so trigger it from a scheduled job (Quartz cron) or add schedules in the UI.
- History tracking per table with `table_configuration.scd_type`: `SCD_TYPE_1` (default, overwrite) or `SCD_TYPE_2` (keeps old rows, `__START_AT`/`__END_AT`). SQL Server SCD2 also takes `sequence_by`; supported column types are timestamp, date, integer, long and string. In the SQL Server example, change tracking does not support SCD_TYPE_2 (CDC required).
- A full refresh replaces the table and removes all previous SCD2 row versions.
- Optional "Auto full refresh" lets the pipeline repair log-cleanup events and some schema evolution by fully refreshing the table (erases history if history tracking is on).

## 4. Operate
- Destination tables are pipeline-owned streaming tables; build silver from them rather than writing to them.
- Incremental ingestion: first run ingests everything; later runs ingest only changes where the source supports it (SQL Server: change tracking or CDC; Salesforce: a cursor column from a set list). Some sources or tables do not support incremental yet.
- Failures: the connector retries with exponential backoff and stores the last cursor position; credential expiry needs your action.
- Monitoring: event logs, pipeline health and data quality metrics; cost via `system.billing.usage`.
- SaaS connectors call source APIs from serverless compute; if the serverless network policy is Restricted access, add the source's API domains to Allowed domains.
- Connectors whose only auth is browser-based OAuth (for example HubSpot, Jira, Slack, Zendesk Support) cannot have connections created programmatically.

## Verify
- [ ] Gateway running continuously; ingestion pipeline scheduled.
- [ ] A changed source row appears in the destination after the next run (new version for SCD2 tables).
- [ ] The pipeline details page shows records processed (enable Upserted and Deleted columns if needed).

## Checked
2026-11-09: read the Lakeflow Connect concepts page, the SQL Server pipeline page and the history tracking (SCD) page in full. Removed unconfirmed claims: SQL Server `ALTER DATABASE ... CHANGE_TRACKING` snippets and retention figures, the Salesforce bundle YAML, Salesforce API-call limits, the Fivetran/Airbyte comparison, a `billing_origin_product` value, and the Salesforce pipeline source (page not read).
Method: documentation only; no commands were run.
