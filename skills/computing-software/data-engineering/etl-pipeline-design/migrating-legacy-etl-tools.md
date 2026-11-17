---
id: computing-software.data-engineering.etl-pipeline-design.migrating-legacy-etl-tools
name: migrating-legacy-etl-tools
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, legacy-etl-migration, ssis, informatica, modernisation]
level: advanced
status: draft
description: "Migrate legacy ETL tools (SSIS, Informatica, DataStage, Talend) to SQL/dbt and modern orchestration: extracting logic from packages, re-architecting to ELT, and validation."
sources:
  - https://learn.microsoft.com/en-us/sql/integration-services/sql-server-integration-services
  - https://docs.getdbt.com/guides/migrate-from-stored-procedures
  - https://docs.informatica.com/data-integration/powercenter.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrating legacy ETL tools (SSIS / Informatica)

**Goal:** move transformation logic out of proprietary ETL packages into maintainable code without changing results.

## Extract the logic
- **SSIS**: `.dtsx` files are XML: list data flows, sources, destinations, Derived Column/Lookup/Conditional Split expressions, Execute SQL tasks, package variables and connection managers. Parse with a script to inventory components.
- **Informatica PowerCenter**: export mappings/workflows as XML from the repository (`pmrep`), list transformations (Expression, Lookup, Router, Aggregator, Update Strategy), session properties (commit intervals, target load types).
- **DataStage/Talend**: exported job XML/items similarly.
Capture hidden behaviour: lookup caching and no-match handling, truncation/rounding rules, error row redirects, sequence generators, pre/post SQL.

## Re-architect, do not transliterate
- ETL (transform in tool, then load) -> **ELT**: land raw with an EL tool, transform in SQL/dbt.
- Row-by-row logic (lookups per row, update strategies) -> set-based SQL joins and MERGE.
- Workflow sequencing -> orchestrator DAGs (Airflow/Dagster) or dbt dependencies.
- Package variables/parameters -> dbt vars, orchestrator params.

| Legacy component | Modern equivalent |
|---|---|
| Lookup (cached) | LEFT JOIN to dimension; handle no-match explicitly |
| Conditional Split / Router | CASE + separate models, or WHERE filters |
| Slowly Changing Dimension wizard | dbt snapshot or SCD2 MERGE |
| Aggregator | GROUP BY |
| Update Strategy (DD_UPDATE...) | MERGE |
| Error output redirection | quarantine tables + tests |

## Validate
Run legacy and new pipelines in parallel on the same inputs; reconcile counts, sums and full row hashes per table per day; investigate every difference (often a legacy bug: decide with owners whether to keep it).

## Gotchas
- Implicit type conversions in the old tool (string truncation, decimal rounding) produce differences that look like bugs.
- Time-based logic using server local time.
- Undocumented manual reruns/steps operators did around the old jobs.

## Verify
Parallel run for at least one full business cycle with zero unexplained differences before decommissioning the legacy job.
