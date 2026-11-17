---
id: computing-software.data-engineering.databricks.job-parameters-and-task-values
name: job-parameters-and-task-values
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-jobs, job-parameters, task-values, dynamic-value-references, dbutils-widgets, task-parameters, parameter-passing]
level: practitioner
status: docs-checked
description: "Pass data through Databricks jobs: job vs task parameters, dynamic value references like {{job.run_id}}, reading params in notebooks and scripts, and task values between tasks."
sources:
  - https://docs.databricks.com/aws/en/jobs/parameters
  - https://docs.databricks.com/aws/en/jobs/dynamic-value-references
  - https://docs.databricks.com/aws/en/jobs/task-values
  - https://docs.databricks.com/aws/en/dev-tools/databricks-utils#taskvalues-utility-dbutilsjobstaskvalues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job parameters and task values

**Goal:** parameterise jobs cleanly (environment, run date) and pass small results between tasks without writing temp tables.

## 1. Job parameters (preferred)
```yaml
parameters:
  - {name: catalog, default: dev}
  - {name: run_date, default: "{{job.start_time.iso_date}}"}
```
- Defined once at job level and available to tasks through dynamic value references and notebook widgets.
- Override at run time: `databricks jobs run-now <job-id> --json '{"job_parameters": {"run_date": "2026-10-01"}}'` or "Run now with different parameters".

Read them:
```python
catalog = dbutils.widgets.get("catalog")          # notebook
```
```python
# python_script / python_wheel task: parameters arrive as CLI args you declare
#   parameters: ["--catalog", "{{job.parameters.catalog}}"]
import argparse; p = argparse.ArgumentParser(); p.add_argument("--catalog"); args = p.parse_args()
```
```sql
-- SQL task / notebook SQL: named parameter markers
SELECT * FROM sales.orders WHERE order_date = :run_date;
```

## 2. Dynamic value references
Resolved at run time inside parameter values and some fields:
| Reference | Value |
|---|---|
| `{{job.id}}` | job ID for lineage/audit columns |
| `{{job.start_time.iso_date}}` | run start date |
| `{{job.parameters.<name>}}` | a job parameter |
| `{{task.name}}`, `{{task.run_id}}` | current task |
| `{{tasks.<task_key>.values.<key>}}` | a task value set upstream |
| `{{job.trigger.file_arrival.location}}` | path that fired a file-arrival trigger |
Check resolved values on the run page after a task completes.

## 3. Task values
```python
# upstream task "extract"
dbutils.jobs.taskValues.set(key="new_files", value=42)
dbutils.jobs.taskValues.set(key="partitions", value=["2026-10-14", "2026-10-15"])
# downstream task
n = dbutils.jobs.taskValues.get(taskKey="extract", key="new_files", default=0, debugValue=0)
```
- Values must be JSON-serialisable and small (size limit applies, ~48 KiB) — pass identifiers, counts and lists, not data.
- `debugValue` is returned when running the notebook interactively outside a job.
- Use in conditions: `condition_task.left: "{{tasks.extract.values.new_files}}"`, or as `for_each_task.inputs`.

## Verify
- [ ] Running with an overridden `run_date` processes that date in every task.
- [ ] No notebook hard-codes catalog names or `current_date()` for the business date.
- [ ] Downstream tasks read task values with a sensible `default`.

## Checked
2026-10-28. Confirmed against the Databricks job parameters, dynamic value references, task values and dbutils pages ({{job.id}}, {{job.start_time.iso_date}}, {{task.name}}, {{task.run_id}}, {{job.trigger.file_arrival.location}}, 48 KiB task value limit, default and debugValue, dbutils.widgets, :param markers, run-now job_parameters). Removed: {{job.run_id}} and iso_datetime references, the trigger.time.iso_date logical-date claim, the Browse dynamic values button, literal pass-through of unknown references, IDENTIFIER() and the task-parameter override rule.
Method: documentation only; no commands were run.
