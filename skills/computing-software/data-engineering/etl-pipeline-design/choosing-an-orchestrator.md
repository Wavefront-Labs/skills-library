---
id: computing-software.data-engineering.etl-pipeline-design.choosing-an-orchestrator
name: choosing-an-orchestrator
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, orchestration, apache-airflow, dagster, prefect, workflow-engines]
level: advanced
status: docs-checked
description: "Choosing a pipeline orchestrator: how Airflow, Dagster, Prefect and Databricks Jobs each describe themselves, and criteria to compare them."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/index.html
  - https://docs.dagster.io/getting-started/concepts
  - https://docs.prefect.io/v3/get-started
  - https://docs.databricks.com/aws/en/jobs/
  - https://cloud.google.com/composer/docs/concepts/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing an orchestrator

**Goal:** one orchestration layer that fits your team and platform, chosen on criteria rather than popularity.

## 1. Do you need a separate orchestrator?
A platform's own job scheduler may be enough when nearly everything runs on that platform. Databricks Lakeflow Jobs, for example, orchestrates tasks (notebooks, pipelines, Python scripts and others) as a DAG with branching and looping, time-based or event-based triggers (such as new data arriving in cloud storage), notifications and system tables for run analysis. It has limits: 2000 concurrent task runs per workspace, 10000 jobs created per hour, 12000 saved jobs, and 1000 tasks per job.

## 2. How the options describe themselves
| | Model |
|---|---|
| Airflow | Open-source platform for developing, scheduling and monitoring workflows, defined entirely in Python ("workflows as code"). A Dag encapsulates a workflow with a schedule, callbacks and tasks; dynamic Dag generation; many built-in operators; web UI to visualise, manage and debug. |
| Dagster | Asset is the core abstraction: a logical unit of data such as a table, dataset or ML model, with dependencies forming lineage. Asset checks cover data quality, freshness or completeness. Jobs, schedules, sensors, partitions, resources, components and automation conditions build on assets. |
| Prefect | Open-source orchestration engine turning Python functions into pipelines, written in pure Python with no DSLs, YAML or special syntax. Runs anywhere Python runs; triggers on schedules, external events or API; can pause for human approval; tasks can be created dynamically at runtime; UI with real-time run monitoring and dependency graphs. |
| Managed Airflow (Google Cloud, formerly Cloud Composer) | Fully managed workflow orchestration built on Apache Airflow, running on environments based on Google Kubernetes Engine; DAGs can be scheduled, triggered manually or by events such as Cloud Storage changes. |

## 3. Evaluation criteria to score
Integrations you need, scheduling model (time-based, event or data-aware, backfills), developer experience (local run, tests, CI), observability, operations (managed option, scaling, cost), security and multi-team access, and team skills. The cited pages do not rank the tools; run a proof of concept on one real pipeline per candidate, including a failure and retry.

## Verify
- [ ] Decision record lists criteria, scores and rejected options.
- [ ] Proof of concept covered a backfill, a failure with retry, and alert delivery.

## Checked
Method: docs-only read on 2026-11-09 of the Dagster concepts page (first 80 lines), Databricks Lakeflow Jobs overview (first 50 lines), Airflow overview (introduction and first Dag example via grep), Prefect get-started introduction (grep) and Google managed Airflow overview (lines 38-82). Removed as unstated: strengths and weaknesses of each tool, ecosystem size claims, hosting comparisons (MWAA, Astronomer, Dagster+, Prefect Cloud), decision heuristics, migration-cost advice, native scheduler list for Snowflake/BigQuery/Azure/AWS, and the tags orchestrator-selection, platform-native-schedulers and architecture-decision.
