---
id: computing-software.data-engineering.apache-airflow.chain-and-edge-labels
name: chain-and-edge-labels
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, chain-dependencies, cross-downstream, edge-labels, task-dependencies]
level: practitioner
status: docs-checked
description: "Wire Airflow task dependencies at scale with chain, chain_linear, cross_downstream and Label edge annotations instead of long bitshift lines."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dags.rst
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/bases/operator.py
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/__init__.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency helpers: chain, cross_downstream, edge labels

**Goal:** express fan-out/fan-in and long linear sequences without unreadable `>>` soup, and make branch edges self-explaining in the Graph view.

## Imports
- `from airflow.sdk import chain, chain_linear, cross_downstream, Label`

## chain
```python
chain(extract, [clean_a, clean_b], [load_a, load_b], publish)
```
- Adjacent lists must be the **same length**: `clean_a >> load_a`, `clean_b >> load_b` (pairwise), not a full cross. Mismatched lengths raise `ValueError`.
- Accepts task groups and XComArgs (TaskFlow outputs) too.

## chain_linear
```python
chain_linear([ingest_a, ingest_b], [check_1, check_2, check_3], report)
```
Every task in one element is upstream of **every** task in the next element (full cross product), unlike `chain`'s pairwise lists. Labels are not supported and raise `ValueError`.

## cross_downstream
```python
cross_downstream([t1, t2, t3], [t4, t5])   # t1..t3 each >> t4 and t5
```
Use for "all sources must finish before any of these consumers". It returns nothing, so add further dependencies on separate lines.

## Edge labels
```python
check >> Label("rows > 0") >> load
check >> Label("empty") >> notify_empty
# or
check.set_downstream(load, Label("rows > 0"))
```
Labels are purely visual (Graph view) and are the cheapest documentation for branch outcomes.

## Gotchas
- `>>` cannot link a list to a list; use `cross_downstream` for the full cross or `chain` for pairwise.
- To build dependencies dynamically, collect tasks in a list and call `chain(*tasks)` once.

## Verify
Open the Graph view (or `airflow dags show`, which renders the DAG to an image file) and confirm the edges match intent.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the `airflow.sdk` exports (`chain`, `chain_linear`, `cross_downstream`, `Label`) in the SDK `__init__`, `chain` pairwise behaviour and the same-length `ValueError`, `chain_linear` cross semantics and its Label restriction (source of `bases/operator.py`), the `Label` forms and `airflow dags show` from dags.rst. Removed the Airflow 2.x import paths, the 2.7 gate, the `edge_modifier=` keyword and the cycle-exception advice, which were not confirmed.

Method: documentation only; no commands were run.
