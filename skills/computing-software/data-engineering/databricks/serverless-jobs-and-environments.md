---
id: computing-software.data-engineering.databricks.serverless-jobs-and-environments
name: serverless-jobs-and-environments
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, serverless-jobs, serverless-compute, environments, performance-mode]
level: practitioner
status: docs-checked
description: "Run Databricks jobs on serverless compute: environments and dependencies, performance modes, usage policies, limitations and cost checks."
sources:
  - https://docs.databricks.com/aws/en/jobs/run-serverless-jobs
  - https://docs.databricks.com/aws/en/compute/serverless/dependencies
  - https://docs.databricks.com/aws/en/compute/serverless/limitations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serverless jobs and environments

**Goal:** jobs that start in seconds with no cluster tuning, with reproducible dependencies and known cost.

## Bundle definition
```yaml
resources:
  jobs:
    nightly:
      name: nightly
      performance_target: STANDARD       # or PERFORMANCE_OPTIMIZED (faster start, higher cost)
      budget_policy_id: ${var.budget_policy}
      environments:
        - environment_key: default
          spec:
            environment_version: "3"
            dependencies:
              - pandas==2.2.3
              - /Volumes/main/libs/wheels/company_utils-1.4.0-py3-none-any.whl
      tasks:
        - task_key: transform
          environment_key: default
          spark_python_task: {python_file: ../src/transform.py}
        - task_key: report
          notebook_task: {notebook_path: ../src/report.ipynb}
```
Serverless is selected by default for supported task types (notebook, Python script, dbt, Python wheel, JAR). Omitting `new_cluster`/`job_cluster_key` in the bundle is the usual way to get it, but confirm in the run details. Requirements: Unity Catalog enabled, and workloads that work in standard access mode. Databricks upgrades the runtime automatically. Tasks run in an isolated environment built from a base environment plus your listed libraries; wheels with native extensions must support both aarch64 and x86_64 because the architecture is not guaranteed (pure-Python `py3-none-any` wheels avoid this).

## Performance modes
- **Standard** (Performance optimized disabled): uses less compute and fewer DBUs for the same SKU; tolerates startup latency of 4 to 6 minutes. Good for batch with relaxed SLAs.
- **Performance optimized**: the job starts and runs faster; for time-sensitive workloads.
The setting only affects serverless tasks and needs at least one serverless task in the job.

## Retries
Serverless auto-optimization retries failed tasks by default. For workloads that must run at most once (not idempotent), untick "Enable serverless auto-optimization (may include additional retries)" in the task retry policy.

## Limitations to check first
- R is unsupported; only Spark Connect APIs, no RDD APIs; ANSI mode is on by default.
- No compute policies, compute-scoped init scripts or libraries, instance pools, compute event logs, Maven coordinates or Databricks Container Services; only a supported list of Spark configurations can be set (session level only).
- Streaming needs `Trigger.AvailableNow()` (recommended) or `Trigger.Once()`; `Trigger.ProcessingTime` and `Trigger.Continuous` are not supported. Maximum runtime is 7 days.
- No Spark UI or Spark logs; use the query profile.
- Supported features evolve; check the limitations page.

## Cost visibility
```sql
SELECT usage_date, sum(usage_quantity) dbus
FROM system.billing.usage
WHERE usage_metadata.job_id = '123' AND sku_name LIKE '%SERVERLESS%'
GROUP BY 1 ORDER BY 1;
```
Serverless usage policies (Public Preview) apply custom tags to serverless usage for billing attribution. They are not applied to existing jobs automatically. Cost can be monitored through the billable usage system table.

## Verify
Job runs with "Serverless" compute in run details; DBU usage per run from `system.billing.usage` is within budget.

## Checked

2026-11-09: reviewed against the Databricks documentation fetched this batch.

Confirmed: default serverless selection and supported task types, Unity Catalog and standard access mode requirements, performance modes (4 to 6 minute standard startup, DBU difference, at least one serverless task), auto-optimization retry opt-out, usage policy behaviour, the architecture caveat for wheels, and the limitations listed above including triggers and the 7-day maximum (run-serverless-jobs, dependencies and limitations pages). Bundle field names and the SQL were matched by phrase search only; the bundle YAML is a sketch.

Removed or corrected: the claims that standard mode is simply lower cost with minutes of startup (now cited as 4 to 6 minutes), Maven/JAR and Scala limits stated loosely, the NCC and private endpoint networking claim, and the budget-policy wording (the page calls these serverless usage policies).

Method: documentation only; no commands were run.
