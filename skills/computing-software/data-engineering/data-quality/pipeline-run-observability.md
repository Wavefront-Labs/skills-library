---
id: computing-software.data-engineering.data-quality.pipeline-run-observability
name: pipeline-run-observability
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, pipeline-run-observability, openlineage, run-metadata]
level: practitioner
status: docs-checked
description: "Make pipeline runs observable: dbt run_results.json fields, the OpenLineage dataset/job/run model and its integrations, and the Airflow OpenLineage provider."
sources:
  - https://openlineage.io/docs/
  - https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/index.html
  - https://docs.getdbt.com/reference/artifacts/run-results-json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline run observability

**Goal:** answer "which run produced this data, how long did it take, how many rows, and is it getting worse?" for every pipeline.

## 1. dbt run_results.json
- Describes a completed dbt invocation with timing and status for each executed node. Many files can be combined to compute average model runtime, test failure rates and snapshot record changes.
- Only executed nodes appear; separate run or test steps with different criteria produce separate results.
- Top-level keys: `metadata`, `args` (the command or rpc_method that produced it), `elapsed_time` (total seconds) and `results`.
- Each result has `unique_id` (maps to the node in manifest.json, which holds the full node object), `status`, `thread_id`, `execution_time`, `timing` (steps, often compile and execute, with started_at and completed_at), `message`, and `adapter_response`.
- `adapter_response` varies by adapter, for example `rows_affected` and `bytes_processed`; not applicable to data tests. `rows_affected` is -1 when the row count cannot be determined or does not apply (such as creating a view).
- Also recorded: `compiled`, `compiled_code`, `relation_name` (the fully-qualified object created or updated).
- Produced by build, clone, compile, docs generate, retry, run, seed, show, snapshot, test and run-operation. Freshness has separate artifacts.

## 2. OpenLineage
- An open framework and specification for lineage metadata, designed to record metadata for a job in execution. Core model: dataset, job and run entities with consistent naming, extended with facets (user-defined atomic metadata attached to an entity).
- The specification is defined using OpenAPI; a configurable backend chooses the protocol events are sent to.
- Listed integrations: Apache Airflow, Apache Flink, Apache Hive, Apache Spark, dbt, Feast, Great Expectations, SQL and Trino.
- Marquez is the reference implementation of the OpenLineage API.

## 3. Airflow provider
Install with `pip install apache-airflow-providers-openlineage` (release 2.21.0 on the page; requires Airflow 2.11.0 or later). Its guides cover the emission policy, supported classes, custom operators, job hierarchy and macros, Spark integration and troubleshooting.

## 4. Practice
Combine orchestrator and dbt run metadata so that for any mart you can find the run, its duration, status and row counts; the cited pages do not prescribe dashboards, run-id columns or thresholds.

## Verify
A dbt run's `run_results.json` shows per-node status, `execution_time` and `rows_affected` where the adapter reports it.

## Checked
Method: docs-only read on 2026-11-09 of the OpenLineage about page and dbt run_results.json page in full, and the Airflow OpenLineage provider home page (installation and requirements; guide pages were not opened). Removed as unstated: capture checklist, Snowflake QUERY_TAG, dbt-ol, openlineage-spark and environment variables, Marquez/DataHub/OpenMetadata compatibility claims, dashboards and alerts, and the monitoring tag.
