---
id: computing-software.data-engineering.data-quality.openmetadata-ingestion
name: openmetadata-ingestion
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, metadata-management, openmetadata-ingestion, openmetadata, data-catalog, lineage, ingestion-workflows, profiler]
level: practitioner
status: docs-checked
description: "Populate an OpenMetadata catalog from a Snowflake-style source: metadata, usage, lineage, profiler and test workflows, the CLI commands, privileges and scheduling."
sources:
  - https://docs.open-metadata.org/latest/connectors
  - https://docs.open-metadata.org/latest/connectors/ingestion/workflows/metadata
  - https://docs.open-metadata.org/latest/connectors/ingestion/workflows/usage
  - https://docs.open-metadata.org/latest/connectors/ingestion/workflows/lineage
  - https://docs.open-metadata.org/latest/connectors/database/snowflake
  - https://docs.open-metadata.org/latest/connectors/database/snowflake/yaml
  - https://docs.open-metadata.org/latest/deployment
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# OpenMetadata ingestion

**Goal:** a catalog that stays current automatically: tables, columns, lineage, usage and quality results from your warehouse.

## Deployment
The deployment page lists a hosted sandbox, local Docker with Docker Compose, and production on EKS, AKS, GKE, on-premises Kubernetes, Kubernetes with Helm charts, or bare metal. Back up metadata before an upgrade and check upgrade compatibility first.

## Running workflows
- From the UI, workflows run through the OpenMetadata Ingestion Container, which ships with custom Airflow plugins. To use your own orchestrator instead, run the ingestion framework externally and install the connector extra, for example `pip3 install "openmetadata-ingestion[snowflake]"` (and `[snowflake-usage]` for usage). The Snowflake page says to use Python 3.10 or later.
- Each workflow is a YAML file run from the CLI. Metadata ingestion and lineage use `metadata ingest -c <path-to-yaml>`, usage uses `metadata usage -c`, profiler uses `metadata profile -c`, auto classification uses `metadata classify -c`, and data quality tests use `metadata test -c`.
- Run metadata ingestion first. Usage, lineage, profiler and the other workflows reuse the same `serviceName`, so the ingestion bot can read the `serviceConnection` from the server.

## Workflow types
| Workflow | What it does |
|---|---|
| Metadata | Extracts service entities (databases, schemas, tables); also a dbt ingestion route |
| Usage | Reads query history to populate the Queries tab on the table page |
| Lineage | Parses query logs, view definitions and stored procedures into the Lineage tab |
| Profiler | `orm-profiler` processor; Data Profiler workflow |
| Data quality | `orm-test-runner` processor; runs all tests present on the table, not only those in the YAML |

Usage is available only for BigQuery, Clickhouse, Databricks, Exasol, MSSQL, PostgreSQL, Redshift and Snowflake, or from a query log file for other sources.

## Snowflake privileges
- Basic metadata: `USAGE` on the warehouse, database and schemas, and `SELECT` on tables (the page also grants `SELECT` on views, external tables and dynamic tables, including future ones).
- Usage and tag ingestion: the user needs `ACCOUNTADMIN` or a role with `IMPORTED PRIVILEGES` on the `SNOWFLAKE` database. Usage reads `snowflake.account_usage.query_history`; tags read `snowflake.account_usage.tag_references`.
- Authentication options: basic, key pair (private key on a single line with line breaks replaced by `\n`, optional passphrase) and SSO.

## Agent settings (from the UI)
- Usage and lineage agents: Query Log Duration (default 1 day), Result Limit (default 1000), optional Filter Condition. Lineage also has Parsing Timeout Limit (default 300 seconds), Query Parser Type (Auto tries SqlGlot, then SqlFluff, then SqlParse) and Incremental Lineage Processing (on by default).
- Schedule: Hourly, Daily, Weekly, Monthly or a custom cron expression, or On Demand; plus Number of Retries and Raise on Error.
- Filter patterns are regular expressions; if include and exclude both match, exclude wins. Leaving all filters empty ingests everything the user can see.
- Snowflake metadata agent: Incremental Extraction is off by default. Mark Deleted Tables is on by default and soft-deletes tables that no longer exist, only within schemas the agent scans.

## Gotchas
- Lineage edges need both source and target tables already ingested, so ingest metadata for both first.
- For cross-database lineage set Cross Database Service Names to specific service names; the page warns that `*` can miss the right service or resolve to the wrong table.
- Do not filter out dynamic tables in the lineage filter patterns.

## Verify
- [ ] A new table appears in the catalog after the next scheduled metadata run.
- [ ] The Lineage tab links a source table to its downstream table.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the OpenMetadata docs pages for deployment, the metadata, usage and lineage workflows, and the Snowflake connector and Snowflake YAML pages. The sample YAML blocks on these pages did not render in the fetched text, so the YAML example in the earlier draft could not be confirmed and was removed. Removed as not confirmed: the Helm chart names and the dependency list (MySQL/Postgres, Elasticsearch/OpenSearch), the dbt workflow details (`manifest.json`, `catalog.json`, `run_results.json`, `meta.owner` mapping; the dbt and profiler pages returned 404), `profileSample` and the profiler weekly schedule advice, the `CATALOG_READER` style role and service user names, the claim that deleted tables are restorable, the claim that complex SQL dialect features may be skipped, the requirement that server and ingestion package versions match, and the advice on teams, domains and glossary.
