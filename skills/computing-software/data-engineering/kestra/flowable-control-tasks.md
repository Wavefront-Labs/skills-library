---
id: computing-software.data-engineering.kestra.flowable-control-tasks
name: flowable-control-tasks
category: computing-software
field: data-engineering
product: kestra
tags: [flowable, parallel, switch, if, dag, workingdirectory, sequential]
level: practitioner
status: docs-checked
description: "Kestra flowable tasks for branching and concurrency: Sequential, Parallel, Switch, If, DAG, Fail, AllowFailure and WorkingDirectory, with their key properties."
sources:
  - https://kestra.io/docs/workflow-components/tasks/flowable-tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `Sequential`: children one after another; sibling outputs via `{{ outputs.sibling_id.value }}`.
- `Parallel`: children concurrently. `concurrent` (`0` = no limit, default); `onChildFailure`: `FAIL` (default), `CANCEL`, `CONTINUE`. Sibling outputs cannot be read inside the same block. The task ends `FAILED` whatever `onChildFailure` is.
- `Switch`: `value` expression and `cases` keyed by value, for example `value: "{{ inputs.param }}"`.
- `If`: `condition`, `then`, optional `else`. `0`, `-0`, `null` and `''` are false; everything else is true.
- `DAG`: tasks with `dependsOn` links; `concurrent` `0` = no limit. YAML only, no no-code form.
- `Fail`: fails the execution, optionally with a `condition`; useful to validate inputs.
- `AllowFailure`: children may fail; the task becomes `WARNING`, remaining children stop, other tasks continue.
- `WorkingDirectory`: runs nested tasks in the same directory on one worker. Props `cache` and `namespaceFiles`. Only runnable tasks may be children; nesting `Parallel` or `Loop` is rejected at save time.

Subflow, Loop and Pause have their own skills.

## Checked

2026-11-04. Confirmed against the Kestra flowable tasks page: Sequential, Parallel (concurrent, onChildFailure values, no sibling outputs, ends FAILED), Switch, If falsy values, DAG with dependsOn and no no-code form, Fail with condition, AllowFailure WARNING behaviour, WorkingDirectory cache, namespaceFiles and the nesting restriction. Nothing removed.

Method: documentation only; no commands were run.
