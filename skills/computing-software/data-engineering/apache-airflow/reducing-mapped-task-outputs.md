---
id: computing-software.data-engineering.apache-airflow.reducing-mapped-task-outputs
name: reducing-mapped-task-outputs
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, mapped-reduce, dynamic-task-mapping, lazy-xcom-sequence, fan-in]
level: advanced
status: docs-checked
description: "Fan in results from Airflow dynamically mapped tasks: lazy XCom sequences, ordering, partial failures with trigger rules, and avoiding pulling huge mapped outputs."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/dynamic-task-mapping.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/xcoms.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reducing mapped task outputs

**Goal:** aggregate N mapped task results into one downstream step correctly and cheaply.

## Basic reduce
```python
@task
def process(path: str) -> int:
    return count_rows(path)

@task
def total(counts) -> int:          # counts is a lazy sequence, not a list
    return sum(counts)

total(process.expand(path=list_files()))
```
- The downstream receives a **lazy sequence** (`LazySelectSequence`) that retrieves each value only when asked; indexing and iteration work, while `list(counts)` eagerly loads every mapped value and can be slow for large counts.

## Partial failure
With the default `all_success` rule one failed mapped instance prevents the reducer from running (it becomes `upstream_failed`). A rule such as `all_done` lets it run after failures:
```python
@task(trigger_rule="all_done")
def total(counts):
    return sum(c for c in counts if c is not None)
```
How failed or skipped instances appear in the sequence is not covered by the docs, so test the filter (see Verify).

## Keep XComs small
The default XCom backend stores values in the Airflow database, which suits small values; large values or a high volume of XComs cause problems. Return a pointer (object storage path, table partition) and let the reducer read the data, or use the object storage XCom backend.

## Transform before reduce
`.map(fn)` on an XCom reference applies a plain Python function (not a task) to each element as pre-processing of the consuming task.

## Gotchas
- `[core] max_map_length` (default 1024) is the longest list or dict that can trigger mapping; a longer one fails the task that pushed it.
- Returning the lazy sequence from a task makes Airflow coerce it to a list (with a warning); call `list()` explicitly if you mean it.
- Depending on a mapped task group's output aggregates the group's returned values into a list, one element per expansion.

## Verify
Run with one deliberately failing input and confirm the reducer's behaviour (fails vs reduces survivors) matches the trigger rule you chose.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the lazy sequence received by a reducer and the `list()` cost, the coercion warning when a proxy is returned, trigger-rule behaviour, `.map()` as non-task pre-processing, group output aggregation, `max_map_length` and the database XCom default with the object storage backend. Removed the cheap `len()` claim, the ordering claim and the per-version `None` behaviour, which are not in the docs.

Method: documentation only; no commands were run.
