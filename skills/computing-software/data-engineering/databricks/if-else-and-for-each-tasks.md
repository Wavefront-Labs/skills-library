---
id: computing-software.data-engineering.databricks.if-else-and-for-each-tasks
name: if-else-and-for-each-tasks
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-jobs, for-each-task, condition-task, if-else-task, run-if, control-flow, fan-out, task-dependencies]
level: practitioner
status: docs-checked
description: "Add control flow to Databricks jobs: if/else condition tasks, run-if dependency rules, and for-each tasks that fan out over a list with bounded concurrency."
sources:
  - https://docs.databricks.com/aws/en/jobs/if-else
  - https://docs.databricks.com/aws/en/jobs/for-each
  - https://docs.databricks.com/aws/en/jobs/run-if
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# If/else and for-each tasks

**Goal:** branch and loop inside one job instead of building separate jobs or orchestration code in notebooks.

## 1. If/else (condition task)
```yaml
tasks:
  - task_key: extract
    notebook_task: {notebook_path: ../src/extract.py}      # sets task value new_rows
  - task_key: has_data
    depends_on: [{task_key: extract}]
    condition_task:
      op: GREATER_THAN              # EQUAL_TO, NOT_EQUAL, GREATER_THAN_OR_EQUAL, LESS_THAN, LESS_THAN_OR_EQUAL
      left: "{{tasks.extract.values.new_rows}}"
      right: "0"
  - task_key: transform
    depends_on: [{task_key: has_data, outcome: "true"}]
    notebook_task: {notebook_path: ../src/transform.py}
  - task_key: notify_empty
    depends_on: [{task_key: has_data, outcome: "false"}]
    notebook_task: {notebook_path: ../src/notify.py}
```
Operands are strings; numeric operators compare numerically when both sides parse as numbers. Tasks on the branch not taken are marked **Excluded**, not failed.

## 2. Run-if rules
Each task's `run_if` decides based on its dependencies' outcomes:
| `run_if` | Runs when |
|---|---|
| `ALL_SUCCESS` | all dependencies succeeded |
| `AT_LEAST_ONE_SUCCESS` | any succeeded |
| `NONE_FAILED` | none failed (some may be excluded/skipped) |
| `ALL_DONE` | all finished regardless of outcome — cleanup / audit tasks |
| `AT_LEAST_ONE_FAILED` / `ALL_FAILED` | failure handlers |
After an if/else, a task that joins both branches needs `NONE_FAILED` (one branch is always excluded).

## 3. For-each
```yaml
  - task_key: load_each_region
    depends_on: [{task_key: list_regions}]
    for_each_task:
      inputs: "{{tasks.list_regions.values.regions}}"     # or a literal JSON array: '["eu","us","apac"]'
      concurrency: 4
      task:
        task_key: load_region_iteration
        notebook_task:
          notebook_path: ../src/load_region.py
          base_parameters: {region: "{{input}}"}
```
- `{{input}}` is the current element; for arrays of objects use `{{input.field}}`.
- `concurrency` caps parallel iterations — size to cluster/warehouse capacity and source API limits.
- A for-each task runs one nested task per input (wrap multi-step work in a notebook).
- `inputs` is limited to 5000 characters (Jobs API reference); for very large lists, batch the inputs.

## 4. Patterns
- Skip downstream when there is no new data (condition on a row-count task value).
- Per-tenant/per-table loads from a config list (metadata-driven) with for-each.
- Always-run audit task with `ALL_DONE` that records run outcome.

## Verify
- [ ] The empty-input branch is exercised in a test run (outcome false path).
- [ ] Join tasks after branches use `NONE_FAILED`.
- [ ] For-each concurrency stays within compute and source limits.

## Checked
2026-10-28. Confirmed against the Jobs API reference and the if/else, run-if and for-each task pages (condition operators and string versus numeric comparison, run_if values, EXCLUDED state, nested task per input, {{input}} and {{input.<key>}}, inputs at most 5000 characters). Removed: the run_if default label, repair-by-iteration claim, run-job task remark and the unnamed iteration cap.
Method: documentation only; no commands were run.
